import React, { useState, useCallback } from 'react';

// Translation service using Gemini API for real-time translation
class TranslationService {
  constructor() {
    this.translationCache = new Map();
    this.activeRequests = new Map();
    this.apiKey = process.env.REACT_APP_GEMINI_API_KEY || process.env.GEMINI_API_KEY;
  }

  // Translation function using Gemini API
  async translateText(text, targetLang = 'ur', sourceLang = 'en') {
    const cacheKey = `${sourceLang}:${targetLang}:${text.substring(0, 100)}`;

    // Check cache first
    if (this.translationCache.has(cacheKey)) {
      return this.translationCache.get(cacheKey);
    }

    // Check if we're already translating this content
    if (this.activeRequests.has(cacheKey)) {
      return await this.activeRequests.get(cacheKey);
    }

    // Perform AI translation
    const translationPromise = this.performAiTranslation(text, targetLang, sourceLang);
    this.activeRequests.set(cacheKey, translationPromise);

    try {
      const result = await translationPromise;
      this.translationCache.set(cacheKey, result);
      return result;
    } finally {
      this.activeRequests.delete(cacheKey);
    }
  }

  async performAiTranslation(text, targetLang, sourceLang) {
    // Check if we have an API key configured
    if (!this.apiKey) {
      // Fallback to mock translation if no API key is available
      return this.mockTranslation(text);
    }

    try {
      // Use Gemini API for translation
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${this.apiKey}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: `Translate the following text to ${this.getLanguageName(targetLang)}. Maintain the original meaning, tone, and context. Respond only with the translated text and nothing else:\n\n${text}`
            }]
          }],
          generationConfig: {
            temperature: 0.3,
            maxOutputTokens: Math.floor(text.length * 1.5) // Rough estimation based on input length
          }
        })
      });

      if (!response.ok) {
        throw new Error(`Translation API error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      const translatedText = data.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || text;

      return translatedText;
    } catch (error) {
      console.error('Translation API error:', error);
      // Fallback to mock translation if API fails
      return this.mockTranslation(text);
    }
  }

  // Mock translation as fallback
  async mockTranslation(text) {
    return new Promise((resolve) => {
      setTimeout(() => {
        // This is a mock translation - in reality, an AI model would translate the text
        const mockTranslations = {
          'Hello': 'ہیلو',
          'Welcome': 'خوش آمدید',
          'Introduction': 'تعارف',
          'Chapter': 'باب',
          'Module': 'ماڈیول',
          'Robotics': 'روبوٹکس',
          'AI': 'مصنوعی ذہانت',
          'Humanoid': 'ہیومنوائڈ',
          'The AI-Native Mindset': 'مصنوعی ذہانت کا جنم دینے والا ذہن',
          'Getting Started': 'شروع کریں',
          'Core Concepts': 'بنیادی تصورات',
          'Advanced Topics': 'اعلیٰ موضوعات',
          'Physical AI & Humanoid Robotics Textbook': 'مصنوعی ذہانت اور ہیومنوائڈ روبوٹکس کا عملی کتاب',
          'A comprehensive guide generated and evolved with AI assistance.': 'مصنوعی ذہانت کی مدد سے تیار کردہ اور ترقی یافتہ ایک جامع گائیڈ',
          'Table of Contents': 'فہرست',
          'Preface': 'پیش لفظ',
          'About the Author': 'مصنف کے بارے میں',
          'License': 'لائسنس',
        };

        // Simple mock translation - replace with real AI translation
        let translated = text;
        for (const [english, urdu] of Object.entries(mockTranslations)) {
          translated = translated.replace(new RegExp(english, 'gi'), urdu);
        }

        // If no specific translation found, create a mock one
        if (translated === text) {
          translated = `[URDU: ${text}]`;
        }

        resolve(translated);
      }, 800); // Simulate API delay
    });
  }

  // Get full language name for API prompt
  getLanguageName(langCode) {
    const languages = {
      'ur': 'Urdu',
      'en': 'English',
      'es': 'Spanish',
      'fr': 'French',
      'de': 'German',
      'it': 'Italian',
      'pt': 'Portuguese',
      'ru': 'Russian',
      'ja': 'Japanese',
      'ko': 'Korean',
      'zh': 'Chinese',
      'ar': 'Arabic',
    };
    return languages[langCode] || langCode;
  }

  // Method to translate larger content blocks
  async translateContentBlock(content, targetLang = 'ur') {
    if (typeof content !== 'string') {
      return content;
    }

    // Split content into sentences/paragraphs for better translation
    const paragraphs = content.split('\n\n');
    const translatedParagraphs = [];

    for (const paragraph of paragraphs) {
      if (paragraph.trim()) {
        const translated = await this.translateText(paragraph, targetLang);
        translatedParagraphs.push(translated);
      } else {
        translatedParagraphs.push(paragraph); // Preserve empty lines
      }
    }

    return translatedParagraphs.join('\n\n');
  }
}

export const translationService = new TranslationService();