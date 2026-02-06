# Skill: multimodal_content_generation

## 1. Description / Purpose

Implements SRS **Creative Engine FR 3.0–3.2** for Project Chimera.

This skill:

- Orchestrates text, image, and video generation via MCP Tools.
- Enforces **character consistency** (FR 3.1) using a `character_reference_id` or style identifier.
- Applies a **tiered video rendering strategy** (FR 3.2) based on budget and campaign priority.

It is invoked by **Workers** responsible for producing creative assets under Planner-defined tasks and is validated by Judges.

---

## 2. Inputs (JSON Schema Example)

```json
{
  "tenant_id": "tenant-xyz",
  "agent_id": "agent-ethiopia-fashion-001",
  "campaign_id": "cmp-summer-ethiopia-2026",
  "creative_brief": {
    "goal": "Promote Ethiopian summer streetwear drop on TikTok.",
    "tone": ["witty", "aspirational"],
    "key_messages": [
      "Local designers",
      "Sustainable fabrics",
      "Streetwear aesthetic"
    ],
    "cta": "Follow for daily Addis street looks."
  },
  "persona_constraints": {
    "forbidden_topics": ["politics", "explicit content"],
    "style_notes": "Highlight Ethiopian culture in a respectful, authentic way."
  },
  "character_reference_id": "chimera-ethiopia-001",
  "platform": "tiktok",
  "tier": "daily",  // "daily" or "hero"
  "budget_hint": {
    "max_generation_cost_usd": 5.0
  }
}
```

Field notes:

- `character_reference_id` MUST always be provided; used to lock visual identity.
- `tier` guides video tool selection:
  - `"daily"` → cost‑effective image‑to‑video or lightweight effects.
  - `"hero"` → full text‑to‑video for major campaigns.

---

## 3. Outputs (JSON Schema Example)

```json
{
  "tenant_id": "tenant-xyz",
  "agent_id": "agent-ethiopia-fashion-001",
  "campaign_id": "cmp-summer-ethiopia-2026",
  "assets": {
    "caption": {
      "text": "Step into Ethiopia's summer in style 🇪🇹✨ Local designers redefining streetwear from Addis to the world.",
      "hashtags": ["#EthiopiaFashion", "#SummerDrop", "#LocalDesigners"]
    },
    "image": {
      "asset_id": "img-123",
      "mcp_tool": "mcp-server-ideogram",
      "character_reference_id": "chimera-ethiopia-001",
      "url": "https://cdn.example.com/img-123.jpg"
    },
    "video": {
      "asset_id": "vid-456",
      "mcp_tool": "mcp-server-runway",
      "tier": "daily",
      "url": "https://cdn.example.com/vid-456.mp4"
    }
  },
  "generation_metadata": {
    "llm_model": "gemini-3-pro",
    "image_model": "ideogram-vX",
    "video_model": "runway-vY",
    "approx_cost_usd": 3.25
  }
}
```

If an asset type is not requested or exceeds budget, it MAY be omitted or replaced with a lower‑cost fallback (documented in metadata).

---

## 4. Preconditions

- MCP Tools available for:
  - Text generation (LLM core, via internal agent runtime).
  - Image generation (e.g., `mcp-server-ideogram`).
  - Video generation (e.g., `mcp-server-runway` or `mcp-server-luma`).
- Persona (`SOUL.md`) and memory accessible for consistent style and references.
- Budget context from Resource Governor or campaign configuration:
  - Per‑campaign and per‑content budget caps.

---

## 5. Dependencies (MCP Servers / Tools)

This skill orchestrates:

- **Text**
  - Internal LLM invocation (Planner/Worker context) with persona + brief.
- **Image**
  - MCP Tool: `generate_image` (e.g., from `mcp-server-ideogram`), always including:
    - `character_reference_id`
    - style / aesthetic hints.
- **Video**
  - MCP Tools:
    - `generate_video_from_image` for `"daily"` tier.
    - `generate_video_from_text` for `"hero"` tier.
  - Tools are provided by servers like `mcp-server-runway` or `mcp-server-luma`.

It may also log usage to a budgeting system for later analysis.

---

## 6. High-Level Flow

1. **Assemble Context**
   - Load persona from `SOUL.md`.
   - Optionally pull relevant memories (Weaviate) for prior successful posts.
2. **Generate Caption**
   - Prompt LLM with:
     - `creative_brief`
     - persona voice and constraints.
   - Validate that generated text:
     - avoids forbidden topics,
     - fits platform limits (e.g., TikTok caption length).
3. **Generate Image**
   - Call `generate_image` MCP Tool with:
     - `character_reference_id`,
     - style instructions based on persona and brief.
   - Receive `image.asset_id` and `url`.
4. **Generate Video (Tiered)**
   - If `tier == "daily"`:
     - Use `generate_video_from_image` with the produced image.
   - If `tier == "hero"`:
     - Use `generate_video_from_text` with a script derived from the caption/brief.
   - Ensure estimated cost ≤ `budget_hint.max_generation_cost_usd` (or request approval from Resource Governor).
5. **Return Assets**
   - Package caption, image, and video into the output JSON.
   - Judges later validate consistency and safety before publishing.

This skill MUST NOT publish content; it only produces assets for downstream review and action.

