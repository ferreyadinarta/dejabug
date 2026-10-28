In `DefaultVideoToolbarContent.tsx` there seems to be an inconsistency with the buttons used. For the first two options we make use of `<TldrawUiButton>` and for the last button we make use of `<TldrawUiToolbarButton>`.

The above mentioned difference leads to a case where the tooltips shown on the buttons are not the same. This is not observed for the `DefaultImageToolbarContent.tsx` as they all use the same type of button which is `<TldrawUiToolbarButton>`

Here is a video demonstrating this.

https://github.com/user-attachments/assets/7fd6dc77-c16a-4602-b823-0b4dcad9b392