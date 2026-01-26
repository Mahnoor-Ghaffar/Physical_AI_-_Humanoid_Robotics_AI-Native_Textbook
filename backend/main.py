"""
RAG Content Ingestion Pipeline

This script implements a complete RAG content ingestion pipeline that:
- Crawls deployed Docusaurus/Vercel URLs
- Extracts and cleans text content
- Chunks the text optimally
- Generates Cohere embeddings
- Stores them in Qdrant vector database

Author: RAG Ingestion Pipeline
Date: 2026-01-12
"""

import os
import sys
import logging
import asyncio
import time
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid
from urllib.parse import urljoin, urlparse
import time

# Import required libraries
try:
    import cohere
    import qdrant_client
    from qdrant_client.http import models
    from bs4 import BeautifulSoup
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required packages. Please install them using: pip install -r requirements.txt")
    raise e

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ingestion_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """
    Represents a segment of text extracted from a web page with associated metadata
    """
    id: str
    content: str
    source_url: str
    position: int
    length: int
    created_at: datetime
    metadata: Dict


class Config:
    """
    Configuration class to manage all settings
    """
    def __init__(self):
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.doc_base_url = os.getenv("DOCUSAURUS_BASE_URL")
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
        self.cohere_model = os.getenv("COHERE_MODEL", "embed-multilingual-v3.0")
        self.qdrant_collection_name = os.getenv("QDRANT_COLLECTION_NAME", "docs_embeddings")
        self.request_delay = float(os.getenv("REQUEST_DELAY", "1"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))

        # Validate required environment variables
        self._validate_config()

    def _validate_config(self):
        """Validate that all required environment variables are set"""
        required_vars = {
            "COHERE_API_KEY": "cohere_api_key",
            "QDRANT_URL": "qdrant_url",
            "QDRANT_API_KEY": "qdrant_api_key"
        }

        # DOCUSAURUS_BASE_URL is not required in initial validation as it can be provided via command line
        missing_vars = []
        for env_var, attr_name in required_vars.items():
            if not getattr(self, attr_name):
                missing_vars.append(env_var)

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


