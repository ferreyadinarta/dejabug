// tldraw.com-like full-screen canvas (light mode) with what is on the canvas in the issue video:
// an outlined rectangle and a "hey" text shape below it.
import { createRoot } from 'react-dom/client';
import { Tldraw, createShapeId, toRichText } from 'tldraw';
import 'tldraw/tldraw.css';

function seed(editor) {
  editor.user.updateUserPreferences({ colorScheme: 'light' });
  editor.createShapes([
    { id: createShapeId('rect'), type: 'geo', x: 300, y: 300, props: { geo: 'rectangle', w: 190, h: 190 } },
    { id: createShapeId('hey'), type: 'text', x: 280, y: 570, props: { richText: toRichText('hey') } },
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
