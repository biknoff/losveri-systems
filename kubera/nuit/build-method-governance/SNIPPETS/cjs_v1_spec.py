# SOURCE: HANDOFF_CRYPTO_PROTOCOL.md § 2.1 — the CJS-v1 (Canonical JSON Serialization) reference
# spec, quoted verbatim from the protocol document (it is itself pseudocode/spec, not a shipped
# module — the real implementation lives inline in the phase-envelope build scripts and in
# receipt_builder.py's `_canonical`, see receipt_chain_link.py in this folder for the real,
# running equivalent).
# REDACTED: nothing.

# SPEC — reference serializer definition (not an implementation)
#
# def canonical_json_v1(obj: dict) -> bytes:
#     """
#     Rules:
#     1. Keys sorted lexicographically, byte-wise ASCII order.
#     2. No whitespace between tokens (no space after ':' or ',').
#     3. UTF-8 encoding; non-ASCII string VALUES pass through as literal UTF-8 bytes
#        (ensure_ascii=False) -- they are not \\uXXXX-escaped.
#     4. Only these types are permitted in a hashed record: str, int, bool, None,
#        and dict/list composed of the same. No float. No datetime objects
#        (serialize as ISO-8601 strings beforehand, at the caller's boundary).
#     5. Dict keys must be str. No non-string keys, no duplicate keys.
#     """
#
# Deliberate deviation from RFC 8785 JCS (§ 2.4 of the protocol):
#   - No UTF-16 code-unit key sort (ASCII-only keys in this protocol -> Python's
#     byte-order sort and JCS's UTF-16 sort agree).
#   - No ECMAScript-6 number serialization (no hashed field is ever a float).
#   - No enforced Unicode NFC normalization (pathological inputs are forbidden by
#     convention; a real NFC/NFD mismatch would be caught by the lock-coherence
#     check and trigger the halt protocol, not silently hash-mismatch forever).
#
# What would force a CJS-v2: a hashed field adding floats, non-ASCII dict keys, or a
# cross-language (non-Python) verifier entering the picture. Any such change is a
# versioned, signed, tagged supersession -- never a silent redefinition of v1.
