### Provide a general summary of the issue here

`data-pressed` attribute isn't removed from the button inside the NumberField when the button gets disabled.

https://github.com/user-attachments/assets/61e2c905-90b8-4a6e-9f77-dbd460c26ae9

### 🤔 Expected Behavior?

`data-pressed` should be removed from the element once the mouse/touch is released.

### 😯 Current Behavior

`data-pressed` statys on the element even after the mouse/touch is released. It's only removed from the element when another click event is registered somewhere on the page.

### 💁 Possible Solution

_No response_

### 🔦 Context

_No response_

### 🖥️ Steps to Reproduce

https://stackblitz.com/edit/vitejs-vite-o2utfctn?file=src%2FApp.tsx

I have given the red color for `data-pressed` state. The `NumberField` has a `minValue=0`. If you press the decrement button for the value to go to 0 you will see the red color is still present on the button even after you have released the mouse. It will be removed only when you click somewhere else on the page.

You can see this issue on the docs examples as well but the pressed colors were not very obvious there, so I used this demo setup.

### Version

1.17.0

### What browsers are you seeing the problem on?

Chrome

### If other, please specify.

Firefox

### What operating system are you using?

Windows 11

### 🧢 Your Company/Team

_No response_

### 🕷 Tracking Issue

_No response_