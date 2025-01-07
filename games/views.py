from django.shortcuts import render
import random
# Create your views here.

def home(request):
    return render(request,'home.html')


number_to_guess = random.randint(1, 100)
chances = 7

def guess_number(request):
    global number_to_guess, chances
    message = "Welcome! Enter your guess below:"
    if request.method == 'POST':
        try:
            guess = int(request.POST.get('guess'))
            if guess == number_to_guess:
                message = f"Congratulations! You guessed it right. The number is {number_to_guess}."
                number_to_guess = random.randint(1, 100)  # Reset the game
                chances = 7  # Reset chances
            elif chances <= 1:
                message = f"Game Over! The correct number was {number_to_guess}. Better luck next time."
                number_to_guess = random.randint(1, 100)  # Reset the game
                chances = 7  # Reset chances
            elif guess > number_to_guess:
                message = "Too high! Try again."
                chances -= 1
            elif guess < number_to_guess:
                message = "Too low! Try again."
                chances -= 1
        except ValueError:
            message = "Please enter a valid number."
    
    return render(request, 'guess_number.html', {'message': message})

# Global variables to hold the game's state
words = ['rainbow', 'computer', 'science', 'programming',
         'python', 'mathematics', 'player', 'condition',
         'reverse', 'water', 'board', 'geeks']

word = random.choice(words)
guesses = ''
turns = 12
hints_used = set()

def guess_word(request):
    global word, guesses, turns, hints_used
    message = "Guess the characters below:"
    hint_message = ""
    displayed_word = " ".join([char if char in guesses else "_" for char in word])

    if request.method == 'POST':
        guess = request.POST.get('guess', '').lower()

        if guess == "reset":
            # Reset the game
            word = random.choice(words)
            guesses = ''
            turns = 12
            hints_used = set()
            displayed_word = " ".join(["_" for _ in word])
            message = "Game has been reset! Start guessing the new word."
        elif guess == "hint":
            hint_choice = request.POST.get('hint_choice', '')
            if hint_choice == '1' and 1 not in hints_used:
                hint_message = f"The first letter of the word is '{word[0]}'."
                hints_used.add(1)
            elif hint_choice == '2' and 2 not in hints_used:
                hint_message = f"The length of the word is {len(word)}."
                hints_used.add(2)
            elif hint_choice == '3' and 3 not in hints_used:
                hint_message = f"The last letter of the word is '{word[-1]}'."
                hints_used.add(3)
            else:
                hint_message = "Invalid choice or hint already used!"
        else:
            if len(guess) == 1 and guess.isalpha():
                guesses += guess
                if guess not in word:
                    turns -= 1
                    message = f"Wrong! You have {turns} more guesses."
                else:
                    message = "Correct guess!"
            else:
                message = "Please enter a single valid character."

        displayed_word = " ".join([char if char in guesses else "_" for char in word])

        if "_" not in displayed_word:
            message = f"You Win! The word is '{word}'."
            word = random.choice(words)
            guesses = ''
            turns = 12
            hints_used = set()
        elif turns == 0:
            message = f"You Lose! The word was '{word}'."
            word = random.choice(words)
            guesses = ''
            turns = 12
            hints_used = set()

    return render(request, 'guess_word.html', {
        'message': message,
        'displayed_word': displayed_word,
        'turns': turns,
        'hint_message': hint_message
    })
    
    
game_list = []
game_status = "Welcome to the 21 Number Game! You can enter 1-3 numbers per turn."
game_over = False

def reset_game():
    """Reset the game state."""
    global game_list, game_status, game_over
    game_list = []
    game_status = "Game reset! Start a new round."
    game_over = False

def player_turn(player_numbers):
    """Handle the player's turn."""
    global game_list, game_status
    for i in range(player_numbers):
        next_value = len(game_list) + 1
        if next_value > 21:
            break
        game_list.append(next_value)

def computer_turn():
    """Handle the computer's turn."""
    global game_list, game_status, game_over
    if len(game_list) == 21:
        game_status = "You win! The computer lost by hitting 21."
        game_over = True
        return

    next_start = len(game_list) + 1
    max_computer_numbers = min(3, 21 - next_start + 1)

    for i in range(max_computer_numbers):
        next_value = next_start + i
        if next_value == 21:
            # Computer hits 21 and loses
            game_status = "You win! The computer hit 21."
            game_over = True
            return
        game_list.append(next_value)

    if len(game_list) == 21:
        game_status = "You lose! The computer wins by leaving you with 21."
        game_over = True

def number_21(request):
    global game_status, game_over, game_list
    if request.method == "POST":
        if "reset" in request.POST:
            reset_game()
        elif not game_over:
            try:
                player_numbers = int(request.POST.get("player_numbers", 1))
                if 1 <= player_numbers <= 3:
                    player_turn(player_numbers)
                    if len(game_list) == 21:
                        game_status = "You lose! You hit 21."
                        game_over = True
                    elif not game_over:
                        computer_turn()
                else:
                    game_status = "Please enter a valid number between 1 and 3."
            except ValueError:
                game_status = "Invalid input. Enter a number between 1 and 3."
    return render(request, "21_number.html", {"game_status": game_status, "game_list": game_list})
