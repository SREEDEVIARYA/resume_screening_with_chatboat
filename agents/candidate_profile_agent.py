
import re
import spacy


class CandidateProfileAgent:

    def __init__(self):

        # Do not load spaCy during initialization
        self.nlp = None

    def load_model(self):

        # Load model only once when needed
        if self.nlp is None:

            print("Loading spaCy NLP model...")

            self.nlp = spacy.load(
                "en_core_web_sm",
                disable=["parser", "lemmatizer"]
            )

        return self.nlp

    def run(self, text):

        # Email extraction
        email = re.findall(
            r'[\w.+-]+@[\w.-]+\.\w+',
            text
        )

        # Indian mobile number extraction
        phone = re.findall(
            r'(?:\+91[-\s]?)?[6-9]\d{9}',
            text
        )

        # Limit text processing
        text = text[:5000]

        # Load NLP model only when required
        nlp = self.load_model()

        doc = nlp(text)

        name = "Not identified"

        # Extract person entities
        for ent in doc.ents:

            if ent.label_ == "PERSON":

                name = ent.text
                break

        return {

            "name": name,

            "email": email[0] if email else "Not found",

            "phone": phone[0] if phone else "Not found"

        }
