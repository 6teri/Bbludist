class Maze:
    def __init__(self):
        self.grid = []
        self.start = None
        self.exit = None

    def load_from_file(self, filename):
        """Načte bludiště ze souboru a identifikuje start a východ."""
        with open(filename, 'r') as file:
            self.grid = [list(line.strip()) for line in file]

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 'R':
                    self.start = (x, y)
                elif cell == 'E':
                    self.exit = (x, y)

    def is_wall(self, x, y):
        """Zjistí, zda je na dané pozici zeď."""
        return self.grid[y][x] == '0'

    def is_exit(self, x, y):
        """Zjistí, zda je na dané pozici východ."""
        return (x, y) == self.exit
