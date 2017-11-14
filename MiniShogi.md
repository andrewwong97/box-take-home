# MiniShogi Specification

## Links

### Utility Functions

We are providing some utility functions in each language (Python, Java, or Javascript). You should use these functions to do some of the tedious input and output so that you don't need to implement it yourself. The utility methods can be modified to suit your needs. They are also optional; not required to be used.
https://cloud.box.com/v/minishogiutilities 

### Tests

We have created a collection of test cases that you can run against your solution to determine if it is correct. You should run your solution on each of the .in files and compare the output to the corresponding .out file — if they do not match your solution has a bug.
https://cloud.box.com/v/minishogitests

Note, the test cases aren't exactly completely exhaustive — there are too many variations on illegal moves and such for creating a totally exhaustive set to be feasible — but for the purposes of evaluating your solution you don't need to consider anything not covered by the provided test cases.

## Game Rules

### Objective

The game has two players, **lower** and **UPPER**. The lower player always moves first.
Each player aims to capture their opponent's king.

The lower player starts on the bottom side of the board, and their pieces are represented
by lower-case characters.  The UPPER player starts on the top side of the board, and their
pieces are represented by upper-case pieces.

### The Pieces

A **king** (k/K) moves one square in any direction:
![king](https://cloud.box.com/shared/static/c4t4jv8rx0rdpghmqh79ll5p73aqp0qh.png)

A **rook** (r/R) moves any number of squares along rows or columns (orthogonal directions):
![rook](https://cloud.box.com/shared/static/0i2nnwxq33de2pilxcccn03uyw0diop4.png)

A **bishop (b/B)** moves any number of squares along diagonal directions:
![bishop](https://cloud.box.com/shared/static/8os7qcj460m7xlemuza79x73qj5kswcp.png)

A **gold general (g/G)** moves one square in any direction except its backward diagonals:
![gold general](https://cloud.box.com/shared/static/hsgw8dzhjoomg02iztkpmiazihh25nzz.png)

A **silver general (s/S)** moves one square in any direction except sideways or directly backward:
![silver general](https://cloud.box.com/shared/static/o3so3mxenqrxfgu10de0548jncah3eei.png)

A **pawn (p/P)** moves one space forward:
![pawn](https://cloud.box.com/shared/static/e5yy8btndh8vu6qm988sra52corqhudi.png)

Note, a rook or bishop cannot jump over pieces in its path of movement.

### The Board

The board is a grid of 5 rows by 5 columns. This is the starting board state:
```
5 | R| B| S| G| K|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | p|__|__|__|__|
1 | k| g| s| b| r|
    a  b  c  d  e
```

### Capturing

A player can capture an opponent’s piece by moving their piece onto the same square as an opponent's piece. The captured piece leaves the board, and can be later dropped onto the board by the player who captured it. A player cannot capture their own pieces (this is an illegal move).


### Promotion

A piece may (but usually does not have to) be **promoted** when it moves into, within, or out of the
**promotion zone**. The promotion zone is the row of the board furthest from each player's starting
position.
* For the lower player, the promotion zone is the top row of the board.
* For the UPPER player, the promotion zone is the bottom row of the board.
* A piece that has been promoted should gain a plus symbol "+" before its letter showing on the board.
* Pawns **must** be promoted once they reach the furthest row (otherwise they would not have any legal moves on the next turn).
    * If a pawn is moved into the last row, it should be promoted automatically.

Pieces promote as follows:
* A **king** cannot be promoted.
* A **gold general** cannot be promoted.
* A **promoted silver general** (+s/+S) moves the same way as a **gold general**.
* A **promoted bishop** (+b/+B) can move like a **bishop** or a **king**.
* A **promoted rook** (+r/+R) can move like a **rook** or a **king**.
* A **promoted pawn** (+p/+P) moves like a **gold general**.


### Drops

Pieces that a player has captured can be dropped back onto the board under the capturing player's control.
Dropping a piece takes your entire turn. Rules:
* You cannot drop a piece onto a square that contains another piece.
* All dropped pieces must start unpromoted (even if they have been captured as promoted pieces and/or are dropped into the promotion zone).
* A pawn may not be dropped into the promotion zone or onto a square that results in an immediate checkmate.
    * Note, other pieces can be dropped into the promotion zone or onto a square that results in an immediate checkmate.
* Two unpromoted pawns may not lie in the same column when they belong to the same player (e.g. If you already have a pawn in the third column, you cannot drop another pawn into that column).

### Game End

#### Move Limit

For simplicity, the game ends in a tie once each player has made 200 moves.  When a game ends in a tie, output the
message "Tie game.  Too many moves." instead of the move prompt.

#### Checkmate

When a player is in a position where their king could be captured on their opponent's next move, they are in **check**.
That player **must** make a move to do one of the following:
* remove their king from danger
* capture the piece that threatens their king
* put another piece between the king and the piece that threatens it to avoid capture

If a player has no moves that they could make to avoid capture, they are in **checkmate** and lose the game.

When a player wins via checkmate, output the message "<UPPER/lower> player wins.  Checkmate." instead of the move
prompt.

#### Illegal Moves

If a player makes a move that is not legal, the game ends immediately and the other player wins.  When a player
loses via an illegal move, output the message "<UPPER/lower> player wins.  Illegal move." instead of the move prompt.

### Reference Reading

* https://en.wikipedia.org/wiki/Shogi#Rules
* https://en.wikipedia.org/wiki/Minishogi

## Game Interface

Your program should accept command line flags to determine which mode to play in:
```
$ myShogi -i
```
In **interactive mode**, two players enter keyboard commands to play moves against each other.

```
$ myShogi -f <filePath>
```
In **file mode**, the specified file is read to determine the game state and which moves to make.

### Interactive Mode

#### Output

At the beginning of each turn, your program should output the following:
1. The current board state, using the utility function provided to generate the text representation of the board
2. An empty line
3. The space-separated list of pieces captured by **UPPER** (in the order that they were captured)
4. The space-separated list of pieces captured by **lower** (in the order that they were captured)
5. An empty line
6. An input prompt for the next player to enter their move, followed by a space

For example, this is how a game would begin:
```
$ myShogi -i
5 | R| B| S| G| K|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | p|__|__|__|__|
1 | k| g| s| b| r|
    a  b  c  d  e

Captures UPPER: 
Captures lower: 

lower> 
```

**NOTE:** You should use the provided utility function `stringifyBoard()` to get the string
representation of the board state.

#### Move Format

The **lower** player would then enter a move using the following formats:

**move <from> <to> [promote]**
To move a piece, enter `move` followed by the location of the piece to be moved, the location to move to,
and (optionally) the word `promote` if the piece should be promoted at the end of the turn.
* `move a2 a3` moves the piece at square a2 to square a3.
* `move a4 a5 promote` moves the piece at square a4 to square a5 and promotes it at the end of the turn.

**drop <piece> <to>**
To drop a piece, enter `drop` followed by the lowercase character representing the piece to drop and
the location to drop the piece.  Pieces are always lower-case, no matter which player is performing
the drop.
* `drop g c3` drops a captured **gold general** at square c3.
* `drop b a1` drops a captured **bishop** at square a1.

Once a player enters their move, your program should display the move made, update the game state, and
go to the next turn. For example:
```
lower> move b1 b2
lower player action: move b1 b2
5 | R| B| S| G| K|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | p| g|__|__|__|
1 | k|__| s| b| r|
    a  b  c  d  e

Captures UPPER: 
Captures lower: 

UPPER> move a5 a2
UPPER player action: move a5 a2
5 |__| B| S| G| K|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | R| g|__|__|__|
1 | k|__| s| b| r|
    a  b  c  d  e

Captures UPPER: P
Captures lower: 

lower> 
```

#### Check Detection

Before a player's turn, you should also determine if they are in check. If so, output a line stating
that they are in check, and output all available moves for them to get out of check (one move per line):
```
5 |__|__|__| K|__|
4 |__|__|__|__|__|
3 |__|__|__|__|__|
2 |__| G|__|__|__|
1 | k|__|__|__|__|
    a  b  c  d  e

Captures UPPER: R B G S P
Captures lower: b p s r

lower player is in check!
Available moves:
move a1 b2
lower> 
```
If your moves out of check are a different ordering than the test case output, alphabetizing the moves should result in the same ordering as expected test output.

If a player is in check and performs an action which is not one of the outputted available moves out of check, we consider it an illegal move. Also, moving oneself into check is considered an illegal move.


#### Game End

When the game ends, output which player won and the reason they won. Examples:
* UPPER player wins. Checkmate.
* lower player wins. Illegal move.
* Tie game. Too many moves.

### File Mode

**File mode** is very similar to **interactive mode** except the input can be a partial game. The file will
contain each piece's current position, an array of pieces captured by UPPER, an array of pieces captured
by lower, and moves to make with one move per line. Your program should output the board state after
the list of moves have been made, or immediately if one player wins in the middle of the input.

You should use file mode to run the provided test cases; use the .in files as the inputs to file mode
and then compare the output to the corresponding .out file.  For example, using the `diff` tool on
a Python solution:

```
$ python mini_shogi.py -f ~/tests/initialMove.in | diff -u ~/tests/initialMove.out -
```

For example, this file begins in the middle of a game and does not complete the game:
```
k a1
g b1
s c1
b d1
r e1
p a2
K e5
G d5
S c5
B b5
R a5
P e4

[]
[]

move a2 a3
move e4 e3
```

**NOTE:** You should use the provided utility function `parseTestCase()` to read in the
test case.  This function will read in the file for you and produce an object with the relevant
information.

The expected output is the same output as **interactive mode** after the last move is made:
```
UPPER player action: move e4 e3
5 | R| B| S| G| K|
4 |__|__|__|__|__|
3 | p|__|__|__| P|
2 |__|__|__|__|__|
1 | k| g| s| b| r|
    a  b  c  d  e

Captures UPPER: 
Captures lower: 

lower> 
```

In the following example, the game ends after the third move and your program does not need to read the last move.

Input:
```
k a1
K e5

[]
[]

move a1 a2
move e5 e4
move a2 e4
move e4 e5
```

Expected output:
```
lower player action: move a2 e4
5 |__|__|__|__|__|
4 |__|__|__|__| K|
3 |__|__|__|__|__|
2 | k|__|__|__|__|
1 |__|__|__|__|__|
    a  b  c  d  e

Captures UPPER: 
Captures lower: 

UPPER player wins. Illegal move.
```
