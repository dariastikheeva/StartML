def drown(board):
    if not board:
        return board

    m, n = len(board), len(board[0])

    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != 'O':
            return
        board[i][j] = '*'
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)

    for i in range(m):
        for j in range(n):
            if i == 0 or i == m - 1 or j == 0 or j == n - 1:
                if board[i][j] == 'O':
                    dfs(i, j)

    for i in range(m):
        for j in range(n):
            if board[i][j] == 'O':
                board[i][j] = 'X'

    for i in range(m):
        for j in range(n):
            if board[i][j] == '*':
                board[i][j] = 'O'

    return board
