import random


domino_set = []
computer = []
player = []
stock = []
domino_snake = [[]]
status = ""
not_over = True
# random.seed(4)


def shuffle():
    global domino_set, computer, player, stock
    computer = []
    player = []
    stock = []
    for x in range(0, 7):
        for y in range(x, 7):
            domino_set.append([x, y])

    for _ in range(7):
        player.append(domino_set.pop(random.randint(0, len(domino_set) - 1)))
        computer.append(domino_set.pop(random.randint(0, len(domino_set) - 1)))

    for _ in range(len(domino_set)):
        stock.append(domino_set.pop(0))


def assign():
    global domino_snake, status

    for i in range(6, -1, -1):
        if [i, i] in player:
            domino_snake[0] = player.pop(player.index([i, i]))
            break
        elif [i, i] in computer:
            domino_snake[0] = computer.pop(computer.index([i, i]))
            break
    if len(domino_snake) == 0:
        shuffle()
        assign()
    if len(player) > len(computer):
        status = "player"
    elif len(computer) > len(player):
        status = "computer"


def play(number):
    global player, computer, status, stock
    if status == "player":
        if number > 0:
            if player[number - 1][0] != domino_snake[-1][1]:
                temp = player[number - 1][0]
                player[number - 1][0] = player[number - 1][1]
                player[number - 1][1] = temp
            domino_snake.append(player.pop(number - 1))
            status = "computer"
            return
        elif number < 0:
            if player[abs(number) - 1][1] != domino_snake[0][0]:
                temp = player[abs(number) - 1][1]
                player[abs(number) - 1][1] = player[abs(number) - 1][0]
                player[abs(number) - 1][0] = temp
            domino_snake.insert(0, player.pop(abs(number + 1)))
            status = "computer"
            return
        else:
            if len(stock) > 0:
                player.append(stock.pop(0))
                status = "computer"
                return
    if status == "computer":
        if number > 0:
            if computer[number - 1][0] != domino_snake[-1][1]:
                temp = computer[number - 1][0]
                computer[number - 1][0] = computer[number - 1][1]
                computer[number - 1][1] = temp
            domino_snake.append(computer.pop(number - 1))
            status = "player"
            return
        elif number < 0:
            if computer[abs(number) - 1][1] != domino_snake[0][0]:
                temp = computer[abs(number) - 1][1]
                computer[abs(number) - 1][1] = computer[abs(number) - 1][0]
                computer[abs(number) - 1][0] = temp
            domino_snake.insert(0, computer.pop(abs(number + 1)))
            status = "player"
            return
        else:
            if len(stock) > 0:
                computer.append(stock.pop(0))
                status = "player"
                return


def check_end():
    global player, computer, domino_snake, not_over
    if len(player) == 0 or len(computer) == 0:
        not_over = False
    elif domino_snake[0][0] == domino_snake[-1][1]:
        count = 0
        for i in range(len(domino_snake)):
            for j in range(len(domino_snake[i])):
                if domino_snake[i][j] == domino_snake[0][0]:
                    count += 1
        if count == 8:
            not_over = False
    else:
        not_over = True


def draw_game():
    global player, computer, domino_snake, status, stock
    for i in range(70):
        print("=",  end="")

    print(f"\nStock size: {len(stock)}")
    print(f"Computer pieces : {len(computer)}\n")
    if len(domino_snake) <= 6:

        for i in domino_snake:
            print(i, end="")
    else:
        print(f"{domino_snake[0]}{domino_snake[1]}{domino_snake[2]}...{domino_snake[-3]}{domino_snake[-2]}"
              f"{domino_snake[-1]}")

    print("\n\nYour pieces:")

    n = 1
    for i in player:
        print(f"{n}:{i}")
        n += 1

    if status == "player" and not_over:
        print("\nStatus: It's your turn to make a move. Enter your command.")
    elif status == "computer" and not_over:
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")


def pc_plays():
    global computer, domino_snake
    values = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    card_values = {}
    for i in range(7):
        for x in computer:
            if x[0] == i == x[1]:
                values[i] += 2
            elif x[0] == i or x[1] == i:
                values[i] += 1
    for i in range(7):
        for x in domino_snake:
            if x[0] == i == x[1]:
                values[i] += 2
            elif x[0] == i or x[1] == i:
                values[i] += 1
    for i in range(len(computer)):
        card_values[i] = values[computer[i][0]] + values[computer[i][1]]
    for _ in range(len(card_values)):
        max_card_index = 0
        max_value = 0
        for i in range(len(computer)):
            if card_values[i] > max_value:
                max_value = card_values[i]
                max_card_index = i
        if computer[max_card_index][0] == domino_snake[-1][1] or computer[max_card_index][1] == domino_snake[-1][1]:
            return max_card_index + 1
        elif computer[max_card_index][0] == domino_snake[0][0] or computer[max_card_index][1] == domino_snake[0][0]:
            return -max_card_index - 1
        else:
            card_values[max_card_index] = 0
            continue
    return 0


shuffle()
assign()
draw_game()

while not_over:
    if status == "player":
        choice = input()
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please try again.")
            continue
        if abs(choice) > len(player):
            print("Invalid input. Please try again.")
            continue
        elif choice > 0 and player[choice - 1][0] != domino_snake[-1][1] != player[choice - 1][1]:
            print("Illegal move. Please try again.")
            continue
        elif choice < 0 and player[abs(choice) - 1][0] != domino_snake[0][0] != player[abs(choice) - 1][1]:
            print("Illegal move. Please try again.")
            continue
        else:
            play(choice)
    else:
        pc_choice = pc_plays()
        ignore = input()
        play(pc_choice)
    check_end()
    draw_game()

if len(player) == 0:
    print("\nStatus: The game is over. You won!")
elif len(computer) == 0:
    print("\nStatus: The game is over. The computer won!")
else:
    print("\nStatus: The game is over. It's a draw!")
