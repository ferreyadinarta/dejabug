# [scheduler] Drag placeholder stays hidden when re-entering the same position (external drag)

### Summary

When dragging an external event (`StandaloneEvent`) into the calendar, if the pointer leaves the drop surface and then re-enters at the same position, the drag placeholder stays invisible — it doesn't reappear until the pointer moves to a different slot. Caused by an asymmetric diff in `shouldUpdateOccurrencePlaceholder`.

### Steps to reproduce

1. Use an external drag source (`StandaloneEvent`) and drag it into the calendar.
2. Hover over a column so the placeholder appears.
3. Drag out of the drop surface (leave the grid) — the placeholder hides (expected).
4. Drag back into the **same** column at the **same** position.

**Expected:** the placeholder reappears.
**Actual:** the placeholder stays invisible until you move to a different slot.

### Repro video
https://github.com/user-attachments/assets/6cf99e55-4eb4-4d31-8e0e-53c9857b8726

### Root cause

`x-scheduler-internals/src/internals/utils/SchedulerStore/SchedulerStore.utils.ts` — `shouldUpdateOccurrencePlaceholder`:

```ts
for (const key in untypedNext) { // only iterates next's keys
  ...
}
```

Flow:
- `onDragLeave` (`useDropTarget.ts:148`) sets the placeholder to `{ ...current, isHidden: true }` — for external drag this always happens (`type === 'external-drag'`).
- On re-enter, `onDrag` computes a fresh placeholder **without** `isHidden` and calls `setOccurrencePlaceholder`.
- `shouldUpdateOccurrencePlaceholder(previous = {...,isHidden:true}, next = {...,no isHidden})` only loops over `next`'s keys, so the `isHidden` key (present in `previous`, absent in `next`) is never compared. If everything else is identical (same column/position), it returns `false` → the store isn't updated → the placeholder stays hidden.

The placeholder is hidden by the selectors when `occurrencePlaceholder.isHidden` is truthy (`eventCalendarOccurrencePlaceholderSelectors`).

This is not specific to `isHidden` — any optional key present in `previous` but dropped in `next` is ignored by the diff.

### Notes on scope

Not seen during normal cell-to-cell dragging: the drop target is the whole column/surface (not per cell), so `onDragLeave` only fires when leaving the surface, and re-entering a *different* position differs enough for the diff to catch it. The bug needs leave + re-enter at the *same* position. Internal drag only hides on leave when `canDropEventsToTheOutside` is enabled; external drag always hides — hence the external-drag repro is the reliable one. Medium severity (edge case, but user-facing in the external-drag flow).

### Suggested fix

Make `shouldUpdateOccurrencePlaceholder` compare the **union** of `previous` + `next` keys (or detect a differing key count), or always normalize `isHidden` so it's present (default `false`).

### Context

`@mui/x-scheduler-internals` (`master`, pre-stable).

