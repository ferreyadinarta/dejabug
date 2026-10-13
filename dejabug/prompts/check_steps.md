Below are draft steps to reproduce a bug, written from a screen recording, then the recording itself as film sheets (every half second, time in the corner, what changed boxed in red, the pointer ringed in yellow when found).

Write one corrected list. Check every step against the frames, one by one:

- Is there a user action at that time? A highlight, a selected state, or content changing on its own is the app, not the user. Remove steps that are only the app reacting.
- Is the kind right? Press-move-release is one drag; one word highlighted at once is a double-click; text appearing at the caret is typing; content changing with the pointer elsewhere is often a key.
- Is it one gesture split into several steps, or the same action listed twice? Merge them.
- Is the time the frame where the action happens (not where its result settles)? Fix it.
- Is the target named the way a person would, using a visible label where there is one?

Add a step only when an action is clearly visible and missing. Then check the bug: it should be the first moment the app does something wrong right after a user action, described by what is visibly wrong.

{drafts}
{context}
Reply with only the corrected JSON, same format.
