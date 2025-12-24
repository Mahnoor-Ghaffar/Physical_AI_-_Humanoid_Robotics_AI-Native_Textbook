import React from 'react';

const BackgroundOverlays = ({ className = "" }) => {
  return (
    <>
      {/* One triangle overlay */}
      <div className={`section-triangle-overlay ${className}-triangle-overlay`}></div>

      {/* One circle overlay */}
      <div className={`section-circle-overlay ${className}-circle-overlay`}></div>
    </>
  );
};

export default BackgroundOverlays;