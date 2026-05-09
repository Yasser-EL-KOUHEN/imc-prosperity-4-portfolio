---
type: daily
tags: [meta, tooling, setup, gsd, obsidian, mcp, claude-code]
sources: []
updated: 2026-04-27
---

# Agentic Tooling Setup

Session note from 2026-04-27 — the day the vault and workflow were initialized.

## What Was Set Up

- **GSD framework** — structured Claude Code planning with phases (PLAN.md → SUMMARY.md → execute loop)
- **Obsidian Prosperity Vault** — this wiki, with MCP connection to Claude Code for persistent context memory across sessions
- **Git repo** — initialized for the full competition project; vault lives inside as `prosperity-vault/`
- **MCP → vault pipeline** — Claude can read and write vault pages directly via the MCP Obsidian connector, meaning research findings, backtest results, and decisions get filed immediately rather than lost in conversation context

## Why This Matters

Without persistent memory, every Claude session re-derives context from scratch — expensive and inconsistent. The vault + MCP setup means:
- Decisions made in session N are available in session N+100
- Backtests are filed with evidence, not just summarized in chat
- The [[CLAUDE]] schema ensures consistency: every page has frontmatter, sources, and cross-links

## Impact on the Competition

The agentic tooling was load-bearing. The Phase 12–17 work (counterparty exploitation, R5 directional strategy, version history v1→v42) was executed across multiple sessions spanning days. Without the vault as a persistent second-brain, the decision trail from [[Research/Decisions_Log]] D1–D25 would not have been recoverable.

Key phases that ran inside this workflow:
- [[Backtests/Phase12_Counterparty]] — Mark taxonomy, Signal C, 4 bug fixes, anti-regression gate
- [[Backtests/Phase13_R5_Directional]] — 7 directional products, $261K baseline, OOS gate
- [[Backtests/Phase14_R5_EDA]] — 6 parallel analyses; XGBoost AUROC 0.653; rest null
- [[Backtests/Phase15_AlphaLab]] — GRU/XGB ML deadend; valid_R²=−0.169

The culminating output of this multi-session work: [[Rounds/Round5_findings]] (v1→v42 post-mortem).

## Links

[[CLAUDE]] · [[Overview]] · [[log]] · [[Carry_Forward]] · [[Research/Decisions_Log]] · [[Backtests/Phase12_Counterparty]] · [[Backtests/Phase13_R5_Directional]] · [[Backtests/Phase14_R5_EDA]] · [[Backtests/Phase15_AlphaLab]] · [[Rounds/Round5_findings]]
