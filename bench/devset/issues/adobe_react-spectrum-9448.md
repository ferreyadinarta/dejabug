# TableLayout: sizes are not rounding correctly

### Provide a general summary of the issue here

When a table has a non-integer width (for example, a percentage width based on the page size), `TableLayout` may round it up to a larger size, which can cause a horizontal scrollbar to appear.

### 🤔 Expected Behavior?

Table should not have horizontal scrollbar.

### 😯 Current Behavior

Table may be scrolled horizontally, even if `overflow-x: clip` is set.

### 💁 Possible Solution

_No response_

### 🔦 Context

_No response_

### 🖥️ Steps to Reproduce

https://stackblitz.com/edit/dtqtnckm?file=src%2FExample.tsx

https://github.com/user-attachments/assets/be23cc5c-c07e-4c84-9c0e-257ef46828e1

### Version

1.14.0

### What browsers are you seeing the problem on?

Chrome

### If other, please specify.

_No response_

### What operating system are you using?

macOS

### 🧢 Your Company/Team

_No response_

### 🕷 Tracking Issue

_No response_
