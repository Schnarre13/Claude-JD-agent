# Claude JD Agent

An AI agent, currently in development, that evaluates job descriptions against a candidate profile and decides which roles are worth pursuing. Built in Python with the Claude API and LangGraph.

## Why I built it

Job searching at scale has the same problem as any AI program: lots of inputs, limited attention, and a need for consistent, explainable decisions. This agent applies a defined scoring policy to every job description, so the go/skip decision is made the same way every time and comes with a reason.

It is also hands-on practice with the decisions I govern in enterprise AI programs: prompt design, structured output, routing logic, and where a human stays in the loop.

## How it works

```
Job description + resume
        |
        v
  [ Fit scoring node ]  -- Claude scores the role against a written policy
        |
        v
  Routing decision
   |            |
 proceed       skip
   |            |
   v            v
[ Tailoring ]  [ Storage ]   (placeholders, next build phase)
```

1. **Fit scoring.** The job description, extracted requirements, and resume data are sent to Claude with a scoring policy (`prompts/fit_scoring_prompt.txt`). Claude returns a structured JSON result: fit score, compensation fit, role type, strengths, missing skills, seniority match, and a recommendation.
2. **Routing.** LangGraph routes the job based on explicit business rules: roles below the compensation threshold are skipped, and roles scoring 0.60 or higher proceed.
3. **Next steps.** Proceeding roles go to resume tailoring; skipped roles go to storage for the record. Both nodes are placeholders today.

## Design decisions

- **Policy lives in a prompt file, not in code.** Scoring rules (target roles, contract penalties, thresholds) can be reviewed and changed without touching the pipeline.
- **Structured output with a fallback.** The agent requires JSON and, if Claude adds extra text, extracts the JSON block instead of failing.
- **Deterministic routing.** The model scores; plain code decides. The go/skip threshold is a visible, testable rule rather than a model judgment.
- **Typed state.** A Pydantic model defines every field the pipeline passes along, so missing or malformed data fails early.
- **Secrets stay out of the code.** The API key is read from a local `.env` file, which is excluded from the repository.

## Governance notes

- **Human in the loop:** the agent recommends; I decide whether to apply. Nothing is submitted automatically.
- **Known limitations:** compensation is inferred when a posting doesn't state it, so that estimate is a judgment, not a fact. Scores have not yet been benchmarked against my own manual assessments.
- **Planned evaluation:** score a set of past job descriptions where the outcome is known and measure agreement between the agent and my own decisions.

## Status

**Work in progress.** The Claude API connection is working and tested (`claude_test.py`). The multi-step pipeline below is designed and coded but not yet running end to end.

| Component | Status |
| --- | --- |
| Claude API connection | Working |
| Fit scoring node | Built, in testing |
| Routing logic | Built, in testing |
| Job description discovery | Planned (test data used today) |
| Resume tailoring node | Placeholder |
| Storage node | Placeholder |

## Running it

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project folder:

```
ANTHROPIC_API_KEY=your-key-here
```

Then run:

```bash
python main.py
```

## Project structure

```
main.py                  Entry point; loads a test job and runs the pipeline
graph.py                 LangGraph workflow and routing rules
nodes/fit_scoring.py     Claude fit scoring node
nodes/placeholders.py    Tailoring and storage stubs
state/fit_score_state.py Pipeline state model
utils/claude_client.py   Claude API client setup
prompts/                 Scoring policy prompt
```

## Author

Eric Schnarr, AI Transformation & Governance. Portfolio: https://schnarre13.github.io