def is_valid_url(url: str) -> bool:
    """
    Validate if the provided string is a valid URL

    Args:
        url (str): URL string to validate

    Returns:
        bool: True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def sanitize_url(url: str) -> str:
    """
    Sanitize and normalize a URL

    Args:
        url (str): URL to sanitize

    Returns:
        str: Sanitized URL
    """
    # Remove trailing slashes
    url = url.rstrip('/')

    # Normalize the URL
    parsed = urlparse(url)
    # Reconstruct with proper formatting
    sanitized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    return sanitized


def get_all_page_urls(base_url: str, max_retries: int = 3, delay: float = 1) -> List[str]:
    """
    Discover all public pages from a given Docusaurus URL

    Args:
        base_url (str): Base URL of the Docusaurus site
        max_retries (int): Maximum number of retries for failed requests
        delay (float): Delay between requests in seconds

    Returns:
        List[str]: List of all discovered page URLs
    """
    if not is_valid_url(base_url):
        raise ValueError(f"Invalid base URL: {base_url}")

    discovered_urls = set()
    visited_urls = set()
    failed_urls = []  # Track failed URLs for statistics
    total_requests = 0  # Track total requests made

    # Start with the base URL
    urls_to_visit = [base_url]

    # Log initial state
    logger.info(f"Starting to crawl: {base_url}")
    logger.info(f"Initial URL queue size: {len(urls_to_visit)}")

    # Create a session for connection reuse
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (compatible; RAG-Ingestion-Bot/1.0)'
    })

    while urls_to_visit:
        current_url = urls_to_visit.pop(0)
        total_requests += 1

        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)
        discovered_urls.add(current_url)

        # Log progress periodically
        if len(visited_urls) % 10 == 0:
            logger.info(f"Crawling progress: {len(visited_urls)} URLs visited, "
                       f"{len(urls_to_visit)} URLs queued, "
                       f"{len(failed_urls)} failed")

        # Apply rate limiting delay
        time.sleep(delay)

        # Retry logic for failed requests
        retry_count = 0
        success = False

        while retry_count < max_retries and not success:
            try:
                response = session.get(current_url, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all links on the page
                new_links_found = 0
                for link in soup.find_all('a', href=True):
                    href = link['href']

                    # Convert relative URLs to absolute
                    absolute_url = urljoin(current_url, href)

                    # Only add URLs that are within the same domain and are HTML pages
                    if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                        # Filter out non-HTML resources (images, pdfs, etc.)
                        if absolute_url.endswith(('.html', '.htm')) or not any(absolute_url.endswith(ext) for ext in ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.svg', '.ico']):
                            if absolute_url not in visited_urls and absolute_url.startswith(base_url):
                                urls_to_visit.append(absolute_url)
                                new_links_found += 1

                logger.debug(f"Fetched {current_url} successfully, found {new_links_found} new links")
                success = True  # Request succeeded

            except requests.Timeout as e:
                retry_count += 1
                logger.warning(f"Timeout fetching {current_url} (attempt {retry_count}/{max_retries}): {str(e)}")
                if retry_count >= max_retries:
                    logger.error(f"Failed to fetch {current_url} after {max_retries} attempts due to timeout")
                    failed_urls.append((current_url, str(e)))

                # Exponential backoff: wait longer after each retry
                time.sleep(min(delay * (2 ** retry_count), 30))  # Cap at 30 seconds

            except requests.ConnectionError as e:
                retry_count += 1
                logger.warning(f"Connection error fetching {current_url} (attempt {retry_count}/{max_retries}): {str(e)}")
                if retry_count >= max_retries:
                    logger.error(f"Failed to fetch {current_url} after {max_retries} attempts due to connection error")
                    failed_urls.append((current_url, str(e)))

                # Exponential backoff
                time.sleep(min(delay * (2 ** retry_count), 30))

            except requests.HTTPError as e:
                retry_count += 1
                status_code = e.response.status_code if e.response else 'Unknown'
                logger.warning(f"HTTP error {status_code} fetching {current_url} (attempt {retry_count}/{max_retries}): {str(e)}")
                if retry_count >= max_retries:
                    logger.error(f"Failed to fetch {current_url} after {max_retries} attempts due to HTTP error {status_code}")
                    failed_urls.append((current_url, f"HTTP {status_code}"))

                # For certain status codes, don't retry (e.g., 404, 403)
                if status_code in [404, 403, 410]:
                    logger.info(f"Skipping {current_url} due to permanent error status {status_code}")
                    failed_urls.append((current_url, f"HTTP {status_code}"))
                    break
                elif retry_count < max_retries:
                    # Exponential backoff for retryable errors
                    time.sleep(min(delay * (2 ** retry_count), 30))

            except requests.RequestException as e:
                retry_count += 1
                logger.warning(f"Request error fetching {current_url} (attempt {retry_count}/{max_retries}): {str(e)}")
                if retry_count >= max_retries:
                    logger.error(f"Failed to fetch {current_url} after {max_retries} attempts due to request error: {str(e)}")
                    failed_urls.append((current_url, str(e)))

                # Exponential backoff
                time.sleep(min(delay * (2 ** retry_count), 30))

            except Exception as e:
                # For unexpected errors, don't retry - just log and continue
                logger.error(f"Unexpected error while processing {current_url}: {str(e)}")
                failed_urls.append((current_url, f"Unexpected error: {str(e)}"))
                break

    # Log final statistics
    logger.info("=" * 50)
    logger.info("CRAWLING COMPLETED - Statistics:")
    logger.info(f"Base URL: {base_url}")
    logger.info(f"Total URLs visited: {len(visited_urls)}")
    logger.info(f"Total URLs discovered: {len(discovered_urls)}")
    logger.info(f"Total failed URLs: {len(failed_urls)}")
    logger.info(f"Total requests made: {total_requests}")
    success_rate = (len(visited_urls)/total_requests)*100 if total_requests > 0 else 0
    logger.info(f"Success rate: {success_rate:.2f}%")
    logger.info("=" * 50)

    return list(discovered_urls)


def create_qdrant_client(config: Config):
    """
    Create and return a Qdrant client with error handling

    Args:
        config (Config): Configuration object with Qdrant settings

    Returns:
        QdrantClient: Initialized Qdrant client
    """
    try:
        client = qdrant_client.QdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            timeout=30  # 30 second timeout for requests
        )

        # Test connection
        client.get_collections()

        logger.info("Successfully connected to Qdrant")
        return client

    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {str(e)}")
        raise


def extract_text_from_html(html_content: str, url: str = "") -> str:
    """
    Extract text content from HTML, focusing on main content areas and removing boilerplate

    Args:
        html_content (str): Raw HTML content to extract text from
        url (str): URL of the page (used for context if needed)

    Returns:
        str: Extracted text content
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()

    # Try to find main content areas specific to Docusaurus
    main_content = None

    # Look for common Docusaurus content containers
    selectors_to_try = [
        'article',  # Common for articles
        '.main-wrapper',  # Common wrapper
        '.container',  # Container class
        '.markdown',  # Markdown content
        '.theme-content',  # Docusaurus theme content
        '.doc-content',  # Documentation content
        '.content',  # Generic content
        'main',  # Main content area
        '.docs-content',  # Docs-specific content
        '[role="main"]'  # Role-based main content
    ]

    for selector in selectors_to_try:
        main_content = soup.select_one(selector)
        if main_content:
            break

    # If no specific container found, use the body
    if not main_content:
        main_content = soup.find('body') or soup

    # Remove common non-content elements
    for element in main_content.find_all(['nav', 'aside', 'sidebar', 'advertisement', 'ad']):
        element.decompose()

    # Get text and clean it up
    text = main_content.get_text(separator='\n')

    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    return text


