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

        self.delete = False

    @abstractmethod
    def update(self, instance_list: list):
        pass

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def render(self, camera_x: float, camera_y: float):
        pass