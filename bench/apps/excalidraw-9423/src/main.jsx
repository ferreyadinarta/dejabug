// Excalidraw with a selected frame containing two rounded rectangles and the
// Properties (stats) panel open, as in the issue video.
import { createRoot } from 'react-dom/client';
import { Excalidraw } from '@excalidraw/excalidraw';
import '@excalidraw/excalidraw/index.css';

const base = {
  strokeColor: '#1e1e1e', fillStyle: 'solid', strokeWidth: 2, strokeStyle: 'solid', roughness: 0,
  opacity: 100, angle: 0, version: 1, versionNonce: 1, isDeleted: false, groupIds: [],
  boundElements: null, updated: 1, link: null, locked: false,
};
const elements = [
  { ...base, type: 'frame', id: 'frame-1', name: null, x: 14401.33, y: -1613, width: 1028.33, height: 248.33,
    backgroundColor: 'transparent', roundness: null, seed: 11, frameId: null },
  { ...base, type: 'rectangle', id: 'rect-yellow', x: 14438, y: -1572, width: 360, height: 130,
    backgroundColor: '#ffec99', roundness: { type: 3 }, seed: 12, frameId: 'frame-1' },
  { ...base, type: 'rectangle', id: 'rect-black', x: 14958, y: -1565, width: 340, height: 115,
    backgroundColor: '#1e1e1e', roundness: { type: 3 }, seed: 13, frameId: 'frame-1' },
];

createRoot(document.getElementById('root')).render(
  <div style={{ height: '100vh' }}>
    <Excalidraw
      initialData={{
        elements,
        appState: { viewBackgroundColor: '#ffffff', selectedElementIds: { 'frame-1': true }, stats: { open: true, panels: 3 } },
        scrollToContent: true,
      }}
    />
  </div>,
);
