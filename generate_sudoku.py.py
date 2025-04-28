from flask import Flask, jsonify
import random

app = Flask(__name__)

# Lettres hébraïques de base
hebrew_letters_4x4 = ['א', 'ב', 'ג', 'ד']  # 4 lettres distinctes pour une grille 4x4
hebrew_letters_6x6 = ['א', 'ב', 'ג', 'ד', 'ה', 'ו']  # 6 lettres distinctes pour une grille 6x6
hebrew_letters_9x9 = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט']  # 9 lettres distinctes pour une grille 9x9

# Fonction pour vérifier si une grille est valide
def is_valid(board, r, c, letter):
    # Vérifier la ligne
    if letter in board[r]:
        return False
    # Vérifier la colonne
    for row in board:
        if row[c] == letter:
            return False
    # Vérifier la sous-grille (on suppose des sous-grilles carrées)
    grid_size = int(len(board)**0.5)  # Taille de la sous-grille (2 pour 4x4, 3 pour 9x9, etc.)
    start_row, start_col = (r // grid_size) * grid_size, (c // grid_size) * grid_size
    for i in range(start_row, start_row + grid_size):
        for j in range(start_col, start_col + grid_size):
            if board[i][j] == letter:
                return False
    return True

# Fonction pour générer une grille valide de Sudoku
def generate_sudoku(size):
    if size == 4:
        letters = hebrew_letters_4x4
    elif size == 6:
        letters = hebrew_letters_6x6
    elif size == 9:
        letters = hebrew_letters_9x9
    else:
        raise ValueError("La taille de la grille n'est pas supportée (choisir 4, 6, ou 9).")

    board = [[None] * size for _ in range(size)]  # Grille vide

    # Essayer de remplir la grille avec des lettres valides
    def solve(r, c):
        if r == size:
            return True  # Si on a rempli toutes les lignes, la grille est valide
        if c == size:
            return solve(r + 1, 0)  # Passer à la ligne suivante
        if board[r][c] is not None:
            return solve(r, c + 1)  # Si la case est déjà remplie, on passe à la suivante

        random.shuffle(letters)  # Mélanger les lettres pour essayer au hasard
        for letter in letters:
            if is_valid(board, r, c, letter):
                board[r][c] = letter
                if solve(r, c + 1):  # Si on trouve une solution valide
                    return True
                board[r][c] = None  # Sinon, on revient en arrière
        return False  # Si aucune lettre ne convient, revenir en arrière

    solve(0, 0)
    return board

@app.route('/generate_sudoku/<int:size>', methods=['GET'])
def generate_sudoku_api(size):
    try:
        board = generate_sudoku(size)
        return jsonify(board)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
