
import React from 'react';

const Logo = () => (
  <svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style={{ stopColor: 'var(--primary-accent)', stopOpacity: 1 }} />
        <stop offset="100%" style={{ stopColor: 'var(--glow-green)', stopOpacity: 1 }} />
      </linearGradient>
    </defs>
    <path d="M50 10 L90 30 L90 70 L50 90 L10 70 L10 30 Z" fill="url(#logo-gradient)" />
    <path d="M50 20 L80 35 L80 65 L50 80 L20 65 L20 35 Z" fill="var(--secondary-background)" />
    <circle cx="50" cy="50" r="10" fill="url(#logo-gradient)" />
  </svg>
);

export default Logo;
