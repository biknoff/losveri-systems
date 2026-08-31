<!-- WHAT: verbatim doctrine quote + read-only-on-live statement from the mirror's own build
     README. REDACTED: hostname replaced with "live host"; the internal path once named in the
     original ("never touched") is generalized rather than quoted verbatim, since it names an
     internal directory layout. Nothing else altered — this is doctrine and a safety statement,
     no operational data. -->

# Doctrine

The build record states plainly, at the top of the mirror's own README, that the live host was
never mutated during the build:

> **Live host was READ-ONLY throughout.** One archive stream to stdout; no edit, no deploy, no
> restart, no state write [to any staging area on the live host].

## The instruction this mirror exists to satisfy (operator, verbatim)

> "The Rust engine at Time Travel is NOT a copy-paste of the live engine plus prism, gold law,
> MES law. And it should be."

> "Time travel should be a MIRROR of the engine. Any change we deploy, we deploy it in time
> travel first, run it, see the result, and then if we like the result we deploy it on the live
> engine."

And the mirror's own conclusion, stated directly under those two quotes:

> **It is now a mirror.**

This is the doctrine restated at the top of [VERIFICATION.md](../../../../VERIFICATION.md) for the
whole repo: *"rehearse in the mirror, observe, then live."* This project is where that sentence
is enforced mechanically rather than left as a process reminder — see
[`symlink_proof.md`](symlink_proof.md) for how "still a mirror" is checked on every build, not
just asserted once.
