import re


def normalize_text(text):
    """Convert text into lowercase normalized format."""
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def get_candidate_name(candidate):
    return candidate.get("name", "Unknown Candidate")


def find_candidates_by_skill(candidates, skill):
    """Find candidates who possess a particular skill."""

    skill = normalize_text(skill)

    matched = []

    for candidate in candidates:

        skills = [
            normalize_text(s)
            for s in candidate.get("skills", [])
        ]

        if skill in skills:
            matched.append(candidate)

    return matched


def get_top_candidates(candidates, limit=3):
    """Return top-ranked candidates."""

    return sorted(
        candidates,
        key=lambda x: float(x.get("final_score", 0)),
        reverse=True
    )[:limit]


def find_candidate(candidates, question):
    """Find a candidate mentioned in the question."""

    question = normalize_text(question)

    for candidate in candidates:

        name = normalize_text(
            candidate.get("name", "")
        )

        email = normalize_text(
            candidate.get("email", "")
        )

        if name and name in question:
            return candidate

        if email and email in question:
            return candidate

    return None


def format_candidate(candidate):

    return (
        f"Candidate: {get_candidate_name(candidate)}\n"
        f"Email: {candidate.get('email', 'Not found')}\n"
        f"Skills: {', '.join(candidate.get('skills', []))}\n"
        f"Skill Score: {candidate.get('skill_score', 0)}%\n"
        f"Semantic Score: {candidate.get('semantic_score', 0)}%\n"
        f"Final Score: {candidate.get('final_score', 0)}%\n"
        f"Matched Skills: {', '.join(candidate.get('matched_skills', []))}\n"
        f"Missing Skills: {', '.join(candidate.get('missing_skills', []))}\n"
        f"Recommendation: {candidate.get('recommendation', 'Not available')}"
    )