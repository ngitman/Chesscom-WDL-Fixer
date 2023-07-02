import random
import chessdotcom
from exceptions import CustomExceptions
import matplotlib.pyplot as plt

username = input("Please enter your chess.com username: ")
game_type = int(input("What game type would you like to view? Bullet = 1, Blitz = 2, Rapid = 3, Daily = 4 (Please input only the number!): "))
game_type_str = ""
win_p = round(float(input("What is your win percentage? (Please enter a decimal number between 0 and 1.")), 2)
draw_p = round(float(input("What is your draw percentage? (Please enter a decimal number between 0 and 1.")), 2)

if not (0 <= win_p <= 1) and (0 <= draw_p <= 1):
    raise CustomExceptions.IllegalProbabilityException
if not (1 <= game_type <= 4):
    raise CustomExceptions.InvalidGameType
elif game_type == 1:
    game_type_str += "chess_bullet"
elif game_type == 2:
    game_type_str += "chess_blitz"
elif game_type == 3:
    game_type_str += "chess_rapid"
elif game_type == 4:
    game_type_str += "chess_daily"

response = chessdotcom.get_player_stats(username).json

trials = 0
wins = response['stats'][game_type_str]['record']['win']
draws = response['stats'][game_type_str]['record']['draw']
losses = response['stats'][game_type_str]['record']['loss']

if wins > losses:
    raise CustomExceptions.PositiveWDL

wins_growth = [wins]
losses_growth = [losses]
draws_growth = [draws]
x = [0]

# 0 = loss, 1 = draw, 2 = win
def win_game(p_win: float, p_draw: float):
    random_number = round(random.random(), 2)
    modified_win_draw = p_win + p_draw
    if modified_win_draw <= 0 or modified_win_draw > 1:
        raise CustomExceptions.IllegalProbabilityException
    elif random_number <= p_win:
        return 2
    elif p_win < random_number < modified_win_draw:
        return 1
    elif random_number >= modified_win_draw:
        return 0

while wins < losses:
    game_outcome = win_game(win_p, draw_p)
    if game_outcome == 2:
        wins += 1
    elif game_outcome == 1:
        draws += 1
    elif game_outcome == 0:
        losses += 1
    trials += 1
    x.append(trials)
    wins_growth.append(wins)
    draws_growth.append(draws)
    losses_growth.append(losses)

fig, ax = plt.subplots()
ax.plot(x, wins_growth, label="Wins")
ax.plot(x, draws_growth, label="Draws")
ax.plot(x, losses_growth, label="Losses")
ax.set_xlabel("Trials (from current standing)")
ax.set_ylabel("Games")
ax.annotate(f"Wins: {wins_growth[0]}", xy=(x[0], wins_growth[0]))
ax.annotate(f"Draws: {draws_growth[0]}", xy=(x[0], draws_growth[0]))
ax.annotate(f"Losses: {losses_growth[0]}", xy=(x[0], losses_growth[0]))
ax.legend()
ax.set_title(f"Projected Chess W/D/L Growth for {username}")
ax.text(float(len(x) / 2), wins_growth[-1], f'{trials} trials expected')
plt.show()