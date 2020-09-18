class Interactable:
    interactableType = ""    # Valid types are: dot, fruit, powerpellet, ghost
    
    def __init__(self,interactableType):
        self.interactableType = interactableType

    def collision():
        if self.interactableType == "dot":
            self.remove()
            return (10)
        elif self.interactableType == "fruit":
            self.remove()
            return (50)
        elif self.interactableType == "powerpellet":
            self.remove()
            return ("stateswap")
        elif self.interactableType == "ghost":
            return ("dedm8")
        else:
            return ("error")





