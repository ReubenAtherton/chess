# Chess Engine ♟️

## How it works 🛠 :

### Piece Moving Calculation ⬇️ ⬆️:

Each of the following piece’s movement also accounts for pins and checks, ensuring legal moves based on the current
board state.  

#### Pawn Moves:
* [ [1, 0], [-1, 0], [2, 0], [-2, 0] ]
<br/>
* Pawns move forward one square unless it’s their first move, where they can move two squares. They capture diagonally one square to the left or right. En passant is handled when an adjacent pawn moves two squares forward.
<br/>
#### Rook Moves:
[ [-1, 0], [0, -1], [1, 0], [0, 1] ]
<br/>
Rooks move vertically or horizontally in straight lines until they hit a piece. They can capture enemy pieces in their path but stop moving after capturing.
<br/>
#### Knight Moves:
[ [-2, -1], [-2, 1], [-1, 2], [1, 2], [2, -1], [2, 1], [-1, -2], [1, -2] ]
<br/>
Knights move in an L-shape: two squares in one direction and then one square perpendicular to it. They are the only piece that can jump over other pieces.
<br/>
#### Bishop Moves:
[ [-1, -1], [-1, 1], [1, 1], [1, -1] ]
<br/>
Bishops move diagonally in any direction as far as possible without obstacles. They stay on the same color square throughout the game.
<br/>
#### Queen Moves:
[ [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [-1, 1], [1, 1], [1, -1] ]
<br/>
The queen combines rook and bishop movement, meaning it can move vertically, horizontally, and diagonally in any direction.
<br/>
#### King Moves:
[ [-1, 0], [0, -1], [1, 0], [0, 1] ]
<br/>
The king moves one square in any direction but cannot move into check. The code ensures the move is legal by checking for threats.
<br/>
### Pins 📍 and Checks ✅:
*Explanation pending...*

