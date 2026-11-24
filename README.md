# Tuesday 24 November 2026 — the world's news in one picture

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/isyaweb-a11y/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/isyaweb-a11y/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One 1024×1024 PNG that sums up **Tuesday 24 November 2026** in world
news: 45 stories in total — 3 leads, 12 numbered panels pinned to a
dotted world map, and 30 briefs — plus a UTC timeline strip,
CONFIRMED / REPORTED / CLAIM status chips with a named source on every
story, and a DATE CHECK box that names the big stories left out
because they belong to other days.

## The three leads

1. **Rescuers race to find 34 missing after a candy factory fire
   kills 24.** The search went on through Tuesday at the Banten
   plant in Indonesia, as families waited for word of the workers
   still unaccounted for. (AP)
2. **Gaza's land, air and water left toxic for decades, report
   warns.** Oxfam and CEOBS found contamination signs across more
   than 99% of the Strip — heavy metals, asbestos and dioxins that
   threaten survival itself. (OXFAM)
3. **Huang walks back into Nvidia HQ as Washington turns up the
   heat.** A day after the board reinstated him, lawmakers attacked
   the move, the Senate set a 3 December hearing, and the probes
   into the chip giant multiplied. (REUTERS)

Every story here happened or was first reported on 24 November 2026,
checked against Reuters, AP, the Washington Post, WSJ, El País,
Oxfam, CEOBS, ESA and official statements.

## How it runs

```sh
python3 main.py /tmp/out.png
```

With no argument it writes to `$MAKEFUN_OUTPUT_DIR/entry.png`, or
`/output/entry.png` — the path the grader reads.

`main.py` is standard library only. It validates `entry.png` — PNG
signature, a full chunk walk with every chunk's CRC checked, exactly
one IHDR, at least one IDAT, nothing after IEND, 1024×1024, no more
than 1 MiB — copies it byte-for-byte to the output path, and reads
the copy back to compare hashes. It also decompresses the IDAT
payload and checks the decoded bytes are exactly the size the header
promises, so a CRC-valid but undecodable image cannot slip through.
The image itself was rendered at build time and is committed as
`entry.png`; nothing is drawn while the entry is graded.

Verified at build time: `python3 main.py /tmp/out.png` produces a
byte-identical copy — sha256
`5387f36d797031fdd8595312954906799420b1b543ac8ea0486fa7892dc4e57b`
(209,795 bytes).

## Inside the picture

- Giant date masthead and a UTC timeline strip
- 3 illustrated leads
- 12 illustrated panels, each pinned to the dotted world map
- 30 numbered briefs, a DATE CHECK box, and a sources footer
- Original drawings throughout — no photos, no third-party images

---

Built for the [make.fun bounty](https://make.fun/bounty/news-image-20261124).
Play make.fun with my referral link: https://make.fun/r/sc1d8ke0
