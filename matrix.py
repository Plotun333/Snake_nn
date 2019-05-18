import random


class Matrix(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []

        for index in range(self.rows):
            self.data.append([])
            for _ in range(self.cols):
                self.data[index].append([])

    def print(self):
        for element in self.data:
            print(element)

    def randomize(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.data[row][col] = (random.randint(0, 2000)/2000)-1

    @staticmethod
    def from_array(arr):
        m = Matrix(len(arr), 1)
        for i in range(len(arr)):
            m.data[i][0] = arr[i]
        m.print()
        return m

    @staticmethod
    def add(add, add2):

        for row in range(add.rows):
            for col in range(add.cols):
                add.data[row][col] += add2.data[row][col]
        return add

    def add_to(self, add):
        for row in range(self.rows):
            for col in range(self.cols):
                self.data[row][col] += add

    @staticmethod
    def multiply(m1, m2):

        if m1.cols != m2.rows:
            print("Error matrix.cols must equal input_matrix.rows")
            return None
        result = Matrix(m1.rows, m2.cols)
        for row in range(result.rows):
            for col in range(result.cols):
                s = 0
                for k in range(m1.cols):
                    s += m1.data[row][k] * m2.data[k][col]
                result.data[row][col] = s
        return result

    def multiply_to(self, multiply):
        for row in range(self.rows):
            for col in range(self.cols):
                    self.data[row][col] *= multiply

    def map(self, fn):
        for row in range(self.rows):
            for col in range(self.cols):
                val = self.data[row][col]
                self.data[row][col] = fn(val)

    def transpose(self):
        result = Matrix(self.cols, self.rows)
        for row in range(self.rows):
            for col in range(self.cols):
                result.data[col][row] = self.data[row][col]
        return result


m = Matrix.from_array([1, 1])
m.print()