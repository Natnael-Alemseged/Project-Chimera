# Rule Version History

This document tracks the evolution of agent rules and configuration across different IDE/agent setups.

## Version 2.0 - Cursor Migration (Current)
**Date**: 2026-02-04  
**IDE**: Cursor  
**Agent**: Cursor AI  
**Configuration Location**: `.cursor/rules/agent.mdc`, `.cursor/mcp.json`

### Changes from v1.0:
- Migrated from VS Code + GitHub Copilot to Cursor + Cursor AI
- Moved rules from `.github/copilot-instructions.md` to `.cursor/rules/agent.mdc`
- Updated MCP configuration from `.vscode/mcp.json` to `.cursor/mcp.json`
- Maintained same core workflow (Plan-First, Persistent Memory, Trigger-Driven)
- Updated all documentation references (README.md, agents.md)

### Rule Structure:
```
.cursor/rules/agent.mdc
├── TENX LOGGING PROTOCOL (MANDATORY)
│   ├── log_passage_time_trigger (ALWAYS)
│   └── log_performance_outlier_trigger (SOMETIMES)
├── AGENT ORCHESTRATION & ENGINEERING STANDARDS
│   ├── Think-First Protocol (Boris Cherny Workflow)
│   ├── Persistence & Memory (agents.md)
│   └── Verification-Driven Development
└── VALIDATION CHECKLIST
```

### MCP Configuration:
- Server: `tenxfeedbackanalytics`
- URL: `https://mcppulse.10academy.org/proxy`
- Headers: `X-Device: mac`, `X-Coding-Tool: cursor`

---

## Version 1.0 - VS Code + GitHub Copilot (Initial)
**Date**: 2026-01-XX (initial setup)  
**IDE**: VS Code  
**Agent**: GitHub Copilot  
**Configuration Location**: `.github/copilot-instructions.md`, `.vscode/mcp.json`

### Initial Setup:
- Created `.github/copilot-instructions.md` for global Copilot rules
- Configured `.vscode/mcp.json` for MCP server connection
- Established `agents.md` as persistent memory
- Implemented Plan-First workflow inspired by Boris Cherny

### Key Learnings:
- Tool-specific file names (e.g., `CLAUDE.md`) caused persona confusion
- Solution: Renamed to generic `agents.md` for better adoption
- Stream termination issues with SSE connections (self-healing verified)

---

## Migration Notes

### Why Migrate to Cursor?
1. **Unified Configuration**: Cursor's `.cursor/` directory consolidates rules and MCP config
2. **Better Integration**: Native MCP support with clearer tool discovery
3. **Improved Workflow**: Cursor AI provides more consistent rule application

### Compatibility:
- All core rules remain unchanged (logging protocol, Plan-First, persistence)
- MCP server configuration identical (same endpoint, headers adjusted)
- `agents.md` structure preserved across both versions

### Breaking Changes:
- None - all functionality preserved, only configuration locations changed
