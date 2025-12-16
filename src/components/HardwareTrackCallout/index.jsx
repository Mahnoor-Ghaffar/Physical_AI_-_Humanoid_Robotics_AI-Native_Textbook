import React from 'react';
import styles from './styles.module.css';

export default function HardwareTrackCallout({ track, children }) {
  let trackColorClass = '';
  switch (track) {
    case 'Track A (Isaac Sim)':
      trackColorClass = styles.isaacSim;
      break;
    case 'Track B (Jetson/Unitree)':
      trackColorClass = styles.jetsonUnitree;
      break;
    case 'Track C (Cloud/CPU)':
      trackColorClass = styles.cloudCpu;
      break;
    default:
      trackColorClass = styles.default;
  }

  return (
    <div className={`${styles.calloutContainer} ${trackColorClass}`}>
      <div className={styles.trackLabel}>{track}</div>
      <div className={styles.content}>{children}</div>
    </div>
  );
}
