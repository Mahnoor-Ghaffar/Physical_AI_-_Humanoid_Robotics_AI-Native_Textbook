import React from 'react';
import CodeBlock from '@theme/CodeBlock';
import Admonition from '@theme/Admonition';

export default function UrdfViewer({ urdfContent, description = "Interactive 3D URDF Visualization" }) {
  return (
    <div style={{ margin: '20px 0', border: '1px solid #ccc', borderRadius: '5px', padding: '15px' }}>
      <h3>{description}</h3>
      <Admonition type="info" title="Interactive Viewer Placeholder">
        This is a placeholder for an interactive 3D URDF/Xacro viewer (e.g., powered by Three.js).
        In a full implementation, you would be able to manipulate joint angles and visualize the robot model directly here.
      </Admonition>
      {urdfContent && (
        <>
          <h4>URDF/Xacro Content (for reference):</h4>
          <CodeBlock language="xml">
            {urdfContent}
          </CodeBlock>
        </>
      )}
    </div>
  );
}
