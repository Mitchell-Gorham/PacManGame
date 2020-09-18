import interactableClass
import movementClass

class Ghost(Interactable, Movement):
    personality = ""    # Valid personalities are the integers: 0 (Inky), 1 (Blinky), 2 (Pinky), 3 (Clyde)
    state = ""          # Valid States are: inactive, active, flee, dead, alternate

    def __init__(self, personality, state):
        self.personality = personality
        self.state = state