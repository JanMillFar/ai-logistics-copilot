# AI evaluation work sample

**Jan Millan Farriols · independent portfolio · 28 October 2026**

This sample connects operational judgement with the evaluation of AI outputs. It contains reproducible findings from an existing Python prototype and a small set of conversational evaluation designs. The code findings are observed; the proposed chatbot prompts have not been run against an external model.

## Start here

| Review item | Evidence | Status |
| --- | --- | --- |
| Numerical reliability and missing records | [Three case studies](observed-cases.md) | Reproduced offline |
| Conversation quality and safety | [Six test cards and two scoring examples](conversation-cases.md) | Authored controls and proposed tests |
| Consistent rating decisions | [Evaluation rubric](rubric.md) | Manual method, not a validated benchmark |
| Reproduction | [Tests](tests/test_observed_behaviour.py) | Seven assertions against reviewed source snapshots |

For a short review, read the duplicate-record case and the instruction-conflict test card. They show the same habit: define the expected behaviour, examine what happened and justify the conclusion.

## Observed code findings

The review uses synthetic records and source from [AI Logistics Copilot at commit 9c06b04](https://github.com/JanMillFar/ai-logistics-copilot/tree/9c06b04f95c5c9462d3814a3a456f91d4fc05f4a). The `evidence` directory preserves the reviewed calculation and health functions. Their Git blob hashes are checked by the tests.

```powershell
python -m pip install pandas
python -m unittest discover -s docs/ai-evaluation/tests -v
```

Run from the repository root. These tests reproduce known limitations; passing them does **not** mean the application is free of defects. No API key, model download or external inference is needed. No customer data is used. See [the recorded run](validation.md).

## Contribution and limits

Jan's background includes operations, incident handling, document research and independent use of ChatGPT, Gemini and local Qwen models. This portfolio was prepared with Codex assistance: Codex drafted the documents, designed the test fixtures and executed the automated checks. Jan is the portfolio owner; his personal review of the new cases is pending. These new cases must not be represented as unaided work or past client engagements.

No live chatbot was evaluated in this package. Example answers in the conversation document are explicitly authored controls. There is no claim of a safety success rate, production red-team experience, measured productivity gain or a completed security audit. Earlier Qwen and Dual Intelligence experiments are context only; unverified transcripts are not published here.
