import sys
def legal(x,y,n,board):
    flag = 1
    for i in range(x-1,-1,-1):
        if board[i][y] == 'O':
            flag = 0
        if board[i][y] == 'X':
            break
    if flag:
        for i in range(y-1,-1,-1):
            if board[x][i] == 'O':
                flag = 0
            if board[x][i] == 'X':
                break
    return flag
def DFS(k,num,n,board):
    map = []
    for i in range(n):
        map.append(board[i][:])
    if k >= n**2:
        return num
    else:
        x = int(k/n)
        y = k%n
        if legal(x,y,n,map) and map[x][y] == '.':
            map[x][y] = 'O'
            return DFS(k+1,num+1,n,map)
        else:
            return DFS(k+1,num,n,map)
# def main():
#     ans = []
#     while 1:
#         n = int(sys.stdin.readline().strip('\n'))
#         if n == 0:
#             break
#         board = []
#         for i in range(n):
#             board.append(list(sys.stdin.readline().strip('\n')))
#         answer = []
#         for i in range(n**2):
#             answer.append(DFS(i,0,n,board))
#         ans.append(max(answer))
#     for i in range(len(ans)):
#         print ans[i]
# if __name__ == '__main__':
#     main()

ans = []
while 1:
    n = int(sys.stdin.readline().strip('\n'))
    if n == 0:
        break
    board = []
    for i in range(n):
        board.append(list(sys.stdin.readline().strip('\n')))
    answer = []
    for i in range(n**2):
        answer.append(DFS(i,0,n,board))
    ans.append(max(answer))
for i in range(len(ans)):
    print ans[i]



