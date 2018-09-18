class Transition(object):
    def __init__(self, rows, columns):
        self.height = rows
        self.width = columns
        self.table = self.setUpEmptyMatrix(rows, columns)

    def __str__(self):
        transitions = "Transitions:\n{0}\n".format(self.table)
        return transitions

    def setUpEmptyMatrix(self, height, width):
        data = [None] * height
        for i in range(height):
            data[i] = [None] * width
        return data

    def setTransition(self, row, colum, value):
        self.table[row][colum] = value

    def shape(self):
        return (self.height, self.width)

    def __getitem__(self, key):
        return self.table[key]
