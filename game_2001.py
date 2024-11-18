from flask import Flask, render_template, request, redirect, url_for
from def_roll import roll_the_dice

app = Flask(__name__)

# Global variables to store user and computer points
user_points = 0
computer_points = 0

def calculate_points(points):
    """Calculate points based on the result of rolling the dice.

    If the roll is 7, the points are divided by 7.
    If the roll is 11, the points are multiplied by 11.
    Otherwise, the rolled value is added to the points.

    :param int points: Current points of the player.
    :rtype: int
    :return: Updated points after applying the rules.
    """
    roll = roll_the_dice("2D6")
    if roll == 7:
        points //= 7
    elif roll == 11:
        points *= 11
    else:
        points += roll
    return points

@app.route("/")
def game_2001():
    """Render the main game page.

    Displays the current points of both the user and the computer.

    :return: Rendered HTML template for the game page.
    """
    return render_template("game.html", user_points=user_points, computer_points=computer_points)

@app.route("/roll", methods=["POST"])
def roll():
    """Handle the dice roll action.

    Rolls the dice for both the user and the computer, updates their points,
    and redirects to the appropriate page based on the game state.

    :return: Redirect to the game page or result page if the game is over.
    """
    global user_points, computer_points
    user_points += roll_the_dice("2D6")
    computer_points += roll_the_dice("2D6")

    user_points = calculate_points(user_points)
    computer_points = calculate_points(computer_points)

    if user_points >= 2001 or computer_points >= 2001:
        return redirect(url_for("result"))

    return redirect(url_for("game_2001"))

@app.route("/result")
def result():
    """Render the result page.

    Determines the winner based on the final points and displays the result.
    Resets the points after determining the winner.

    :return: Rendered HTML template for the result page with the winner information.
    """
    global user_points, computer_points
    if computer_points > user_points:
        winner = "Computer wins!"
    elif user_points > computer_points:
        winner = "User wins!"
    else:
        winner = "Draw"

    # Reset the points after determining the winner
    user_points = 0
    computer_points = 0

    return render_template("result.html", winner=winner)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
