---
name: oracle
description: "Use the @steipete/oracle CLI to bundle a prompt plus the right files for GPT-5.4 Pro. On this machine, render/copy with Oracle, then use the @Chrome plugin to submit and watch ChatGPT when the user clearly asked for that context; fall back to manual paste when Chrome automation is unavailable or unsafe."
---

# Oracle (CLI)

Oracle bundles your prompt plus selected files into one "one-shot" request so ChatGPT can answer with real repo context. Treat outputs as advisory and verify them against the codebase and tests.

On this machine, Oracle is a **bundler first**. The default path is:

1. use Oracle to bundle and render the exact prompt plus attachments
2. copy that rendered bundle to the clipboard
3. use the `@Chrome` plugin to open or reuse `https://chatgpt.com`
4. submit the bundle to ChatGPT when the user clearly asked to send that file set
5. watch for the final answer and bring the result back into the agent workflow

Manual paste remains the fallback when Chrome automation is unavailable, logged out, interrupted, or unsafe for the current context.

Do not use Oracle API mode for routine work. Do not use Oracle's native browser automation by default. Do not use remote browser-host flows.

## Preferred Default (macOS)

For ChatGPT runs on this Mac, the default is:

```bash
oracle --render --copy -p "<task>" --file "src/**"
```

Then:

1. Use the `@Chrome` plugin / Codex Chrome Extension, not the in-app `@Browser` plugin.
2. Open or reuse `https://chatgpt.com/` in the user's Chrome session.
3. Verify ChatGPT is logged in by checking for the composer, not a login page.
4. Prefer the current Pro or Extended Pro mode if visible; only change the model/thinking mode when needed.
5. Paste the rendered Oracle bundle from the clipboard.
6. Submit and watch until the final answer is visible.
7. Bring the response back into Codex and verify it against the repo.

Why this is the preferred path:

- Oracle still does the useful part: prompt bundling, file attachment expansion, and markdown rendering
- Chrome can reuse the user's logged-in ChatGPT session and existing tabs
- manual paste is still available when the browser state is not reliable

## Chrome Plugin Path

Use this path for normal Oracle work when the `@Chrome` plugin is available.

Recommended defaults:

- Oracle action: `--render --copy`
- Model in ChatGPT: `GPT-5.4 Pro`
- Browser/session: user's Chrome session via the `@Chrome` plugin at `https://chatgpt.com/`
- Thinking: Pro or Extended Pro when visible; otherwise leave the current selected mode unless the user requested a specific mode
- Attachments: directories and globs plus excludes; avoid secrets

If ChatGPT is logged out, stop after opening the page and ask the human to log in. Do not handle passwords, OTPs, or CAPTCHA.

## Manual-Paste Fallback

Use this path when Chrome automation is unavailable, logged out, interrupted, or not appropriate for the current context.

1. Render and copy the bundle with `oracle --render --copy`.
2. Tell the human the bundle is on the clipboard.
3. Have the human paste and submit it in ChatGPT.
4. Continue only after the human provides the response back.

## Golden Path

1. Pick a tight file set with the minimum files that still contain the truth.
2. Preview what you are about to send with `--dry-run` and `--files-report` when needed.
3. Render and copy the bundle with `oracle --render --copy`.
4. Use the `@Chrome` plugin to open or reuse ChatGPT.
5. If the bundle is clearly authorized and not sensitive, paste and submit it.
6. Watch for the final answer, extract the result, and verify it before acting.

## Commands

- Show help:
  - `oracle --help`

- Check installed/upstream versions:
  - `oracle --version`
  - `npm view @steipete/oracle version dist-tags --json`
  - `npm list -g @steipete/oracle --depth=0`

- Update to the npm-supported latest release:
  - `npm install -g @steipete/oracle@latest`
  - Prefer the npm `latest` dist-tag over older/deprecated semver tags unless the user explicitly asks for a specific version.

