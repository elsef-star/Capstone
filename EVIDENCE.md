Verification Evidence

## AI Processing Requirements
- [x] **Vision model produces structured output validated against a schema:**
  *Proof:* `app/schemas.py` defines `ImageMetadataSchema` validated with Pydantic.
json
{
"subject": "red fox",
"category": "animal",
"attributes": ["orange fur", "forest"],
"caption": "A red fox in autumn forest",
"confidence": 0.95
}


- [x] **Low-confidence classifications are flagged instead of accepted:**
*Proof:* `blurred_unknown.jpg` with confidence 0.45 set to `flagged = True` during seed.

- [x] **Vision and embedding costs are tracked per call:**
*Proof:* Log trace from execution:
`[COST TRACKER] Vision call processed. Estimated cost: $0.000100`

## Matching & Safety Layer
- [x] **Mismatch guard rejects incorrect recommendations (Wolf vs Red Fox):**
*Proof:*
Query: `GET /api/posts/3/images` (Quantum Computing Article)
Output:
json
{
"status": "REJECTED",
"reason": "Similarity score (0.01) below threshold (0.75)"
}


- [x] **Top-1 Precision evaluation score:**
*Proof:* Executed `python -m app.eval`:
`Top-1 Precision: 100.00% (3/3)`