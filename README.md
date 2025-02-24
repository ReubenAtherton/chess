# Chess Engine ♟️

## How it works 🛠 :

### Piece Moving Calculation ⬇️ ⬆️:

Each of the following piece’s movement also accounts for pins and checks, ensuring legal moves based on the curren  
board state.  

#### Pawn Moves:
Move list: [ [1, 0], [-1, 0], [2, 0], [-2, 0] ]
<br/>
Pawns move forward one square unless it’s their first move, where they can move two squares. They capture diagonally  
one square to the left or right. En passant is handled when an adjacent pawn moves two squares forward.
<br/>
#### Rook Moves:
Move list: [ [-1, 0], [0, -1], [1, 0], [0, 1] ]
Rooks move vertically or horizontally in straight lines until they hit an obstacle (a piece). They can capture enemy  
pieces in their path but stop moving after capturing.
<br/>
<br/>
#### Knight Moves:
Move list: [ [-2, -1], [-2, 1], [-1, 2], [1, 2], [2, -1], [2, 1], [-1, -2], [1, -2] ]
Knights move in an L-shape: two squares in one direction and then one square perpendicular to it. They are the only  
piece that can jump over other pieces.
<br/>
<br/>
#### Bishop Moves:
Move list: [ [-1, -1], [-1, 1], [1, 1], [1, -1] ]
Bishops move diagonally in any direction as far as possible without obstacles. They stay on the same color square  
throughout the game.
<br/>
<br/>
#### Queen Moves:
Move list: [ [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [-1, 1], [1, 1], [1, -1] ]
The queen combines rook and bishop movement, meaning it can move vertically, horizontally, and diagonally in any  
direction.
<br/>
<br/>
#### King Moves:
Move list: [ [-1, 0], [0, -1], [1, 0], [0, 1] ]
The king moves one square in any direction but cannot move into check. The code ensures the move is legal by checking  
for threats.
<br/>
<br/>
### Pins 📍 and Checks ✅:
*Explanation pending...*

