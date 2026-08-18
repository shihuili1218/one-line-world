# one-line-world

Everyone gets exactly **one line**. The repo grows forever.

Each pull request adds exactly **one line** to the repo — a brand-new
file containing just your line, or one more line in a file that is
already here. A validator checks every PR, and valid ones merge
themselves.

## How to play

1. Fork the repo
2. Add one line — create a new file containing just your line, or add
   your line to any existing file
3. Open a pull request
4. If the checks pass, it merges automatically

No reviews, no approvals — the validator decides.

## The rules

**One line, one PR:**

- the PR adds exactly 1 line — in a new file, or in any existing file
- exactly 1 file per PR
- existing lines are never touched: no edits, no deletions, ever
- nothing under `.github/`

**The line itself (every file type):**

- non-empty, no trailing whitespace, max 400 characters
- LF line endings, the file must end with a newline
- no binary content, no control or invisible characters

**TypeScript (`.ts` files):**

- the whole file must pass `tsc --strict` — your line included
- the line itself: no `eval`, `Function` constructor, `while (true)`,
  `for (;;)`, `debugger`, and no `@ts-ignore` / `@ts-nocheck` /
  `@ts-expect-error`

Other file types (`.md`, `.txt`, extensionless, ...) have no language
check — one line of anything is a valid contribution.

The validator lives in [`.github/workflows/`](.github/workflows/) —
reading it is allowed, touching it is not.

## FAQ

**Can I add my line to someone else's file?** Yes. That's the game —
files grow one stranger at a time.

**Can I create a new file?** Yes, containing exactly one line.

**Does my TypeScript actually run?** Yes. The [gallery](https://shihuli1218.github.io/one-line-world/)
compiles every `.ts` file and executes it in a sandboxed frame right on the
page. Use `console.log(...)`, or `export` something — both are shown under
the code. Type-only lines honestly report `no runtime output`.

**Can my line draw or animate?** Yes. If your code puts anything into the
DOM — a `<canvas>` animation, for instance — the card grows a live stage
and it runs right there. `import "./anims/lissajous";` is a complete,
working example: one line, someone else's animation.

**Can I fix a typo in an existing line?** No. Every line is someone's
contribution; lines are append-only.

**Can I use a directory that doesn't exist yet?** Yes. Directories come
into existence when files are added to them.

**Why was my PR rejected?** The check output tells you exactly which
rule you hit.
