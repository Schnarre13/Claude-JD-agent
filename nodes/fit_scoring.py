import json
from utils.claude_client import get_claude_client

# Load the Claude prompt from the prompts folder
with open("prompts/fit_scoring_prompt.txt", "r", encoding="utf-8") as f:
    CLAUDE_FIT_SCORING_PROMPT = f.read()

claude = get_claude_client()

def fit_scoring_node(state):
    """
    Sends JD + resume + metadata to Claude Sonnet 5 using the Fit Scoring prompt.
    Enforces strict JSON-only output and safely parses the response.
    """

    user_payload = {
        "job_title": state.job_title,
        "company": state.company,
        "source_site": state.source_site,
        "job_url": state.job_url,
        "job_id": state.job_id,
        "jd_text": state.jd_text,
        "jd_requirements": state.jd_requirements,
        "resume_json": state.resume_json
    }

    response = claude.messages.create(
        model="claude-sonnet-5",
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": (
                    CLAUDE_FIT_SCORING_PROMPT
                    + "\n\nIMPORTANT: Return ONLY valid JSON. No explanation, no commentary."
                )
            },
            {
                "role": "user",
                "content": json.dumps(user_payload)
            }
        ]
    )

    raw_output = response.content[0].text.strip()

    # --- Robust JSON extraction for Sonnet 5 ---
    try:
        # Sonnet 5 usually returns pure JSON, but we guard against edge cases.
        result = json.loads(raw_output)
        explanation = ""
    except json.JSONDecodeError:
        # Fallback: extract the first JSON object from mixed output
        import re
        json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
        if not json_match:
            raise ValueError(f"Claude returned non-JSON output: {raw_output}")

        json_block = json_match.group(0)
        result = json.loads(json_block)
        explanation = raw_output.replace(json_block, "").strip()

    # --- Update state ---
    state.fit_score = result.get("fit_score")
    state.compensation_estimate = result.get("compensation_estimate")
    state.compensation_fit = result.get("compensation_fit")
    state.role_type = result.get("role_type")
    state.contract_penalty_applied = result.get("contract_penalty_applied")
    state.missing_skills = result.get("missing_skills")
    state.strengths = result.get("strengths")
    state.seniority_match = result.get("seniority_match")
    state.role_alignment = result.get("role_alignment")
    state.keyword_density = result.get("keyword_density")
    state.recommendation = result.get("recommendation")

    state.explanation = explanation

    return state

