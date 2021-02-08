from dataclasses import dataclass

@dataclass
class FrameInfo:
    # __slots__ = ['frameWidth' , 'frameWidthLimitR' , 'frameWidthLimitL' , 'frameHeight' , 'frameHeightLimitB' , 'frameHeightLimitT']
    frameWidth:int = 640 
    frameWidthLimitR:int = 540 #Limit for right Side
    frameWidthLimitL:int = 100 #Limit for left Side
    frameHeight:int = 480
    frameHeightLimitB:int = 450 #Limit for bottom Side
    frameHeightLimitT:int = 60 #Limit for top Side

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



@dataclass
class ObstaclePoint:
    x:int = 0
    y:int = 0
    w:int = 0
    h:int = 0
