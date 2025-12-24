import React from 'react';

const StatusSection = () => {
  return (
    <section className="status-section">
      <div className="container">
        <div className="status-content">
          <div className="status-stats">
            <div className="status-stat-item">
              <span className="status-stat-number">10K+</span>
              <span className="status-stat-label">Developers</span>
            </div>
            <div className="status-stat-item">
              <span className="status-stat-number">500+</span>
              <span className="status-stat-label">Robots</span>
            </div>
            <div className="status-stat-item">
              <span className="status-stat-number">50+</span>
              <span className="status-stat-label">Countries</span>
            </div>
          </div>

          <div className="status-features">
            <div className="status-feature">
              <span className="status-feature-icon">⚡</span>
              <span>Real-time Inference</span>
            </div>
            <div className="status-feature">
              <span className="status-feature-icon">🛡️</span>
              <span>Secure Platform</span>
            </div>
            <div className="status-feature">
              <span className="status-feature-icon">🌐</span>
              <span>Global Scale</span>
            </div>
            <div className="status-feature">
              <span className="status-feature-icon">🚀</span>
              <span>Easy Deployment</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default StatusSection;