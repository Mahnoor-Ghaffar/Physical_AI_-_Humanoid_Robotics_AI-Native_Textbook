import React from 'react';
import StatusSection from './StatusSection';

const HeroStatus = () => {
  console.warn('HeroStatus component is deprecated. Please use StatusSection instead.');
  return (
    <StatusSection />
  );
};

export default HeroStatus;