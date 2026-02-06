# Skill: trend_detection_alerting

## 1. Description / Purpose

Implements SRS **Perception FR 2.2 (Trend Detection)** for Project Chimera.

This skill:

- Periodically analyzes aggregated data from MCP Resources (news and social feeds).
- Detects emerging topic clusters over a time window (e.g., 4 hours).
- Emits structured **Trend Alerts** that the Planner can use to adjust campaigns.

It is invoked by a **Worker** (Trend Spotter) under direction of the Planner.

---

## 2. Inputs (JSON Schema Example)

```json
{
  "tenant_id": "tenant-xyz",
  "agent_id": "agent-ethiopia-fashion-001",
  "window_hours": 4,
  "resources": [
    "news://ethiopia/fashion/trends",
    "twitter://mentions/recent"
  ],
  "min_cluster_score": 0.75,
  "max_trends": 10,
  "now": "2026-02-06T10:00:00Z"
}
```

Field notes:

- `tenant_id` – required for multi‑tenancy isolation.
- `agent_id` – which agent’s niche/persona context to use for relevance.
- `window_hours` – rolling time window for analysis.
- `resources` – MCP Resource URIs to pull data from.
- `min_cluster_score` – minimum score for a topic cluster to be considered a trend.
- `max_trends` – maximum number of trends to emit in one run.
- `now` – timestamp used for window calculations (can be fetched via time MCP).

---

## 3. Outputs (JSON Schema Example)

```json
{
  "tenant_id": "tenant-xyz",
  "agent_id": "agent-ethiopia-fashion-001",
  "window_hours": 4,
  "generated_at": "2026-02-06T10:00:05Z",
  "trends": [
    {
      "trend_id": "trend-987",
      "topic": "ethiopian-summer-streetwear",
      "score": 0.92,
      "regions": ["ethiopia", "east-africa"],
      "tags": ["fashion", "summer", "streetwear"],
      "supporting_samples": [
        {
          "resource": "news://ethiopia/fashion/trends",
          "excerpt": "Local designers debut summer streetwear line in Addis.",
          "timestamp": "2026-02-06T07:30:00Z"
        }
      ]
    }
  ]
}
```

If no trends pass the threshold, `trends` MAY be an empty array.

---

## 4. Preconditions

- Accessible MCP Resources for:
  - News feeds (e.g., `news://...`).
  - Social mentions (e.g., `twitter://mentions/recent`).
- Agent persona and niche are defined (via `SOUL.md` and memory), so relevance can be judged.
- Time MCP server available or equivalent way to obtain `now`.

---

## 5. Dependencies (MCP Servers / Tools)

This skill wraps and orchestrates:

- **Perception Resources**
  - `news://{region}/{topic}/trends` (mcp-server-news).
  - `twitter://mentions/recent` (mcp-server-twitter or equivalent).
- **Optional Memory Tools**
  - `search_memory` from `mcp-server-weaviate` to check historical trend patterns.

It returns a summarized, structured view; it does not update memory directly (a separate memory‑write skill can handle that).

---

## 6. High-Level Flow

1. **Fetch Windowed Data**
   - For each `resources[]` entry:
     - Read from the MCP Resource.
     - Filter entries to the last `window_hours`.
2. **Normalize & Embed (Optional)**
   - Normalize text (lowercase, strip noise).
   - Optionally compute embeddings to cluster semantically similar items.
3. **Cluster & Score**
   - Cluster items into topics (e.g., via embeddings or keyword groups).
   - Compute a `score` per cluster based on volume, velocity, and recency.
4. **Filter**
   - Drop clusters with `score < min_cluster_score`.
   - Limit to `max_trends` highest scoring clusters.
5. **Emit Trend Alerts**
   - Return a `trends[]` list as above.
   - Planner consumes these and creates/adjusts tasks (e.g., new content around “ethiopian-summer-streetwear”).

This skill MUST NOT publish content directly; it only informs planning.

