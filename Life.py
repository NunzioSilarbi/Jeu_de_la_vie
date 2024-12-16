import tkinter as tk

window_size = 600
square_size = 12

grid_matrix = [
    [0] * 48 for _ in range(48)
]

running = False
preview = False
selected_shape = None

root = tk.Tk()
root.title("Jeu de la Vie")

root.geometry(f"{window_size + 120}x{window_size}")  # Ajout d'un espace supplémentaire pour le bandeau

canvas = tk.Canvas(root, width=window_size, height=window_size)
canvas.pack(side="left")

shapes = {
    "Planeur": [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],  # Planeur
    "Canon à Planeur": [  # Canon à planeur
        (5, 1), (5, 2), (6, 1), (6, 2),
        (5, 11), (6, 11), (7, 11), (4, 12), (8, 12), (3, 13), (3, 14), (9, 13), (9, 14),
        (6, 15), (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), (6, 18),
        (3, 21), (4, 21), (5, 21), (3, 22), (4, 22), (5, 22), (2, 23), (6, 23),
        (1, 25), (2, 25), (6, 25), (7, 25),
        (3, 35), (4, 35), (3, 36), (4, 36)
    ],
    "Oie du Canada": [
            (0, 0), (1, 0), (2, 0), (2, 1), (1, 2),
            (4, 1), (5, 2), (6, 3),
            (5, 4), (4, 4), (3, 4), (2, 3)
        ]
}


def draw_grid():
    canvas.delete("all")
    for row in range(len(grid_matrix)):
        for col in range(len(grid_matrix[row])):
            color = "black" if grid_matrix[row][col] == 1 else "white"
            x1, y1 = col * square_size, row * square_size
            x2, y2 = x1 + square_size, y1 + square_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")


def place_shape(row, col):
    if selected_shape and selected_shape in shapes:
        for dr, dc in shapes[selected_shape]:
            r, c = row + dr, col + dc
            if 0 <= r < len(grid_matrix) and 0 <= c < len(grid_matrix[r]):
                grid_matrix[r][c] = 1



def on_click(event):
    global selected_shape
    col = event.x // square_size
    row = event.y // square_size

    if 0 <= row < len(grid_matrix) and 0 <= col < len(grid_matrix[row]):
        if selected_shape:
            place_shape(row, col)
            selected_shape = None
        else:
            grid_matrix[row][col] = 1 - grid_matrix[row][col]  # Basculer entre 0 et 1
    draw_grid()


canvas.bind("<Button-1>", on_click)


def get_population(col, row):
    rows = len(grid_matrix)
    cols = len(grid_matrix[0])

    voisins = [
        grid_matrix[(row + 1) % rows][col],
        grid_matrix[(row + 1) % rows][(col + 1) % cols],
        grid_matrix[row][(col + 1) % cols],
        grid_matrix[(row - 1) % rows][(col + 1) % cols],
        grid_matrix[(row - 1) % rows][col],
        grid_matrix[(row - 1) % rows][(col - 1) % cols],
        grid_matrix[row][(col - 1) % cols],
        grid_matrix[(row + 1) % rows][(col - 1) % cols]
    ]

    return voisins


def next_generation(grid):
    rows = len(grid)
    cols = len(grid[0])
    new_population = [[0 for _ in range(cols)] for _ in range(rows)]
    voisin = 0

    for i in range(rows):
        for j in range(cols):
            pop = get_population(j, i)
            for k in pop:
                if k == 1:
                    voisin += 1
            if grid[i][j] == 1:
                new_population[i][j] = 1 if voisin in [2, 3] else 0
            else:
                new_population[i][j] = 1 if voisin == 3 else 0
            voisin = 0
    return new_population


