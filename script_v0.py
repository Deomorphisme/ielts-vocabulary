import json
import random
from datetime import datetime
import requests

def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    data = response.json()[0]["meanings"]
    partOfSpeech = set([meaning["partOfSpeech"] for meaning in data])
    print(f"Part of speech : {partOfSpeech}")
    for meaning in data:
        pos = meaning["partOfSpeech"]
        definition = meaning["definitions"][0]["definition"]
        print(f"Definition [{pos}]: {definition}")
        try:
            example = meaning["definitions"][0]["example"]
            print(f"Example : {example}")
        except:
            None

def greetings():
    current_hour = int(datetime.now().strftime("%H"))
    if 6 < current_hour < 13:
        print("Good morning Deo !")
    elif 12 < current_hour < 19:
        print("Good afternoon Deo !")
    else:
        print("Good evening Deo")

def load_words(level):
    json_file = f"{level.lower()}words.json"
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The file {json_file} was not found.")
        return {}

def update_json_file(level, words):
    json_file = f"{level.lower()}words.json"
    try:
        with open(json_file, 'w') as file:
            json.dump(words, file, indent=2)
        print(f"The data has been updated for level {level}.")
    except Exception as e:
        print(f"An error occurred while updating the file {json_file}: {e}")

def choose_level():
    while True:
        level = input("Which level do you want to learn ?\nA1, A2, B1 or B2 : ")
        if level in ('A1','A2','B1','B2'):
            return level
        else:
            print("\nInvalid choice. Please enter 'A1', 'A2', 'B1' or 'B2'.\n")

def choose_action():
    while True:
        action = input("Do you want to discover new words or revise known words? (new/revise/exit): ").lower()
        if action in ('new', 'revise', 'exit'):
            return action
        else:
            print("Invalid choice. Please enter 'new', 'revise', or 'exit'.")

def classify(dico):
    learned_words = []
    new_words = []
    for word in dico:
        if dico[word] > 10:
            learned_words.append(word)
        else:
            new_words.append(word)
    return learned_words, new_words

def learn_new_words(dico, new_words, newly_learned_words, n=20):
    words_to_test = random.sample([x for x in new_words if x not in newly_learned_words], n)
    print("It's going to start now...")
    print("")
    cpt = 0
    for word in words_to_test:
        while True:
            answer = input(f"Do you know the word '{word}' (yes/no) : ")
            if answer == 'yes':
                cpt += 1
                dico[word] += 1
                break
            elif answer == 'no':
                dico[word] = dico[word] - 1 if dico[word] != 0 else 0
                get_definition(word)
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
        print("")
    print(f"You have {cpt} good answer(s). Keep going !\n")
    return dico, new_words, newly_learned_words

def revise_learned_words(dico, learned_words, newly_revised_words, n=20):
    words_to_test = random.sample([x for x in learned_words if x not in newly_revised_words], n)
    print("It's going to start now...")
    print("")
    cpt = 0
    for word in words_to_test:
        while True:
            answer = input(f"Do you know the word '{word}' (yes/no) : ")
            if answer == 'yes':
                cpt += 1
                dico[word] += 1
                break
            elif answer == 'no':
                dico[word] = dico[word] - 1 if dico[word] != 0 else 0
                get_definition(word)
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
        print("")
    print(f"You have {cpt} good answer(s). Keep going !\n")
    return dico, learned_words, newly_revised_words

def run():
    print("\n-----------------------------------------------")
    print("========== VOCABULARY FOR IELTS PREP ==========")
    print("-----------------------------------------------\n")
    greetings()
    while True:
        level = choose_level()
        dico = load_words(level)
        learned_words, new_words = classify(dico)
        newly_learned_words = []
        newly_revised_words = []
        print("\n----------------------------------------------")
        print(f"---------- Let's learn level {level} now ----------\n\n")

        while True:
            action = choose_action()
            if action == "new":
                dico, new_words, newly_learned_words = learn_new_words(dico, new_words, newly_learned_words)
                update_json_file(level, dico)
            elif action == "revise":
                dico, learned_words, newly_revised_words = revise_learned_words(dico, learned_words, newly_revised_words)
                update_json_file(level, dico)
            else:
                break
        while True:
            continue_learn = input("Do you want to continue with another level ? (yes/no)")
            if continue_learn in ("yes","no"):
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
        if continue_learn == "no":
            break 
    return None

run()