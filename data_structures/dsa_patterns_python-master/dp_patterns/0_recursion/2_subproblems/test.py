class Temp:
    def __init__(self):
        self.x = 23
        self._y = 45


t = Temp()
print(t.x, t._y)