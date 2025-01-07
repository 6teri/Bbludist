import random


class Robot:
    def __init__(self, maze):
        self.maze = maze
        self.x, self.y = maze.start
        self.path = []
        self.visited = set()
        self.exit_found = False

    def move(self, x, y):
        """Posune robota na novou pozici, pokud tam není zeď."""
        if not self.maze.is_wall(x, y):
            self.x, self.y = x, y
            self.path.append((x, y))
            self.visited.add((x, y))
            print(f"Robot se přesunul na pozici: ({self.x}, {self.y})")
            return True
        else:
            print(f"Robot narazil na zeď na pozici: ({x}, {y})")
            return False

    def step(self):
        """Provede jeden krok při hledání východu."""
        if self.maze.is_exit(self.x, self.y):
            self.exit_found = True
            print(f"Robot našel východ na pozici: ({self.x}, {self.y})")
            return True

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Dolů, doprava, nahoru, doleva
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if (new_x, new_y) not in self.visited:  # Nepůjdeme tam, kde už jsme byli
                if self.move(new_x, new_y):
                    return False

        # Pokud jsou všechny směry vyzkoušené, vrátíme se na předchozí pozici
        if self.path:
            self.x, self.y = self.path.pop()
            print(f"Robot se vrací na pozici: ({self.x}, {self.y})")
        else:
            print("Robot nemůže pokračovat, není žádná cesta zpět.")
            self.exit_found = True
        return False
