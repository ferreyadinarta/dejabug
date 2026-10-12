// tldraw.com-like full-screen canvas (light mode) with a single frame named "Frame" sitting just
// above the bottom toolbar, as in the issue video (the "more shapes" popup overlaps the frame).
import { createRoot } from 'react-dom/client';
import { Tldraw, createShapeId } from 'tldraw';
import 'tldraw/tldraw.css';

function seed(editor) {
  editor.user.updateUserPreferences({ colorScheme: 'light' });
  const vp = editor.getViewportScreenBounds();
  const w = 520, h = 290;
  const topLeft = editor.screenToPage({ x: vp.w / 2 - 300, y: vp.h - 115 - h });
  editor.createShape({
    id: createShapeId('frame'), type: 'frame', x: topLeft.x, y: topLeft.y,
    props: { w, h, name: 'Frame' },
  });
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
