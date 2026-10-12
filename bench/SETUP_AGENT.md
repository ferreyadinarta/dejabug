# Benchmark setup + run instructions (one issue at a time)

You are running the dejabug benchmark for a list of GitHub issues. dejabug turns a bug
screen recording into a failing Playwright test. Your job per issue is to SET UP the
app at the buggy and the fixed version, then let dejabug run BLIND, then record results.

Repo: /Users/mkpmobile/Documents/Ferrey Code/dejabug   (run commands from there)
Issue data: bench/issues.json (fields: id, url, video_urls, steps_to_reproduce, fix, ...)
Reference setup (copy its shape): bench/apps/mui-47203 (buggy) and bench/apps/mui-47203-fixed

For each issue in your list:

1. Video: make sure bench/videos/<owner>_<repo>-<number>.<ext> exists (download from
   video_urls[0] with curl -L if missing). Check duration with:
   uv run python -c "import imageio_ffmpeg,subprocess,sys;print(subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-i',sys.argv[1]],capture_output=True,text=True).stderr)" <file> | grep Duration

2. Versions: find the last published npm version WITH the bug and the first WITH the fix
   (fix PR merge date vs `npm view <pkg> time --json`; read the issue, PR and changelog
   via WebFetch on api.github.com / github.com). If the issue has no fix, set up the buggy
   version only.

3. App: create bench/apps/<slug>/ (buggy) and bench/apps/<slug>-fixed/ as minimal Vite +
   React apps (or the smallest equivalent: e.g. `npx create-docusaurus` pinned to the
   version for Docusaurus) that show the SAME component/page/setup as in the video,
   matching it as closely as you reasonably can (same demo content, same props,
   same data). Pin exact versions. Add node_modules/ to its .gitignore.
   Start each with `npm run dev -- --port <PORT> --strictPort` in the background
   (nohup ... &; record the PID), wait for HTTP 200.

4. Sanity check (optional but recommended): you may write a quick throwaway script at
   bench/apps/<slug>/sanity.py to confirm the bug is visible on the buggy build. Never
   put it where dejabug writes, never pass it to dejabug.

5. Run dejabug BLIND (it spawns its own agent, which must not see the issue):
     uv run dejabug run bench/videos/<file> --url http://localhost:<BUGGY_PORT> --blind --tries 2 -o out/bench-run/<slug>
   This can take 5-15 minutes. Run it in the background (nohup ... > out/bench-run/<slug>.log 2>&1 &)
   and poll for out/bench-run/<slug>/result.json (check every ~30 s with a short wait loop,
   e.g. `perl -e 'select(undef,undef,undef,30)'`). Give up after 25 minutes.
   Do NOT edit or help with the generated test. Do NOT edit any file under dejabug/.

6. If result.json says REPRODUCED and a fixed build exists, run the generated test against it:
     uv run dejabug test out/bench-run/<slug>/repro_test.py --url http://localhost:<FIXED_PORT>; echo exit=$?
   (exit 0 = passes on the fix = the test is specific to this bug).

7. Write bench/results/<slug>.json:
   {"id","slug","buggy_version","fixed_version","setup_notes","dejabug_verdict",
    "coverage","attempts_used","seconds","fixed_build_exit","bug_inferred_by_dejabug"
    (one sentence from the agent log / test docstring),"matches_real_bug" (your honest
    yes/partly/no judgement vs the issue), "notes"}

8. Clean up: kill both dev servers (kill <PIDs>; pkill -f "port <PORT>" as backup), then
   delete bench/apps/<slug>/node_modules and bench/apps/<slug>-fixed/node_modules.
   Check `df -h /` — stop and report if free space < 3 GB.

Be honest: a failed reproduction is a valid, useful result. Never adjust a result to look better.