def clean_extracted_content(content: str) -> str:
    """
    Clean extracted text content by removing navigation elements and boilerplate

    Args:
        content (str): Raw extracted content

    Returns:
        str: Cleaned content
    """
    if not content:
        return ""

    # Remove common navigation and UI elements
    lines = content.split('\n')
    cleaned_lines = []

    for line in lines:
        stripped_line = line.strip()

        # Skip empty lines
        if not stripped_line:
            continue

        # Skip common navigation elements
        skip_keywords = [
            'navigation', 'menu', 'sidebar', 'table of contents', 'toc',
            'previous', 'next', '«', '»', 'on this page', 'jump to',
            'twitter', 'facebook', 'linkedin', 'share', 'tweet',
            'copyright', '©', 'all rights reserved', 'privacy policy'
        ]

        if any(keyword in stripped_line.lower() for keyword in skip_keywords):
            continue

        # Skip very short lines that might be menu items
        if len(stripped_line) < 5 and any(char in stripped_line for char in ['‹', '›', '»', '«', '→', '←']):
            continue

        cleaned_lines.append(stripped_line)

    return '\n'.join(cleaned_lines)


def validate_content_quality(content: str, min_length: int = 50) -> Dict[str, any]:
    """
    Validate the quality of extracted content

    Args:
        content (str): Content to validate
        min_length (int): Minimum character length for valid content

    Returns:
        Dict: Validation results with 'valid' boolean and 'details' dict
    """
    if not content:
        return {
            'valid': False,
            'details': {
                'empty_content': True,
                'length': 0,
                'message': 'Content is empty'
            }
        }

    # Check length
    content_length = len(content)
    if content_length < min_length:
        return {
            'valid': False,
            'details': {
                'empty_content': False,
                'length': content_length,
                'min_length': min_length,
                'message': f'Content too short ({content_length} chars), minimum required: {min_length}'
            }
        }

    # Check for meaningful content (not just repeated characters or symbols)
    unique_chars_ratio = len(set(content)) / len(content) if content else 0
    if unique_chars_ratio < 0.1:  # Less than 10% unique characters
        return {
            'valid': False,
            'details': {
                'empty_content': False,
                'length': content_length,
                'unique_char_ratio': unique_chars_ratio,
                'message': f'Content has low character diversity ({unique_chars_ratio:.2%})'
            }
        }

    # Check for presence of actual text (not just symbols/numbers)
    import re
    text_ratio = len(re.findall(r'[a-zA-Z]', content)) / len(content) if content else 0
    if text_ratio < 0.1:  # Less than 10% letters
        return {
            'valid': False,
            'details': {
                'empty_content': False,
                'length': content_length,
                'text_ratio': text_ratio,
                'message': f'Content has low text ratio ({text_ratio:.2%}), likely not meaningful text'
            }
        }

    # Content is valid
    return {
        'valid': True,
        'details': {
            'empty_content': False,
            'length': content_length,
            'unique_char_ratio': unique_chars_ratio,
            'text_ratio': text_ratio,
            'message': 'Content meets quality standards'
        }
    }


