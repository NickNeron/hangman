from ascii_hangman import draw_hangman
import json
import random
import inflect

def main():
    # Opens in local folder json list of nouns
    with open("list_of_nouns.json") as wordlist:
        words = json.load(wordlist)

    lives = 7  # Total number of lives

    while True:
        # Computer generates random word
        word = str(random.choice(words["nouns"])).upper()

        # User plays hangman
        if hangman_game(word, lives) == False:  # Congratulatory message
            draw_hangman(0)
            print(f"\nSorry, you died. 😵\n\nThe word was: {word}")
        else:  # Loss
            draw_hangman()  
            print(f"\nCongratulations, you won! 🎉🎉🎉\n\nThe word was: {word}\n")

        # If user wants to play again - repeat loop
        if play_again():
            pass
        else:
            break

def hangman_game(word, lives=7):
    """Hangman game. 7 lives by default."""

    p = inflect.engine()

    # how many lives user has, what letters they've used and guessed
    used_letters = []
    revealed_letters = []

    # Loop until user guesses the word or loses
    while True:
        life_str = p.plural_noun('life', lives) # word "life" in plural or single
        used_letters_str = " ".join(used_letters).upper()  # Used letters as str

        # Print lives; print already used letters unless the game just started
        print(f"\nYou have {lives} {life_str} left.")
        draw_hangman(lives)
        if len(used_letters) != 0:
            print("\nYou have used these letters:", used_letters_str) 
        
        # Outputs blank for every unrevealed letter of the word,
        print("\nCurrent word: ", end="")
        for letter in word:
            if letter in revealed_letters:
                print(letter + " ", end="")
            else: 
                print("_ ", end="")

        # Asks user to type a letter
        guess = input("\nGuess a letter: ").strip().upper()

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
        
        # when out of lives - game is lost, return False
        if lives == 0:
            return False
        
        # If every letter revealed - game won, return True
        if check_win(letter, word, revealed_letters):
            return True
            

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


def play_again():
    """Proposes user to play a game again"""
    while True:
        again = input("Do you want to play again? 🤔\n(type Yes or No): ").strip().lower()
        if again == "yes":
            return True
        elif again == "no":
            return False


if __name__ == "__main__":
    main()