- Preview without spending tokens:
  - `oracle --dry-run summary -p "<task>" --file "src/**" --file "!**/*.test.*"`
  - `oracle --dry-run full -p "<task>" --file "src/**"`

- Token and cost sanity:
  - `oracle --dry-run summary --files-report -p "<task>" --file "src/**"`

- Default run:
  - `oracle --render --copy -p "<task>" --file "src/**"`
  - `--copy` is a hidden alias for `--copy-markdown`

## Attaching Files (`--file`)

`--file` accepts files, directories, and globs. Pass it multiple times as needed.

`--file` is local-filesystem context only. Oracle does not directly attach GitHub repos via a GitHub connector, remote repo URL, or Codex connector state. If a repo only exists on GitHub, clone it locally or fetch the specific files you want to attach.

- Include:
  - `--file "src/**"`
  - `--file src/index.ts`
  - `--file docs --file README.md`

- Exclude:
  - `--file "src/**" --file "!src/**/*.test.ts" --file "!**/*.snap"`

- Defaults from the current implementation:
  - Default-ignored dirs: `node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, `tmp`
  - Honors `.gitignore` when expanding globs
  - Does not follow symlinks
  - Dotfiles are filtered unless you explicitly opt in with a pattern like `--file ".github/**"`
  - Files over 1 MB are rejected unless you raise `ORACLE_MAX_FILE_SIZE_BYTES` or `maxFileSizeBytes` in `~/.oracle/config.json`

## Budget and Observability

- Target: keep total input under about 196k tokens
- Use `--files-report` or `--dry-run json` to find token-heavy files before spending
- For hidden and advanced knobs: `oracle --help --verbose`

## Engine Policy

- Normal use is render-and-copy plus `@Chrome` submit/watch
- Manual paste is the fallback
- Do not use `--engine api`
- Do not use `--models`, `--background`, Azure flags, or API follow-up flows for routine work
- Do not use remote browser host/client flows
- On macOS, prefer `oracle --render --copy`

### Oracle Native Browser Mode

Oracle's native browser mode is not the default for Codex work on this machine. Use it only when the user explicitly asks for it or Chrome automation cannot handle the workflow and the user approves the experimental path.

If using Oracle native browser mode for a long Pro run, the installed CLI supports auto-reattach flags:

```bash
oracle --engine browser \
  --browser-timeout 6m \
  --browser-auto-reattach-delay 30s \
  --browser-auto-reattach-interval 2m \
  --browser-auto-reattach-timeout 2m \
  -p "<task>" --file "src/**"
```

These flags apply to Oracle's own browser driver, not to the `@Chrome` plugin.

## Prompt Template

Oracle starts with zero project knowledge. Include:

- Project briefing: stack, build and test commands, platform constraints
- Where things live: key directories, entrypoints, config files, dependency boundaries
- Exact question, what you tried, and the error text verbatim
- Constraints: public API limits, performance budgets, do-not-change areas
- Desired output: patch plan, tests, risky assumptions, options with tradeoffs

### Exhaustive Prompt Pattern

When you expect a long investigation, make the prompt self-contained:

- Top: 6 to 30 sentences with the project briefing and current goal
- Middle: concrete repro steps, exact errors, and what you already tried
- Bottom: attach every context file needed to understand the issue from scratch

Oracle runs are one-shot. If you need the same context later, re-run with the same prompt and `--file` set.

## Safety

- Treat submitting an Oracle bundle to ChatGPT as transmitting the included prompt and file contents to a third party.
- If the user clearly asks to run Oracle on a specific repo/file set, that is enough to submit normal source code and docs.
- Pause before submitting when the selected files or prompt include secrets, `.env` files, API keys, auth tokens, customer data, personal documents, private logs, medical/legal/financial data, browser/search history, or other sensitive data.
- Pause when the file scope is broad or ambiguous enough that you cannot tell whether sensitive data is included.
- Do not attach secrets by default such as `.env`, key files, or auth tokens.
- Prefer just-enough context instead of dumping the whole repo
