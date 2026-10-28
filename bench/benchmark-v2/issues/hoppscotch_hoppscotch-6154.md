### Is there an existing issue for this?

- [x] I have searched existing issues and this bug hasn't been reported yet

### Platform

Web App

### Browser

Chrome

### Operating System

Windows

### Bug Description

## What happened?

When I hover a variable placeholder inside a request field (URL / request text) to view/edit it (collection / environment / global variables), the hover UI stops working when the request contains additional text around the variable. I see the small hover popup/modal with the edit icon briefly, but as soon as I move the mouse toward it (or even while hovering), it disappears and I can’t click it or edit the variable.

What I expected is that the variable hover popup/modal stays visible and interactive so I can click the edit icon and edit the variable.

So what is correct is URLs like `<<variable>>` or `text<<variable>>` but not `<<variable>>text`, so we should fix this.

## Steps to reproduce

1. Go to 'Hoppscotch REST request page'
2. Click on the request URL (or relevant request text field) and enter a variable with surrounding text, e.g. https://<<variable>>.com
3. Hover the variable placeholder <<variable>> and try to move the cursor to the edit icon/popup
4. See that hovering/editing stops working (popup disappears / cannot click)

## Screenshots

https://github.com/user-attachments/assets/53115f00-9940-4e4e-b902-3d6d96f35b9f

## Additional details (if relevant)

This happens for me on Windows using the web app of Hoppscotch but also on Mac, both using Google Chrome.

### Deployment Type

Hoppscotch Cloud

### Version

_No response_