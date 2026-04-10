# Page-Truth Migration Note

Removed synthetic page-truth behavior from production paths:

- Removed automatic `<!-- PAGE:1 -->` injection in markdown auditing and merge paths.
- Removed `current = 1` defaults from page-marker parsers.
- Removed chunk-marker expansion as a source of trusted page markers (`expand_chunk_markers` is now a no-op).
- Markerless markdown is now treated as missing page truth (`{}` / failure), not as page 1.
- Quality gating now treats untrusted page-truth modes (`chunk_fallback`, `native_or_fallback`, and other fallback/synthetic modes) as hard failures.
