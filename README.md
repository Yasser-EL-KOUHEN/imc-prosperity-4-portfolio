# IMC Prosperity 4 — A Solo Entry's Lessons 🦊

This write-up shares the algorithm, the manual derivations, and the lessons that brought a solo entry to **#346 globally out of 18,803 teams (top 1.84%)** in IMC Prosperity 4 (2026). Country rank **#11 in France**. Final cumulative score (R3 + R4 + R5): **383,727 XIREC**. Every product, every round, every failure trail is documented here.

<table width="80%">
  <tbody>
    <tr>
      <td align="center" valign="top" width="220px">
        <a href="https://github.com/Yasser-EL-KOUHEN">
          <img src="https://github.com/Yasser-EL-KOUHEN.png" width="160" alt="Yasser EL KOUHEN"/>
          <br/>
          <p><b>Yasser EL KOUHEN</b><br/><sub>Solo competitor, no team</sub></p>
        </a>
      </td>
      <td valign="top">
        <p><b>Background:</b> MPSI / MP* (intensive French preparatory-class mathematics and physics) → MEng Computer Science / Machine Learning → MSc Data Science &amp; Business Analytics.</p>
        <p><b>Market-finance prior to this competition:</b> none. The quant content here was learned <em>during</em> the competition itself, with deliberate use of ML analogies to bridge unfamiliar concepts to familiar ones (AR(1), regularisation, train/test distribution mismatch, calibrated probability, Kelly-style sizing).</p>
        <p><b>Why I entered:</b> in late February 2026, I missed an in-person Natixis CIB recruiting event in London because the flights from Paris were too expensive. Three weeks later I made up for it: I paid double the cost of the missed trip to attend the ETH Zurich Kontakt Party in mid-March. That evening I met quants and recruiters from Jane Street, Citadel, Hudson River Trading, Optiver, IMC Trading, and Flow Traders. By the end of it I had decided what I want to do — become a quantitative researcher / trader at a top market-maker. I had no quant project on my CV, no proof I belonged. Prosperity 4 was my first concrete step.</p>
      </td>
    </tr>
  </tbody>
</table>

<br/>

I'm sharing this repository for three reasons. **First**, as a portfolio piece for grad-school applications and quant-trading recruiting — the work in here is what I have to show. **Second**, for the next solo competitor who arrives at Prosperity 5 with the same starting point I had (no quant project on the CV, no formal market-finance background) and wants a worked example of how to spend 17 days on it. **Third**, to give back to the Prosperity community: prior write-ups from teams like [Frankfurt Hedgehogs (Prosperity 3, 2nd globally)](https://github.com/jmerle/imc-prosperity-3-backtester), [Stanford Cardinal (Prosperity 2)](https://github.com/ShubhamAnandJain/IMC-Prosperity-2023-Stanford-Cardinal), and [Jasper](https://github.com/jmerle/imc-prosperity-2) were what I learned from when I started; I'd like this to play the same role for somebody else.

This write-up goes beyond presenting the final algorithm. It walks through every round — the algorithmic side and the manual side — in the order the competition presented them, including the strategies that did not work and the decisions behind the ones that did. The 17 days were a real effort with real low moments (the Round 3 first-backtest 0-PnL incident is documented honestly), and the report tries to capture the experience as well as the result.

If you're a recruiter or admissions reader who wants the substance without reading 200+ pages, the right entry point is **[`report/report-extract.pdf`](report/report-extract.pdf)** (12 pages, distilled). If you want the full chronological depth, **[`report/report.pdf`](report/report.pdf)** (217 pages) has every numerical claim sourced and the failed approaches preserved as evidence.

<br/>

## Final Result

| Metric | Value |
|---|---|
| Overall rank | **#346 / 18,803** (top 1.84%) |
| Algorithmic rank | #537 |
| Manual rank | **#204** |
| Country rank | **#11** (France; 1,549 universities; 117 countries) |
| Final cumulative score (R3+R4+R5) | **383,727 XIREC** |
| Algorithmic share of total | 40.6% (155,759) |
| Manual share of total | **59.4%** (227,968) |

Cumulative-rank trajectory: **~#2,000 → #1,522 → #802 → #592 → #346**. Monotone improvement across all five rounds.

<br/>

## IMC Prosperity 4

