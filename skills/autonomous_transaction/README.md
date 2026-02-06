# Skill: autonomous_transaction

## 1. Description / Purpose

Implements SRS **Agentic Commerce** requirements (wallets and transactions) for Project Chimera.

This skill:

- Executes **budget‑aware on‑chain transactions** using Coinbase AgentKit via MCP.
- Ensures every transaction respects:
  - Per‑campaign and per‑agent budget caps.
  - Policy rules defined by a CFO / Resource Governor.
- Returns structured receipts for logging and auditing.

It is invoked by Workers acting under Planner instructions and is always overseen by Judges (CFO‑style governance).

---

## 2. Inputs (JSON Schema Example)

```json
{
  "tenant_id": "tenant-xyz",
  "agent_id": "agent-ethiopia-fashion-001",
  "wallet_id": "wallet-abc",
  "network": "base",
  "asset": "USDC",
  "amount": "25.00",
  "to_address": "0x1234abcd...",
  "purpose": "pay_for_video_generation",
  "campaign_id": "cmp-summer-ethiopia-2026",
  "budget_guard": {
    "max_per_tx": "50.00",
    "max_daily": "200.00",
    "max_campaign_total": "1000.00"
  },
  "metadata": {
    "task_id": "uuid-1234",
    "external_invoice_id": "inv-789"
  }
}
```

Field notes:

- `tenant_id` and `agent_id` ensure multi‑tenant isolation and attribution.
- `budget_guard` contains **hard caps**; if any would be exceeded, the skill MUST NOT execute the transaction.

---

## 3. Outputs (JSON Schema Example)

```json
{
  "tenant_id": "tenant-xyz",
  "agent_id": "agent-ethiopia-fashion-001",
  "wallet_id": "wallet-abc",
  "network": "base",
  "asset": "USDC",
  "amount": "25.00",
  "to_address": "0x1234abcd...",
  "purpose": "pay_for_video_generation",
  "campaign_id": "cmp-summer-ethiopia-2026",
  "status": "executed",
  "tx_hash": "0xdeadbeef...",
  "executed_at": "2026-02-06T10:05:00Z",
  "post_balances": {
    "wallet_balance": "475.00",
    "campaign_spend_today": "75.00",
    "campaign_spend_total": "325.00"
  },
  "metadata": {
    "task_id": "uuid-1234",
    "external_invoice_id": "inv-789"
  }
}
```

On failure or rejection (e.g., budget exceeded), `status` MUST be `"rejected"` or `"failed"` and include a `reason` field:

```json
{
  "status": "rejected",
  "reason": "max_daily budget exceeded for campaign cmp-summer-ethiopia-2026"
}
```

---

## 4. Preconditions

- Coinbase AgentKit MCP server is available and configured for this tenant:
  - Wallets have been created and associated with `agent_id`.
- Budget and policy configuration is accessible (e.g., via Postgres or an MCP Resource).
- Judge / CFO policy is defined so that high‑risk or large transactions can be escalated to HITL if needed.

---

## 5. Dependencies (MCP Servers / Tools)

This skill orchestrates:

- **Coinbase AgentKit MCP**
  - Tool: `get_balance` – check current wallet balance.
  - Tool: `send_transaction` – execute the transfer.
- **Budget / Policy MCP**
  - Resource: `campaign://{campaign_id}/budget` – retrieve configured caps.
  - Resource: `campaign://{campaign_id}/spend` – retrieve current spend totals.

It MAY also write transaction logs via a logging or analytics MCP server.

---

## 6. High-Level Flow

1. **Load Budget and Policy**
   - Read budget configuration and current spend via MCP Resources.
2. **Check Wallet Balance**
   - Call `get_balance` to confirm that `amount` is available.
3. **Budget Guard Evaluation**
   - Compute:
     - New per‑transaction amount vs `max_per_tx`.
     - New daily spend vs `max_daily`.
     - New campaign total vs `max_campaign_total`.
   - If any threshold is exceeded:
     - Do **not** call `send_transaction`.
     - Return `status: "rejected"` with an explanatory `reason`.
4. **Execute Transaction**
   - Call `send_transaction` with:
     - `network`, `asset`, `amount`, `to_address`, and metadata.
   - Capture `tx_hash` and confirmation info.
5. **Return Receipt**
   - Return a structured receipt as in the output schema.
   - Judges (and optionally HITL reviewers) can validate high‑risk or anomalous transactions.

This skill MUST never bypass budget checks or policy; if in doubt, it should refuse to execute and ask for human or Judge intervention.

