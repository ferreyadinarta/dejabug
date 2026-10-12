// Excalidraw editor with one YouTube embeddable on the canvas (as in the issue video).
import { createRoot } from 'react-dom/client';
import { Excalidraw } from '@excalidraw/excalidraw';
import '@excalidraw/excalidraw/index.css';

const elements = [
  {
    type: 'embeddable', id: 'yt-embed', x: 220, y: 120, width: 560, height: 315,
    link: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', strokeColor: 'transparent',
    backgroundColor: 'transparent', fillStyle: 'solid', strokeWidth: 2, roughness: 0, opacity: 100,
    angle: 0, seed: 1, version: 1, versionNonce: 1, isDeleted: false, groupIds: [], frameId: null,
    boundElements: null, updated: 1, locked: false, roundness: null, validated: true,
  },
];

createRoot(document.getElementById('root')).render(
  <div style={{ height: '100vh' }}>
    <Excalidraw initialData={{ elements, appState: { viewBackgroundColor: '#ffffff' }, scrollToContent: false }} />
  </div>,
);
