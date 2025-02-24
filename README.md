# Chess Engine ♟️

## How it works 🛠 :

### Piece Moving Calculation ⬇️ ⬆️:

#### Pawn Moves:
* [ [1, 0], [-1, 0], [2, 0], [-2, 0], [-1, 1], [-1, -1], [1, -1], [1, -1]] 
* Pawns move forward one square unless it’s their first move, where they can move two squares. They capture diagonally one square to the left or right. En passant is handled when an adjacent pawn moves two squares forward.

#### Rook Moves:
* [ [-1, 0], [0, -1], [1, 0], [0, 1] ]
* Rooks move vertically or horizontally in straight lines until they hit a piece. They can capture enemy pieces in their path but stop moving after capturing.

#### Knight Moves:
* [ [-2, -1], [-2, 1], [-1, 2], [1, 2], [2, -1], [2, 1], [-1, -2], [1, -2] ]
* Knights move in an L-shape: two squares in one direction and then one square perpendicular to it. They are the only piece that can jump over other pieces.

#### Bishop Moves:
* [ [-1, -1], [-1, 1], [1, 1], [1, -1] ]
* Bishops move diagonally in any direction as far as possible without obstacles. They stay on the same color square throughout the game.

#### Queen Moves:
* [ [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [-1, 1], [1, 1], [1, -1] ]
* The queen combines rook and bishop movement, meaning it can move vertically, horizontally, and diagonally in any direction.

#### King Moves:
* [ [-1, 0], [0, -1], [1, 0], [0, 1] ]
* The king moves one square in any direction but cannot move into check. The code ensures the move is legal by checking for threats.

### Pins 📍 and Checks ✅:
*Explanation pending...*