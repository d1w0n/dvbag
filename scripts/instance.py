from abc import ABC, abstractmethod

class Instance(ABC):

    @abstractmethod
    def __init__(self, type: str, window, x: float, y: float, width: int, height: int):
        self.type = type
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._distance = 0

        self.remove = False

    @abstractmethod
    def update(self, instance_list: list, room: "Instance", camera: "Instance"):
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
        return self.x + self.width > self._room_width / 2 or self.x - self.width < -self._room_width / 2
    
    def get_room_collision_y(self):
        return self.y + self.width > self._room_height / 2 or self.y - self.width < -self._room_height / 2