def preview_generation(grid):
    preview_grid = next_generation(grid)
    rows = len(grid)
    cols = len(grid[0])
    embouteillage = [[0 for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            if preview_grid[row][col] == 0 and grid[row][col] == 0:
                embouteillage[row][col] = 0  # Case reste vide
            elif preview_grid[row][col] == 1 and grid[row][col] == 1:
                embouteillage[row][col] = 1  # Case reste vivante
            elif preview_grid[row][col] == 0 and grid[row][col] == 1:
                embouteillage[row][col] = 2  # Cellule morte
            elif preview_grid[row][col] == 1 and grid[row][col] == 0:
                embouteillage[row][col] = 3  # Nouvelle cellule vivante

    return embouteillage


def preview_generation_grid():
    embouteillage = preview_generation(grid_matrix)
    canvas.delete("all")
    for row in range(len(embouteillage)):
        for col in range(len(embouteillage[row])):
            if embouteillage[row][col] == 0:
                color = "white"
            elif embouteillage[row][col] == 1:
                color = "blue"
            elif embouteillage[row][col] == 2:
                color = "green"
            elif embouteillage[row][col] == 3:
                color = "red"
            x1, y1 = col * square_size, row * square_size
            x2, y2 = x1 + square_size, y1 + square_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")


def update_grid():
    global grid_matrix

    if running:
        grid_matrix = next_generation(grid_matrix)  # Calculer la génération suivante
        draw_grid()  # Afficher l'état actuel

        if preview:
            preview_generation_grid()  # Afficher la prévisualisation en surcouche

        root.after(50, update_grid)  # Appeler récursivement pour la prochaine mise à jour


def start_simulation():
    global running
    if not running:
        running = True
        update_grid()  # Démarrer la simulation


def stop_simulation():
    global running
    running = False
    if preview:  # Si la prévisualisation est active, elle reste affichée
        preview_generation_grid()


def reset_grid():
    global grid_matrix
    grid_matrix = [[0] * 48 for _ in range(48)]
    draw_grid()


def preview_the_grid():
    global preview
    if not preview:
        preview = True
        update_grid()


def toggle_preview():
    global preview

    if preview:  # Désactiver la prévisualisation
        preview = False
        canvas.delete("preview")  # Supprimer le calque de prévisualisation
    else:  # Activer la prévisualisation
        preview = True
        preview_generation_grid()  # Afficher la prévisualisation


# Charger les images avec Tkinter
start_img = tk.PhotoImage(file="Vue/play.png")
start_img = start_img.subsample(16, 16)

stop_img = tk.PhotoImage(file="Vue/stop.png")
stop_img = stop_img.subsample(16, 16)

reset_img = tk.PhotoImage(file="Vue/reset.png")  # Assurez-vous d'avoir une image reset.png
reset_img = reset_img.subsample(16, 16)

preview_img = tk.PhotoImage(file="Vue/preview.png")  # Assurez-vous d'avoir une image reset.png
preview_img = preview_img.subsample(16, 16)

glider_img = tk.PhotoImage(file="Vue/glider.png")  # Assurez-vous d'avoir une image reset.png
glider_img = glider_img.subsample(16, 16)

canon_img = tk.PhotoImage(file="Vue/canon.png")  # Assurez-vous d'avoir une image reset.png
canon_img = canon_img.subsample(16, 16)

# Supprimer les largeurs fixes pour laisser Tkinter ajuster automatiquement
control_frame = tk.Frame(root, bg="gray")
control_frame.pack(side="right", fill="y")

# Ajout de deux colonnes dans control_frame
control_frame.columnconfigure(0, weight=1)  # Colonne pour les formes
control_frame.columnconfigure(1, weight=1)  # Colonne pour les actions

# Sous-cadre pour les formes (colonne 0)
shape_frame = tk.Frame(control_frame, bg="lightgray")
shape_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Sous-cadre pour les actions (colonne 1)
button_bar = tk.Frame(control_frame, bg="darkgray")
button_bar.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Boutons dans shape_frame
glider_button = tk.Button(shape_frame, image=glider_img, command=lambda: select_shape("Planeur"), borderwidth=0)
glider_button.pack(pady=10)

canon_button = tk.Button(shape_frame, image=canon_img, command=lambda: select_shape("Canon à Planeur"), borderwidth=0)
canon_button.pack(pady=10)

oie_button = tk.Button(shape_frame, text="Oie du Canada", command=lambda: select_shape("Oie du Canada"), borderwidth=0)
oie_button.pack(pady=10)


# Boutons dans button_bar
start_button = tk.Button(button_bar, image=start_img, command=start_simulation, borderwidth=0)
start_button.pack(pady=10)

stop_button = tk.Button(button_bar, image=stop_img, command=stop_simulation, bg="gray", borderwidth=0)
stop_button.pack(pady=10)

reset_button = tk.Button(button_bar, image=reset_img, command=reset_grid, bg="gray", borderwidth=0)
reset_button.pack(pady=10)

preview_button = tk.Button(button_bar, image=preview_img, command=toggle_preview, bg="gray", borderwidth=0)
preview_button.pack(pady=10)

# Optionnel : forcer l'ajustement automatique de la taille
root.update_idletasks()  # Force l'interface à calculer les dimensions
root.geometry("")  # Ajuste automatiquement la taille de la fenêtre
preview_button.pack(pady=10)


# Fonction pour sélectionner une forme
def select_shape(shape_name):
    global selected_shape
    selected_shape = shape_name
    print(f"Forme sélectionnée : {shape_name}")

# Dessiner la grille initiale
draw_grid()

root.mainloop()
