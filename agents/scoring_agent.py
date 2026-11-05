class ScoringAgent:

    def run(
        self,
        candidate_skills,
        required_skills,
        semantic_score
    ):

        required = set(required_skills)

        matched = set(candidate_skills) & required

        if required:

            skill_score = (
                len(matched) / len(required)
            ) * 100

        else:

            skill_score = 0

        final_score = (
            skill_score * 0.40
            +
            semantic_score * 0.60
        )

        return {
            "skill_score": round(skill_score, 2),
            "semantic_score": round(semantic_score, 2),
            "final_score": round(final_score, 2),
            "matched_skills": list(matched),
            "missing_skills": list(required - matched)
        }