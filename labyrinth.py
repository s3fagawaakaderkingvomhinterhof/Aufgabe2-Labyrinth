

class Labyrinth:

    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.columns_with_borders = columns + 2
        self.rows_with_borders = rows + 2
        self.labyrinth = self.create_data_model()

    def create_data_model(self):
        labyrinth = [[-1 for column in range(0, self.columns_with_borders)] for row in range(self.rows_with_borders)]
        for i in range(1, self.columns+1):
            for j in range(1, self.rows+1):
                labyrinth[j][i] = 0
        return labyrinth

    def get_data_model(self):
        return self.labyrinth

    def clear_labyrinth(self):
        for i in range(1, self.columns_with_borders - 1):
            for j in range(1, self.rows_with_borders - 1):
                self.labyrinth[j][i] = 0

    def print_labyrinth(self):
        for i in range(0, self.rows_with_borders):
            for j in range(0, self.columns_with_borders):
                print(self.labyrinth[i][j], end='|')
            print()

    def set_wall(self, x, y):
        self.labyrinth[y][x] = -1

    def undo_wall(self, x, y):
        self.labyrinth[y][x] = 0

    def toggle_wall(self, x, y):
        if self.labyrinth[y][x] == 0:
            self.set_wall(x, y)
        elif self.labyrinth[y][x] == -1:
            self.undo_wall(x, y)

    def get_field_value(self, x, y):
        return self.labyrinth[y][x]

    def set_field_value(self, x, y, value):
        self.labyrinth[y][x] = value                     # important for agent