# Architecture — Fay

## Scope

Fay is not a service or a daemon — it is a working *pipeline and corpus*, operated day by day: a schedule document, a set of day-named output folders, and a dispatch step. There is no long-running Fay process; the intelligence is applied per cycle (weekly schedule → daily objectives → translated message → sent message), and the artifacts of every cycle are kept.

## The flow

1. **Schedule.** A `WEEKLY_SCHEDULE_<staff>.md`-pattern document (rewritten as the arrangement changes — several dated `.bak_*` revisions exist, e.g. a "reset mandate" revision, a "bathroom stock rule" revision) holds the recurring weekly structure: which day, which tasks.
2. **Prioritize.** A day-specific `HOY_<date>_objetivos*` file (Spanish: "today's objectives") is generated from the schedule — today's actual task list, not the whole week restated.
3. **Translate.** A `MENSAJE_<staff>_HOY_<date>*` file is produced per day, in two forms sitting side by side: a Spanish/draft version and a `_KREYOL` (Haitian Creole) version. Some days also carry a `_DEEP` variant (a fuller version) alongside the standard one. The Creole file is not optional or generated on request — it exists as its own artifact for essentially every dispatch day in the corpus.
4. **Dispatch.** A shell script (`schedule_<staff>_morning.sh`-pattern) computes seconds-until-target-time for each scheduled send (e.g., a wake-up/pickup message, a fuller daily briefing) and calls straight into Hanuman's canonical WhatsApp sender — `cd .../whatsapp-mcp && npx tsx ./send_whatsapp_once.ts --recipient '<jid>' --message-file '<path>'`. See `EVIDENCE/dispatch_dependency_on_hanuman.md`.

## Corpus as the artifact of record

Rather than a database, Fay's record of what was decided and sent is the corpus itself: day-named folders (Lunes/Martes/Miércoles/Jueves/Viernes — Spanish weekday names, operator-facing) each holding that day's objectives file, message drafts, and rendered outputs (`.md`, `.html`, `.pdf` — the same content in multiple render targets). This is legible by design: anyone can open a day's folder and see exactly what was decided, in what language, and in what form it was delivered, without needing to replay a program.

## The boundary with Hanuman

Fay contains zero WhatsApp code. It does not hold a session, does not know a JID format beyond passing one through to Hanuman's sender, and does not implement retries, delivery confirmation, or contact lookup — all of that is Hanuman's responsibility (see [Hanuman/ARCHITECTURE.md](../hanuman/ARCHITECTURE.md)). Fay's dispatch script is a thin caller: it decides *when* (time-of-day scheduling) and *what file* (the day's already-translated message); Hanuman's `send_whatsapp_once.ts` decides how a JID and a message file actually become a delivered WhatsApp message. This is the same "protocols, not content" boundary Hanuman's own docs describe, seen from the consumer side.

## Cross-language operation is structural

The Creole output isn't a translation flag on a generic message generator — it's a first-class file in the corpus, produced and named as its own artifact every cycle (`_KREYOL` suffix), sitting next to the Spanish/draft version rather than replacing it. That pairing — draft in the operator's working language, final in the household staff's own language — is the actual mechanism that makes this a cross-language operations tool rather than a task-list generator that happens to support one extra locale.
