from dotenv import load_dotenv
load_dotenv()

import json
from state.fit_score_state import FitScoreState
from graph import graph

def load_test_job():
    """
    Temporary test function.
    Replace this with your JD discovery node later.
    """
    return FitScoreState(
        job_title="Senior Technical Program Manager",
        company="ExampleCorp",
        source_site="Indeed",
        job_url="https://www.indeed.com/viewjob?jk=12345",
        job_id="12345",
        jd_text="Example job description text goes here...",
        jd_requirements={
            "skills": ["cloud", "infrastructure", "security"],
            "responsibilities": ["lead programs", "manage stakeholders"],
            "seniority": "senior"
        },
        resume_json={
            "skills": ["cloud", "security", "TPM leadership"],
            "experience": ["cloud modernization", "security rollout"]
        }
    )

def run_pipeline():
    initial_state = load_test_job()
    final_state = graph.invoke(initial_state)

    print("\n=== FIT SCORING RESULTS ===")
    print(f"Job Title: {final_state.job_title}")
    print(f"Company: {final_state.company}")
    print(f"Fit Score: {final_state.fit_score}")
    print(f"Compensation Estimate: {final_state.compensation_estimate}")
    print(f"Compensation Fit: {final_state.compensation_fit}")
    print(f"Recommendation: {final_state.recommendation}")
    print(f"Explanation: {final_state.explanation}")

if __name__ == "__main__":
    run_pipeline()