[IMC Prosperity 4](https://prosperity.imc.com/) (2026) is a global [algorithmic trading](https://www.investopedia.com/terms/a/algorithmictrading.asp) and game-theory competition run by [IMC Trading](https://www.imc.com/), a market-making firm headquartered in Amsterdam and Chicago. The 2026 edition ran across **5 rounds and 17 days** with **18,803 teams** participating across **117 countries**. The challenge was to design a Python algorithm to maximise profit across simulated products that mirror real-world opportunities — [market making](https://www.investopedia.com/terms/m/marketmaker.asp), [mean reversion](https://www.investopedia.com/terms/m/meanreversion.asp), [statistical arbitrage](https://www.investopedia.com/terms/s/statisticalarbitrage.asp), [options](https://www.investopedia.com/terms/o/option.asp) trading, and counterparty exploitation.

Each team submitted a single-file Python algorithm (`trader.py`) implementing a `Trader` class. On every tick (every 100ms of simulated time), the algorithm received a `TradingState` snapshot of the [limit order book](https://www.investopedia.com/terms/o/order-book.asp) for every tradable product and decided what orders to send. Profit was denominated in a synthetic currency called **XIREC**.

Each round also featured a **manual challenge** — closed-form game-theory or optimisation puzzles whose solutions fed directly into the round's PnL. In Prosperity 3 these were a small fraction of total PnL, but in Prosperity 4 they ended up carrying **59.4%** of the cumulative score for me — more on that below.

The competition was structured as a 5-round progression:
- **Round 0 (Tutorial)**: 2 stable products, no points; just to hook your code up to the IMC infrastructure.
- **Rounds 1–2 (Qualifier)**: 3 real products + manual auction/allocation games. Cumulative ≥ 200K to advance.
- **Rounds 3–5 (Cumulative-scoring phase)**: options arrive in R3, counterparty information in R4, full 50-product structural break in R5. Only these three rounds count for the final ranking.

For the official documentation, see the [Prosperity 4 platform](https://prosperity.imc.com/).

<br/>

## Structural Overview

- [Tools](#tools)
- [Algorithmic Challenge](#algorithmic-challenge)
  - [Round 0 (Tutorial): EMERALDS and TOMATOES](#round-0-tutorial-emeralds-and-tomatoes)
  - [Round 1: Mean Reversion + Trend (ACO + IPR)](#round-1-mean-reversion--trend-aco--ipr)
  - [Round 2: Same Algorithm, Manual-Heavy Round](#round-2-same-algorithm-manual-heavy-round)
  - [Round 3: HYDROGEL Mean-Reversion + VEV Options](#round-3-hydrogel-mean-reversion--vev-options)
  - [Round 4: Counterparty Exploitation (Mark Taxonomy)](#round-4-counterparty-exploitation-mark-taxonomy)
  - [Round 5: 50 Products, ±10 Limit, the v34 → v42 Evolution](#round-5-50-products-10-limit-the-v34--v42-evolution)
- [Manual Challenge](#manual-challenge)
  - [Round 1: Intarian Welcome — Clearing-Price Auction](#round-1-intarian-welcome--clearing-price-auction)
  - [Round 2: MAF Bid + Invest & Expand](#round-2-maf-bid--invest--expand)
  - [Round 3: Bio-Pods Bayesian-Nash Auction](#round-3-bio-pods-bayesian-nash-auction)
  - [Round 4: AETHER_CRYSTAL Exotic Options](#round-4-aether_crystal-exotic-options)
  - [Round 5: Ashflow Alpha Allocation](#round-5-ashflow-alpha-allocation)
- [Lessons Learned](#lessons-learned)
- [Day-1 Plan for Prosperity 5](#day-1-plan-for-prosperity-5)
- [FAQ](#faq)
- [Honest Acknowledgements](#honest-acknowledgements)

<br/>

## Tools

### Backtester

I used two backtesters with different roles:

1. **[`prosperity3bt`](https://github.com/jmerle/imc-prosperity-3-backtester)** (the open-source local backtester, retroactively retargeted at Prosperity 4 data). Fast iteration, full simulation. Documented systematic ~8.6× fill inflation versus the real Prosperity engine when run with `--match-trades all`. Useful for catching bugs and exploring parameter ranges; **not trustworthy for tier decisions**.
2. **The Prosperity website's official backtester**. Real engine, real fills, but only runs the **first 10% of Day 4** (~100,000 of 1,000,000 ticks). The most reliable per-version PnL signal I had during the competition.

The disconnect between these two was the central methodological insight of Round 5 — see [Lessons Learned](#lessons-learned).

### Cross-Version Prosperity-Log Methodology

For Round 5, I aggregated **N=12 official Prosperity backtester logs** across versions (v1, v9, v11, v14, v21, v23, v25, v26, v27, v31, v34, v35, v36, v39, v40) and used per-product PnL stability across versions as the blacklist signal. Products with average PnL ≤ −$500 AND 0/12 positive runs were blacklisted. This is documented in `round5/research/analyze_prosperity_logs.py`.

### Prosperity Vault (Obsidian Wiki)

I kept a 115-page [second-brain](https://en.wikipedia.org/wiki/Building_a_Second_Brain) Obsidian wiki at [`prosperity-vault/`](prosperity-vault/) organised into Concepts, Strategies, Products, Rounds, Backtests, Parameters, Research, Performance, Marks (R4 counterparty profiles), and Manuals. Every load-bearing claim in the report is traceable here. It also serves as the source-of-truth check during writing — I cross-referenced the report against the vault to catch inconsistencies.

### Planning Trail (GSD Framework)

The full project planning lives in [`.planning/`](.planning/) under 16 numbered phases (`01-backtest-engine` through `16-heavyweight-gru-synthetic`). Each phase has a `PLAN.md` (what I'm trying to do), a `RESEARCH.md` (what I've found that informs the plan), and a `SUMMARY.md` (what was delivered). This was overkill for Round 1 and exactly right for Round 5.

<br/>

# Algorithmic Challenge

## Round 0 (Tutorial): EMERALDS and TOMATOES

The tutorial round paid no points and existed solely so teams could verify their submission pipeline. Two products:

- **EMERALDS**: stable fair value at 10,000. The classic introduction to [market making](https://www.investopedia.com/terms/m/marketmaker.asp) — post bids below 10,000 and asks above, earn the spread. Almost no inventory risk because the price doesn't move.
- **TOMATOES**: drifting fair value with short-term mean-reversion structure. Lag-1 autocorrelation of price changes was ~−0.42 in the full sample. The standard playbook here is an [adaptive market-maker](https://en.wikipedia.org/wiki/Market_maker): track an EMA of the mid, post quotes around it, correct for AR(1) reversion when the recent change is large.

The tutorial round was where I built the foundational primitives the rest of the competition leveraged: order-book parsing, fill-priority simulation, position tracking, the mean-reversion correction term. Documented in [report.tex §Tutorial Products](report/report.tex). Round 0 paid no points, but the AR(1) framework here carried directly into Round 1 ACO and Round 3 HYDROGEL.

<br/>

## Round 1: Mean Reversion + Trend (ACO + IPR)

**Products: ACO (ASH_COATED_OSMIUM), IPR (INTARIAN_PEPPER_ROOT), EMERALDS.**

ACO and IPR were the qualifier-round real products. They had structurally opposite dynamics, and the fact that the competition presented them simultaneously was a deliberate test:

### ACO — Anchor-Blend Market Making (ρ₁ = −0.495)

ACO had a stable fundamental fair value near 10,000 with strong short-term mean-reversion (lag-1 autocorrelation of mid-changes ρ = −0.494 measured between consecutive two-sided book states; even stronger at large moves: ρ = −0.74 for |Δmid| ∈ [5,10] ticks). I treated this as an anchor-blended fair-value problem: $\mathrm{FV}_t = 0.85 \cdot \mathrm{EMA}_t + 0.15 \cdot 10{,}000$, with quotes posted symmetrically around FV and aggressive takes triggered when the book offered prices outside the next-tick reverted FV. Documented in [report.tex §Round 1 EDA](report/report.tex#L1613) and [report §Post-Round-1 Edge Audit](report/report.tex). The full V1-submitted source is [`round1/logs/V1/118067.py`](round1/logs/V1/118067.py).

### IPR — Greedy Long Accumulation (+0.1/tick trend)

IPR had a strong intraday upward drift (+0.1 ticks/timestep on average) with no exploitable mean-reversion. The right strategy was to ignore market-making entirely and just accumulate the long position aggressively up to the position cap. I never sold IPR. The strategy hit roughly 99.2% of the structural ceiling — 238,054 / 240,000 XIREC over the qualifying period (limited only by the spread cost of building a 50-unit position aggressively across 1–2 hours of ticks).

The asymmetry between ACO and IPR was instructive: ACO rewarded patient calibration of a continuous reversion model; IPR rewarded recognising a directional drift and taking it in one shape. Trying to apply ACO's framework to IPR (or vice versa) would have failed. Documented in [report.tex §Round 1 Strategy Design](report/report.tex#L1611).

<br/>

## Round 2: Same Algorithm, Manual-Heavy Round

Round 2 introduced no new tradable products — ACO + IPR + EMERALDS continued from Round 1. The algorithmic side was a continuation of the V1 trader (the only deliberate change was an explicit `bid()` method to participate in the **MAF auction** on the manual side, see below). The strategic shift in Round 2 was **all-in on the manuals**: MAF (a one-shot bid auction for a +25% quote-volume bonus) and Invest & Expand (a 3-pillar resource-allocation game). These delivered $\$153{,}345$ XIREC manual PnL — the largest manual contribution of any round, and on its own ~40% of the entire R3+R4+R5 cumulative-scoring total. See [Manual Challenge: Round 2](#round-2-maf-bid--invest--expand) below.

<br/>

## Round 3: HYDROGEL Mean-Reversion + VEV Options

**Products: HYDROGEL_PACK, VELVETFRUIT_EXTRACT, VEV vouchers (10 strikes from 4,000 to 6,500). Round 1–2 products retired.**

Round 3 was the structural break before Round 5's structural break. All previous products were retired. **Options arrived for the first time** in the competition: the VEV voucher chain was a 10-strike European call ladder on the underlying VELVETFRUIT_EXTRACT. The introduction of [Black–Scholes](https://www.investopedia.com/terms/b/blackscholes.asp), [implied volatility](https://www.investopedia.com/terms/i/iv.asp), the [Greeks](https://www.investopedia.com/terms/g/greeks.asp), and [delta hedging](https://www.investopedia.com/terms/d/deltahedging.asp) on top of an algorithm that had been working on simple mean-reverting products was disorienting. The first official Round 3 backtest came back near $0 PnL after I had been at a steady ~$10K through Round 2. I document this honestly in the report (§Round 3 personal note) — it felt like falling into a well with no end. Three days later, the same algorithm earned +$40K on the official computation day and my rank jumped #1,500 → #800.

### HYDROGEL — AR(1) Mean-Reversion Market Making

HYDROGEL had **bucketed lag-1 autocorrelation**: small mid-changes had weak reversion (ρ_small ≈ 0.08), large mid-changes had strong reversion (ρ_large ≈ 0.42). The bucketing matters: a single ρ underweights the large-move regime where the signal actually lives. I calibrated this via a 49-config grid sweep ([round3/research/hydrogel_audit.py](round3/research/hydrogel_audit.py)) and added an anchor-blend term ($w = 0.20$ blend toward 10,000) to keep the fair value from drifting away during low-information periods.

Documented in [report.tex §Round 3 — Phase 4 HYDROGEL Parameter Tuning](report/report.tex). HYDROGEL was the strongest single algorithmic product of Round 3 (~131,640 XIREC across the round's 3 days of training data).

### VEV Vouchers — Per-Strike IV Surface + Two-Level Quoting

The VEV voucher chain (strikes 4,000 / 4,500 / 5,000 / 5,100 / 5,200 / 5,300 / 5,400 / 5,500 / 6,000 / 6,500) was a textbook setup for [implied-volatility surface](https://en.wikipedia.org/wiki/Volatility_smile) calibration. With $r=0$ (the Prosperity simulator has zero risk-free rate), Black–Scholes simplifies cleanly. I calibrated a per-strike σ via Newton–Raphson inversion of the market mid prices, getting a smile pattern with σ in [0.230, 0.249] across strikes — the trough at 0.230 sat at the ATM 5,400 strike, with smile on both wings as expected from demand asymmetry.

Strategy: posted two-level quotes (inner + outer) on each strike with sizing biased by the **IV z-score** — when implied vol on a strike was high relative to the smile-fitted curve, I sized larger on the bid (passive long-volatility); when low, larger on the ask. Delta hedging was done **passively only** (joining VEV mid quotes rather than crossing the spread), since spread-crossing on a 200-position-limit underlying was prohibitively expensive. Documented in [report.tex §Round 3 Phase 6–8 (Black–Scholes / Quoting / OBI)](report/report.tex).

The Phase 11 box-and-lines signal investigation was a confirmed **null result** ([report.tex §Round 3 Phase 11](report/report.tex)): support/resistance levels did not survive out-of-sample testing on Day 4. Documented as the first time I formally killed a signal candidate.

### Round 3 Final

R3 algo PnL: $40,800. R3 manual PnL (Bio-Pods, see below): $75,238. Round total: $116,038. The cumulative-scoring phase begins fresh at R3, so this is also the start of the final-leaderboard total.

<br/>

## Round 4: Counterparty Exploitation (Mark Taxonomy)

**Products: HYDROGEL + VEV continuation. New data: every trade now lists the named bot it was against.**

Round 4 added one piece of information to the trade record: every trade now exposed the identity of the bot counterparty (Mark_01, Mark_14, Mark_22, Mark_38, Mark_49, Mark_55, Mark_67). This was the prompt for a [counterparty taxonomy](prosperity-vault/Strategies/Counterparty_Exploitation.md) — clustering bots by behaviour and biasing my quotes accordingly.

I built per-Mark profiles ([prosperity-vault/Marks/](prosperity-vault/Marks/)):

- **Mark_67** — dip buyer (+1,510 net VELVETFRUIT). Buys only at ≥5MA lows; never sells. Strong directional signal: when Mark_67 buys, it is informed.
- **Mark_49** — local-high seller (−956 net VEL). Passive at local highs; 500 ms cooldown after detection.
- **Mark_22** — OTM call short-seller (~184 events/day). Frequency is one to two orders of magnitude higher than Mark_67/49; excluded from `mark_net` composite signal because including it would drown the directional signal.
- **Mark_14 / Mark_38** — bilateral pair on HYDROGEL. Tick-alternating maker roles; net ~0 by construction.
- **Mark_01** — VELVETFRUIT MM + long-OTM-call accumulator (Mark_22's bilateral counterpart).
- **Mark_55** — symmetric taker / arbitrageur. Net ~0; market-efficiency signal only.

The composite signal `mark67 - mark49` (the two strongest directional Marks) biased VELVETFRUIT bid/ask aggressiveness when |signal| ≥ 5. Mark_49's local-high seller behaviour also triggered a 500 ms half-size cooldown after detection (Signal C in [report.tex §Round 4 Phase 12](report/report.tex)).

R4 algo PnL: +$57,048. R4 manual PnL (AETHER_CRYSTAL exotic options): +$57,516. Round total: +$114,564.

<br/>

## Round 5: 50 Products, ±10 Limit, the v34 → v42 Evolution

**Products: 50 entirely new products in 10 categories. All previous products retired. Hard ±10 position limit per product.**

Round 5 was the structural break of the competition. The 10 categories:

| Category | Products | Day-2 mid range |
|---|---|---|
| GALAXY_SOUNDS | DARK_MATTER, BLACK_HOLES, PLANETARY_RINGS, SOLAR_WINDS, SOLAR_FLAMES | wide |
| SLEEP_POD | SUEDE, LAMB_WOOL, POLYESTER, NYLON, COTTON | medium |
| MICROCHIP | CIRCLE, OVAL, SQUARE, RECTANGLE, TRIANGLE | medium |
| PEBBLES | XS, S, M, L, XL | medium (strongest within-category structure: XL +10 vs S/M/L/XS −10 directional basket) |
| ROBOT | VACUUMING, MOPPING, DISHES, LAUNDRY, IRONING | medium |
| UV_VISOR | YELLOW, AMBER, ORANGE, RED, MAGENTA | medium |
| TRANSLATOR | SPACE_GRAY, ASTRO_BLACK, ECLIPSE_CHARCOAL, GRAPHITE_MIST, VOID_BLUE | tightest spreads |
| PANEL | 1X2, 2X2, 1X4, 2X4, 4X4 | medium (3 of 5 ended on the blacklist) |
| OXYGEN_SHAKE | MORNING_BREATH, EVENING_BREATH, MINT, CHOCOLATE, GARLIC | wide (GARLIC +10 was top single-product earner) |
| SNACKPACK | CHOCOLATE, VANILLA, PISTACHIO, STRAWBERRY, RASPBERRY | structural pairs (CHOC/VAN ρ=−0.916; STRAW/PIST ρ=+0.913; STRAW/RASP ρ=−0.924) |

All 50 products had AR(1) coefficient ≈ +0.999 — effectively unit-root prices. Tradable mean-reversion (the R3 / Tutorial regime) was gone. The only extractable signal was **multi-day directional drift**.

The strategy went through **42 versioned iterations** — see [`round5/strategies/round5_v1_trader.py`](round5/strategies/round5_v1_trader.py) through [`round5/strategies/round5_v42_trader.py`](round5/strategies/round5_v42_trader.py). The major waypoints:

- **v1 → v23**: experimented with multiple architectures including ML-based direction classifiers (XGBoost AUROC OOS = 0.653, did not survive PnL gate; GRU sequence model at AUROC ≈ 0.50 on real Day 4 OOS). All ML failed the PnL gate. Phase 13 was locked at directional ±10 holds + per-product MM with skew.
- **v34** (the directional baseline): 12 directional positions at fixed ±10 + 9 TIER3 products at LIMIT 5 + 3-product zero-fill blacklist. Prosperity backtester score: $62,299.
- **v36** (cross-version log methodology): added 8 more BLACKLIST products selected by N=12 cross-version Prosperity log evidence. **Backtester champion at $78,799.** Was NOT submitted.
- **v40** (the controlled disaster, not submitted): removed TIER3 entirely (LIMIT 5 → 10 on 9 products) on the false hypothesis "more trades on the full day = recovery". The adverse-selection loss roughly **doubled**. Empirical demonstration of Insight 2.
- **v41** (TIER3 restored + STRAWBERRY +10 added): undid v40's mistake, plus added SNACKPACK_STRAWBERRY directional based on HIGH-confidence sign-stable full-day-drift gate.
- **v42 (submitted)**: v41 + 8 confirmed cross-version losers added to BLACKLIST. Final composition: 13 directional positions, 11 BLACKLIST products (LIMIT 0), 2 small-loss TIER3 products (LIMIT 5), HEDGED_NO_SKEW pair on SNACKPACK CHOC+VAN (ρ=−0.916, inner_size 8 instead of default 6, no inventory skew), default MM on the rest. **Backtester score $72,000 — deliberately $6,799 below v36.**

The v36 → v42 decision is documented as the single most consequential decision of the competition. v36 was the obvious local-optimum submission; choosing v42 meant accepting a measurable backtester regression in exchange for expected full-day robustness. See [Lessons Learned](#lessons-learned) below for what this felt like in real time.

### Round 5 realised PnL decomposition (v42, JSON-verified)

Re-applying v42's strategy lists to the per-product PnL in [`performance/algorithmic trading/round 5/581865.json`](performance/algorithmic%20trading/round%205/581865.json):

| Bucket | Realised PnL | Notes |
|---|---:|---|
| DIRECTIONAL (13 products at ±10) | **+$67,111** | 7 of 13 paid; PEBBLES sub-basket carried (+$38,974 alone) |
| HEDGED_NO_SKEW (SNACKPACK CHOC+VAN) | **+$9,858** | structural-pair hypothesis validated on Day 5 |
| TIER3 (2 products at LIMIT 5) | −$2,764 | contained as designed |
| BLACKLIST (11 products at LIMIT 0) | **$0 exactly** | as designed; saved an estimated $30K–$45K vs counterfactual |
| DEFAULT_MM (other products) | −$16,294 | dominated by MICROCHIP_SQUARE alone (−$18,636) |
| **Total v42 (full Day 5)** | **+$57,911** | matches the JSON `profit` field exactly |

Round 5 algo + manual: **$153,125** — the largest single-round increment of the competition, lifting the cumulative score from $230,601 to **$383,727** and the overall rank from #592 to **#346**.

<br/>

# Manual Challenge

The manual challenges in Prosperity 4 ended up carrying **59.4% of the cumulative score**. Five challenges, one per round; their realised contributions were $71,500 (R1) + $153,345 (R2) + $75,238 (R3) + $57,516 (R4) + $95,214 (R5) = **$452,813 across the competition**, with $227,968 of that landing in the cumulative-scoring phase (R3+R4+R5).

## Round 1: Intarian Welcome — Clearing-Price Auction

A one-time uniform-price [call auction](https://www.investopedia.com/terms/c/callauction.asp) on two goods (Dryland Flax, Ember Mushroom). Each player submits one limit order per good. The exchange clears at the single price that maximises traded volume; ties broken upward. All fills execute at the clearing price regardless of submitted bid.

**Strategy.** Because all fills execute at the cleared $P^*$ (not the submitted bid), bidding above the implied $P^*$ is free for existing fills — it only affects the cleared price itself. The optimisation reduces to: choose $(B, Q)$ to maximise $f(B,Q) \cdot (\mathrm{liq} - P^*(B,Q) - \mathrm{fee})$. Closed-form for both goods after enumerating cleared prices.

**Submitted: Dryland Flax 5k @ 29 (forces $P^*=29$); Ember Mushroom 35k @ 18.** Realised: **$71,500**. Displayed manual rank ~#72, but the actual tie-broken rank was ~#3,000 — this is a **massive-tie regime** where every quantitatively-prepared team converges on the same closed-form solution and the displayed rank is essentially noise. As I would discover in R3, this pattern repeats. Full derivation in [report.tex §Manual Trading: Intarian Welcome Auction](report/report.tex).

## Round 2: MAF Bid + Invest & Expand

Two manual challenges in R2.

### Part B: MAF (Market Access Fee) Bid

A one-shot sealed-bid auction for a +25% quote-volume bonus. Win condition: bid above the median peer bid. Payoff: $\pi(b) = V_{\text{extra}} - b$ if won, 0 otherwise. The challenge is estimating $V_{\text{extra}}$ — the value of the +25% quote bonus on next-round PnL.

**Estimate.** Local backtest of $V_{\text{extra}}$ at +25% volume gave $13K, but the website-PnL/local-PnL ratio was 168/291 ≈ 0.58 (a 42% queue-illusion haircut on the local figure). Website-scaled estimate: $V_{\text{extra}} \in [5,000, 7,000]$. Asymmetric regret: missing low costs $V_{\text{extra}} \approx 6$K; missing high costs only the excess over the necessary bid (~1K). 6:1 regret ratio favours overbidding.

**Submitted: $b^* = 3,000.** Won the auction. Verified by the official Prosperity per-component algo JSON (raw R2 PnL 94,529 vs displayed-leaderboard 91,529 = +3,000 rebate exactly matching the bid). The volume bonus itself was modest because the IPR position-cap ceiling already bound at 99.2% without the bonus, so the marginal alpha was small — but the bid mechanism worked as designed.

### Part C: Invest & Expand

A 3-pillar resource-allocation game: choose $(x_R, x_S, x_V) \in [0,100]^3$ summing to 100, where $x_R$ is the "Refining" fraction (logarithmic return), $x_S$ is "Scale" (linear return), $x_V$ is "Visibility" (rank-proxy return based on relative position vs peers).

**Solution.** First-order conditions on a log×linear×rank EV system. Setting marginal returns equal across pillars: $x_S = 12.5 + x_V$ and $(100 - x_R - x_V) = (1 + x_R) \ln(1 + x_R)$. Numerical root: $x_V \approx 35.7$, $x_R \approx 16.1$, $x_S \approx 48.2$. Snapping to the integer grid: $(16, 48, 36)$. Exhaustive grid-search over $\{0..100\}^3$ confirms this is the global optimum at $f^* = 110,065$ XIREC under uniform-rank prior.

**Submitted: (15, 50, 35)** — slight deviation from the FOC optimum to hedge against my uncertainty in the rank-proxy distribution. Realised **$153,345 XIREC** — the largest manual contribution of any round. Full derivation in [report.tex §Round 2 Part C: Manual "Invest & Expand"](report/report.tex).

## Round 3: Bio-Pods Bayesian-Nash Auction

A two-bid sealed auction with $b_1, b_2$ on the discrete grid $\{670, 675, ..., 920\}$. Each counterparty has a uniformly distributed reserve $r_i$ on the same grid. Profit per counterparty: $920 - b_1$ if first-bid hits, otherwise $920 - b_2$ (with a cubic penalty if $b_2 < \overline{b_2}$, the population mean second bid).

**Symmetric Bayesian-Nash equilibrium.** At symmetric NE, $\overline{b_2} = b_2^*$ and the penalty multiplier is exactly 1. The expected profit reduces to $f(b_1, b_2) = (b_1 - 670)/255 \cdot (920 - b_1) + (b_2 - b_1)/255 \cdot (920 - b_2)$. FOCs give the linear system $2b_1 - b_2 = 670$, $-b_1 + 2b_2 = 920$. Discrete optimum on the 5-unit grid: **$(b_1^*, b_2^*) = (755, 840)$**, $f^* = 81.67$ per counterparty.

**Submitted: (760, 855)** — the *robust* play from the sensitivity table, hedging against peer over-bidding above the focal-point NE. The hypothesis was wrong: realised peer behaviour clustered at the focal-point NE, and the unique-NE (755, 840) would have been strictly better. Realised PnL: **$75,238 over N=1,000 counterparties** (75.24/CP, 92% of the $f^* = 81.67$ NE optimum).

Displayed manual rank #234 was the same massive-tie regime as R1 — many teams converged on the same focal-point NE. True tie-broken rank ~#1,200. Full derivation in [report.tex §Bio-Pod Manual Auction: Bayesian-Nash Solution](report/report.tex).

## Round 4: AETHER_CRYSTAL Exotic Options

A 12-instrument exotic-options portfolio on AETHER_CRYSTAL (GBM-modelled underlying with σ ≈ 251% annualised, $S_0 = 50$). The instruments included:

- 8 vanilla calls and puts at strikes {35, 40, 45, 50, 60} with two expiries (T_1 = 2w, T_2 = 3w)
- **AC_50_CO**: a [chooser option](https://en.wikipedia.org/wiki/Chooser_option) (K=50, with chooser date $T_c < T$) — pricing: $V_{\text{chooser}} = C(T) + P(T_c)$ at $r=0$
- **AC_40_BP**: a [binary put](https://www.investopedia.com/terms/b/binary-option.asp) (K=40, payout 10) — fair value $10 \cdot N(-d_2)$
- **AC_45_KO**: a [knock-out put](https://en.wikipedia.org/wiki/Barrier_option) (K=45, barrier B=35) — Merton barrier formula plus Broadie–Glasserman discrete adjustment for the 60-tick discrete observation grid

**Edge analysis.** The market-implied prices revealed exploitable mispricings at three structural points: chooser **+$0.30 sell edge**, binary-put **+$0.232 sell edge**, knock-out put **+$0.045 buy edge**. The naked binary-put short was hedged by a [bull put spread](https://www.investopedia.com/terms/b/bullputspread.asp) (short the AC_40_BP, long the AC_40_P, short the AC_35_P) to eliminate cliff risk. The chooser arbitrage was static-replicated as $C(T) + P(T_c)$.

**Submitted: 12-instrument portfolio.** Pre-trade expected value $E[+175,200]$. Realised **$57,516 — 33% of E**. The shortfall was not a pricing error: the realised underlying path was V-shaped (sharp drawdown into $T_1$, recovery into $T_2$), which knocked the long-knockout-put hedges out and ate most of the chooser-arb edge. Critically, peer position data published after the round showed that the median competitor ran a substantively similar portfolio — this was a **common-knowledge manual** where every quantitatively-prepared team converged on the same Black–Scholes-priced trade list, and when everyone's edge collapses on the same path, no one out-performs.

Full derivation in [report.tex §Round 4 Manual: Vanilla Just Isn't Exotic Enough](report/report.tex).

## Round 5: Ashflow Alpha Allocation

A one-day-only allocation game on the Ignith exchange. **9 goods**, budget $B = 1,000,000$ XIREC. Per-product fee: quadratic in the percentage allocation $p_i \in [0, 100]$: $\mathrm{fee}_i = (p_i / 100)^2 \cdot B$. Gross return: $100 \cdot p_i \cdot s_i$ where $s_i$ is the per-archetype "Ashflow signal" — but the news on each product gave only an *archetype classification*, not a signal magnitude. The challenge was: classify each product into one of ~6 archetypes, infer the signal $s_i$, allocate.

**ML analogy.** The fee is structurally identical to **L2 regularisation with $\lambda = 100$**. The gross return is linear in $p_i$. Closed-form ridge solution: $p_i^* = s_i / 2$. At the optimum, net PnL per product equals the fee paid: $\Pi_i^* = 100 \cdot (p_i^*)^2 = \mathrm{fee}_i$.

**Submitted allocation.** Classified 6 of 9 goods into the bullish/bearish archetypes I had identified, allocated $p_i^* = s_i / 2$ on each, totalling 85% of the budget; left 3 goods at $p = 0$ (sparse solution because the archetype model assigned $s = 0$ to those three). Model-PnL prediction: $140,100$.

**Realised: $95,214** — about 68% of model PnL. Back-solved $s_i$ across the 6 allocated archetypes: 4 of 6 were directionally correct (sign right, magnitude estimate within tolerance); the remaining 2 (Magma + Ashes) were directionally right but with magnitude estimates an order of magnitude too small. This is the **asymmetric-information manual** where the alpha lives in the decomposition (which archetype taxonomy you choose) rather than the formula. Full derivation in [report.tex §Manual Challenge — Ashflow Alpha (Ignith Exchange)](report/report.tex).

<br/>

# Lessons Learned

These are written in personal voice, not formal third-person. The full versions are in [report/report.pdf §Conclusion](report/report.pdf) and [report/report-extract.pdf §Lessons Learned](report/report-extract.pdf).

### Round 3 nearly broke me, then taught me the most.

I had been at a steady ~$10K PnL through Round 2; the first Round 3 backtest came back near $0. The introduction of options on top of an already-failing strategy felt like falling into a well with no end. Three days later the same algorithm earned +$40K on the official computation day; my rank jumped #1,500 → #800. The oscillation taught me: local backtest numbers can be wildly off the real engine, emotional response to a low number tells me nothing about the underlying signal, and persistence through a bad rank is just the price of being there at the next reading.

### The backtester taught me what overfitting actually feels like.

v36 won my local backtester at $78,799. v42 came in at $72,000 — a real $6,799 regression. v36 was the local optimum and submitting it was the obvious move. But the Prosperity backtester runs only 10% of one day; the competition scores the full next day. Under naive linear scaling, the backtester predicts $720K full-day; the realised was $57,911 — Day 5 was about 12× weaker than the first 10% of Day 4. v36 had hit its local-window number by blacklisting two products whose drift was negative in the early window but positive over the full day. I had read about overfitting in every ML textbook; this was the first time I felt what it actually does to your decisions in real time. It terrified me to ship the lower number.

### Manuals carried 59.4% of the cumulative score — and that says something.

I put far more hours into the algorithmic side than the manuals. My algorithmic rank (#537) was meaningfully weaker than my manual rank (#204). The manuals were essentially closed-form game-theory puzzles: read the rules carefully, write the right code once. The algorithm rewards continuous iteration and patient calibration. Both are skills; I now know which I need to deepen for the role I want.

### The before-and-after.

Before Prosperity 4, I had no quant project on my CV, no track record in this field, and no concrete picture of how a serious quant works. Seventeen days later I have a framework. I know what to study, what to build next, and how to be patient with the gap between where I am and where I want to be. The result — top 1.84%, country #11, monotone improvement #2,000 → #346 across all five rounds — is not the end-state I want, but it is a concrete signal that the trajectory works if I keep at it.

<br/>

# Day-1 Plan for Prosperity 5

If I entered next year's competition tomorrow, four concrete actions would change from how I started this one.

1. **Manuals first, every round, before the algorithm.** This year I left the manuals to the last few hours of each round, after the algorithmic work was already deep. The manuals are closed-form: their PnL ceiling is fixed once the puzzle is decoded, and the optimisation is bounded. The algorithm is open-ended; it will absorb every minute you give it. Doing manuals first lets the algorithm time become the residual — not the other way round. R3 Bio-Pods and R5 Ashflow were both submitted under time pressure hours before the deadline; this alone would have improved both.
2. **Understand the signal before implementing the strategy.** I caught myself multiple times this year writing code first and rationalising the alpha after. Round 5 made the cost of this concrete: the v40 TIER3-removal mistake came from not actually understanding why TIER3 was set the way it was in v34 to begin with. Next year, every strategy goes through a written one-paragraph justification (*what is the structural source of edge here*) before any implementation.
3. **Use the LLM as a research assistant, not as a code-writer-of-record.** This was a real failure mode for me this year. When I was tired or stuck, I asked Claude to write a function and shipped it without fully reading what it did. Some of the bugs that cost me the most — the R3 website-backtester 0-PnL incident among them — happened in code I had not actually read line-by-line. Next year: the LLM is a research collaborator for understanding edges, exploring concepts, and explaining unfamiliar mathematics. It is not a code generator I deploy without review. Every line of trader code I submit, I read.
4. **Read the code I write.** Corollary of (3). Before any submission, read every line of the trader file top-to-bottom, with intent. This sounds basic. It is.

<br/>

# FAQ

### Why did the manuals carry 59.4% of the total when most teams treat them as a side game?

Two reasons. First, the manuals in Prosperity 4 had real magnitude — R2 Invest & Expand alone paid $153,345 XIREC, larger than any single algorithmic round-contribution. Second, the asymmetric-information manuals (R2 I&E, R5 Ashflow) had real solver-level alpha; the common-knowledge manuals (R1 Intarian Welcome, R3 Bio-Pods, R4 AETHER) paid out in massive-tie regimes where the closed-form optimum is what every quantitatively-prepared team submits and the displayed rank is essentially noise. For a solo competitor with limited time, the manual side of the competition has higher ROI per hour than the algorithmic side. I learned this too late.

### Why did v42 score lower than v36 on the backtester but I submitted v42 anyway?

Because the Prosperity backtester runs only the first 10% of Day 4, while the competition scores the full Day 5. v36 was the local-window optimum, but it had hit its number by blacklisting two products whose drift was negative in the early window and positive over the full day. v42 kept those products. Under naive 10× linear scaling, both versions' backtester numbers were structurally not the actual scoring scale, and v36's specific edge over v42 was an artefact of the window. See the v42 decision-moment paragraph in [report.tex §v42 — The Final Submitted Strategy](report/report.tex#L6734) and Insight 1 in [report-extract.pdf](report/report-extract.pdf).

### How can I verify the v42 bucket decomposition?

The official Prosperity per-product algo JSON for Round 5 is at [`performance/algorithmic trading/round 5/581865.json`](performance/algorithmic%20trading/round%205/581865.json). Re-applying v42's strategy lists from [`round5/strategies/round5_v42_trader.py`](round5/strategies/round5_v42_trader.py) (TARGETS_DIR, MM_BLACKLIST, TIER3_PRODUCTS, HEDGED_NO_SKEW) to the per-product `profit_and_loss` field at the last timestamp gives DIRECTIONAL +$67,111 / HEDGED +$9,858 / TIER3 −$2,764 / BLACKLIST $0 / DEFAULT_MM −$16,294, summing to the JSON's `profit` field of $57,911 exactly. The verification script is documented in [report.tex §v42 final-design](report/report.tex#L6734).

### Why is local backtest PnL not the same as Prosperity backtest PnL?

Two distinct biases. **(1) Queue-priority illusion**: the open-source `prosperity3bt` with `--match-trades all` fills our orders against any historical trade that crosses our quoted price, regardless of queue priority. On the real exchange, our quotes sit behind every existing order at that price level and only fill if the bot's queue ahead of us is exhausted. **(2) Counterparty model**: the local engine has no model of which bots will trade against us; the real engine does. The combined inflation on Round 5 was approximately **8.6×** (e.g. v34 local across 3 days ~$532K vs real Day-4-first-10% $62,299). For tier decisions (which products to blacklist, which to TIER3) only the real engine's logs are trustworthy.

### Are options strategies in Prosperity competitive with the rest?

In R3 they were. The VEV voucher chain offered a per-strike implied-volatility surface that any team familiar with Black–Scholes could calibrate. Best results came from passive two-sided quoting biased by IV z-score, not from aggressive directional or gamma-scalp positions (those bled to spread costs). In R4 the AETHER_CRYSTAL exotic-options manual was the same picture — the Black–Scholes pricing edges (chooser +$0.30, binary-put +$0.232, knock-out put +$0.045) were obvious to any prepared team. The R4 33%-of-E result is the cost of common-knowledge convergence: my edge collapsed when the population's edge collapsed.

### Did Claude (the LLM) write the strategy code?

No. The strategy logic, the version evolution v1 → v42, the manual derivations, the failed approaches and the decisions are mine. The LLM was used substantially during the *writing* of this report and the README — for editorial assistance, structural feedback, JSON-verification of numerical claims, and typographic polish. The personal narrative and the technical content are mine; the phrasing in some sections benefited from LLM assistance. I'm flagging this transparently because the report's polish is part of what makes it useful as a portfolio piece, and I'd rather a reader know than guess. **Day-1 Plan item #3 above** is the lesson I'm taking forward: treat the LLM as a research assistant for understanding and writing, not as a code-writer-of-record for trader strategy.

### What would I do differently with hindsight?

Three load-bearing changes would have lifted v42's $57,911 algo realisation:
1. Add **MICROCHIP_SQUARE** to BLACKLIST (Day-5 alone: +$18,636 save). Cross-version log evidence was inconsistent so it failed my criterion; a complementary drift-magnitude blacklist criterion would have caught it.
2. Add the v37-recommended **GALAXY_SOUNDS_BLACK_HOLES flip** (−10 instead of +10) on the strict condition that Day 5 sub-window was opening down. The v37 hypothesis was wrong over Days 2–4 but correct on Day 5 specifically.
3. Tighten **HEDGED_NO_SKEW inner_size** from 8 to 10 (the position-limit ceiling). The pair absorbed more flow than designed; the captured spread was $9,858 vs an estimable $12,000.

Hypothetical v43 with all three changes: ~$80K algo + $95K Ashflow ≈ $175K Round 5, vs realised $153K. A ~14% uplift, but every component is hindsight-only.

<br/>

# Honest Acknowledgements

- **The vault, the planning trail, the 76 research scripts, the 42 R5 versioned traders, and every strategic decision are mine.** The reports were written iteratively with substantial editorial assistance from Claude (Anthropic's LLM), specifically: structural feedback on document organisation, threading the personal narrative I shared in conversation through the technical sections, JSON-verifying numerical claims against the official Prosperity per-product results, formal bibliography formatting, and typographic polish. The personal narrative, the technical content, the v34→v42 evolution, the failed approaches, and the conclusions are mine. The phrasing in some sections benefited from LLM assistance. I'm flagging this explicitly because the report's polish is part of what makes it useful as a portfolio piece.
- **The competition, the simulator, the bots, the round briefings, the official scoring, and the product names** (HYDROGEL_PACK, VELVETFRUIT_EXTRACT, the SNACKPACK family, etc.) are IMC Trading's. This repository documents my engagement with their public competition; it is not affiliated with IMC.
- **Prior-competition write-ups I learned from** (and recommend): the [Frankfurt Hedgehogs Prosperity 3 write-up](https://github.com/Tan-yon/imc-prosperity-3-hedgehogs) (2nd place 2025) — the structural inspiration for this README; [Stanford Cardinal's Prosperity 2 repo](https://github.com/ShubhamAnandJain/IMC-Prosperity-2023-Stanford-Cardinal); [Jasper's open-source backtester and writeups](https://github.com/jmerle/imc-prosperity-2). The bot-pattern detection idea (counterparty taxonomy) was a continuation of methods documented in those repos.

<br/>

# Reach out

- **GitHub**: [@Yasser-EL-KOUHEN](https://github.com/Yasser-EL-KOUHEN)
- **For QR / QT recruiting or grad-school admissions**: open an issue on this repo or contact via the channels listed on my GitHub profile.

If you're a future Prosperity competitor and any of this helps you, I'd be grateful to hear about it. The competitive surface-area in this competition is high, and a solo entrant at the start has very few worked examples to learn from. This repository is partly my attempt to leave one.
