import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid'; // Mermaid is already installed via Docusaurus (remark-mermaid)

mermaid.initialize({
  startOnLoad: true,
  securityLevel: 'loose', // Allow some HTML in diagrams if needed
});

export default function RosNodeDiagram({ chart }) {
  const mermaidRef = useRef(null);
  const [svg, setSvg] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    if (mermaidRef.current && chart) {
      mermaid.render('mermaid-svg-chart', chart)
        .then(({ svg }) => {
          setSvg(svg);
          setError(null);
        })
        .catch((e) => {
          setError(`Failed to render Mermaid chart: ${e.message}`);
          console.error(e);
        });
    }
  }, [chart]);

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error}</div>;
  }

  return (
    <div className="mermaid" ref={mermaidRef} dangerouslySetInnerHTML={{ __html: svg }} />
  );
}
