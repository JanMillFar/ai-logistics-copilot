# Observed reliability cases

Reviewed commit: `9c06b04f95c5c9462d3814a3a456f91d4fc05f4a`. Date: 28 October 2026. Method: isolated Python reproduction with synthetic data; no live model or browser session. Ratings below are provisional operational assessments, not formal security severity scores.

## R01 Duplicate sales rows inflate inventory value

**Input.** Inventory contains one product A: stock 10, unit price 2. Sales contains two rows for A, with daily sales 1 and 2.

**Expected.** The application should reject ambiguous duplicates or apply an explicit aggregation policy. Inventory value should remain 20 under either legitimate sales interpretation.

**Observed.** The application's inner merge on Product produces two rows. Summing stock × price on the merged table returns 40. The individual value function is arithmetically correct; the defect arises from join cardinality and absent validation.

**Impact.** A decision-maker could receive a plausible but doubled inventory valuation. Provisional priority: high for numerical reliability.

**Reproduce.** `test_duplicate_sales_inflate_value`. The test asserts both the correct pre-merge value and the observed post-merge value.

**Proposed correction.** Specify the sales grain, validate product uniqueness and use merge cardinality validation after any deliberate aggregation. Add a conservation check for inventory value. Not implemented in this portfolio change.

**AI evaluation relevance.** A fluent explanation of a wrong total is still wrong. Verify the underlying number against an independent oracle.

## R02 Missing sales records silently remove inventory

**Input.** Inventory contains A (10 × 2) and B (5 × 4), total 40. Sales contains only A.

**Expected.** Retain B and flag its unknown sales, or stop with a clear validation message. Do not silently treat the incomplete intersection as total inventory.

**Observed.** The inner join drops B. The merged inventory value becomes 20.

**Impact.** The displayed population is incomplete. Provisional priority: high for data completeness.

**Reproduce.** `test_missing_sales_drop_inventory`. This reconstructs the merge used in the app; it does not run the whole Streamlit UI.

**Proposed correction.** Preserve the inventory population, report unmatched records and make missing-demand semantics explicit. Not implemented here.

**AI evaluation relevance.** A response can be locally correct while omitting information necessary for the user's decision.

## R03 Unknown demand looks like healthy coverage

**Input.** Stock 0, daily sales 0. A second control uses stock 10 and daily sales -1.

**Expected.** Represent no-demand/undefined coverage separately; reject invalid negative sales unless a documented business policy supports them.

**Observed.** Both return 999 days. The app classifies coverage ≥21 as healthy. Zero-stock/zero-demand therefore contributes to the healthy count. The classification is reconstructed from the application rule, not verified through browser interaction.

**Impact.** A numeric fallback disguises uncertainty as a reassuring status. Provisional priority: medium; operational significance depends on the product and demand policy.

**Reproduce.** `test_zero_demand_uses_sentinel` and `test_negative_sales_use_same_sentinel`.

**Additional edge cases.** Coverage 6.96 is rounded to 7.0 before classification, moving it across the seven-day boundary. An empty population gets score 0 and status Critical. These observations call for explicit business definitions; they are not evidence of a model safety vulnerability.

**AI evaluation relevance.** Prefer a clearly stated limitation over false precision or unjustified confidence.
