import interactableClass
import movementClass

class Ghost(Interactable, Movement):
    personality = ""    # Valid personalities are: Inky, Blinky, Pinky, Clyde
    state = ""          # Valid States are: inactive, active, flee, dead, alternate

    def __init__(self, personality, state):
        self.personality = personality
        self.state = state