
from pprint import pprint

class Point:
    def __init__(self, x, y ):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point ({self.x}, {self.y})"

    def top(self):
        return Point(self.x-1, self.y)

    def bottom(self):
        return Point(self.x + 1, self.y)

    def left(self):
        return Point(self.x, self.y-1)

    def right(self):
        return Point(self.x, self.y+1)

class SupList():

    def __init__(self, lst):
        self.lst = lst

    def __get__(self, point):
        return self.lst[point.x][point.y]

    def __getitem__(self, item):
        if isinstance(item, Point):
            return self.lst[item.x][item.y]
        else :
            raise KeyError ("Argument must be a Point ")
if __name__ == '__main__':
    pass
    # tableau = [[ col for col in range(5)] for  row in range(8)]
    tableau = SupList([[ col for col in range(5)] for  row in range(8)])
    P = Point(1,2)

    print("Le tableau est ")
    pprint(tableau)
    # print(tableau[P.x][P.y])

    Q = Point(2,3)
    print(tableau["f"])
    # Je voudrais pouvoir écrire : tableau[P]
