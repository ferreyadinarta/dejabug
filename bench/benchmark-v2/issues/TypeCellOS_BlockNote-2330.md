Problem:
1. Create bullet/numbered/checklist item
2. Try to paste text into its content
3. List item gets replaced with paragraph (This happens when list item content is empty).

The following code solves the problem, but I don't if it is ideal:
```js
pasteHandler: ({ event, editor, defaultPasteHandler }) => {
	const currentBlock = editor.getTextCursorPosition().block;
	const blockSpec = editor.schema.blockSchema[currentBlock.type];
	
	const hasInlineContent = blockSpec?.content === "inline";
	const isEmpty = !currentBlock.content || 
		(Array.isArray(currentBlock.content) && currentBlock.content.length === 0);
	
	if (hasInlineContent && isEmpty) {
		const plainText = event.clipboardData?.getData("text/plain");
		if (plainText) {
			editor.pasteText(plainText);
			return true;
		}
	}
	
	return defaultPasteHandler();
},
```

https://github.com/user-attachments/assets/47196d1c-db14-48c2-8bc1-fbc4cb2bbf10