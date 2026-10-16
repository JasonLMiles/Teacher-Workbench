# Release 1.4.1 documentation validation

Checked September 29, 2026. This release changes the teacher guide, package documentation and creation specifications. The 40 skill implementations, supporting resources, scripts and numerical tests are byte-for-byte unchanged from the preceding 1.4.0 package.

- Guide coverage was checked against all 40 canonical skill names and the packaged capability contracts. The guide uses ordinary teacher requests, worked examples, practical review questions and a five-session practice sequence.
- The Markdown, Word and PDF editions contain the same guide. The PDF has 21 pages. Every final page image was visually reviewed at original resolution for legibility, layout, wrapping and completeness.
- All 15 navigation links in the Word/PDF topic finder point to valid guide sections. The 19 unique external source destinations appear in each edition and were opened and checked; see [guide source record](guide-source-verification.json).
- Both archives retain all 40 skill folders and include identical copies of the three guide editions. Manifest version, catalogs, prompts, completion records, file hashes, relative documentation links and ZIP integrity were checked. The creation archive has its own checksums.
- The guide's small arithmetic examples were independently reviewed: the revised lesson totals 12 minutes; matched pre/post gain is 2.5 score points for two learners; 0.80 × 82 + 0.20 × 97 = 85. Examples are labeled illustrations rather than prescribed interventions or validated policies.

This was an editorial and document/packaging review, not a novice-user usability study or classroom effectiveness trial. The five-session practice sequence is proposed by this guide. No new skill behavior trials or numerical regression tests were needed for this documentation change.

The preceding release's 35 numerical checks and behavior trials remain documented in [the historical 1.4.0 validation](HISTORICAL_VALIDATION_1_4.md). They are historical results, not new runs. Earlier reports retain their original scope and dates. Native Google Sheets/Canva creation, private sign-in, live gradebook writes, destination installation and public plugin publication were not performed for this release. Full IRT calibration remains a separate analysis requiring suitable data and a verified runtime.
