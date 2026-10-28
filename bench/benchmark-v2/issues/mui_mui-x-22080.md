### Steps to reproduce

Steps:
1. Open this link: https://mui.com/x/react-data-grid/column-dimensions/#fluid-width (v9.0.1, but happening in v8 too)
2. Resize the first column until a horizontal scrollbar appears.
3. Scroll horizontally to the far right of the table.
4. Shrink the first column back.

https://github.com/user-attachments/assets/01869937-2922-44dc-9c90-4a13665f6f81


### Current behavior

The first column is cut off.

### Expected behavior

There are no cut-off columns after resizing.

### Context

This workaround fixes my issue (it's AI slop so I'm not confident in it):

```javascript
import { useEffect } from 'react';

export default function useResetScrollAfterColumnResize(apiRef) {
    useEffect(
        function resetScrollAfterColumnResize() {
            return apiRef.current.subscribeEvent('columnResizeStop', () => {
                const root = apiRef.current?.rootElementRef?.current;
                if (!root) return;
                const scroller = root.querySelector(
                    '.MuiDataGrid-virtualScroller'
                );
                if (!scroller || scroller.scrollLeft === 0) return;
                scroller.scrollLeft = 0;
            });
        },
        [apiRef]
    );
}
```

### Your environment

<details>
  <summary><code>npx @mui/envinfo</code></summary>

```
  System:
    OS: Windows 11 10.0.26200
  Binaries:
    Node: 24.9.0 - ...\.nvm\versions\node\v24.9.0\bin\node.EXE
    npm: 11.6.0 - ...\.nvm\versions\node\v24.9.0\bin\npm.CMD
    pnpm: 10.25.0 -  ...\.nvm\versions\node\v24.9.0\bin\pnpm.CMD
  Browsers:
    Chrome: 147.0.7727.55
    Edge: Chromium (146.0.3856.109)
  npmPackages:
    @emotion/react: ^11.14.0 => 11.14.0 
    @emotion/styled: ^11.14.1 => 11.14.1 
    @mui/icons-material: 5.16.14 => 5.16.14 
    @mui/material: 5.16.14 => 5.16.14 
    @mui/styles: 5.16.14 => 5.16.14 
    @mui/utils: 5.17.1 => 5.17.1 
    @mui/x-data-grid-pro: ^8.27.1 => 8.27.1 
    @mui/x-date-pickers: ^7.29.4 => 7.29.4 
    @mui/x-license: ^8.26.0 => 8.26.0
    react: 18.3.0 => 18.3.0
    react-dom: 18.2.0 => 18.2.0
```
</details>



**Search keywords**: flex column trimmed cut scroll resize

**Order ID**: 120603