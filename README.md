# Bi-dimention
Bidimention is a modular, vault-first digital asset exchange and automation engine built for deterministic trading, secure custody, and scalable execution. It integrates Redis, AWS, and CI/CD pipelines to power state-driven strategies, rebalancing, and observability-ready infrastructure.

# Bidimention Trading Engine  
**Glyph-Driven · Deterministic · Vault-First**

Bidimention is a deterministic, window-based trading engine built around a **glyph formalism** that unifies:

- Backtesting  
- Live execution  
- TradingView visualization  
- JSON audit logs  
- Multi-pair correlation  
- Machine-learning tokenization  

The same glyph stream drives **backtests, live trading, UI playback, audit verification, and ML training**.

The system is designed with **strict custody separation**, **deterministic replay**, and **institution-grade auditability**.

Nothing in this system is heuristic or discretionary.

---

## Core Invariants (Non-Negotiable)

- Deterministic execution (no randomness)
- Continuous 24/7 rolling windows (never pause)
- No stop-loss (window-forced close only)
- Exactly **10 Take-Profit (TP)** levels per trade
- Parallel TP hits allowed
- Locked trading universe (USDT pairs only)
- Exchange is **execution-only**
- Vault is the **source of truth**
- UI is **read-only**
- All truth is ledger-derived

---

## Glyph Formalism

Every trade emits a **strictly ordered glyph stream**:

| Glyph | Meaning |
|------:|--------|
| `G_E` | Entry |
| `G_TP_i` | Take-Profit i |
| `G_P_i_j` | Parallel TP hit |
| `G_FC` | Window-forced close |
| `G_END` | Trade terminal |

Rules:

- Multiple glyphs per bar allowed  
- Order is preserved  
- No mutation, no deletion  
- Serializable and ML-safe  

Backtests, live execution, UI playback, and ML training **consume the same glyphs**.

---

## System Architecture

### 1. Engine (Authoritative Logic)

- Implements the **A-3 deterministic strategy**
- Schedules continuous rolling windows
- Allocates fixed capital per window
- Executes the 10-TP ladder
- Emits glyphs (JSON / CSV)
- Fully replayable offline and online

The engine **never**:
- Reads from the UI  
- Accepts discretionary input  
- Touches custody  
- Knows whether it is “live” or “offline”  

---

### 2. Backend (Data Plane Only)

- Webhook ingestion (TradingView-compatible)
- Glyph schema validation
- Deterministic ordering
- Immutable persistence (JSONL / CSV)
- Reconciliation and exports
- ML token stream generation

The backend **never**:
- Makes trading decisions  
- Alters glyphs  
- Holds funds  

---

### 3. Vault & Rebalancing (Custody Truth)

- Vault is the **authoritative balance source**
- All capital starts and ends in the vault
- Exchange accounts are **temporary execution surfaces**

**Rebalancing is explicit and deterministic:**

- Before a window:  
  - Capital is provisioned from the vault
- During execution:  
  - Exchange executes orders only
- After window completion (offline or online):  
  - Realized PnL is reconciled
  - Funds are **settled back to the vault**
  - Ledger reflects final truth

Offline simulations and live trading follow **the same rebalance logic**.

---

### 4. UI (Read-Only Observability)

- Live glyph playback
- Window timelines and PnL
- Playback scrubber (frame-accurate)
- CSV / JSON export
- Dark / light mode
- Accessibility & multilingual support

The UI **cannot**:
- Trigger trades  
- Move funds  
- Modify state  

It only explains **what already happened**.

---

### 5. Audit Layer

Built to **prove correctness**, not optimize performance.

Stored artifacts:

- Immutable glyph logs
- Order submissions & fills
- Fee breakdowns
- Reconciliation reports
- Deterministic replay proofs
- ML tensor hashes

Guarantees:

- Every trade is traceable
- Every TP is auditable
- Every replay is identical
- No hidden behavior exists

---

## Offline ↔ Online Parity

| Mode | Engine | Backend | Vault | UI |
|----:|:------:|:-------:|:----:|:--:|
| Offline | ✅ | ✅ | ✅ | ✅ |
| Online  | ✅ | ✅ | ✅ | ✅ |

- The engine can **think offline**
- Execution **requires explicit intent**
- Ledger truth is identical in all modes
- UI behavior never changes

