# Set up spaCy
import spacy
parser = spacy.load('en')

my_possessions = []
your_possessions = []


def is_plural(word):
    return word.pos == spacy.parts_of_speech.NOUN and word.lemma != word.lower

def has_possession(possession, possessions):
    if possession in possessions:
        return True
    else:
        for thing in possessions:
            if possession.lemma == thing.lemma:
                return True
        return False

def add_possession(possession, possessions):
    if is_plural(possession):
        if has_possession(possession, possessions):
            for x in range(len(possessions)):
                if possession.lemma == possessions[x].lemma:
                    break
            possessions[x] = possession
        else:
            possessions.append(possession)
    else:
        if not has_possession(possession, possessions):
            possessions.append(possession)

while True:
    sentence = input()
    doc = parser(sentence)
    response = []
    # shown as: original token, dependency tag, head word, left dependents, right dependents
    if sentence == "What are my possessions?":
        print(my_possessions)
    elif sentence == "What are your possessions?":
        print(your_possessions)
    else:
        for word in doc:
            left = [t for t in word.lefts]
            right = [t for t in word.rights]
            if word.pos_ == "VERB" and word.lemma_ == "have":
                if len(left) > 0 and len(right) > 0:
                    if left[0].text == "I":
                        add_possession(right[0], my_possessions)
                    if left[0].text == "You" or left[0].text == "you":
                        add_possession(right[0], your_possessions)
                    if left[0].text == "We" or left[0].text == "we":
                        add_possession(right[0], my_possessions)
                        add_possession(right[0], your_possessions)
                    if len(left) > 1 and len(right) > 1:
                        if left[0].lemma_ == "do" and right[1].text == "?":
                            if left[1].lower_ == "i":
                                if has_possession(right[0], my_possessions):
                                    response.append("Yes.")
                                else:
                                    response.append("No.")
                            if left[1].text == "you":
                                if has_possession(right[0], your_possessions):
                                    response.append("Yes.")
                                else:
                                    response.append("No.")
                            if left[1].text == "we":
                                if has_possession(right[0], my_possessions) and has_possession(right[0], your_possessions):
                                    response.append("Yes.")
                                else:
                                    response.append("No.")
            if word.pos_ == "VERB" and word.lemma_ == "get":
                if len(left) > 0 and len(right) > 0:
                    if left[0].text == "I":
                        add_possession(right[0], my_possessions)
                    if left[0].text == "You" or left[0].text == "you":
                        add_possession(right[0], your_possessions)
                    if left[0].text == "We" or left[0].text == "we":
                        add_possession(right[0], my_possessions)
                        add_possession(right[0], your_possessions)
                    if len(left) > 1 and len(right) > 1:
                        if left[0].lemma_ == "have" and right[1].text == "?":
                            if left[1].lower_ == "i":
                                if has_possession(right[0], my_possessions):
                                    response.append("Yes.")
                                else:
                                    response.append("No.")
                            if left[1].text == "you":
                                if has_possession(right[0], your_possessions):
                                    response.append("Yes.")
                                else:
                                    response.append("No.")
                            if left[1].text == "we":
                                if has_possession(right[0], my_possessions) and has_possession(right[0], your_possessions):
                                    response.append("Yes.")
                                else:
                                    response.append("No.")
            print(word.text, word.lemma_, word.tag_, word.pos_, word.dep_, word.head.text, [t.text for t in word.lefts], [t.text for t in word.rights])
    for line in response:
        print("Response: " + line)