def chunk_text(content: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Split text content into chunks using LangChain's RecursiveCharacterTextSplitter

    Args:
        content (str): Text content to chunk
        chunk_size (int): Maximum size of each chunk
        chunk_overlap (int): Number of characters to overlap between chunks

    Returns:
        List[str]: List of text chunks
    """
    if not content:
        return []

    # Create the text splitter with specified parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", " ", ""]
    )

    # Split the content into chunks
    chunks = text_splitter.split_text(content)

    logger.debug(f"Split content into {len(chunks)} chunks with size {chunk_size} and overlap {chunk_overlap}")

    return chunks


class EmbeddingModel:
    """
    Class to encapsulate vector operations and embedding generation
    """
    def __init__(self, config: Config):
        self.config = config
        self.client = cohere.Client(config.cohere_api_key)
        self.vector_dimension = 1024  # Cohere v3 models produce 1024-dim vectors

    def generate_embeddings(self, chunks: List[str], max_retries: int = 3) -> List[List[float]]:
        """
        Generate embeddings for text chunks using Cohere API with rate limiting and retry logic

        Args:
            chunks (List[str]): List of text chunks to embed
            max_retries (int): Maximum number of retries for failed requests

        Returns:
            List[List[float]]: List of embedding vectors (each vector is a list of floats)
        """
        if not chunks:
            return []

        embeddings = []
        total_chunks = len(chunks)

        logger.info(f"Generating embeddings for {total_chunks} text chunks...")

        # Process chunks in batches to respect API limits
        batch_size = 96  # Cohere's max batch size is 96

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            logger.debug(f"Processing batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")

            # Retry logic for API calls
            retry_count = 0
            success = False

            while retry_count < max_retries and not success:
                try:
                    # Generate embeddings for the batch
                    response = self.client.embed(
                        texts=batch,
                        model=self.config.cohere_model,
                        input_type="search_document"  # Specify this is for document search
                    )

                    # Extract embeddings from response
                    batch_embeddings = response.embeddings

                    # Validate each embedding in the batch
                    for j, embedding in enumerate(batch_embeddings):
                        if len(embedding) != self.vector_dimension:
                            logger.warning(f"Embedding {i+j} has unexpected dimension: {len(embedding)}, expected {self.vector_dimension}")

                        embeddings.append(embedding)

                    logger.debug(f"Completed batch, got {len(batch_embeddings)} embeddings")
                    success = True  # Mark as successful

                except cohere.errors.TooManyRequestsError as e:
                    retry_count += 1
                    logger.warning(f"Rate limit exceeded for batch {i//batch_size + 1} (attempt {retry_count}/{max_retries}): {str(e)}")

                    if retry_count >= max_retries:
                        logger.error(f"Failed to generate embeddings for batch after {max_retries} attempts due to rate limiting")
                        raise
                    else:
                        # Exponential backoff with jitter
                        import random
                        sleep_time = min(2 ** retry_count + random.uniform(0, 1), 60)  # Cap at 60 seconds
                        logger.info(f"Waiting {sleep_time:.2f}s before retry {retry_count + 1}")
                        time.sleep(sleep_time)

                except cohere.errors.ServiceUnavailableError as e:
                    retry_count += 1
                    logger.warning(f"Service unavailable for batch {i//batch_size + 1} (attempt {retry_count}/{max_retries}): {str(e)}")

                    if retry_count >= max_retries:
                        logger.error(f"Failed to generate embeddings for batch after {max_retries} attempts due to service unavailability")
                        raise
                    else:
                        # Exponential backoff
                        sleep_time = min(2 ** retry_count, 60)  # Cap at 60 seconds
                        logger.info(f"Waiting {sleep_time:.2f}s before retry {retry_count + 1}")
                        time.sleep(sleep_time)

                except cohere.errors.CohereAPIError as e:
                    # For other API errors, don't retry if it's a client error
                    if e.http_status >= 400 and e.http_status < 500:
                        logger.error(f"Client error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
                        raise
                    else:
                        # Server-side errors might be retryable
                        retry_count += 1
                        logger.warning(f"API error for batch {i//batch_size + 1} (attempt {retry_count}/{max_retries}): {str(e)}")

                        if retry_count >= max_retries:
                            logger.error(f"Failed to generate embeddings for batch after {max_retries} attempts due to API error")
                            raise
                        else:
                            sleep_time = min(2 ** retry_count, 60)  # Exponential backoff
                            logger.info(f"Waiting {sleep_time:.2f}s before retry {retry_count + 1}")
                            time.sleep(sleep_time)

                except Exception as e:
                    logger.error(f"Unexpected error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
                    raise

        logger.info(f"Successfully generated embeddings for {len(embeddings)} chunks")
        return embeddings

    def validate_embedding(self, embedding: List[float]) -> bool:
        """
        Validate that an embedding vector has the correct properties

        Args:
            embedding (List[float]): Embedding vector to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(embedding, list):
            return False

        if len(embedding) != self.vector_dimension:
            return False

        # Check if all values are finite numbers
        for value in embedding:
            if not isinstance(value, (int, float)) or not (float('-inf') < value < float('inf')):
                return False

        return True

    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embedding vectors

        Args:
            embedding1 (List[float]): First embedding vector
            embedding2 (List[float]): Second embedding vector

        Returns:
            float: Cosine similarity value between -1 and 1
        """
        import math

        if not self.validate_embedding(embedding1) or not self.validate_embedding(embedding2):
            raise ValueError("Invalid embedding vectors provided")

        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))

        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in embedding1))
        magnitude2 = math.sqrt(sum(b * b for b in embedding2))

        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        # Calculate cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity


def generate_embeddings_for_chunks(chunks: List[str], config: Config, max_retries: int = 3) -> List[List[float]]:
    """
    Generate embeddings for text chunks using Cohere API with rate limiting and retry logic

    Args:
        chunks (List[str]): List of text chunks to embed
        config (Config): Configuration object with Cohere settings
        max_retries (int): Maximum number of retries for failed requests

    Returns:
        List[List[float]]: List of embedding vectors (each vector is a list of floats)
    """
    embedding_model = EmbeddingModel(config)
    return embedding_model.generate_embeddings(chunks, max_retries)


def create_qdrant_collection(client, collection_name: str, vector_size: int = 1024):
    """
    Create a Qdrant collection with proper schema for document chunks

    Args:
        client: Qdrant client instance
        collection_name (str): Name of the collection to create
        vector_size (int): Size of the embedding vectors (default 1024 for Cohere)
    """
    try:
        # Check if collection already exists
        collections = client.get_collections()
        existing_collections = [col.name for col in collections.collections]

        if collection_name in existing_collections:
            logger.info(f"Collection '{collection_name}' already exists, using existing collection")
            return

        # Create collection with HNSW index for efficient similarity search
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE  # Cosine distance for semantic similarity
            ),
            # Set up payload schema for metadata
            optimizers_config=models.OptimizersConfigDiff(
                memmap_threshold=20000,  # Use memory mapping for efficiency
                indexing_threshold=20000  # Index vectors efficiently
            )
        )

        logger.info(f"Successfully created Qdrant collection: {collection_name}")

    except Exception as e:
        logger.error(f"Failed to create Qdrant collection '{collection_name}': {str(e)}")
        raise


def upsert_embeddings_to_qdrant(client, collection_name: str, chunks: List[DocumentChunk], embeddings: List[List[float]],
                               batch_size: int = 64, max_retries: int = 3):
    """
    Implement upsert functionality to store embeddings with metadata in Qdrant

    Args:
        client: Qdrant client instance
        collection_name (str): Name of the collection to upsert to
        chunks (List[DocumentChunk]): List of document chunks to store
        embeddings (List[List[float]]): Corresponding embeddings for the chunks
        batch_size (int): Number of records to process in each batch
        max_retries (int): Maximum number of retries for failed operations
    """
    if not chunks or not embeddings or len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings must be non-empty and of equal length")

    total_records = len(chunks)
    logger.info(f"Upserting {total_records} embeddings to collection '{collection_name}'")

    # Process in batches
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        batch_embeddings = embeddings[i:i + batch_size]

        # Prepare points for upsert
        points = []
        for j, (chunk, embedding) in enumerate(zip(batch_chunks, batch_embeddings)):
            point_id = str(uuid.uuid4())  # Generate unique ID for each point

            # Prepare payload with metadata
            payload = {
                "content": chunk.content,
                "source_url": chunk.source_url,
                "position": chunk.position,
                "length": chunk.length,
                "created_at": chunk.created_at.isoformat(),
                "chunk_id": chunk.id
            }

            # Add any additional metadata from the chunk
            if chunk.metadata:
                for key, value in chunk.metadata.items():
                    payload[f"meta_{key}"] = value

            # Create PointStruct for Qdrant
            point = models.PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            )
            points.append(point)

        # Retry logic for upsert operation
        retry_count = 0
        success = False

        while retry_count < max_retries and not success:
            try:
                # Upsert the batch to Qdrant
                client.upsert(
                    collection_name=collection_name,
                    points=points
                )

                logger.debug(f"Successfully upserted batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}, "
                           f"{len(points)} records")

                success = True  # Mark as successful

            except Exception as e:
                retry_count += 1
                logger.warning(f"Failed to upsert batch {i//batch_size + 1} (attempt {retry_count}/{max_retries}): {str(e)}")

                if retry_count >= max_retries:
                    logger.error(f"Failed to upsert batch after {max_retries} attempts: {str(e)}")
                    raise
                else:
                    # Exponential backoff
                    sleep_time = min(2 ** retry_count, 30)  # Cap at 30 seconds
                    logger.info(f"Waiting {sleep_time:.2f}s before retry {retry_count + 1}")
                    time.sleep(sleep_time)

    logger.info(f"Successfully upserted {total_records} embeddings to collection '{collection_name}'")


def validate_embeddings_indexed(client, collection_name: str, expected_count: int, sample_size: int = 5) -> Dict[str, any]:
    """
    Add validation to ensure embeddings are properly indexed

    Args:
        client: Qdrant client instance
        collection_name (str): Name of the collection to validate
        expected_count (int): Expected number of records in the collection
        sample_size (int): Number of records to sample for detailed validation

    Returns:
        Dict: Validation results with 'valid' boolean and 'details' dict
    """
    try:
        # Get collection info
        collection_info = client.get_collection(collection_name)
        actual_count = collection_info.points_count

        logger.info(f"Collection '{collection_name}' contains {actual_count} points (expected: {expected_count})")

        # Check if count matches expected
        count_valid = actual_count == expected_count

        # Sample some points to validate their structure
        sample_points = []
        if actual_count > 0:
            # Limit sample size to actual count
            sample_size = min(sample_size, actual_count)

            # Get a few random points to validate
            sample_points = client.scroll(
                collection_name=collection_name,
                limit=sample_size,
                with_payload=True,
                with_vectors=False
            )[0]

        # Validate structure of sample points
        structure_valid = True
        validation_details = []

        for point in sample_points:
            # Check if required fields exist in payload
            required_fields = ['content', 'source_url', 'chunk_id']
            missing_fields = [field for field in required_fields if field not in point.payload]

            if missing_fields:
                structure_valid = False
                validation_details.append(f"Point {point.id} missing fields: {missing_fields}")

        # Overall validation result
        is_valid = count_valid and structure_valid

        result = {
            'valid': is_valid,
            'details': {
                'count_match': count_valid,
                'expected_count': expected_count,
                'actual_count': actual_count,
                'structure_valid': structure_valid,
                'sampled_points': len(sample_points),
                'validation_details': validation_details,
                'message': f"Validation {'passed' if is_valid else 'failed'}: {actual_count}/{expected_count} points with valid structure"
            }
        }

        if is_valid:
            logger.info(f"✓ Embedding validation passed for collection '{collection_name}'")
        else:
            logger.warning(f"✗ Embedding validation failed for collection '{collection_name}'")
            for detail in validation_details:
                logger.warning(f"  - {detail}")

        return result

    except Exception as e:
        logger.error(f"Error validating embeddings in collection '{collection_name}': {str(e)}")
        return {
            'valid': False,
            'details': {
                'error': str(e),
                'message': f"Error during validation: {str(e)}"
            }
        }


def verify_embeddings_searchable(client, collection_name: str, test_query: str = "test", top_k: int = 3) -> Dict[str, any]:
    """
    Create function to verify stored embeddings are searchable

    Args:
        client: Qdrant client instance
        collection_name (str): Name of the collection to test
        test_query (str): Test query to search for
        top_k (int): Number of results to return

    Returns:
        Dict: Search validation results with 'valid' boolean and 'details' dict
    """
    try:
        # First, get some embeddings from the collection to use as test
        scroll_result = client.scroll(
            collection_name=collection_name,
            limit=1,
            with_payload=True,
            with_vectors=True
        )

        if not scroll_result[0]:
            return {
                'valid': False,
                'details': {
                    'message': 'No points found in collection to test search functionality'
                }
            }

        # Use the first point's content as a test query to ensure we get relevant results
        test_point = scroll_result[0][0]
        test_content = test_point.payload.get('content', '')

        if not test_content:
            # If no content in payload, use a simple test query
            test_content = test_query

        # Generate embedding for the test content using the same model
        # For this test, we'll use a simple approach: search with a known point's embedding
        test_vector = test_point.vector

        # Perform search with the test vector
        search_results = client.search(
            collection_name=collection_name,
            query_vector=test_vector,
            limit=top_k,
            with_payload=True
        )

        # Check if search returned results
        search_successful = len(search_results) > 0

        # Check if the original point is among the results (should be if search is working)
        original_point_found = any(result.id == test_point.id for result in search_results)

        # Additional validation: check that results have expected payload structure
        valid_payloads = all(
            'content' in result.payload and 'source_url' in result.payload
            for result in search_results
        )

        is_valid = search_successful and original_point_found and valid_payloads

        result = {
            'valid': is_valid,
            'details': {
                'search_successful': search_successful,
                'original_point_found': original_point_found,
                'valid_payloads': valid_payloads,
                'results_returned': len(search_results),
                'expected_results': top_k,
                'message': f"Search test {'passed' if is_valid else 'failed'}: Found {len(search_results)} results, original point {'found' if original_point_found else 'not found'}"
            }
        }

        if is_valid:
            logger.info(f"✓ Search functionality validation passed for collection '{collection_name}'")
        else:
            logger.warning(f"✗ Search functionality validation failed for collection '{collection_name}'")
            logger.warning(f"  - Search successful: {search_successful}")
            logger.warning(f"  - Original point found: {original_point_found}")
            logger.warning(f"  - Valid payloads: {valid_payloads}")

        return result

    except Exception as e:
        logger.error(f"Error testing search functionality in collection '{collection_name}': {str(e)}")
        return {
            'valid': False,
            'details': {
                'error': str(e),
                'message': f"Error during search validation: {str(e)}"
            }
        }


def cleanup_failed_uploads(client, collection_name: str, threshold_date: datetime = None):
    """
    Implement cleanup function to handle failed uploads

    Args:
        client: Qdrant client instance
        collection_name (str): Name of the collection to clean up
        threshold_date (datetime): Delete records older than this date (optional)
    """
    try:
        if threshold_date is None:
            # Default to 30 days ago if no threshold specified
            from datetime import timedelta
            threshold_date = datetime.now() - timedelta(days=30)

        logger.info(f"Starting cleanup for collection '{collection_name}' with threshold date: {threshold_date}")

        # Get all points in the collection with pagination
        offset = None
        points_to_delete = []
        total_points = 0

        while True:
            scroll_result = client.scroll(
                collection_name=collection_name,
                with_payload=True,
                with_vectors=False,
                limit=1000,  # Process in batches of 1000
                offset=offset
            )

            batch_points, next_page_offset = scroll_result

            if not batch_points:
                break

            total_points += len(batch_points)

            # Identify points to delete based on criteria
            for point in batch_points:
                should_delete = False

                # Check if there's a creation date in the payload and if it's older than threshold
                created_at_str = point.payload.get('created_at')
                if created_at_str:
                    try:
                        created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                        if created_at < threshold_date:
                            should_delete = True
                    except ValueError:
                        # If date parsing fails, continue without deleting
                        pass

                # Add other criteria for failed uploads here if needed
                # For example, check for any error flags in the payload

                if should_delete:
                    points_to_delete.append(point.id)

            # Check if we've reached the end
            if next_page_offset is None:
                break
            offset = next_page_offset

        # Delete the identified points
        if points_to_delete:
            client.delete(
                collection_name=collection_name,
                points_selector=models.PointIdsList(
                    points=points_to_delete
                )
            )
            deleted_count = len(points_to_delete)
            logger.info(f"Deleted {deleted_count} points from collection '{collection_name}'")
        else:
            deleted_count = 0
            logger.info(f"No points to delete from collection '{collection_name}'")

        logger.info(f"Cleanup completed. Processed {total_points} total points, deleted {deleted_count} points.")

    except Exception as e:
        logger.error(f"Error during cleanup of collection '{collection_name}': {str(e)}")
        raise


def health_check(config: Config) -> Dict[str, any]:
    """
    Create health check function to validate service connectivity

    Args:
        config (Config): Configuration object with service settings

    Returns:
        Dict: Health check results with 'healthy' boolean and 'services' status
    """
    health_result = {
        'healthy': True,
        'timestamp': datetime.now().isoformat(),
        'services': {}
    }

    # Check Cohere API connectivity
    try:
        cohere_client = cohere.Client(config.cohere_api_key)

        # Test with a simple embedding request
        test_response = cohere_client.embed(
            texts=["health check"],
            model=config.cohere_model
        )

        if test_response and hasattr(test_response, 'embeddings') and len(test_response.embeddings) > 0:
            health_result['services']['cohere'] = {'status': 'healthy', 'message': 'API connectivity OK'}
        else:
            health_result['services']['cohere'] = {'status': 'unhealthy', 'message': 'API connectivity failed'}
            health_result['healthy'] = False

    except Exception as e:
        logger.error(f"Cohere health check failed: {str(e)}")
        health_result['services']['cohere'] = {'status': 'unhealthy', 'message': f'API connectivity failed: {str(e)}'}
        health_result['healthy'] = False

    # Check Qdrant connectivity
    try:
        qdrant_client_instance = qdrant_client.QdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            timeout=10
        )

        # Test connection by getting collections
        collections = qdrant_client_instance.get_collections()

        health_result['services']['qdrant'] = {
            'status': 'healthy',
            'message': f'Connected successfully, {len(collections.collections)} collections found'
        }

    except Exception as e:
        logger.error(f"Qdrant health check failed: {str(e)}")
        health_result['services']['qdrant'] = {'status': 'unhealthy', 'message': f'Connection failed: {str(e)}'}
        health_result['healthy'] = False

    # Check base URL accessibility
    try:
        response = requests.head(config.doc_base_url, timeout=10)
        if response.status_code < 400:
            health_result['services']['base_url'] = {
                'status': 'healthy',
                'message': f'URL accessible, status code: {response.status_code}'
            }
        else:
            health_result['services']['base_url'] = {
                'status': 'unhealthy',
                'message': f'URL not accessible, status code: {response.status_code}'
            }
            health_result['healthy'] = False
    except Exception as e:
        logger.error(f"Base URL health check failed: {str(e)}")
        health_result['services']['base_url'] = {'status': 'unhealthy', 'message': f'URL not accessible: {str(e)}'}
        health_result['healthy'] = False

    # Log overall health status
    if health_result['healthy']:
        logger.info("Health check passed: All services are healthy")
    else:
        logger.warning("Health check failed: Some services are unhealthy")
        for service, status in health_result['services'].items():
            if status['status'] == 'unhealthy':
                logger.warning(f"  - {service}: {status['message']}")

    return health_result


def main():
    """
    Main function to orchestrate the full ingestion pipeline
    """
    import argparse

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='RAG Content Ingestion Pipeline')
    parser.add_argument('--base-url', type=str, help='Base URL of the Docusaurus site to crawl')
    parser.add_argument('--chunk-size', type=int, help='Size of text chunks')
    parser.add_argument('--chunk-overlap', type=int, help='Overlap between text chunks')
    parser.add_argument('--cohere-model', type=str, help='Cohere model to use for embeddings')
    parser.add_argument('--collection-name', type=str, help='Qdrant collection name')
    parser.add_argument('--request-delay', type=float, help='Delay between requests in seconds')
    parser.add_argument('--max-retries', type=int, help='Maximum number of retries for failed requests')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--health-check', action='store_true', help='Run health check and exit')

    args = parser.parse_args()

    # Update logging level if verbose is requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("Starting RAG Content Ingestion Pipeline...")

    try:
        # Initialize configuration
        config = Config()

        # Override config values with command line arguments if provided
        if args.base_url:
            config.doc_base_url = args.base_url
        if args.chunk_size:
            config.chunk_size = args.chunk_size
        if args.chunk_overlap:
            config.chunk_overlap = args.chunk_overlap
        if args.cohere_model:
            config.cohere_model = args.cohere_model
        if args.collection_name:
            config.qdrant_collection_name = args.collection_name
        if args.request_delay:
            config.request_delay = args.request_delay
        if args.max_retries:
            config.max_retries = args.max_retries

        # If health check is requested, run it and exit
        if args.health_check:
            health_result = health_check(config)
            print(f"Health Check Result: {'PASS' if health_result['healthy'] else 'FAIL'}")
            print(f"Timestamp: {health_result['timestamp']}")
            for service, status in health_result['services'].items():
                print(f"  {service}: {status['status']} - {status['message']}")
            return

        logger.info("Configuration loaded successfully")
        logger.info(f"Using base URL: {config.doc_base_url}")
        logger.info(f"Using chunk size: {config.chunk_size}, overlap: {config.chunk_overlap}")
        logger.info(f"Using Cohere model: {config.cohere_model}")
        logger.info(f"Using Qdrant collection: {config.qdrant_collection_name}")

        # Initialize clients
        logger.info("Initializing Qdrant client...")
        qdrant_client_instance = create_qdrant_client(config)

        logger.info("Creating Qdrant collection...")
        create_qdrant_collection(qdrant_client_instance, config.qdrant_collection_name)

        # Start the ingestion pipeline
        logger.info(f"Starting ingestion pipeline for: {config.doc_base_url}")

        # Step 1: Discover all pages
        logger.info("Discovering pages...")
        page_urls = get_all_page_urls(config.doc_base_url, config.max_retries, config.request_delay)
        logger.info(f"Discovered {len(page_urls)} pages")

        if not page_urls:
            logger.error("No pages discovered. Exiting.")
            return

        # Step 2: Extract and clean content from each page
        logger.info("Extracting and cleaning content...")
        document_chunks = []
        for i, url in enumerate(page_urls):
            try:
                logger.debug(f"Processing page {i+1}/{len(page_urls)}: {url}")

                # Fetch the page content
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                # Extract text content
                text_content = extract_text_from_html(response.text, url)
                cleaned_content = clean_extracted_content(text_content)

                # Validate content quality
                validation_result = validate_content_quality(cleaned_content)
                if not validation_result['valid']:
                    logger.warning(f"Content from {url} failed quality validation: {validation_result['details']['message']}")
                    continue

                # Create document chunk
                chunk = DocumentChunk(
                    id=str(uuid.uuid4()),
                    content=cleaned_content,
                    source_url=url,
                    position=i,
                    length=len(cleaned_content),
                    created_at=datetime.now(),
                    metadata={"page_title": "", "section": ""}
                )
                document_chunks.append(chunk)

            except Exception as e:
                logger.error(f"Error processing page {url}: {str(e)}")
                continue

        logger.info(f"Processed {len(document_chunks)} valid document chunks from {len(page_urls)} pages")

        if not document_chunks:
            logger.error("No valid document chunks to process. Exiting.")
            return

        # Step 3: Chunk the content
        logger.info("Chunking content...")
        all_chunks = []
        for doc_chunk in document_chunks:
            text_chunks = chunk_text(doc_chunk.content, config.chunk_size, config.chunk_overlap)
            for j, text in enumerate(text_chunks):
                chunk = DocumentChunk(
                    id=f"{doc_chunk.id}_{j}",
                    content=text,
                    source_url=doc_chunk.source_url,
                    position=j,
                    length=len(text),
                    created_at=doc_chunk.created_at,
                    metadata=doc_chunk.metadata
                )
                all_chunks.append(chunk)

        logger.info(f"Created {len(all_chunks)} text chunks")

        if not all_chunks:
            logger.error("No text chunks created. Exiting.")
            return

        # Step 4: Generate embeddings
        logger.info("Generating embeddings...")
        # Extract just the content strings for embedding
        content_list = [chunk.content for chunk in all_chunks]
        embeddings = generate_embeddings_for_chunks(content_list, config, config.max_retries)
        logger.info(f"Generated embeddings for {len(embeddings)} chunks")

        # Step 5: Store embeddings in Qdrant
        logger.info("Storing embeddings in Qdrant...")
        upsert_embeddings_to_qdrant(
            qdrant_client_instance,
            config.qdrant_collection_name,
            all_chunks,
            embeddings,
            batch_size=64,
            max_retries=config.max_retries
        )

        # Step 6: Validate the ingestion
        logger.info("Validating ingestion...")
        validation_result = validate_embeddings_indexed(
            qdrant_client_instance,
            config.qdrant_collection_name,
            expected_count=len(all_chunks),
            sample_size=min(10, len(all_chunks))
        )

        if validation_result['valid']:
            logger.info("✓ Ingestion validation passed!")
        else:
            logger.warning("✗ Ingestion validation failed!")

        # Step 7: Test search functionality
        logger.info("Testing search functionality...")
        search_test_result = verify_embeddings_searchable(
            qdrant_client_instance,
            config.qdrant_collection_name,
            test_query="test",
            top_k=3
        )

        if search_test_result['valid']:
            logger.info("✓ Search functionality test passed!")
        else:
            logger.warning("✗ Search functionality test failed!")

        logger.info("RAG Content Ingestion Pipeline completed successfully")

    except Exception as e:
        logger.error(f"Error in main pipeline: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()