# The dead ADK scaffold's own self-description

Verbatim excerpt from `ANIMA/6th House (Fay)/agent.md`, dated March 31, 2026 —
superseded before the working corpus (which starts April 9, 2026) began.
Kept here as the "one line, no more" evidence this scaffold existed and was
abandoned, not iterated into the working system.

---

```markdown
# Fay — 6th House Domestic Coordination Agent

**Version:** 0.1.0
**House:** 6th (Health, Daily Rhythms, Service)
**Runtime:** Vertex AI Agent Engine (google-adk)
**Model:** Gemini 2.0 Flash

## Overview

Fay coordinates household operations for the family. She reads cleaning
schedules from a spreadsheet, generates prioritized task lists, translates
them for domestic staff, and delivers via Telegram/WhatsApp.
```

Everything after this header — the spreadsheet ID, tab structure, and tool
list — is scaffold detail for a runtime (google-adk / Vertex AI Agent
Engine / Gemini 2.0 Flash) that was never built out past this file and two
small supporting modules (`agent.py`, `tools/household_tools.py`). The
working system documented in the rest of this directory does the same job
— schedule → prioritize → translate → dispatch — on a plain file-corpus +
shell-script implementation instead, dispatching through Hanuman's
transport rather than a Telegram/WhatsApp abstraction of its own.
