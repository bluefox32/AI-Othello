EMPTY, BLACK, WHITE = '.', 'B', 'W'
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              ( 0, -1),          ( 0, 1),
              ( 1, -1), ( 1, 0), ( 1, 1)]

def create_board():
    board = [[EMPTY] * 8 for _ in range(8)]
    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE
    return board

def print_board(board):
    print("\n     " + "   ".join(str(i+1) for i in range(8)))
    print("   +" + "---+" * 8)
    for i, row in enumerate(board):
        row_cells = " | ".join(pretty_cell(c) for c in row)
        print(f"{i+1:2} | {row_cells} |")
        print("   +" + "---+" * 8)
       
def pretty_cell(cell):
    return '●' if cell == BLACK else '○' if cell == WHITE else ' '

def is_on_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def valid_moves(board, player):
    return [(x, y) for x in range(8) for y in range(8)
            if board[x][y] == EMPTY and would_flip(board, x, y, player)]

def would_flip(board, x, y, player):
    other = WHITE if player == BLACK else BLACK
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if is_on_board(nx, ny) and board[nx][ny] == other:
            while is_on_board(nx, ny) and board[nx][ny] == other:
                nx += dx
                ny += dy
            if is_on_board(nx, ny) and board[nx][ny] == player:
                return True
    return False

def make_move(board, x, y, player):
    board[x][y] = player
    other = WHITE if player == BLACK else BLACK
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        to_flip = []
        while is_on_board(nx, ny) and board[nx][ny] == other:
            to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if is_on_board(nx, ny) and board[nx][ny] == player:
            for fx, fy in to_flip:
                board[fx][fy] = player

def get_move_input(moves):
    while True:
        raw = input("あなたの手を入力（例: 34 → 3行4列）: ").strip()
        if len(raw) == 2 and raw.isdigit():
            x, y = int(raw[0]) - 1, int(raw[1]) - 1
            if (x, y) in moves:
                return x, y
        print("無効な手です。もう一度。")

def count_pieces(board):
    black = sum(row.count(BLACK) for row in board)
    white = sum(row.count(WHITE) for row in board)
    return black, white

def ai_move(board, moves, player):
    def flip_count(x, y):
        count = 0
        other = WHITE if player == BLACK else BLACK
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            temp = 0
            while is_on_board(nx, ny) and board[nx][ny] == other:
                temp += 1
                nx += dx
                ny += dy
            if is_on_board(nx, ny) and board[nx][ny] == player:
                count += temp
        return count
    best_move = max(moves, key=lambda move: flip_count(*move))
    print(f"AIの手（白○）: {best_move[0]+1}{best_move[1]+1}")
    return best_move

def game_loop():
    board = create_board()
    player = BLACK
    while True:
        print_board(board)
        moves = valid_moves(board, player)
        if not moves:
            print(f"{player} に有効な手がないためパスします。")
            player = WHITE if player == BLACK else BLACK
            if not valid_moves(board, player):
                print("両者とも手がないため、ゲーム終了！")
                b, w = count_pieces(board)
                print(f"結果 - 黒●: {b} | 白○: {w}")
                winner = "黒●" if b > w else "白○" if w > b else "引き分け"
                print(f"勝者: {winner}")
                break
            continue

        if player == BLACK:
            x, y = get_move_input(moves)
        else:
            x, y = ai_move(board, moves, player)
        make_move(board, x, y, player)
        player = WHITE if player == BLACK else BLACK

if __name__ == "__main__":
    game_loop()