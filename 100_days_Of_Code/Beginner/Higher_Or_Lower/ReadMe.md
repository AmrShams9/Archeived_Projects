<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Higher or Lower Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        .container {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
        }
        pre {
            text-align: left;
            background: #eee;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Higher or Lower Game</h1>
        <p>Welcome to the Higher or Lower game! This project is a fun comparison game where you have to guess which account has more followers.</p>
        
        <h2>How to Play</h2>
        <ul>
            <li>Each round, you will be presented with two accounts.</li>
            <li>You need to guess which account has more followers.</li>
            <li>If you guess correctly, you score a point and move to the next round.</li>
            <li>If you guess incorrectly, the game ends and your final score is displayed.</li>
        </ul>

        <h2>Code Overview</h2>
        <pre>
import random
from replit import clear
from art import logo, vs
from game_data import data

def get_random_account():
    """Get data from random account"""
    return random.choice(data)

def format_data(account):
    """Format account into printable format: name, description and country"""
    name = account["name"]
    description = account["description"]
    country = account["country"]
    return f"{name}, a {description}, from {country}"

def check_answer(guess, a_followers, b_followers):
    """Checks followers against user's guess 
    and returns True if they got it right.
    Or False if they got it wrong."""
    if a_followers > b_followers:
        return guess == "a"
    else:
        return guess == "b"

def game():
    print(logo)
    score = 0
    game_should_continue = True
    account_a = get_random_account()
    account_b = get_random_account()

    while game_should_continue:
        account_a = account_b
        account_b = get_random_account()

        while account_a == account_b:
            account_b = get_random_account()

        print(f"Compare A: {format_data(account_a)}.")
        print(vs)
        print(f"Against B: {format_data(account_b)}.")

        guess = input("Who has more followers? Type 'A' or 'B': ").lower()
        a_follower_count = account_a["follower_count"]
        b_follower_count = account_b["follower_count"]
        is_correct = check_answer(guess, a_follower_count, b_follower_count)

        clear()
        print(logo)
        if is_correct:
            score += 1
            print(f"You're right! Current score: {score}.")
        else:
            game_should_continue = False
            print(f"Sorry, that's wrong. Final score: {score}")

game()
        </pre>

        <h2>How to Run</h2>
        <ol>
            <li>Clone the repository.</li>
            <li>Ensure you have Python installed.</li>
            <li>Install the required modules using <code>pip install -r requirements.txt</code>.</li>
            <li>Run the script using <code>python higher_or_lower.py</code>.</li>
        </ol>

        <p>Enjoy the game! 😊</p>
    </div>
</body>
</html>
