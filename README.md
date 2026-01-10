Below is a complete, production-grade README.md for your A-3 system.
It is written to be clear, auditable, launch-ready, and aligned with everything you locked (engine, UI, on-chain, AWS, Gate.io, ML, audits).

You can copy-paste this directly into your GitHub repository root.


---

# A-3 — Canonical Glyph-Based Trading System

A-3 is a **deterministic, ledger-authoritative, glyph-driven trading system** with:

- No stop-losses
- Time-windowed take-profit execution
- Cryptographic auditability (Merkle proofs)
- Multi-user vault architecture
- On-chain enforcement mirror (ERC-20 USDT)
- ML advisory layer (non-authoritative)
- Production-safe AWS + Gate.io LIVE deployment

This repository contains the **complete A-3 stack**: engine, adapters, UI, audits, and infrastructure.

---

## Table of Contents

- [System Overview](#system-overview)
- [Core Principles](#core-principles)
- [Architecture](#architecture)
- [Glyph System](#glyph-system)
- [Trading Logic](#trading-logic)
- [On-Chain Vault](#on-chain-vault)
- [Multi-User Model](#multi-user-model)
- [Audit & Transparency](#audit--transparency)
- [Frontend UI](#frontend-ui)
- [Backend API](#backend-api)
- [Authentication & Security](#authentication--security)
- [AWS Deployment](#aws-deployment)
- [LIVE Mode](#live-mode)
- [Environment Variables](#environment-variables)
- [CI/CD](#cicd)
- [Operational Controls](#operational-controls)
- [Compliance & Invariants](#compliance--invariants)
- [Launch Checklist](#launch-checklist)

---

## System Overview

**A-3** trades using **events (glyphs)** instead of price prediction.

Trades are represented as a **finite state machine** over glyphs, which are:

- Deterministic
- Serializable
- ML-token compatible
- Replay-safe

All capital movement is governed by a **ledger-first authority model**.

---

## Core Principles

- **Ledger is the sole authority**
- **No stop-loss exists**
- **ML is advisory only**
- **UI has no trading power**
- **On-chain contracts enforce rules, not strategies**
- **Backtest ≡ Live ≡ ML ≡ Audit**

---

## Architecture

Users (10 whitelisted Gmail UIDs) │ ▼ Next.js UI (React) │ ▼ FastAPI UI Backend (JWT) │ ├── REST (snapshots) ├── WebSocket (glyphs) ├── Audit API (Merkle proofs) │ ▼ A-3 Trading Engine (Python) │ ├── TP Glyph State Machine ├── Ledger (authoritative) ├── Volatility Selector ├── Gate.io v4 Adapter │ ▼ On-Chain Vault (ERC-20 USDT, Ethereum)

---

## Glyph System

### Locked Vocabulary

G_PAD   – outside trade G_NULL  – trade active, no event G_E     – entry

G_TP_1 … G_TP_10 – take profit levels G_P_i_j          – parallel TP hits G_FC             – forced close G_END            – trade terminal

Glyph IDs are **immutable** and shared across:
- Engine
- ML datasets
- UI
- Audit proofs

---

## Trading Logic

- 10 Take-Profit levels per trade
- Fixed trading windows
- No stop-loss
- Forced close at window end
- One active trade per window
- Compounding is automatic

**Entry rule (LIVE):**

IF vault_balance ≥ 50 USDT AND no active trade AND pair ∈ top volatility set THEN allow ENTRY

---

## On-Chain Vault

- ERC-20 USDT (Ethereum)
- Enforces:
  - Minimum deposit: **50 USDT**
  - Minimum withdrawal: **20 USDT**
  - Withdrawal fee: **3%**
  - Daily withdrawals: **10 per UID**
- UID = Gmail → keccak256 hash
- On-chain balance mirrors off-chain ledger

> On-chain contracts **never trade**.

---

## Multi-User Model

- Exactly **10 pre-configured Gmail accounts**
- Each Gmail:
  - Is a unique UID
  - Has its own ledger balance
  - Has its own on-chain vault entry
- Multiple users may sign up from the same IP

No public registration.

---

## Audit & Transparency

- End-of-day ledger snapshot
- Merkle tree generated daily
- Public Merkle root
- Per-user Merkle proof
- Browser-side verification (trustless)

Users can verify balance inclusion without exposing others.

---

## Frontend UI

**Framework:** Next.js (React)

### Pages
- Welcome
- Get Started
- Policy
- FAQ
- Contact Support
- Login
- Dashboard
- Wallet
- Withdraw
- Audit
- Admin (read-only)

### Features
- TradingView charts (read-only)
- Live glyph visualizer (WebSocket)
- Wallet view
- Withdrawal flow (email confirmation)
- Maintenance mode support

---

## Backend API

**Framework:** FastAPI

### Capabilities
- JWT authentication
- Gmail whitelist enforcement
- Ledger read-only access
- Withdrawal authorization
- Merkle audit proofs
- Admin audit endpoints
- WebSocket glyph streaming

No trading logic exists in the API.

---

## Authentication & Security

- Gmail OAuth
- JWT (HS256)
- Email confirmation for withdrawals
- AWS Secrets Manager for keys
- IAM roles (no static AWS credentials)

---

## AWS Deployment

- Lightsail (starter) or EC2 (scale)
- Dockerized services
- CloudWatch logging
- Secrets Manager for:
  - Gate.io keys
  - Infura RPC
  - JWT secret

---

## LIVE Mode

LIVE mode activates:
- Gate.io v4 execution
- Fee-confirmed reconciliation
- Volatility-based token selection
- AWS logging & fallback logic

UI and ML **cannot trade**.

---

## Environment Variables

### Frontend

NEXT_PUBLIC_API_BASE NEXT_PUBLIC_WS_BASE NEXT_PUBLIC_MAINTENANCE_MODE

### Backend / Engine

MODE=LIVE AWS_REGION MAINTENANCE_MODE

Secrets are loaded from AWS Secrets Manager.

---

## CI/CD

- Docker build
- GitHub Actions
- Push → build → deploy
- No secrets in repo
- Deterministic runtime

---

## Operational Controls

- Maintenance mode (UI + API)
- Admin audit dashboard (read-only)
- Emergency trade skip (window-level)
- Safe rollback (Lightsail ↔ EC2)

---

## Compliance & Invariants

**Locked and immutable:**

- Glyph vocabulary
- TP state machine
- Ledger authority
- On-chain vault rules
- ML advisory-only role

Any system respecting these is **A-3 compliant**.

---

## Launch Checklist

- [ ] Gate.io API keys created
- [ ] AWS Secrets configured
- [ ] IAM role attached
- [ ] On-chain vault deployed
- [ ] Gmail whitelist verified (10 users)
- [ ] Maintenance mode tested
- [ ] Audit page verified
- [ ] LIVE mode enabled

---

## Status

**A-3 is complete, locked, and production-ready.**


---

If you want, next I can:

Split this into ENGINE / UI / INFRA READMEs

Add architecture diagrams

Add legal disclaimer section

Add investor / auditor appendix


Just say the word.
Below is a complete, production-grade engineREADME.md focused only on the A-3 Trading Engine.
It excludes UI, frontend, and marketing content, and documents exactly what operators, auditors, and backend engineers need.

You can drop this file into the engine repository root.


---

# A-3 Trading Engine — Canonical README

The **A-3 Trading Engine** is the deterministic, ledger-authoritative core of the A-3 system.  
It is responsible for **trade execution, capital accounting, glyph emission, and audit-safe logging**.

This engine is **strategy-complete** and **UI-independent**.

---

## Scope of This Engine

### What the Engine DOES
- Executes the A-3 **10-TP glyph state machine**
- Manages **ledger-authoritative capital**
- Selects trading pairs based on **volatility**
- Executes trades via **Gate.io API v4**
- Emits **glyph streams** (REST / WebSocket / logs)
- Produces **ML-ready glyph data**
- Reconciles **fees and fills**
- Writes **AWS CloudWatch logs**
- Mirrors balances to **on-chain vault**

### What the Engine DOES NOT Do
- ❌ User authentication
- ❌ UI rendering
- ❌ Manual trading
- ❌ Stop-loss execution
- ❌ ML-driven execution
- ❌ Fund custody on-chain
- ❌ Admin overrides

---

## Core Design Principles

1. **Ledger is the sole authority**
2. **No stop-loss exists**
3. **Trades are window-bound**
4. **Glyphs are atomic events**
5. **Execution is deterministic**
6. **ML is advisory only**
7. **Backtest ≡ Live ≡ Audit**

---

## Architecture Overview

Price Feed (Gate.io) │ ▼ Volatility Scanner │ ▼ A-3 TP State Machine │ ├── Glyph Emitter ├── Ledger (Authoritative) ├── Fee Reconciliation │ ▼ Gate.io Execution Adapter │ ▼ On-Chain Vault Mirror (ERC-20 USDT)

---

## Glyph System (LOCKED)

### Vocabulary (Immutable)

G_PAD     – outside trade / window G_NULL    – trade active, no event G_E       – entry

G_TP_1 … G_TP_10 – take profit levels G_P_i_j          – parallel TP hits G_FC             – forced close G_END            – trade terminal

- Glyph IDs are **immutable**
- Glyphs are **ML tokens**
- Parallel glyphs are stored in a **side-channel**
- No stop-loss glyph exists

---

## Trading Logic

### Trade Lifecycle

ENTRY → TP1 → TP2 → … → TP10 → END ↘ FORCED_CLOSE → END

### Core Rules
- One trade per window
- Fixed window length
- No backward transitions
- Forced close at window end
- Capital compounds per window

---

## Volatility-Driven Pair Selection

- Engine scans a **universe of pairs**
- Computes short-term volatility
- Selects **top 12 most volatile pairs**
- Orders pairs deterministically
- Trades **one window at a time**

This ensures:
- Capital efficiency
- Deterministic pair ordering
- ML-compatible alignment

---

## Execution Adapter (Gate.io v4)

### Supported Operations
- Market Buy (Entry)
- Limit Sell (TP legs)
- Fee-confirmed fill reconciliation
- REST retry + fallback logic

### Execution Safety
- Retry limits enforced
- REST fallback on timeout
- Window skipped on execution failure
- No partial state mutation

---

## Ledger (Authoritative)

### Ledger Properties
- Single source of truth
- All balance changes pass through ledger
- Fees explicitly recorded
- Slippage reconciled
- Replay-safe

### Ledger Flow

ENTRY allocation → TP fills → Forced close (if any) → Fee reconciliation → Final balance

---

## On-Chain Vault Mirror

- ERC-20 USDT (Ethereum)
- Enforces:
  - Min deposit: 50 USDT
  - Min withdrawal: 20 USDT
  - Withdrawal fee: 3%
  - Daily withdrawal limit: 10
- UID = Gmail → keccak256 hash
- Engine mirrors ledger balances on-chain
- On-chain contract never trades

---

## LIVE Mode

### Activation
```bash
MODE=LIVE

LIVE Behavior

Gate.io v4 execution enabled

AWS CloudWatch logging enabled

Volatility scanner active

Fee reconciliation enforced

UI and ML remain non-authoritative



---

Environment Variables

Required

MODE=LIVE | PAPER | BACKTEST
AWS_REGION

Loaded from AWS Secrets Manager

a3/gate        → Gate.io API keys
a3/infura     → Ethereum RPC
a3/runtime    → runtime tuning

No secrets are stored in code or .env.


---

AWS Integration

CloudWatch Logs (engine output)

IAM Role (no static keys)

Secrets Manager

Lightsail or EC2 compatible

Dockerized runtime



---

Maintenance Mode Interaction

Engine continues running

UI and API may be blocked

Ledger and execution unaffected

Safe for audits and upgrades



---

Failure Handling

Scenario	Behavior

Gate.io API down	Skip window
Price feed timeout	Retry → skip
Fee mismatch	Ledger reconciliation
Secrets unavailable	Fail fast
AWS logging failure	Local fallback


Skipping a window is legal and safe.


---

Determinism & Replay

The engine guarantees:

Same inputs → same glyph outputs

Backtest == Live == Audit

Deterministic volatility selection

Deterministic TP resolution

Deterministic ledger state



---

Compliance & Invariants (LOCKED)

The following must never change:

Glyph vocabulary

TP state machine

Ledger authority

No stop-loss rule

ML advisory-only role

On-chain vault enforcement rules


Any change breaks A-3 compliance.


---

Operational Checklist

[ ] Gate.io keys configured

[ ] AWS Secrets loaded

[ ] IAM role attached

[ ] CloudWatch log group exists

[ ] On-chain vault deployed

[ ] LIVE mode tested

[ ] Maintenance mode tested

[ ] Audit snapshot verified



---

Status

A-3 Trading Engine is complete, locked, and production-ready.

---

If you want next, I can:

- Split this into **Operator vs Developer READMEs**
- Add **sequence diagrams**
- Add **incident response runbook**
- Add **formal invariant appendix**

Just tell me.
