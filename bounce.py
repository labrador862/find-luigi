import tkinter as tk
import random
import os
import sys

# for use with creating a shareable .exe with pyinstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# initialize window, set title and icon
window = tk.Tk()
window.title("Find Luigi!")
window.iconbitmap(resource_path("myicon.ico"))

# window variables, change to whatever
windowWidth = 480
windowHeight = 480
msBetweenFrames = 10 # has an effect on perceived speed,
                     # lower is faster

# creates place for balls to bounce within the window
canvas = tk.Canvas(window, width=windowWidth, height=windowHeight)
canvas['bg'] = "black"
canvas.pack(fill=tk.BOTH, expand=1)

# dictionary to hold character data
characters = {
    "luigi": {
        "image": tk.PhotoImage(file=resource_path("luigi.png")),
        "num": 1,
    },
    "mario": {
        "image": tk.PhotoImage(file=resource_path("mario.png")),
        "num": 35,
    },
    "wario": {
        "image": tk.PhotoImage(file=resource_path("wario.png")),
        "num": 35,
    },
    "yoshi": {
        "image": tk.PhotoImage(file=resource_path("yoshi.png")),
        "num": 35
    }
}

# add image sizes to dictionary dynamically
# image width and height are 
# important for bounce mechanics
for key in characters:
    img = characters[key]["image"]
    characters[key]["width"] = img.width()
    characters[key]["height"] = img.height()

class Ball:
    def __init__(self, canvas, x, y, vspd, hspd, image, image_width, image_height):
        self.x = x          # centermost x coordinate
        self.y = y          # centermost y coordinate
        self.hspd = hspd    # horizontal speed, measured in pixels
        self.vspd = vspd    # vertical speed, measured in pixels
        self.image = image  # .png to represent a ball
        self.image_width = image_width
        self.image_height = image_height
        self.image_instance = canvas.create_image(self.x, self.y, image = self.image)
    
    # updates ball position     
    def update(self) -> None:
        self.x += self.hspd # x coordinate changes in accordance with the horizontal speed
        self.y += self.vspd # y coordinate changes in accordance with the vertical speed
        canvas.coords(self.image_instance, self.x, self.y)
        
        # if the ball hits the edge of the window,
        # reverse its horizontal or vertical direction
        if(self.x < 0 + self.image_width / 2 or self.x > windowWidth - self.image_width / 2): 
            self.hspd *= -1
        if(self.y < 0 + self.image_height / 2 or self.y > windowHeight - self.image_height / 2):
            self.vspd *= -1 
            
class Luigi(Ball):
    def __init__(self, canvas, x, y, hspd, vspd):
        luigi_image = characters["luigi"]["image"]
        luigi_width = characters["luigi"]["width"]
        luigi_height = characters["luigi"]["height"]
        super().__init__(canvas, x, y, hspd, vspd, luigi_image, luigi_width, luigi_height)
        
        # unique tag for luigi used for click detection
        canvas.itemconfig(self.image_instance, tags="luigi")            
            
class Mario(Ball):
    def __init__(self, canvas, x, y, hspd, vspd):
        mario_image = characters["mario"]["image"]
        mario_width = characters["mario"]["width"]
        mario_height = characters["mario"]["height"]
        super().__init__(canvas, x, y, hspd, vspd, mario_image, mario_width, mario_height)
        
class Wario(Ball):
    def __init__(self, canvas, x, y, hspd, vspd):
        wario_image = characters["wario"]["image"]
        wario_width = characters["wario"]["width"]
        wario_height = characters["wario"]["height"]
        super().__init__(canvas, x, y, hspd, vspd, wario_image, wario_width, wario_height)

class Yoshi(Ball):
    def __init__(self, canvas, x, y, hspd, vspd):
        yoshi_image = characters["yoshi"]["image"]
        yoshi_width = characters["yoshi"]["width"]
        yoshi_height = characters["yoshi"]["height"]
        super().__init__(canvas, x, y, hspd, vspd, yoshi_image, yoshi_width, yoshi_height)
        
# factory for creating ball objects
class BallFactory:
    def create_ball(self, canvas, character, x, y, hspd, vspd) -> Ball:
        if character == "luigi":
            return Luigi(canvas, x, y, hspd, vspd)
        elif character == "mario":
            return Mario(canvas, x, y, hspd, vspd)
        elif character == "wario":
            return Wario(canvas, x, y, hspd, vspd)
        elif character == "yoshi":
            return Yoshi(canvas, x, y, hspd, vspd)
        else:
            raise ValueError(f"Unknown character: {character}")
        
# balls lol 
balls = []

# create balls for each character
# the sign of hspd/vspd indicates direction,
# distance from 0 indicates speed
def createBalls() -> None:
    factory = BallFactory()  # instantiate the factory

    for character, data in characters.items():
        for _ in range(data["num"]):
            x = random.uniform(data["width"], windowWidth - data["width"])
            y = random.uniform(data["height"], windowHeight - data["height"])

            # get speed based on character, Luigi is
            # uniquely slow compared to the others
            if character == "luigi":
                hspd = random.uniform(-2, 2)
                vspd = random.uniform(-2, 2)
            else:
                hspd = random.uniform(-5, 5)
                vspd = random.uniform(-5, 5)

            # use factory to create balls
            ball = factory.create_ball(canvas, character, x, y, hspd, vspd)
            balls.append(ball)

# place the ball in the canvas
def draw() -> None:
    for ball in balls:
        ball.update()                    # update the balls' positions
    window.after(msBetweenFrames, draw)  # after a short delay

def on_luigi_click(event) -> None:
    clicked = canvas.find_withtag("current") # find any tagged items under the click
    if "luigi" in canvas.gettags(clicked):
        print("You found Luigi!")
        
        # display victory message (image) in the center
        youwin_image = tk.PhotoImage(file=resource_path("youwin.png"))
        canvas.image = youwin_image
        canvas.create_image(windowWidth // 2, windowHeight // 2, anchor = tk.CENTER, image = youwin_image)

canvas.tag_bind("luigi", "<Button-1>", on_luigi_click) # if the luigi tag is left clicked, call on_luigi_click()
createBalls()
window.after(msBetweenFrames, draw) # initial placement of all balls
window.mainloop()
