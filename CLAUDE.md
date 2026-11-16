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
