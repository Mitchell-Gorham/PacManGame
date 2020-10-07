class Interactable:
    interactableType = ''    # Valid types are: d (dot), f (fruit), p (powerpellet), g (ghost)
    xPos = 0
    yPos = 0
    location = [xPos,yPos]

    def __init__(self,interactableType):
        self.interactableType = interactableType
    
    def remove(self):    # Visually remove this thing
        pass