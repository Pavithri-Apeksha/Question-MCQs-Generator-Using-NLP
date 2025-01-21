import random
import spacy
from collections import Counter
text = """The Greek historian knew what he was talking about. The Nile River fed Egyptian civilization for hundreds of years. The Longest River the Nile is 4,160 miles long-the world's longest river. It begins near the equator in Africa and flows north to the Mediterranean Sea. In the south the Nile churns with cataracts. A cataract is a waterfall. Near the sea the Nile branches into a delta. A delta is an area near a river's mouth where the water deposits fine soil called silt. In the delta, the Nile divides into many streams. The river is called the upper Nile in the south and the lower Nile in the north. For centuries, heavy rains in Ethiopia caused the Nile to flood every summer. The floods deposited rich soil along the Nile's shores. This soil was fertile, which means it was good for growing crops. Unlike the Tigris and Euphrates, the Nile River flooded at the same time every year, so farmers could predict when to plant their crops."""
num_questions = 5
nlp = spacy.load('en_core_web_sm')

def generate_mcqs(text, num_questions=5):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    selected_sentences = random.sample(sentences, min(num_questions, len(sentences)))
    mcqs = []
    for sentence in selected_sentences:
        sent_doc = nlp(sentence)

        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]

        if len(nouns) < 2:
            continue

        noun_counts = Counter(nouns)

        if noun_counts:
            subject = noun_counts.most_common(1)[0][0]

            question_stem = sentence.replace(subject, "_______")

            answer_choices = [subject]

            for _ in range(3):
                distractor = random.choice(list(set(nouns) - set([subject])))
                answer_choices.append(distractor)

            random.shuffle(answer_choices)

            correct_answer = chr(64 + answer_choices.index(subject) + 1)  # Convert index to letter
            mcqs.append((question_stem, answer_choices, correct_answer))

    return mcqs

results = generate_mcqs(text, num_questions=7)


for i, mcq in enumerate(results,start=1):
    question_stem, answer_choices, correct_answer = mcq

    print(f"Q{i}: {question_stem}")
    for j, choice  in enumerate(answer_choices, start=1):
        print(f"{chr(64+j)}: {choice}")