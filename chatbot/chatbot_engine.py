from chatbot.chatbot_utils import (
    normalize_text,
    find_candidates_by_skill,
    get_top_candidates,
    find_candidate,
    format_candidate
)


class RecruitmentChatbot:

    def __init__(self):

        self.name = "AI Recruitment Assistant"

    def get_response(self, question, candidates):

        question = normalize_text(question)

        if not candidates:

            return (
                "No candidate screening results are available. "
                "Please upload resumes and complete screening first."
            )

        # 1. Total candidates
        if any(word in question for word in [
            "total candidates",
            "how many candidates",
            "number of candidates"
        ]):

            return (
                f"A total of {len(candidates)} candidates "
                "have been screened."
            )

        # 2. Top candidates
        if any(word in question for word in [
            "top candidates",
            "best candidates",
            "highest ranked",
            "top 3",
            "top three"
        ]):

            top = get_top_candidates(candidates, 3)

            response = "Here are the top candidates:\n\n"

            for index, candidate in enumerate(top, 1):

                response += (
                    f"{index}. {getattr_dummy(candidate)} "
                    f"- {candidate.get('final_score', 0)}%\n"
                )

            return response

        # 3. Best candidate
        if any(word in question for word in [
            "best candidate",
            "highest score",
            "who is the best",
            "first rank",
            "top candidate"
        ]):

            best = get_top_candidates(candidates, 1)[0]

            return (
                f"The highest-ranked candidate is "
                f"{best.get('name', 'Unknown')}.\n\n"
                f"Final Matching Score: "
                f"{best.get('final_score', 0)}%\n"
                f"Recommendation: "
                f"{best.get('recommendation', 'Not available')}"
            )

        # 4. Skill-based search
        skill_keywords = [
            "python", "java", "django", "flask",
            "sql", "machine learning", "deep learning",
            "power bi", "tensorflow", "pytorch",
            "react", "javascript", "html", "css",
            "nlp", "computer vision", "generative ai",
            "fastapi", "aws", "docker", "tableau"
        ]

        for skill in skill_keywords:

            if skill in question:

                matched = find_candidates_by_skill(
                    candidates,
                    skill
                )

                if matched:

                    response = (
                        f"Candidates having {skill.upper()} skill:\n\n"
                    )

                    for candidate in matched:

                        response += (
                            f"- {candidate.get('name', 'Unknown')} "
                            f"({candidate.get('final_score', 0)}%)\n"
                        )

                    return response

                return (
                    f"No candidates with {skill.upper()} "
                    "skill were found."
                )

        # 5. Missing skills
        if any(word in question for word in [
            "missing skills",
            "lack skills",
            "skills missing"
        ]):

            candidate = find_candidate(candidates, question)

            if candidate:

                missing = candidate.get("missing_skills", [])

                return (
                    f"Missing skills for "
                    f"{candidate.get('name', 'Unknown')}:\n"
                    + (
                        ", ".join(missing)
                        if missing else "No missing skills identified."
                    )
                )

            return (
                "Please mention the candidate's name "
                "to check missing skills."
            )

        # 6. Candidate score
        if any(word in question for word in [
            "score", "matching percentage",
            "matching score", "rank"
        ]):

            candidate = find_candidate(candidates, question)

            if candidate:

                return format_candidate(candidate)

            return (
                "Please mention the candidate's name "
                "to view their screening score."
            )

        # 7. Candidate comparison
        if any(word in question for word in [
            "compare", "comparison", "difference"
        ]):

            if len(candidates) < 2:

                return "At least two candidates are needed for comparison."

            top = get_top_candidates(candidates, 2)

            response = "Candidate comparison:\n\n"

            for candidate in top:

                response += (
                    f"{candidate.get('name', 'Unknown')}: "
                    f"{candidate.get('final_score', 0)}%\n"
                    f"Skills: {', '.join(candidate.get('skills', []))}\n\n"
                )

            return response

        # 8. General help
        if any(word in question for word in [
            "hello", "hi", "hey"
        ]):

            return (
                "Hello! Welcome to AI Recruitment Assistant.\n\n"
                "I can help you analyze candidates, compare "
                "skills and understand resume matching scores."
            )

        if "help" in question:

            return (
                "You can ask me questions like:\n\n"
                "1. Who is the best candidate?\n"
                "2. Show top three candidates.\n"
                "3. Find candidates with Python skills.\n"
                "4. How many candidates were screened?\n"
                "5. Show Candidate A's score.\n"
                "6. What are the missing skills?\n"
                "7. Compare candidates."
            )

        return (
            "I can answer questions about the candidates "
            "currently screened on this website. "
            "Please ask about candidate names, skills, "
            "matching scores, rankings or missing skills."
        )


def getattr_dummy(candidate):

    return candidate.get("name", "Unknown Candidate")