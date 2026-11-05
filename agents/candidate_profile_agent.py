import re
import spacy

class CandidateProfileAgent:

    def __init__(self):

        self.nlp = spacy.load("en_core_web_sm")

    def run(self, text):

        email = re.findall(
            r'[\w.+-]+@[\w.-]+\.\w+',
            text
        )

        phone = re.findall(
            r'(?:\+91[-\s]?)?[6-9]\d{9}',
            text
        )

        doc = self.nlp(text[:10000])

        name = "Not identified"

        # Extract person entities from the beginning
        for ent in doc.ents:

            if ent.label_ == "PERSON":

                name = ent.text
                break

        return {

            "name": name,

            "email": email[0] if email else "Not found",

            "phone": phone[0] if phone else "Not found"

        }