---

## Repository Structure

```text
engine/      # A-3 deterministic engine & glyph state machine
backend/     # APIs, ingestion, reconciliation, ML exports
ui/          # Read-only dashboard & playback
audit/       # Logs, proofs, compliance artifacts
data/        # Glyph logs & tensors (gitignored in prod)

# Engine — A-3 Glyph Trading Core

The Engine is the **sole authoritative decision-maker** in the Bidimention system.

It implements the **A-3 strategy** using a **formal, deterministic glyph state machine**.
It decides *when* and *what* to trade — never *how* execution occurs.

The Engine is **pure logic**.

---

## 🔐 Authority Model

The Engine is the **only component that thinks**.

- Generates trade intent
- Emits glyphs
- Mutates the authoritative ledger
- Enforces strategy invariants

All other components (backend, execution, UI, audit) are **downstream consumers only**.

---

## Core Responsibilities

- Window scheduling  
  - 30-day epochs  
  - 12 windows per day  
- Entry gating  
  - Spot balance ≥ 50 USDT  
- Capital allocation  
  - 20% per active window  
- A-3 strategy evaluation  
- 10-TP ladder generation  
- Parallel TP detection  
- Window-forced close (no stop-loss)  
- Glyph emission (JSON / CSV / JSONL)  
- Deterministic replay (offline & live)  

---

## Explicit Non-Responsibilities (Hard Rules)

The Engine **never**:

❌ Holds funds  
❌ Accesses private keys  
❌ Executes orders  
❌ Reads UI state  
❌ Trusts exchange reports  
❌ Accepts discretionary input  
❌ Uses OAuth / Firebase / Firestore  
❌ Performs ML inference  
❌ Makes API calls  

If any of the above appear in this directory, **CI MUST FAIL**.

---

## Supported Trading Pairs

LINK_USDT  
UNI_USDT  
PEPE_USDT  
AAVE_USDT  
ETH_USDT  
ENA_USDT  
ONDO_USDT  
OKB_USDT  
ARB_USDT  
GT_USDT  
NEAR_USDT  
BONK_USDT  

Pair activation is governed by **volatility and configuration constants only**.

---

## Glyph Formalism

Each trade emits a **strictly ordered glyph stream**.

| Glyph     | Meaning                         |
|----------|---------------------------------|
| `G_E`    | Entry                           |
| `G_TP_i` | Take-Profit level *i*           |
| `G_P_i_j`| Parallel TP hit                 |
| `G_FC`   | Forced close (window end)       |
| `G_END`  | Trade terminal                  |

### Glyph Rules

- Multiple glyphs per bar allowed  
- No stop-loss glyph exists  
- Order is strictly preserved  
- Append-only  
- Serializable  
- ML-safe  

### Lifecycle

# Backend — Glyph Ingestion, Ledger, and Read-Only APIs

The Backend is the **policy-enforced data and coordination plane** of the Bidimention system.

It ingests **glyph events**, validates and persists them immutably, reconciles externally
confirmed execution data when explicitly enabled, and exposes **read-only APIs** for
visibility, audit, replay, and machine-learning use.

The backend **does not decide** and **does not mutate strategy state**.

---

## Core Design Doctrine

- Deterministic
- Append-only
- Read-only by default
- No silent mutation
- No strategy logic
- No custody authority

The backend is a **truth server**, not a trader.

---

## Functional Roles (Layered)

The backend operates in **strictly separated layers**, some of which may be disabled
at runtime.

### 1. Glyph Ingestion Layer (Always On)

Ingests glyph events from TradingView and other authorized producers.

#### Responsibilities

- TradingView-compatible webhook ingestion
- Pair universe enforcement (locked)
- Glyph schema validation
- Deterministic ordering
- Per-pair separation
- JSONL persistence
- ML token stream generation

#### Accepted Glyph Inputs

Each glyph event **must** contain:

- `pair`
- `timestamp` (ISO-8601)
- `trade_id`
- `glyph`
- `price`

Invalid glyphs or unauthorized pairs are **rejected**.
No glyph is mutated.

#### Guarantees

- No silent drops
- No execution logic
- No custody logic
- No mutation of glyph data

---

### 2. Pair Universe (Locked)

- Only predefined **USDT pairs** are accepted
- No dynamic symbols
- No user-supplied assets
- Enforcement happens at ingress

---

### 3. Persistence Layer (Append-Only)

The backend persists data **immutably**.

#### Outputs

- Global glyph event log
- Per-pair glyph logs
- Append-only ledger
- ML token files (one token per line)

All persisted data is replayable and ML-safe.

---

### 4. Optional Execution Reconciliation Adapter (Explicitly Enabled)

> ⚠️ This layer is **disabled by default**.

When explicitly enabled, the backend may **observe** execution results from external
systems for reconciliation only.

#### Responsibilities (Observer-Only)

- Gate.io API v4 adapter (read execution results)
- Fee-confirmed reconciliation
- Executed quantity verification  
  `executed_qty == sum(fills.amount)`
- Fee verification  
  `fees == sum(fills.fee)`
- AWS fallback execution *confirmation* (never initiation)

#### Execution Flow (Observed, Not Driven)

```text
Glyph → Order (external) → Fill → Fee → Ledger → ML

