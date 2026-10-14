# Radix One-Time Password Field - Values Not Persisting and Keyboard Navigation Broken

I recently integrated the Radix UI One-Time Password Field library into my project and am experiencing critical functionality issues:

1. **Values not persisting**: When typing digits, the focus correctly moves to the next input field, but the previously entered values disappear or don't display. The hidden input field doesn't seem to be capturing the complete OTP value.

2. **Broken keyboard navigation**: 
   - **Tab key**: Doesn't properly navigate between input fields
   - **Backspace/Delete**: Fails to clear the current field or move focus back to the previous input as expected

The component appears to handle focus management but fails at value retention and standard keyboard interactions.

**Environment:**
- Package: `@radix-ui/react-one-time-password-field`
- Version: 0.1.8
- Framework: React
- OS: MacOS
- Browser: Google Chrome

**Code Example:**
```tsx
<OneTimePasswordField.Root name="otp" >
  <OneTimePasswordField.Input />
  <OneTimePasswordField.Input />
  <OneTimePasswordField.Input />
  <OneTimePasswordField.Input />
  <OneTimePasswordField.HiddenInput />
</OneTimePasswordField.Root>
```

https://github.com/user-attachments/assets/c9a3c0e1-02dd-4e49-ae72-044639725c96

Has anyone else experienced similar problems? Any guidance would be appreciated.
