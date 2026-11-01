# Reel Analytics — the user's project (context for linking)

Source: the user's files `Reel Analytics.xlsx` + `Reel Analytics - Guide.pdf` (Egyptian Arabic guide, 10 chapters), shared 2026-11-01. Not stored in the repo; ask for the latest version if the structure seems to have changed.

## What it is
An Excel tool that answers 3 questions:
1. Which creative worked, and why? → tab **Ads**
2. What do I report this month? → tab **Report**
3. Which product do I shoot next? → tab **What To Shoot** (+ **Products Raw**)

Colour rule: yellow = input, grey = formula (never type), blue = result.
Data: monthly GMT report «A&A Brand Gallery – Creative Report & Scripts» (Meta ads, EGP); SEZLUXE product export (eyewear SKUs like `SUN-JMM-2013-02`).

## Tab Ads (A1:U501) — one row per creative per month
Inputs: Month (`'2026-09` text), Brand, Creative, Reel Code (optional), Category (Ties, Belts, Mixed…), Reach, CTR, Hook Rate, Hold Rate, Purchases, Spend, Purchase Value.
Formulas:
- ROAS = Value/Spend · CPP = Spend/Purchases · AOV = Value/Purchases (all wrapped in `IF(OR(x="",x=0),"",…)`)
- Group = Month & " " & Brand — creatives are compared only inside their month + brand
- Hook Rank / Hold Rank / ROAS Rank = share of the group this creative beats: `COUNTIFS(Group,g,metric,"<"&x)/(COUNTIFS(Group,g)-1)`; blank if group < 2
- Diagnosis (top half = rank ≥ 0.5):
  - ROAS≥.5 & Hook≥.5 → «Winner: stops the scroll and sells» → make 2 variants, tell the media buyer
  - ROAS≥.5 → «Sells, but the opening is weak» → keep body, test new hook
  - Hook≥.5 & Hold<.5 → «Opening works, the body loses them» → keep hook, shorten script
  - Hook≥.5 → «Watched, but did not buy» → problem is product/price/offer, not the video
  - else → «Weak opening» → redo first 3 seconds
- Next Step reads the first word of Diagnosis.

## Tab Report
Pick Month + Brand → Creatives count, Spend, Revenue, Purchases, True ROAS (total value / total spend), Average ROAS, avg Hook/Hold, top performers (MAXIFS + INDEX/MATCH), count per diagnosis, and 3 written lessons: What won / What lost / What we test next.

## Tab What To Shoot / Products Raw
Model = SKU without the last «-NN» (colour). Per model: colours count, and Done counts for Videos / Unboxing / Talking head. Status: 0 pieces → Shoot next, 1 → Needs more, ≥2 → Covered. Priority 1–3 set by hand. Weekly: pick top 5 «Shoot next». (Oct 2026: 75 of 88 SEZLUXE models have no content.)

## September 2026 numbers (Brand Gallery, 9 creatives) — use to test ideas
| Creative | Reach | CTR | Hook | Hold | Purch. | Spend | Value | ROAS |
|---|---|---|---|---|---|---|---|---|
| 1 See the Difference | 128,752 | 3.57% | 20.43% | 5.96% | 22 | 12,910 | 76,655 | 5.94 |
| 2 Elegant Ties (Ties) | 33,108 | 2.48% | 16.26% | 8.67% | 13 | 6,678 | 59,220 | 8.87 |
| 3 More Than the Ordinary | 60,558 | 4.94% | 27.38% | 13.76% | 12 | 5,036 | 28,310 | 5.62 |
| 4 Elegant Ties Variant (Ties) | 192,174 | 6.30% | 56.45% | 12.48% | 11 | 5,277 | 39,410 | 7.47 |
| 5 | 102,308 | 4.57% | 23.46% | 12.77% | 48 | 19,311 | 130,110 | 6.74 |
| 6 New Arrivals (Mixed) | 36,228 | 1.82% | 5.09% | 11.42% | 20 | 12,131 | 107,180 | 8.84 |
| 7 Elegant Belt (Belts) | 102,471 | 3.59% | 22.26% | 10.76% | 18 | 9,223 | 99,210 | 10.76 |
| 8 New Arrivals Combined (Mixed) | 62,300 | 3.73% | 16.88% | 11.35% | 32 | 16,789 | 110,110 | 6.56 |
| 9 Luxury in Every Detail | 67,143 | 5.82% | 22.35% | 23.08% | 10 | 9,553 | 54,140 | 5.67 |
Totals: spend 96,908 · value 704,345 · True ROAS 7.27x. Hook vs ROAS correlation ≈ −0.17.

## Known weaknesses (the file is an early tool; the course outranks it — expect bigger changes than these)
- **Ranks are relative only**: in a bad month the top half is still «Winner». No absolute floor (e.g. break-even ROAS, target CPP).
- **Small samples**: 10–48 purchases per creative; no minimum spend/purchases before trusting a diagnosis.
- **CTR is collected but unused** in the diagnosis (could split "video problem" vs "landing page/offer problem").
- **No fatigue / time view**: monthly totals only; Reel Code is optional, so the same creative can't be tracked across months (frequency, decay).
- **Revenue is Meta-reported**: no COD confirmation/delivery/return rate, so real profit is unknown.
- **Creative attributes aren't tagged** (hook type, format, talent, length, angle), so the file can't say *which kind* of creative wins — only which one.
