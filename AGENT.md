# Entry handoff: make.fun bounty promotion

This repository prepares one quote post for the public X account @WangLin_trx.
The account holder publishes it manually; this build must not post or submit.

## Preserve these entry details

- Bounty: post-x-promote-make-your-own-bounty-01.
- Quote target: https://x.com/makefunai/status/2124915864336236646.
- Posting copy: `post-text.txt`, retaining its paragraph breaks.
- Required line: Make your own bounty on @makefunai: https://make.fun/sponsor/new
- Play code: makefun-fern-mantis-croquet.
- Attach the finished `promo.png` to the quote itself, not as a reply or preview.
- Deadline: November 26, 2026 at 18:35 UTC (November 27 at 01:35 WIB).
- Keep the post and account public until the results on December 11, 2026.

## Current blockers

`POST.json` deliberately retains the starter placeholder. Only after the account
holder publishes the quote may the next agent replace it with that post's real
URL. Never substitute the source post's URL or invent a status ID.

The finished `promo.png` is a 1024 × 1024 image with the official ghost mark,
generated and visually inspected in this session. Use this finished image,
not the earlier `out/layout-preview.png` typography proof.
The deterministic renderer is `render-promo.py` at the repository root; its
required source path is `out/mark-1024.png`. The official source SHA-256 is
`78fc23c446a592dbc9fb7aa65a770bfc2fff7e108e7b4453326c55f2d923b339`.

Recorded transcripts will be bundled by a later agent. Do not fabricate or
rewrite session logs. No bundle, submit, account creation or credential access
is authorized during this build.

## Local program check

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
cmp POST.json out/POST.json
```

The program uses only Node's standard library and copies the file unchanged.
Only genuine replies, reposts and quotes affect the score; likes and views do
not. Do not arrange fake, purchased, self-made or coordinated engagement.
