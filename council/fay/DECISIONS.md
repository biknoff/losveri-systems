# Decisions — Fay

Each entry: the choice made, and the alternative considered and rejected.

## 1. Meet the staff in their language
**Chosen:** every dispatch produces a Haitian Creole artifact as its own first-class file, delivered as the actual message the household staff receives.
**Rejected:** forcing the household onto the operators' language (Spanish or English). A task list the person doing the work has to mentally translate is friction and a source of real error on real household operations — dates, quantities, which room, which day. Translating at the source, once, per cycle, moves that cost to the system instead of the person doing the work.

## 2. Ride Hanuman's WhatsApp transport rather than build a second one
**Chosen:** Fay's dispatch script calls directly into Hanuman's canonical sender (`npx tsx send_whatsapp_once.ts`), the same path documented as canonical in Hanuman's own SKILL.md.
**Rejected:** Fay holding its own WhatsApp session or writing its own Baileys integration. That would duplicate a session to protect, duplicate the JID-normalization and delivery-confirmation logic Hanuman already has, and break the entire point of a shared comms gate (see [Hanuman/DECISIONS.md](../hanuman/DECISIONS.md) #1). Fay stays a pure content-and-scheduling layer.

## 3. State the unofficial-bridge dependency honestly
**Chosen:** this document and the README say plainly that delivery rides Baileys, an unofficial WhatsApp bridge library, inherited transitively through Hanuman.
**Rejected:** hiding the dependency, or describing delivery only as "sent via WhatsApp" without naming the mechanism. The operator's own working notes already call this dependency out in the same terms; restating it honestly here rather than glossing over it is consistent with that discipline, and it's the accurate technical picture — anyone reasoning about reliability or risk needs to know the transport is not an officially sanctioned API.

## 4. Corpus-as-record over a database
**Chosen:** every cycle's schedule, prioritized objectives, and translated message exist as dated, day-folder-organized files — the filesystem is the record.
**Rejected:** a database or task-tracker backend. For a coordination loop this small (one household, a handful of recurring days, low message volume), a database adds operational surface (schema, backups, a query layer) without buying anything a dated folder structure doesn't already give: anyone can open a day's folder and see exactly what was sent, in what language, without running a program.

## 5. Kill the ADK scaffold rather than maintain two implementations
**Chosen:** an earlier Vertex AI Agent Engine (google-adk) scaffold for Fay was abandoned once the schedule→translate→dispatch pipeline above was working.
**Rejected:** running both, or migrating the working pipeline onto the ADK scaffold's framework. The scaffold predates the working corpus by more than a week and was never touched again after — keeping two live implementations of the same responsibility would have meant maintaining a framework dependency (Gemini 2.0 Flash, google-adk, a specific spreadsheet-tab data source) that the actually-working system doesn't need.
