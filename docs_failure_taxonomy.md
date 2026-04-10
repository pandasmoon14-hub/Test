# Failure taxonomy

Quarantined or rerouted automatically:
- Invalid PDF magic bytes -> quarantine folder.
- Missing/weak page truth markers under strict mode -> runtime error / queue.
- Thin output, table structure failures, glyph corruption, reading order failures -> repair queue.
- Image-only profiles -> direct surgeon routing (no lane guessing).
