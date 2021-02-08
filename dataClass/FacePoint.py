from dataclasses import dataclass

@dataclass
class FacePoint:
    x:int = 0   #X coordinate
    y:int = 0  #Y coordinate
    w:int = 0  #Width of rectangle
    h:int = 0  #Height of rectangle

    def __eq__(self, o: object) -> bool:
        if self.x == o.x & self.y == o.y & self.w == o.w & self.h == o.h :
            return True
        else :
            return False