"""
Language Detective (student starter)
Python 3, standard library only. Keep this file in the same folder as samples.py.

Every language leaves a fingerprint: the little 3-letter chunks it uses most.
English loves "the", German loves "en " and "ein".
We collect those fingerprints, then match mystery messages against them.
"""
import math
import sys
import unicodedata
from collections import Counter
from samples import SAMPLES
THRESHOLD = 0.15 
if hasattr(sys.stdout, "reconfigure"):
     sys.stdout.reconfigure(encoding="utf-8")
def char_trigrams(text):
    cleaned = []
    for ch in text.lower():
        if ch.isalpha() or unicodedata.category(ch).startswith("M"):
          cleaned.append(ch)
    else:
        cleaned.append(" ")
    padded = " " + " ".join("".join(cleaned).split()) + " "
    # TODO: return a Counter of every 3-character slice padded[i:i + 3]
    #       for i from 0 up to len(padded) - 3
    return Counter()
PROFILES = {language: char_trigrams(text) for language, text in SAMPLES.items()}
def cosine(p, q):
    # TODO 1: dot = for every gram in p that is also in q, add p[gram] * q[gram]
    # TODO 2: size_p = square root of the sum of (count * count) for p; same for q
    # TODO 3: return 0.0 if either size is 0, otherwise dot / (size_p * size_q)
    return 0.0
def rank_languages(text):
    mystery = char_trigrams(text)
    scores = {}
    # TODO: for every language and profile in PROFILES,
    #   scores[language] = cosine(mystery, profile)
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
def detect(text):
    ranking = rank_languages(text)
    if not ranking:
        return "Unknown"
    best_language, best_score = ranking[0]
    # TODO (final mission): return "Unknown" if best_score is below THRESHOLD
    return best_language
def clues(text,language,n=6):
    """The trigrams the mystery text shares with language: the evidence!"""
    if language not in PROFILES:
        return[]
    mystery = char_trigrams(text)
    shared = Counter({g:c*PROFILES[language][g] for g,c in mystery.items() if g in PROFILES[language]})
    return[g for g, _ in shared.most_common(n)]
CASE_FILES = [
    ("The library is closed on Sundays but the café is open.", "English"),
    ("¿Dónde está la estación de tren? Necesito comprar un billete.", "Spanish"),
    ("Ieri sera abbiamo mangiato una pizza buonissima con gli amici.", "Italian"),
    ("Je voudrais un croissant et un chocolat chaud, s'il vous plaît.", "French"),
    ("Ich habe heute keine Zeit, weil ich für die Prüfung lernen muss.", "German"),
    ("आज मौसम बहुत अच्छा है, चलो बाहर घूमने चलते हैं।", "Hindi"),
    ("Yaar aaj bahut garmi hai, chalo ice cream khaane chalte hain.", "Hinglish"),
]
COLD_CASES = ["pizza", "Hola!", "la pasta è buona", "Kal meeting hai, please don't be late",
             "12345", "こんにちは、元気ですか"]
def play():
        you = detective = 0
        print("Read each message and type your guess (e.g. French). Then see what the detective says.\n")
        for number, (text, answer) in enumerate(CASE_FILES, 1):
            print(f"Case {number}: {text}")
            guess = input(" Your guess: ").strip().title()
            found = detect(text)
            you += guess == answer
            detective += found == answer
            print(f" Detective: {found} Answer: {answer} Clues: {clues(text, found)}\n")
        print(f"Final score - You: {you}/{len(CASE_FILES)} Detective: {detective}/{len(CASE_FILES)}")

if __name__ == "__main__":
    play()
    print("\nCold cases:")
    for text in COLD_CASES:
        top_two = ", ".join(f"{lang} {score:.2f}" for lang, score in rank_languages(text)[:2])
        print(f" {text!r:<42} -> {detect(text):<9} (top two: {top_two})")
    print("\nInterrogation room: type any text ('quit' to stop).")
    while True:
        text = input("\n> ")
        if text.strip().lower() == "quit":
            break
        for language, score in rank_languages(text):
           print(f" {language:<9} {'#' * round(score * 30):<30} {score:.2f}")