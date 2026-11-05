class RecommendationAgent:

    def run(self, candidate):

        score = candidate["final_score"]

        matched = candidate["matched_skills"]

        missing = candidate["missing_skills"]

        if score >= 80:

            recommendation = "Strong Match"

        elif score >= 60:

            recommendation = "Moderate Match"

        else:

            recommendation = "Low Match"

        explanation = (
            f"Matched skills: {', '.join(matched)}. "
            f"Missing skills: {', '.join(missing)}."
        )

        return {
            "recommendation": recommendation,
            "explanation": explanation
        }