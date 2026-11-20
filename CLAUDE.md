## The four rules (the owner of this repo, 12 Nov 2026)

Every agent working in this repo follows these on every task. They are in the CLAUDE.md of each of his repos.

1. **No silent assumptions.** If a request can mean more than one thing, ask before building and say
   out loud what is unclear. Never build on a guess you didn't mention.
2. **No over-engineering.** Write the least code that solves the real problem. No extra layers for code
   that runs once, no clever patterns that make it harder to maintain.
3. **No collateral damage.** Touch only the files and functions the task needs. If something nearby looks
   wrong, say so; don't quietly fix it.
4. **Say what you don't know.** If you're not sure, say so. Never invent a function, a fact or a result;
   make the doubt visible.

## Modern web (the owner of this repo, 15 Nov 2026)

Any work on a web page or a web app (HTML, CSS, client-side JavaScript) follows Google Chrome's «Modern Web Guidance»,
always its current version. Before writing that code, run `npx -y modern-web-guidance@latest search "<2-5 words naming
the task>"`, read the guide it names with `npx -y modern-web-guidance@latest retrieve "<guide id>"`, and follow it. It
does not apply to backend code, scripts, data or tests. Source: github.com/GoogleChrome/modern-web-guidance (Apache 2.0).

## Look before you deliver (the owner of this repo, 18 Nov 2026)

Never hand the owner anything you have not looked at yourself. Before you send it, open it the way
he will: render a page or a design on a phone (390 px) and on a desktop (1440 px) and look at the
screenshots, open a document or file, run the code, read the text back. Compare it with what was
asked and with the work it must match, fix what is wrong, and only then deliver. If you cannot look
at it, say so plainly instead of sending it. This holds even when a tool's own instructions say not
to check the result.

## Agentic engineering, not vibe coding (the owner of this repo, 20 Nov 2026)

Every agent working in this repo follows Google's «The New SDLC With Vibe Coding» (Osmani, Saboo, Kartakis, May 2026):
what separates engineering from vibe coding is verification. The owner does not read code, so he owns the spec and the
checks, and an independent agent reviews the code. Details and page references: the `agentic-engineering` skill; if it
is not loaded, these six lines are enough.

1. **Spec before code.** Write what the work must do and how we will know it works; the owner approves that.
2. **Tests and evals before code.** Tests for fixed behaviour, an eval with a rubric for anything an AI model decides.
   The bar is the eval, not the demo.
3. **An independent reviewer.** What ships is checked by an agent that did not write it, plus the automatic checks.
   Every new package is checked to be real (models invent package names, and attackers register them).
4. **Every repeated mistake becomes one line** in this file or in a skill, so no agent repeats it.
5. **Short rule files.** This file keeps only what every task needs; procedures go in skills or docs, linked by a line.
6. **Prototype or production, said out loud.** Exploration may move fast; anything people use gets the full checks.
