### What’s broken?

In Table blocks, cell text color and cell background color are no longer applied when using the Table Handle Menu. This is a regression from v0.47.3.

Detailed behavior by entry point:

| Entry Point          | Text Color    | Background Color |
|----------------------|---------------|------------------|
| Table Handle Menu    | ❌ Not applied | ❌ Not applied    |
| Formatting Toolbar   | ✅ Applied     | ❌ Not applied    |
| Block Side Menu      | ✅ Applied     | (not tested)     |

Common issue across all entry points: The modern color picker UI does not commit/apply the selected color — the picker appears to accept input but no color change is reflected in the cell.

### What did you expect to happen?

All color options (text color and background color) should be applied to table cells regardless of which UI entry point is used — Table Handle Menu, Formatting Toolbar, or Block Side Menu.

The color picker should visually confirm and apply the selected color immediately upon selection.

This worked correctly in v0.47.3.

### Steps to reproduce

1. Go to https://www.blocknotejs.org/examples/ui-components/advanced-tables (confirmed reproducible on the official playground)
2. Click on a table cell to focus it
3. Open the Table Handle Menu (click the table handle icon)
4. Attempt to change text color or background color
5. Observe that no color change is applied

To confirm partial behavior via Formatting Toolbar:
1. Select text inside a table cell
2. Open the Formatting Toolbar
3. Apply text color → ✅ color is applied
4. Apply background color → ❌ color is NOT applied

### BlockNote version

v0.51.1 

### Environment

_No response_

### Additional context

Regression confirmed between v0.47.3 (working) and v0.51.1 (broken).


- 0_47_3_OK.mov — v0.47.3: text color & background color work correctly via Table Handle Menu

https://github.com/user-attachments/assets/08c09bf1-f651-4c50-94d3-d8d0d690cdbe

- 0_51_1_error.mov — v0.51.1: color not applied via Table Handle Menu

https://github.com/user-attachments/assets/b477af80-2195-4c89-b93e-7a575796bd45

- 0_51_1_toolbar_ok.mov — v0.51.1: text color works via Formatting Toolbar; background color still broken

https://github.com/user-attachments/assets/fe59e9b2-c7f4-474d-bb77-0841a74026d5

- 0_51_1_handlemenu_ok.mov — v0.51.1: text color works via Block Side Menu

https://github.com/user-attachments/assets/ea7fc7a2-e6b9-4f02-8196-4e91fa9717c3

- 0.47.3 color picker 

<img width="177" height="682" alt="Image" src="https://github.com/user-attachments/assets/6ed5c5ee-30b2-432c-83fa-ca6a451fec3c" />

- 0.51.1 color picker

 
<img width="171" height="686" alt="Image" src="https://github.com/user-attachments/assets/3a3e261b-dbb5-4789-b9f2-92e1dde54c3f" />


### Contribution

- [ ] I'd be interested in contributing a fix for this issue

### Sponsor

- [x] I'm a [sponsor](https://www.blocknotejs.org/pricing) and would appreciate if you could look into this sooner than later 💖