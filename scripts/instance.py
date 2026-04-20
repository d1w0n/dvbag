from abc import ABC, abstractmethod

class Instance(ABC):

    @abstractmethod
    def __init__(self, type: str, window, x: float, y: float, width: int, height: int, room_width: int, room_height: int):
        self.type = type
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._room_width = room_width
        self._room_height = room_height
        self._distance = 0

        self.remove = False

    @abstractmethod
    def update(self, instance_list: list, camera: "Instance"):
        pass

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def render(self, camera_x: float, camera_y: float):
        pass

    def get_magnitude(self, dx, dy):
        return (dx ** 2 + dy ** 2) ** 0.5
    
    def get_collision(self, other: "Instance"):
        _distance = self.get_magnitude(self.x - other.x, self.y - other.y)
        return _distance <= self.width + other.width or _distance <= self.height + other.height
    
    def get_room_collision_x(self):
        return self.x > self._room_width / 2 or self.x < -self._room_width / 2
    
    def get_room_collision_y(self):
        return self.y > self._room_height / 2 or self.y < -self._room_height / 2