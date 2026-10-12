// tldraw.com-like full-screen canvas (dark mode) with the shapes seen in the issue video:
// a freehand squiggle, an arrow, a blue filled rectangle and a green outlined rectangle.
import { createRoot } from 'react-dom/client';
import { Tldraw, createShapeId, b64Vecs } from 'tldraw';
import 'tldraw/tldraw.css';

function squigglePoints() {
  const corners = [[0, 130], [55, 65], [40, 155], [105, 90], [120, 225], [135, 165], [190, 225]];
  const out = [];
  for (let i = 0; i < corners.length - 1; i++) {
    const [x0, y0] = corners[i], [x1, y1] = corners[i + 1];
    for (let t = 0; t < 1; t += 0.1) out.push({ x: x0 + (x1 - x0) * t, y: y0 + (y1 - y0) * t, z: 0.5 });
  }
  out.push({ x: 190, y: 225, z: 0.5 });
  return out;
}

function seed(editor) {
  editor.user.updateUserPreferences({ colorScheme: 'dark' });
  editor.createShapes([
    {
      id: createShapeId('squiggle'), type: 'draw', x: 150, y: 0,
      props: { color: 'white', segments: [{ type: 'free', path: b64Vecs.encodePoints(squigglePoints()) }], isComplete: true },
    },
    {
      id: createShapeId('arrow'), type: 'arrow', x: 400, y: 108,
      props: { color: 'white', start: { x: 0, y: 0 }, end: { x: 165, y: 0 } },
    },
    { id: createShapeId('blue'), type: 'geo', x: 375, y: 195, props: { geo: 'rectangle', w: 95, h: 95, color: 'blue', fill: 'solid' } },
    { id: createShapeId('green'), type: 'geo', x: 527, y: 181, props: { geo: 'rectangle', w: 190, h: 165, color: 'green' } },
  ]);
  editor.selectNone();
}

function App() {
  return (
    <div style={{ position: 'fixed', inset: 0 }}>
      <Tldraw onMount={seed} />
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
