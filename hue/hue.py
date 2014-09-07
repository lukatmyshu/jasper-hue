import phue
import re

WORDS = ["LIGHTS", "LIGHT"]

def isValid(text):
    return bool(re.search(r'\bLight\b', text, re.IGNORECASE))
