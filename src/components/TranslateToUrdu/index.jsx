import React, { useState, useEffect } from 'react';
import { translationService } from './TranslationService';

const TranslateToUrdu = ({ children, contentKey }) => {
  const [isTranslated, setIsTranslated] = useState(false);
  const [translatedContent, setTranslatedContent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Simple hash function to create a content key if not provided
  const createContentKey = (content) => {
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return hash.toString();
  };

  const getContentKey = () => {
    if (contentKey) return contentKey;
    if (typeof children === 'string') {
      return createContentKey(children);
    }
    return 'dynamic-content';
  };

  const translateContent = async () => {
    setLoading(true);
    setError(null);

    try {
      // Get the content to translate
      let contentToTranslate = '';

      if (typeof children === 'string') {
        contentToTranslate = children;
      } else if (React.isValidElement(children)) {
        // Extract text content from React elements
        contentToTranslate = children.props?.children || 'Content to translate';
      } else {
        contentToTranslate = JSON.stringify(children);
      }

      // Perform AI-powered translation
      const translated = await translationService.translateContentBlock(contentToTranslate, 'ur');
      setTranslatedContent(translated);
      setIsTranslated(true);
    } catch (err) {
      setError('Translation failed. Please try again.');
      console.error('Translation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetTranslation = () => {
    setIsTranslated(false);
    setTranslatedContent(null);
  };

  const currentContent = isTranslated && translatedContent ? translatedContent : children;

  return (
    <div className="translate-to-urdu-component">
      <div className="translation-controls" style={{ marginBottom: '10px', textAlign: 'right' }}>
        {!isTranslated ? (
          <button
            onClick={translateContent}
            disabled={loading}
            className="button button--secondary button--sm"
            style={{
              marginRight: '10px',
              padding: '5px 10px',
              fontSize: '0.85rem'
            }}
          >
            {loading ? 'Translating...' : '.Translate to Urdu'}
          </button>
        ) : (
          <button
            onClick={resetTranslation}
            className="button button--secondary button--sm"
            style={{
              marginRight: '10px',
              padding: '5px 10px',
              fontSize: '0.85rem'
            }}
          >
            Show in English
          </button>
        )}
      </div>

      {error && (
        <div className="alert alert--danger" style={{ marginBottom: '10px' }}>
          {error}
        </div>
      )}

      <div
        className={isTranslated ? 'urdu-content' : 'english-content'}
        style={isTranslated ? {
          direction: 'rtl',
          textAlign: 'right',
          fontFamily: "'Jameel Noori Nastaleeq', 'Urdu Typesetting', serif"
        } : {}}
      >
        {currentContent}
      </div>
    </div>
  );
};

export default TranslateToUrdu;