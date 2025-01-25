import tkinter as tk
import random
import os
import sys

# for use with creating a sharable .exe with pyinstaller
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

# size variables, change to whatever
width = 480
height = 480
numLuigi = 1
numMario = 50
numWario = 35
numYoshi = 25
msBetweenFrames = 10 # has an effect on speed

# creates place for balls to bounce within the window
canvas = tk.Canvas(window, width=width, height=height)
canvas['bg'] = "black"
canvas.pack(fill=tk.BOTH, expand=1)

# create dictionary to hold image data
images = {
    "mario": {
        "image": tk.PhotoImage(file=resource_path("mario.png")),
    },
    "luigi": {
        "image": tk.PhotoImage(file=resource_path("luigi.png")),
    },
    "wario": {
        "image": tk.PhotoImage(file=resource_path("wario.png")),
    },
    "yoshi": {
        "image": tk.PhotoImage(file=resource_path("yoshi.png")),
    }
}

# add image sizes to dictionary
# image width and height are 
# important for bounce mechanics
for key in images:
    img = images[key]["image"]
    images[key]["width"] = img.width()
    images[key]["height"] = img.height()

class Ball:
    def __init__(self, canvas, x, y, vspd, hspd, image, image_width, image_height):
        self.x = x          # x coordinate
        self.y = y          # y coordinate
        self.hspd = hspd    # horizontal speed
        self.vspd = vspd    # vertical speed
        self.image = image  # .png to represent a ball
        self.image_width = image_width    # width of specific .png
        self.image_height = image_height  # height of specific .png
        self.image_instance = canvas.create_image(self.x, self.y, image = self.image)
    
    # updates ball position     
    def update(self):
        self.x += self.hspd # x coordinate changes in accordance with the horizontal speed
        self.y += self.vspd # y coordinate changes in accordance with the vertical speed
        canvas.coords(self.image_instance, self.x, self.y)
        
        # if the ball hits the edge of the window,
        # reverse its horizontal or vertical direction
        if(self.x < 0 + self.image_width / 2 or self.x > width - self.image_width / 2): 
            self.hspd *= -1
        if(self.y < 0 + self.image_height / 2 or self.y > height - self.image_height / 2):
            self.vspd *= -1 
            
class Mario(Ball):
    def __init__(self, canvas, x, y, hspd, vspd):
        mario_image = images["mario"]["image"]
        mario_width = images["mario"]["width"]
        mario_height = images["mario"]["height"]
        super().__init__(canvas, x, y, hspd, vspd, mario_image, mario_width, mario_height)

class Luigi(Ball):
    def __init__(self, canvas, x, y, hspd, vspd):
        luigi_image = images["luigi"]["image"]
        luigi_width = images["luigi"]["width"]
        luigi_height = images["luigi"]["height"]
        super().__init__(canvas, x, y, hspd, vspd, luigi_image, luigi_width, luigi_height)
        
        # unique tag for luigi used for click detection
        canvas.itemconfig(self.image_instance, tags="luigi")
        
class Wario(Ball):
    def __init__(self, canvas, x, y, hspd, vspd):
        wario_image = images["wario"]["image"]
        wario_width = images["wario"]["width"]
        wario_height = images["wario"]["height"]
        super().__init__(canvas, x, y, hspd, vspd, wario_image, wario_width, wario_height)

class Yoshi(Ball):
    def __init__(self, canvas, x, y, hspd, vspd):
        yoshi_image = images["yoshi"]["image"]
        yoshi_width = images["yoshi"]["width"]
        yoshi_height = images["yoshi"]["height"]
        super().__init__(canvas, x, y, hspd, vspd, yoshi_image, yoshi_width, yoshi_height)
        
# balls lol 
balls = []

# create balls for each character
# the sign of hspd/vspd indicates direction,
# distance from 0 indicates speed
def createBalls():
    # create Luigi(s) first, so he is on the bottom "layer" and harder to spot
    for _ in range(numLuigi):
        x = random.uniform(images["luigi"]["width"], width - images["luigi"]["width"])
        y = random.uniform(images["luigi"]["height"], height - images["luigi"]["height"])
        hspd = random.uniform(-2, 2)
        vspd = random.uniform(-2, 2)
        balls.append(Luigi(canvas, x, y, hspd, vspd))
        
    # create Marios
    for _ in range(numMario):
        x = random.uniform(images["mario"]["width"], width - images["mario"]["width"])
        y = random.uniform(images["mario"]["height"], height - images["mario"]["height"])
        hspd = random.uniform(-5, 5)
        vspd = random.uniform(-5, 5)
        balls.append(Mario(canvas, x, y, hspd, vspd))
    
    # create Warios
    for _ in range(numWario):
        x = random.uniform(images["wario"]["width"], width - images["wario"]["width"])
        y = random.uniform(images["wario"]["height"], height - images["wario"]["height"])
        hspd = random.uniform(-5, 5)
        vspd = random.uniform(-5, 5)
        balls.append(Wario(canvas, x, y, hspd, vspd))
        
    # create Yoshis
    for _ in range(numYoshi):
        x = random.uniform(images["yoshi"]["width"], width - images["yoshi"]["width"])
        y = random.uniform(images["yoshi"]["height"], height - images["yoshi"]["height"])
        hspd = random.uniform(-5, 5)
        vspd = random.uniform(-5, 5)
        balls.append(Yoshi(canvas, x, y, hspd, vspd))
    

# place the ball in the canvas
def draw():
    for ball in balls:
        ball.update()                    # update the balls' positions
    window.after(msBetweenFrames, draw)  # after a short delay

def on_luigi_click(event):
    clicked = canvas.find_withtag("current") # find any tagged items under the click
    if "luigi" in canvas.gettags(clicked):
        print("You found Luigi!")
        
        # display victory message (image)
        youwin_image = tk.PhotoImage(file=resource_path("youwin.png"))
        canvas.image = youwin_image
        canvas.create_image(width // 2, height // 2, anchor = tk.CENTER, image = youwin_image)

canvas.tag_bind("luigi", "<Button-1>", on_luigi_click) # if the luigi tag is left clicked, call on_luigi_click()
createBalls()
window.after(msBetweenFrames, draw)      # initial placement of all balls
window.mainloop()
