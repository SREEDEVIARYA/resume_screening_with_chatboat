class RankingAgent:

    def run(self, candidates):

        ranked_candidates = sorted(
            candidates,
            key=lambda x: x["final_score"],
            reverse=True
        )

        for index, candidate in enumerate(
            ranked_candidates,
            start=1
        ):

            candidate["rank"] = index

        return ranked_candidates