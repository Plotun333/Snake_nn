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
                self.data[row][col] = (random.randint(0, 2000)/1000)-1

    @staticmethod
    def from_array(arr):
        m = Matrix(len(arr), 1)
        for i in range(len(arr)):
            m.data[i][0] = arr[i]
        return m

    def to_Array(self):
        arr = []
        for row in range(self.rows):
            for col in range(self.cols):
                arr.append(self.data[row][col])
        return arr

    @staticmethod
    def add(add, add2):
        if add.rows != add.rows:
            assert "Error Subtract row do not equal"
        if add.cols != add2.cols:
            assert "Error Subtract columns do not equal"

        result = Matrix(add.rows, add.cols)
        for row in range(result.rows):
            for col in range(result.cols):
                result.data[row][col] = add.data[row][col] + add2.data[row][col]

        return result

    def add_to(self, add):
        for row in range(self.rows):
            for col in range(self.cols):
                self.data[row][col] += add

    @staticmethod
    def subtract(sub, sub2):
        if sub.rows != sub2.rows:
            assert "Error Subtract row do not equal"
        if sub.cols != sub2.cols:
            assert "Error Subtract columns do not equal"

        result = Matrix(sub.rows, sub.cols)
        for row in range(result.rows):
            for col in range(result.cols):
                 result.data[row][col] = sub.data[row][col] - sub2.data[row][col]

        return result

    def subtract_to(self, sub):
        for row in range(self.rows):
            for col in range(self.cols):
                self.data[row][col] -= sub

    @staticmethod
    def multiply(m1, m2):

        if m1.cols != m2.rows:
            assert "Error matrix.cols must equal input_matrix.rows"
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

    @staticmethod
    def divide(d1, d2):

        if d1.cols != d2.rows:
            assert "Error matrix.cols must equal input_matrix.rows"
        result = Matrix(d1.rows, d2.cols)
        for row in range(result.rows):
            for col in range(result.cols):
                s = 0
                for k in range(d1.cols):
                    s += d1.data[row][k] / d2.data[k][col]
                result.data[row][col] = s
        return result

    def divide_to(self, divide):
        for row in range(self.rows):
            for col in range(self.cols):
                    self.data[row][col] /= divide

    @staticmethod
    def map(matrix, fn):
        for row in range(matrix.rows):
            for col in range(matrix.cols):
                val = matrix.data[row][col]
                matrix.data[row][col] = fn(val)
        return matrix

    @staticmethod
    def transpose(matrix):
        result = Matrix(matrix.cols, matrix.rows)
        for row in range(matrix.rows):
            for col in range(matrix.cols):
                result.data[col][row] = matrix.data[row][col]
        return result
