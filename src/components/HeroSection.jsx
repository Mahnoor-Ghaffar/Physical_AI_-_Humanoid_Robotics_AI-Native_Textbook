import React from 'react';
import { motion } from 'framer-motion';
import Link from '@docusaurus/Link';

const HeroSection = () => {
  return (
    <motion.header
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      className="hero-section"
    >
      <div className="hero-triangle-overlay"></div>
      <div className="hero-triangle-overlay"></div>
      <div className="hero-triangle-overlay"></div>

      <div className="hero-content">
        <div className="hero-text">
          <h1 className="hero-subtitle">Next Generation Platform</h1>
          <h2 className="hero-title">Discover Horizon Robotics AI Inference Platform</h2>
          <p className="hero-tagline">
            Experience cutting-edge AI-robotics innovation with our advanced platform designed for the next generation of robotics engineers and developers.
          </p>

          <div className="hero-buttons">
            <Link to="/chapter1" className="button button--primary">Get Started</Link>
            <Link to="/intro" className="button button--secondary">Learn More</Link>
          </div>
        </div>

        <div className="hero-image-container">
          <img
            src={require('@site/images/hero_img.png').default}
            alt="Photorealistic 3D humanoid robot in confident pose"
            className="hero-image"
          />
        </div>
      </div>
    </motion.header>
  );
};

export default HeroSection;