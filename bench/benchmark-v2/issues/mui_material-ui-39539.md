### Steps to reproduce 🕹

Link to live example: https://stackblitz.com/edit/react-tsmx9v?file=src%2Fstyle.css

https://github.com/user-attachments/assets/b1135362-65cf-4c89-9c6c-c8ff1b4d9e1a

Steps:

1. Load the page in Chrome 117 or newer

### Current behavior 😯

The very first frame has the text input box rendered extra tall. The next frame has it at the normal size.
This is happening because the mui-auto-fill-cancel keyframes rule starts an animation.

### Expected behavior 🤔

No animation should be started and the first frame should be the same as the final state.

### Context 🔦

Hello! I recently implemented a feature in chrome which makes the `display` property animatable: https://chromestatus.com/feature/5154958272364544

Before I made this change, `@keyframes` rules with `display` in them did nothing. The mui-auto-fill keyframes rules in particular would have not started an animation because they didn't contain any animatable properties. Now that `display` is animatable, it is creating an animation which is only lasting for a single frame.

This was added here: https://github.com/mui/material-ui/pull/28070

Based on the issue which that PR fixed, it sounds like there has to be some styles inside the keyframes which don't actually start an animation. I recommend using a property which is pretty much guaranteed to never be upgraded to become animatable, such as the `animation-name` property. So perhaps replacing `display:block` with `animation-name:hello-world` would fix it?

### Your environment 🌎

<details>
  <summary><code>npx @mui/envinfo</code></summary>

```
  Don't forget to mention which browser you used.
  Output from `npx @mui/envinfo` goes here.
```
</details>
