import random
import os

def make_grid():
    global grid_vals
    global size

    header = "   "
    
    for i in range(size):
        header += "     " + str(i + 1)
        
    print(header)

    for row in range(size):
        line = "     "
        
        if row == 0:
            line += "______" * size
            print(line)

        line = "     " + "|     " * size + "|"
        
        print(line)

        line = "  " + str(row + 1) + "  "
        
        for col in range(size):
            line += "|  " + str(grid_vals[row][col]) + "  "
            
        print(line + "|")

        line = "     " + "|_____" * size + "|"
        
        print(line)

    print()

def place_mines():
    global game_board
    global total_mines
    global size

    mines_placed = 0
    
    while mines_placed < total_mines:
        random_val = random.randint(0, size * size - 1)
        row, col = random_val // size, random_val % size

        if game_board[row][col] != -1:
            mines_placed += 1
            game_board[row][col] = -1

def get_numbers():
    global game_board
    global size

    for row in range(size):
        for col in range(size):
            if game_board[row][col] == -1:
                continue

            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= row + dx < size and 0 <= col + dy < size:
                        if game_board[row + dx][col + dy] == -1:
                            game_board[row][col] += 1

def check_neighbors(r, c):
    global grid_vals
    global game_board
    global visited

    if [r, c] not in visited:
        visited.append([r, c])
        if game_board[r][c] == 0:
            grid_vals[r][c] = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= r + dx < size and 0 <= c + dy < size:
                        check_neighbors(r + dx, c + dy)

        elif game_board[r][c] != 0:
            grid_vals[r][c] = game_board[r][c]

def clear_screen():
    os.system("clear")

def game_instructions():  
    print("\n\t\t[  M I N E S W E E P E R  ]\n")
    print("Instructions:")
    print("1. Enter row and column number [e.g., '2 3'] to select a cell.")
    print("2. To flag a cell as a mine, enter 'F' after row and column [e.g., '2 3 F'].\n\n")

def check_win():
    global grid_vals
    global size
    global total_mines

    uncovered_cells = sum(
        1 for row in range(size) for col in range(size)
        if grid_vals[row][col] != ' ' and grid_vals[row][col] != 'F'
    )

    return uncovered_cells == size * size - total_mines

def reveal_mines():
    global grid_vals
    global game_board
    global size

    for row in range(size):
        for col in range(size):
            if game_board[row][col] == -1:
                grid_vals[row][col] = 'M'

if __name__ == "__main__":
    size = 9
    total_mines = 25

    game_board = [[0 for _ in range(size)] for _ in range(size)]
    grid_vals = [[' ' for _ in range(size)] for _ in range(size)]
    flags = []
    
    place_mines()
    get_numbers()
    game_instructions()

    game_over = False

    while not game_over:
        make_grid()
        user_input = input("Enter row and column = ").split()

        if len(user_input) == 2:
            try:
                row, col = map(int, user_input)
            except ValueError:
                clear_screen()
                print("Invalid input. ")
                game_instructions()
                continue

        elif len(user_input) == 3 and user_input[2] in ('F', 'f'):
            try:
                row, col = map(int, user_input[:2])
            except ValueError:
                clear_screen()
                print("Invalid input. ")
                game_instructions()
                continue

            if 1 <= row <= size and 1 <= col <= size:
                row -= 1
                col -= 1

                if [row, col] not in flags and grid_vals[row][col] == ' ':
                    clear_screen()
                    print("Flag set")
                    flags.append([row, col])
                    grid_vals[row][col] = 'F'
                else:
                    clear_screen()
                    print("Invalid flag position. ")
            else:
                clear_screen()
                print("Invalid input. ")
            continue

        else:
            clear_screen()
            print("Invalid input. ")
            game_instructions()
            continue

        if 1 <= row <= size and 1 <= col <= size:
            row -= 1
            col -= 1
        else:
            clear_screen()
            print("Invalid input. ")
            game_instructions()
            continue

        if [row, col] in flags:
            flags.remove([row, col])

        if game_board[row][col] == -1:
            grid_vals[row][col] = 'M'
            reveal_mines()
            make_grid()
            print("You hit a mine. Game Over!")
            game_over = True

        elif game_board[row][col] == 0:
            visited = []
            grid_vals[row][col] = '0'
            check_neighbors(row, col)

        else:
            grid_vals[row][col] = game_board[row][col]

        if check_win():
            reveal_mines()
            make_grid()
            print("Congratulations! You Win!")
            game_over = True

        clear_screen()