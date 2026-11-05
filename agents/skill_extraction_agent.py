import re

class SkillExtractionAgent:

    def __init__(self):

        self.skills = [
            "python",
            "java",
            "sql",
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "data science",
            "power bi",
            "tableau",
            "django",
            "flask",
            "tensorflow",
            "pytorch",
            "keras",
            "pandas",
            "numpy",
            "scikit-learn",
            "html",
            "css",
            "javascript",
            "react",
            "aws",
            "docker",
            "nlp",
            "computer vision",
            "generative ai",
            "langchain",
            "fastapi",
            "communication",
            "teamwork",
            "leadership"
        ]

    def run(self, text):

        text = text.lower()

        found_skills = []

        for skill in self.skills:

            pattern = (
                r'(?<!\w)' +
                re.escape(skill) +
                r'(?!\w)'
            )

            if re.search(pattern, text):

                found_skills.append(skill)

        return found_skills