from pprint import pprint


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point ({self.x}, {self.y})"

    def top(self):
        return Point(self.x - 1, self.y)

    def bottom(self):
        return Point(self.x + 1, self.y)

    def left(self):
        return Point(self.x, self.y - 1)

    def right(self):
        return Point(self.x, self.y + 1)


class SupList:

    def __init__(self, lst):
        self.lst = lst   # list of lists
        self.row_nb = len(lst)
        self.col_nb = len(lst[0])

        # préparer une liste simple des non visités.
        self.unchecked = [ self.lst[x][y] for x in range(self.row_nb) for y in range(self.col_nb)]

        print(self.unchecked)


    def __get__(self, point):
        return self.lst[point.x][point.y]

    def __getitem__(self, item):
        if isinstance(item, Point):
            return self.lst[item.x][item.y]
        elif isinstance(item, int):
            return self.lst[item]
        else:
            raise KeyError("Argument must be a Point ")

    def __setitem__(self, key, value):
        if isinstance(key, Point):
            self.lst[key.x][key.y] = value
        else:
            raise KeyError("Argument must be a Point ")

    def set_as_checked(self, point):
        self.lst[point.x][point.y] = "/"


    # def __repr__(self):
    #     return self.lst


if __name__ == '__main__':
    tableau = SupList([[col for col in range(5)] for row in range(8)])
    P = Point(1, 2)

    print("Le tableau est ")
    print(tableau)
    print(tableau[P.x][P.y])

    Q = Point(2, 3)
    print("Appel par un Point")
    print(tableau[Q])
    print("Appel par un index")
    print(tableau[2])
    print("Appel par 2 index")
    print(tableau[2][3])
    print("Changer une valeur")
    tableau[Q] = "/"
    print("Vérification du stockage par appel par un Point")
    print(tableau[Q])

