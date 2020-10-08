class Interactable:
    interactableType = ''    # Valid types are: d (dot), p (powerpellet), + more for fruits
    #C(herry)=100, S(trawberry)=300, O(range)=500, A(pple)=700, M(elon)=1000, G(alaxian)=2000, B(ell)=3000, K(ey)=5000
    interactableValue = [10, 50, 100, 300, 500, 700, 1000, 2000, 5000]
    score = 0
    xPos = 0
    yPos = 0
    position = [xPos,yPos]

    def __init__(self, view, position, interactableType):
        self.view = view
        self.position = position
        self.xPos = position[0]
        self.yPos = position[1]
        self.interactableType = interactableType
        self.score = self.interactableValue[interactableType]

    def remove(self, interactList, value):    # Visually remove this thing
        interactList.pop(value)