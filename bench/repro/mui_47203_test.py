"""Repro for mui_material-ui-47203 (derived only from video evidence).

Steps: open the "Checkboxes" multiple Autocomplete (disableCloseOnSelect), click
the input again to close the popup, click once more to reopen it, scroll
the listbox down with the mouse wheel until "Inception" is visible, click it.
Expected: the option gets selected (chip appears) and the listbox keeps its
scroll position so "Inception" stays visible under the cursor.
Bug (video 3.8s -> 4.3s): list jumps back to the top ("The Shawshank Redemption").
"""
import sys
from dejabug.harness import open_page

URL = "http://localhost:5173"


def main() -> int:
    with open_page(URL) as page:

        combo = page.get_by_role("combobox", name="Checkboxes")
        listbox = page.get_by_role("listbox")
        # Video 0.0s open -> 0.3s closed -> 1.1s open again: user clicked the input 3 times.
        combo.click()
        listbox.wait_for()
        combo.click()
        listbox.wait_for(state="detached")
        combo.click()
        listbox.wait_for()
        page.wait_for_timeout(300)

        inception = listbox.get_by_role("option", name="Inception", exact=True)
        # Scroll with the wheel like the user did (hovering the list).
        box = listbox.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        for _ in range(20):
            if inception.is_visible() and _in_view(listbox, inception):
                break
            page.mouse.wheel(0, 120)
            page.wait_for_timeout(100)
        page.wait_for_timeout(300)

        scroll_before = listbox.evaluate("el => el.scrollTop")
        in_view_before = _in_view(listbox, inception)
        print(f"listbox scrollTop before click: {scroll_before}, Inception in view: {in_view_before}")
        if scroll_before <= 0 or not in_view_before:
            print("SETUP ERROR: could not scroll Inception into view")
            return 2

        inception.click()
        page.wait_for_timeout(500)

        chip = page.locator(".MuiChip-root", has_text="Inception")
        chip_count = chip.count()
        selected = inception.get_attribute("aria-selected")
        scroll_after = listbox.evaluate("el => el.scrollTop")
        in_view_after = _in_view(listbox, inception)
        first_visible = listbox.evaluate(
            """el => { const r = el.getBoundingClientRect();
                 const o = [...el.querySelectorAll('[role=option]')]
                   .find(li => li.getBoundingClientRect().bottom > r.top + 1);
                 return o ? o.textContent : null; }"""
        )
        print(f"chip 'Inception' count: {chip_count}, aria-selected: {selected}")
        print(f"listbox scrollTop after click: {scroll_after}, Inception in view: {in_view_after}, "
              f"first visible option: {first_visible!r}")

    if chip_count != 1 or selected != "true":
        print("SETUP ERROR: Inception was not selected")
        return 2
    if abs(scroll_after - scroll_before) > 2 or not in_view_after:
        print(f"ASSERTION FAILED: selecting an option reset the listbox scroll position "
              f"(scrollTop {scroll_before} -> {scroll_after}; first visible option now {first_visible!r}); "
              f"expected the list to stay scrolled with 'Inception' visible.")
        return 1
    print("PASS: listbox kept its scroll position after selecting an option")
    return 0


def _in_view(listbox, option) -> bool:
    lb = listbox.bounding_box()
    ob = option.bounding_box()
    if not lb or not ob:
        return False
    return ob["y"] >= lb["y"] - 1 and ob["y"] + ob["height"] <= lb["y"] + lb["height"] + 1


if __name__ == "__main__":
    sys.exit(main())
