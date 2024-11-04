
class TokenConfig:
    def __init__(self, player,gridX, gridY):
        self.player = player
        self.gridX = gridX
        self.gridY = gridY
        self.posX = 80 + (gridY * 80)
        self.posY = 80 + (gridX * 80)

class Token(TokenConfig):
    def __init__(self, player, gridX, gridY, image, GAME):
        super().__init__(player, gridX, gridY)
        self.image = image
        self.GAME = GAME 
        
    def animateTransition(self, imagesTransition, imagesResult ):
        for i in range(30):
            self.image = imagesTransition[i // 10]
            self.GAME.displayWindow()
        self.image = imagesResult
    
    def displayWindow(self, window):
        window.blit(self.image, (self.posX, self.posY))        
