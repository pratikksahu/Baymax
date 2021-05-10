from dataclasses import dataclass

@dataclass
class FacePoint:
    x:int = 0   #X coordinate
    y:int = 0  #Y coordinate
    w:int = 0  #Width of rectangle
    h:int = 0  #Height of rectangle
    cx:int = 0  #Center x point of face
    cy:int = 0  #Center y point of face

    def __eq__(self, o: object) -> bool:
        if (isinstance(o,FacePoint)):
            return self.x == o.x and self.y == o.y and self.w == o.w and self.h == o.h and self.cx == o.cx and self.cy == o.cy
        return False
