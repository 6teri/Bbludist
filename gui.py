import tkinter as tk
from tkinter import filedialog
from bludiste import Maze
from robot import Robot


class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bludiště")
        self.maze = Maze()
        self.robot = None

        self.cell_size = 40
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(self.root, text="Načíst bludiště", command=self.load_maze)
        self.load_button.pack()

        self.run_button = tk.Button(self.root, text="Spustit robota", command=self.run_robot, state=tk.DISABLED)
        self.run_button.pack()

        # Událost pro změnu velikosti okna
        self.canvas.bind("<Configure>", self.on_resize)

        # Událost pro kliknutí myší na canvas (výběr startovní pozice)
        self.canvas.bind("<Button-1>", self.set_start_position)

        # Inicializace startovní pozice
        self.start_position_set = False

    def load_maze(self):
        """Načte bludiště ze souboru a vykreslí jej."""
        file_path = filedialog.askopenfilename(
            title="Vyberte soubor s bludištěm",
            filetypes=[("Textové soubory", "*.txt")]
        )
        if file_path:
            self.maze.load_from_file(file_path)
            self.robot = None  # Resetování robota před novým načtením
            self.start_position_set = False  # Resetování flagu startovní pozice
            self.draw_maze()

    def draw_maze(self):
        """Vykreslí bludiště a pozici robota."""
        self.canvas.delete("all")

        if not self.maze.grid:
            return

        # Vypočítáme velikost buněk podle velikosti okna
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.cell_size = min(width // len(self.maze.grid[0]), height // len(self.maze.grid))

        for y, row in enumerate(self.maze.grid):
            for x, cell in enumerate(row):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "white"
                if cell == '0':
                    color = "black"
                elif cell == 'E':
                    color = "green"
                elif (x, y) == self.maze.start:
                    color = "blue"  # Zobrazí startovní pozici

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

        self.update_robot_position()

    def update_robot_position(self):
        """Vykreslí aktuální pozici robota."""
        if not self.robot:
            return

        self.canvas.delete("robot")
        self.canvas.create_oval(
            self.robot.x * self.cell_size + 5,
            self.robot.y * self.cell_size + 5,
            (self.robot.x + 1) * self.cell_size - 5,
            (self.robot.y + 1) * self.cell_size - 5,
            fill="red",
            tags="robot"
        )

    def run_robot(self):
        """Postupně spustí pohyb robota."""
        if not self.robot:
            print("Robot nebyl inicializován.")
            return

        def step_robot():
            if not self.robot.exit_found:
                self.robot.step()
                self.update_robot_position()
                self.root.after(300, step_robot)  # Zpoždění 300 ms mezi kroky

        step_robot()  # Spustíme pohyb robota

    def on_resize(self, event):
        """Znovu vykreslí bludiště při změně velikosti okna."""
        if self.maze.grid:
            self.draw_maze()

    def set_start_position(self, event):
        """Nastaví startovní pozici robota podle kliknutí myší."""
        if not self.maze.grid:
            return

        # Získáme pozici kliknutí
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        # Pokud je pozice v rozsahu bludiště, nastavíme startovní pozici
        if 0 <= x < len(self.maze.grid[0]) and 0 <= y < len(self.maze.grid):
            self.maze.start = (x, y)
            self.start_position_set = True
            print(f"Startovní pozice byla nastavena na: ({x}, {y})")

            # Inicializujeme robota až po nastavení startovní pozice
            self.robot = Robot(self.maze)

            # Povolení tlačítka pro spuštění robota
            self.run_button.config(state=tk.NORMAL)

            # Při změně startovní pozice překreslíme bludiště
            self.draw_maze()


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