# UI — Bidimention Read-Only Observability Dashboard

The Bidimention UI is a **strictly read-only visualization layer**.

It reflects **ledger-derived truth only**.  
It never executes trades, moves funds, or influences strategy.

If the UI disappears, **trading continues safely**.

---

## 🎯 Purpose

The UI exists to:

- Visualize **what already happened**
- Provide transparency for users and auditors
- Enable deterministic inspection and replay
- Surface reconciliation and settlement state

It is **not** a control plane.

---

## 🚫 Explicit Non-Responsibilities

The UI **cannot**:

- Place trades
- Modify engine state
- Influence risk or execution
- Access private keys
- Interact directly with exchanges
- Mutate ledgers or balances

There are **no write paths**.

---

## 🌐 Pages

### Public Pages
- Welcome
- Get Started
- Policy
- FAQ
- Contact Support

### Authenticated Pages
- Dashboard
- Vault Balance
- Transaction History
- Deposit Instructions
- Withdrawal Requests
- Security Settings
- Playback & PnL
- Audit Attestation

---

## 🔐 Authentication Model

- Exactly **4 pre-configured users**
- Gmail-only whitelist
- OTP + Google Authenticator (2FA)
- Nigerian phone number validation (withdrawals only)

> Authentication enables **visibility**, not authority.

---

## 📊 Core Features

- Ledger-derived vault balances
- Allocated vs free capital (informational)
- Unsettled PnL
- Settlement timestamps
- Rolling window countdown (24/7)
- Per-window PnL timeline
- Animated glyph playback
- Frame-accurate playback scrubber
- Epoch selector
- Merkle root display
- User proof verification
- CI replay hashes
- Daily CSV / PDF exports
- Dark / Light mode
- Optional sound cues (muted by default)

---

## ⌨️ Keyboard Controls (Glyph Playback)

| Key | Action |
|----:|:-------|
| Space | Play / Pause |
| ← | Step backward |
| → | Step forward |
| ↑ | Speed ×2 |
| ↓ | Speed ×0.5 |
| R | Restart |

---

## 🔌 Data Sources

- Backend WebSocket (read-only)
- REST read endpoints
- Cached glyph logs
- Static audit artifacts

No direct exchange connectivity exists in the UI.

---

## 🧱 Technology Stack

- React
- Vite
- Tailwind
- WebSockets
- Lightweight state store
- Plotly (visualization)

---

## ♿ Accessibility (WCAG 2.1 AA)

- ARIA labels
- Screen reader announcements
- Keyboard-only navigation
- No sound-only information
- Deterministic focus order

---

## 🌍 Jurisdiction Awareness

Supported jurisdictions:

- EU-R3
- Nigeria

Jurisdiction affects:
- Legal copy
- Disclosures
- Currency display (informational only)

---

## 🔁 Offline / Online Parity

| Feature | Offline | Online |
|------|--------|--------|
| Playback | ✅ | ✅ |
| Scrubber | ✅ | ✅ |
| Sounds | ✅ | ✅ |
| Exports | ✅ | ✅ |
| Audit Verification | ✅ | ✅ |

Rendering is deterministic in all modes.

---

## 🚀 Build & Deployment

### Local Development
```bash
npm install
npm run dev
