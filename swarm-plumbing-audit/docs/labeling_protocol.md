# Labeling protocol

Each sampled payload (first 700 characters) was assigned one label by following this ordered
procedure, stopping at the first match. Redaction tags such as `[CREDENTIAL n]`,
`[REDACTED:destination:n]`, `[ENCODED BLOB]` and `[SHORTENER URL n]` are placeholders and are
ignored when reading.

1. `opaque`: nothing readable, or only a placeholder
2. `chunk_carrier`: stores or assembles pieces (numbered slots, shortener-code lists, `x+=blob;n(...)`, `A[] batch` headers)
3. `delivery_stub`: only a redirect, or loads a script from a link
4. `hf_access`: calls huggingface.co or datasets-server.huggingface.co (read or write)
5. `recon`: queries another server to inspect or map it
6. `credential_access`: loops over many tokens to test or list them (using one token does not qualify)
7. `other_behavior`: a real action that fits none of the above
8. `unclear`: cannot tell

Mapping used to compare with the regex rule: `chunk_carrier`, `delivery_stub` -> plumbing;
`opaque` -> opaque; everything else -> behavior. The `unclear` row is excluded from accuracy.

**Provenance:** labels were assigned by an LLM (Claude) following this procedure, blind to the
rule's prediction. They are LLM-assisted labels, not human ground truth.
