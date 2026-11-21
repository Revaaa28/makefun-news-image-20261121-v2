# The World in One Day — Saturday 21 November 2026

[![Competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/Revaaa28/makefun-news-image-20261121-v2/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/badge/news-image-20261121/Revaaa28/makefun-news-image-20261121-v2/reward.svg)](https://make.fun/bounty/news-image-20261121)

Entry for the make.fun competition **news-image-20261121**: one
1024×1024 image that sums up the world's news of **Saturday
21 November 2026**.

Version 2 is a dense broadsheet front page: **36 stories across 7
regions**, every one of them an event that happened — or was first
reported — on that Saturday in at least one time zone. It carries a
stat strip, a region bar, three illustrated hero stories, six
illustrated briefs and a 27-item index. A red **DATE CHECK** box on
the page names the big stories deliberately *left out* because they
belong to Thursday 19 or Friday 20 November, not to Saturday.

All artwork is original flat drawing rendered in code (no
photographs). Claims are attributed to their sources; unconfirmed
reports are flagged as such.

## The 36 stories

**Heroes**
1. **Antalya, Türkiye** — COP31 runs into overtime with no deal (Reuters, UN News)
2. **Kryvyi Rih & Kyiv, Ukraine** — Russian strikes kill 12 in a day across Ukraine (AP, city officials)
3. **Riyadh, Saudi Arabia** — Coalition downs three Houthi missiles over Riyadh (Reuters, AFP)

**Briefs**
4. **Warsaw** — Rutte in Warsaw as Poland seeks more cover (AP)
5. **Mercury** — BepiColombo reaches Mercury after eight years (ESA)
6. **Washington** — US clears some 900,000 AI chips for China (House panel)
7. **Kharg Island** — Iran masses tankers to test the US blockade (Reports)
8. **Imphal, India** — Manipur's capital counts 11 dead as violence spreads (Officials)
9. **Pasadena** — Voyager 1 is now one light-day from Earth (NASA)

**Index**
10. **Delhi** — Modi opens an SCO dialogue forum on culture and cooperation. (PIB)
11. **London** — A UK military official says Britain hit Moscow with cyberattacks. (UK)
12. **Jakarta** — The ministry asks Google why 19,000 YouTube accounts are gone. (Ministry)
13. **Sumy** — A HIMARS strike wipes out 20 Russian commanders, reports say. (Reports)
14. **California** — The attorney general subpoenas Nvidia over its ex-CEO's exit. (AG)
15. **New Delhi** — India launches its first home-made H5N1 vaccine, for chickens. (PIB)
16. **Copenhagen** — Denmark charges two over a plot to kill a Ukrainian rapper. (Reports)
17. **Brussels** — The EU completes its largest-ever reform payment to Kyiv, nearly 8bn euros. (EU)
18. **Hodeidah** — The UN warns coalition port strikes threaten Yemen's aid lifeline. (UN, AP)
19. **Wellington** — India resume day three on 159/1; NZ made 368, Nicholls 175 not out. (Scorecard)
20. **Turin** — Medvedev meets Zverev in tonight's ATP semi-final. (ATP)
21. **Las Vegas** — F1 qualifying runs under the lights today; race on Sunday. (F1)
22. **Melbourne** — Australia and England open their T20 series at the MCG tonight. (AFP diary)
23. **Berlin** — Students march against rearmament and mandatory military service. (Reports)
24. **Baghdad** — Iraq's pipeline chief is arrested over oil-trading claims. (Reports)
25. **Seoul** — South Korean exporters pass a $1 trillion year on chip demand. (Reports)
26. **Nairobi** — Kenya's Treasury keeps fuel subsidies to hold down the import bill. (Reports)
27. **Lagos** — A security report counts 7.8bn naira in ransoms paid in the year to July. (Report)
28. **Atlanta** — Measles ends US elimination status; cases are the highest in 35 years. (Reports)
29. **Brasilia** — Brazil advances an Indigenous land bill as Raoni visits. (Reports)
30. **Madrid** — A general strike halts Spain; Amnesty faults police force. (Reports)
31. **Rome** — Workers and students march against Meloni's budget. (Reports)
32. **Los Angeles** — A jury convicts the man who started the 2025 Palisades Fire. (Court reports)
33. **Washington** — Trump: no rush on new Iran strikes; may not decide until 2027. (Interview)
34. **Kyiv** — Ukraine to send large-scale food aid to nine countries. (Kyiv)
35. **Bern** — Switzerland calls the Myanmar ruling an important step. (Swiss govt)
36. **Mumbai** — IndusInd ends its ex-CEO Kathpalia's job and seeks to recover his pay. (Reuters)

## How to run

```sh
python3 build.py   # renders entry.png (1024x1024, deterministic)
python3 main.py    # validates entry.png and copies it to the output dir
```

`main.py` is standard-library only. It checks the PNG signature,
every chunk's CRC32, the IHDR dimensions (≤1024×1024), the 1 MiB
size cap and the presence of IEND, then copies the file byte-for-byte
to `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to `/output`, then
`./out`). Two runs of `build.py` produce byte-identical output, and
`main.py`'s copies are byte-identical to `entry.png`.

See [SOURCES.md](SOURCES.md) for per-story provenance and the date
discipline notes.
