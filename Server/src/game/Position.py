class Position():
    _x: float
    _y: float
    _z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x: float) -> None:
        self._x = x


    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y: float) -> None:
        self._y = y


    @property
    def z(self) -> float:
        return self._z
        
    @z.setter
    def z(self, z: float) -> None:
        self._z = z


    def to_list(self) -> list[float]:
        return [self.x, self.y, self.z]