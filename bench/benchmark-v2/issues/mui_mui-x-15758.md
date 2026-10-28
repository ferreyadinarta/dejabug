### Steps to reproduce

Steps:
1. Open this link to live example: https://codesandbox.io/embed/kcf4hp?module=/src/Demo.tsx&fontsize=12
2. Open the DateTimePicker with a Digital Clock and scroll down to a later time.
3. Press down on a time and wait a second before mouse up.
4. If you try it again, it will work

### Current behavior

The DigitalClock is returning to the top and not clicking on the time. If you open the picker and click a time without clicking a date first, if you aren't fast enough at releasing your click (if there's a little bit of delay between mousedown and mouseup), it doesn't register your click and just scrolls back to the time you had selected.

https://github.com/user-attachments/assets/e13df325-b454-47c4-8fce-bc2fdb8ddc00



### Expected behavior

The time is selected on key down the first time no matter how slow the click.

### Context

 I am hoping that we can fix this issue so that anyone, no matter the speed of their click, can easily click on a time. 


### Your environment

<details>
  <summary><code>npx @mui/envinfo</code></summary>

```
  Run on Chrome
  System:
    OS: macOS 15.1.1
  Binaries:
    Node: 20.11.1 - ~/.nvm/versions/node/v20.11.1/bin/node
    npm: 10.8.2 - ~/.nvm/versions/node/v20.11.1/bin/npm
    pnpm: 9.13.2 - ~/.nvm/versions/node/v20.11.1/bin/pnpm
  Browsers:
    Chrome: 131.0.6778.108
    Edge: Not Found
    Safari: 18.1.1
```
</details>



**Search keywords**: DigitalClock