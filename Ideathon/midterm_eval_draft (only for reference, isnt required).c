#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

#define MAXSIDE 25
#define MAXMINES 99
#define MOVESIZE 526 

int SIDE;   // side length of the board
int MINES;  // number of mines on the board

// is a valid cell or not
bool isValid(int row, int col) {
    return (row >= 0) && (row < SIDE) && (col >= 0) && (col < SIDE);
}

// A Utility Function to check whether given cell (row, col) has a mine or not.
bool isMine(int row, int col, char board[][MAXSIDE]) {
    return (board[row][col] == '*');
}

// A Function to print the current gameplay board
void printBoard(char myBoard[][MAXSIDE]) {
    int i, j;
    printf("   ");
    for (i = 0; i < SIDE; i++)
        printf(" %d ", i);
        
    printf("\n");
    for (i = 0; i < SIDE; i++) {
        printf(" %d ", i);

        for (j = 0; j < SIDE; j++)
            printf(" %c ", myBoard[i][j]);
        printf("\n");
    }
}

// count no of mines
int countAdjacentMines(int row, int col, char realBoard[][MAXSIDE]) {
    int count = 0;
    int A[] = {-1, 0, 1};
    for (int u = 0; u < 3; u++) {
        for (int uu = 0; uu < 3; uu++) {
            int nrow = row + A[u];
            int ncol = col + A[uu];
            if (isValid(nrow, ncol) && isMine(nrow, ncol, realBoard))
                count++;
        }
    }
    return count;
}

// A Function to place the mines randomly on the board
void placeMines(int x, int y, char realBoard[][MAXSIDE], char myBoard[][MAXSIDE]) {
    bool mark[MAXSIDE * MAXSIDE];
    memset(mark, false, sizeof(mark));

    for (int i = 0; i < MINES;) {
        int random = rand() % (SIDE * SIDE);
        int r = random % SIDE;
        int c = random / SIDE;

        if (!mark[random] && !(abs(r - x) <= 1 && abs(c - y) <= 1)) {
            realBoard[r][c] = '*';
            mark[random] = true;
            i++;
        }
    }

    // Open the first cell
    for (int u = -1; u <= 1; u++) {
        for (int uu = -1; uu <= 1; uu++) {
            int nrow = x + u;
            int ncol = y + uu;
            if (isValid(nrow, ncol) && !isMine(nrow, ncol, realBoard))
                myBoard[nrow][ncol] = countAdjacentMines(nrow, ncol, realBoard) + '0';
        }
    }
}

// play playMinesweeper
void playMinesweeper() {
    bool gameOver = false;
    char realBoard[MAXSIDE][MAXSIDE], myBoard[MAXSIDE][MAXSIDE];
    int movesLeft = SIDE * SIDE - MINES, x, y;

    // Initialize the game board
    for (int i = 0; i < SIDE; i++) {
        for (int j = 0; j < SIDE; j++) {
            myBoard[i][j] = realBoard[i][j] = '-';
        }
    }

    // Display the initial state of the board with mines
    printf("Initial State of Board (Mines are denoted by '*'):\n");
    printBoard(realBoard);

    // Get the first move from the user
    printf("Enter your first move (row, column): ");
    scanf("%d %d", &x, &y);

    // Place mines after the first move
    placeMines(x, y, realBoard, myBoard);

    int currentMoveIndex = 0;
    int A[] = {-1, 0, 1};

    while (!gameOver) {
        printf("Current Status of Board : \n");
        printBoard(myBoard);
        printf("Enter your move (row, column) -> ");
        scanf("%d %d", &x, &y);

        currentMoveIndex++;

        // Revealing the cell and updating the game state
        if (isMine(x, y, realBoard)) {
            // Player hit a mine
            printf("Game Over!\n");
            gameOver = true;

            // Reveal all bombs
            for (int i = 0; i < SIDE; i++) {
                for (int j = 0; j < SIDE; j++) {
                    if (isMine(i, j, realBoard))
                        myBoard[i][j] = '*';
                }
            }

            // Print the final board
            printBoard(myBoard);
        } else {
            // Player didn't hit a mine
            int count = 0;
            for (int u = 0; u < 3; u++) {
                for (int uu = 0; uu < 3; uu++) {
                    int nrow = x + A[u];
                    int ncol = y + A[uu];
                    if (isValid(nrow, ncol) && isMine(nrow, ncol, realBoard))
                        count++;
                }
            }
            movesLeft--;

            myBoard[x][y] = count + '0';

            if (count == 0) {
                // If the revealed cell has no adjacent mines, recursively reveal neighboring cells
                for (int u = 0; u < 3; u++) {
                    for (int uu = 0; uu < 3; uu++) {
                        int nrow = x + A[u];
                        int ncol = y + A[uu];
                        if (isValid(nrow, ncol) && !isMine(nrow, ncol, realBoard))
                            myBoard[nrow][ncol] = countAdjacentMines(nrow, ncol, realBoard) + '0';
                    }
                }
            }

            // Check if the player has won
            if (movesLeft == 0) {
                printf("Congratulations! You won!\n");
                gameOver = true;
            }
        }
    }
}

// A Function to choose the difficulty level of the game
void chooseSize() {
    int m, mines;

    printf("Enter the size of the board (m): ");
    scanf("%d", &m);
    printf("Enter the number of mines: ");
    scanf("%d", &mines);

    SIDE = m;
    MINES = mines;

    return;
}

// Driver Program to test above functions
int main() {
    chooseSize();
    playMinesweeper();
    return 0;
}
