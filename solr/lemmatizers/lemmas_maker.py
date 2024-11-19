import spacy

nlp = spacy.load("en_core_web_sm")

input_file = "words_alpha.txt" 
words = []

with open(input_file, "r") as f:
    words = [line.strip() for line in f]

output_file = "lemmas_spacy.txt"
with open(output_file, "w") as f:
    for word in words:
        doc = nlp(word)
        lemma = doc[0].lemma_ 
        f.write(f"{word} => {lemma}\n")

print(f"Lemmatized results saved to {output_file}")

