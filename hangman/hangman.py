from ascii_hangman import draw_hangman
import json
import random
import inflect

def main():
    # open json files with English and Russian words
    with open(R"list_of_nouns.json") as eng_words:
            e_words = json.load(eng_words)
    with open(R"list_of_nouns_rus.json") as rus_words:
            r_words = json.load(rus_words)

    lives = 7  # Total number of lives

    while True:
        lang = language_select()
         # refer to eng or rus words depending on user's choice of language
        if lang == "eng":
            words = e_words
        elif lang == "rus":
            words = r_words
        # Computer generates random word
        word = str(random.choice(words["nouns"])).upper()

        # User plays hangman
        if hangman_game(lang, word, lives) == False:  # Loss
            draw_hangman(lang, 0)
            if lang == "eng":
                print(f"\nSorry, you died. ☠️\n\nThe word was: {word}\n")
            elif lang == "rus":    
                print(f"\nК сожалению, ты был повешен. ☠️\n\nЗагаданное слово: {word}\n")
        else:  # Victory
            draw_hangman(lang)  
            if lang == "eng":
                print(f"\nCongratulations, you won! 🎉🎉🎉\n\nThe word was: {word}\n")  # Congratulatory message
            elif lang == "rus":
                print(f"\nПоздравляю, ты победил! 🎉🎉🎉\n\nОтгаданное слово: {word}\n")  

        # If user wants to play again - repeat loop
        if play_again(lang):
            pass
        else:
            break
        
def hangman_game(lang, word, lives=7):
    """Hangman game. 7 lives by default."""
    p = inflect.engine()

    # how many lives user has, what letters they've used and guessed
    used_letters = []
    revealed_letters = []

    # Loop until user guesses the word or loses
    while True:
        life_str_eng = p.plural_noun('life', lives)  # use plural or singlular of "life" 
        if lives == 1:  # Russian "жизнь" with corresponding suffixes
            life_str_rus = "жизнь"
        elif lives in [2,3,4]:
            life_str_rus = "жизни"
        else:
            life_str_rus = "жизней"

        used_letters_str = " ".join(used_letters).upper()  # Used letters as str

        # Print lives; print already used letters unless the game just started
        # Eng version:
        if lang == "eng":
            print(f"\nYou have {lives} {life_str_eng} left.")
            draw_hangman(lang, lives)
            if len(used_letters) != 0:
                print("\nYou have used these letters:", used_letters_str) 
            print("\nCurrent word: ", end="")

        # Rus version:
        elif lang == "rus":
            print(f"\nУ тебя осталось {lives} {life_str_rus}.")
            draw_hangman(lang, lives)
            if len(used_letters) != 0:
                print("\nТы уже использовал следующие буквы:", used_letters_str) 
            print("\nЗагаданное слово: ", end="")


        # Outputs blank for every unrevealed letter of the word,
        for letter in word:
            if letter in revealed_letters:
                print(letter + " ", end="")
            else: 
                print("_ ", end="")

        if lang == "eng":
            # Asks user to type a letter
            guess = input("\n\nGuess a letter: ").strip().upper()
            # if user inputs symbol,number or multiple letters: -1 life
            if (guess.isalpha() == False) or (len(guess) > 1):
                print(f"\n{guess} is not a letter.") 
                lives -= 1
            elif guess in used_letters:   # if user guessed already used letter: -1 life
                print("\nYou've already guessed that letter.")
                lives -= 1
            elif guess not in word: # if guess is wrong, add to used list, -1 life
                print(f"\nWrong ❌ Letter {guess} is not in the word.")
                used_letters.append(guess)
                lives -=1
            else: # if guess is right, add it to used and revealed lists
                print("\nCorrect ✔️")
                used_letters.append(guess)
                revealed_letters.append(guess)
        
        elif lang == "rus":
            # Asks user to type a letter
            guess = input("\n\nУгадай букву: ").strip().upper()
            # if user inputs symbol,number or multiple letters: -1 life
            if (guess.isalpha() == False) or (len(guess) > 1):
                print(f"\n'{guess}' не является буквой.") 
                lives -= 1
            elif guess in used_letters:   # if user guessed already used letter: -1 life
                print("\nТы уже угадывал эту букву.")
                lives -= 1
            elif guess not in word: # if guess is wrong, add to used list, -1 life
                print(f"\nНеверно ❌ Буквы '{guess}' нет в загаданном слове.")
                used_letters.append(guess)
                lives -=1
            else: # if guess is right, add it to used and revealed lists
                print("\nВерно ✔️")
                used_letters.append(guess)
                revealed_letters.append(guess)

        # when out of lives - game is lost, return False
        if lives == 0:
            return False
        
        # If every letter revealed - game won, return True
        if check_win(letter, word, revealed_letters):
            return True
            

def language_select():
    while True:
        language = input("\n\nPlease select language / Пожалуйста, выберите язык:\n  1. ENGLISH\n  2. RUSSIAN / РУССКИЙ\n Enter/Ввод: ").strip().lower()
        if (language.find("en") != -1) or (language.find("1") != -1):
            return "eng"
        elif (language.find("ru") != -1) or (language.find("2") != -1) or (language.find("ру") != -1):
            return "rus"


def check_win(letter, word, used_list):
    """Function verifies if user has guessed all the letters and therefore won"""

    # Verify what letters of the word have been guessed
    verification_list = []
    for letter in word:
        if letter in used_list:
            verification_list.append("T")
        else:
            verification_list.append("F")
            
    # If every letter has been already guessed - return True
    if "F" not in verification_list:
        return True
    else:
        return False


def play_again(lang):
    """Proposes user to play a game again"""
    while True:
        if lang == "eng":    
            again = input("Do you want to play again? 🤔\n(type Yes or No): ").strip().lower()
            if again == "yes":
                return True
            elif again == "no":
                return False
        elif lang == "rus":
            again = input("Хочешь сыграть снова? 🤔\n(Введите 'да' или 'нет'): ").strip().lower()
            if again == "да":
                return True
            elif again == "нет":
                return False
    

if __name__ == "__main__":
    main()
