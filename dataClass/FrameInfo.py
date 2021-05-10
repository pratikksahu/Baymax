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
    frameCX:int = 320
    frameCY:int = 240