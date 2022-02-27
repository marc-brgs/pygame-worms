from PIL import Image, ImageDraw

class Evironment():
    def __init__(self, groundPath, backgroundPath):
        self.ground = ground = Image.open(groundPath).convert("RGBA")
        self.background = Image.open(backgroundPath).convert("RGBA")
        self.actualGround = ground.copy().convert("RGBA")
        self.background_show = Image.alpha_composite(self.background, self.actualGround).convert('RGB')
        #self.background_show.show()
        self.saveBackground()

    def updateBackgroundFusion(self, img1, img2):
        self.background_show = Image.alpha_composite(img1, img2)

    def save(self, name, img):
        img.save('assets/' + name + '.png', 'PNG')

    def saveBackground(self):
        self.background_show.save("assets/background_show.jpg")

    def destruction(self, center, size):
        draw = ImageDraw.Draw(self.actualGround)
        draw.ellipse(((center[0], center[1]), center + size, center + size), fill=(255, 255, 255, 0))
        self.save("ground-actual", self.actualGround)
        self.updateBackgroundFusion(self.background, self.actualGround)
        self.save("background_show", self.background_show)



