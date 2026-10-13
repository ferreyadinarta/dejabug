# dejabug as a GitHub Action

When someone files an issue with a screen recording, dejabug can reply with steps to reproduce written from the video. Add this file to your repo as `.github/workflows/dejabug.yml`:

```yaml
name: dejabug
on:
  issues:
    types: [labeled]

permissions:
  issues: write

jobs:
  steps:
    if: github.event.label.name == 'dejabug'
    runs-on: ubuntu-latest
    steps:
      - uses: ferreyadinarta/dejabug@v0.2.0
        with:
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          # or, to use a Claude subscription: claude-code-oauth-token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

Then add the `dejabug` label to an issue that has a video. The action downloads the video, writes the steps with Claude and comments once. It skips issues without a video and issues it has already commented on.

To run on every new issue instead, use `types: [opened]` and drop the `if:` line. Anyone who can open an issue can then spend your API credit (about $0.55 per video), so the label is the safer default on public repos.

What it sends where: the video frames and the issue text go to Anthropic. The comment contains only what the model wrote from them. The model has no tools; it can't run code or touch your repo.
