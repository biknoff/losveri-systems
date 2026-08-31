<!-- What: existence + line count of glass.py's own blocked.log (the gateway logging its own
     refusals), a redacted tail sample, and the glass.py .bak iteration timestamps as
     active-development evidence, all read live from the small VM the product runs on.
     Redacted: none beyond the standard hostname rule (127.0.0.1 is the tunnel's own loopback
     hop, not an external identifier, and is left as-is). -->

## The gateway logs its own refusals

```
$ wc -l blocked.log
120 blocked.log
```

120 refused requests logged at the time of this snapshot — this is enforcement observed, not
just enforcement designed. A redacted tail (method + path + loopback source only; the "127.0.0.1"
here is the tunnel's own local hop, not an external caller identity):

```
2026-08-30T15:49:34Z REFUSED POST   /order   (method) from 127.0.0.1
2026-08-30T15:58:33Z REFUSED POST   /order   (method) from 127.0.0.1
2026-08-30T16:43:40Z REFUSED POST   /order   (method) from 127.0.0.1
2026-08-30T16:43:40Z REFUSED PUT    /order   (method) from 127.0.0.1
2026-08-30T16:43:40Z REFUSED DELETE /order   (method) from 127.0.0.1
```

Every refusal in this sample is the method-default-deny layer (`EVIDENCE/01`) firing against the
exact operative path (`/order`) that the earlier keyword-matching incident collided on — the
current gateway refuses it cleanly across `POST`, `PUT`, and `DELETE`.

## Active development, timestamped

`glass.py`'s own `.bak_YYYYMMDDTHHMMSSZ` backups (the gateway snapshots itself before each edit)
give a direct iteration timeline on a single day:

```
glass.py.bak_20260830T143849Z    (9.8 KB)
glass.py.bak_20260830T144112Z   (11.6 KB)
glass.py.bak_20260830T152404Z   (17.0 KB)
glass.py.bak_20260830T154651Z   (17.2 KB)
glass.py.bak_20260830T160724Z   (19.7 KB)
glass.py.bak_20260830T160832Z   (21.0 KB)
glass.py.bak_20260830T161103Z   (22.9 KB)
glass.py.bak_20260830T161617Z   (23.0 KB)
glass.py.bak_20260830T163449Z   (23.6 KB)
glass.py               (current, 26.8 KB, last modified 16:51 UTC same day)
```

Nine snapshots between 14:38 and 16:51 UTC on 2026-08-30 — roughly one edit every 13 minutes over
a two-and-a-quarter-hour working session, growing the file from ~10 KB to ~27 KB. This is the
privilege-separation design in `EVIDENCE/01` being actively built and hardened (the exact-path
denylist fix described there is one of the changes inside this window), not a static artifact.
The companion app front-end (`app/index.html`) carries its own same-day `.bak`/`.shelved`
snapshots from 15:35–15:46 UTC.
