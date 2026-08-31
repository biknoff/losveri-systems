# whatsapp-mcp — recent commit history

**What this is:** the ten most recent commits on the `whatsapp-mcp` repo (`git log --oneline -10`), as evidence this is an actively maintained integration rather than a one-off script that was run once and abandoned.

**Redactions:** none — commit subjects only, no author emails included.

---

```
a3d38c7 fix(whatsapp): suppress auto-open QR pairing tab
ce9b144 fix: Resolve contact names in searchMessages
809dc28 fix: Resolve contact names in getChats and getChat
1f2bd6d Merge pull request #7 from benliong/feature/enhance-contact-management
7c300f5 Fix an issue with message timestamp being wrong during message sync.
da6f791 Enhance contact search with error handling
be17097 Add contacts table and wire up contact search
76d6067 Use configurable data dir for logs and remove console login output
573e1f0 Capture removal of dependency on qrcode-terminal in lock file
91bf24e Merge pull request #2 from smithery-ai/smithery/config-ceb0
```

The history mixes upstream-derived fixes (this MCP server has an open-source lineage — see the `smithery-ai` and contributor-attributed merges) with local operational fixes (QR pairing UX, timestamp correctness, contact-name resolution) — consistent with a real, running integration that gets debugged against actual usage rather than a fork left untouched after the initial clone.
