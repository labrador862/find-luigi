import tkinter as tk
import random
import os
import sys

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
numBalls = 100
msBetweenFrames = 15

# creates place for balls to bounce within the window
canvas = tk.Canvas(window, width=width, height=height)
canvas['bg'] = "black"
canvas.pack(fill=tk.BOTH, expand=1)

# image file (.png) to use as balls 
ball_image_path = resource_path("luigi.png")
ball_image = tk.PhotoImage(file=ball_image_path)
image_width = ball_image.width()    # gets width and height of used image
image_height = ball_image.height()  # to improve bounce mechanics

class Ball:
    def __init__(self, canvas, x, y, vspd, hspd, image):
        self.x = x          # x coordinate
        self.y = y          # y coordinate
        self.hspd = hspd    # horizontal speed
        self.vspd = vspd    # vertical speed
        self.image = image  # .png to represent a ball
        
        self.image_instance = canvas.create_image(self.x, self.y, image = ball_image)
    
    # updates ball position     
    def update(self, canvas):
        self.x += self.hspd # x coordinate changes in accordance with the horizontal speed
        self.y += self.vspd # y coordinate changes in accordance with the vertical speed
        canvas.coords(self.image_instance, self.x, self.y)
        
        # if the ball hits the edge of the window,
        # reverse its horizontal or vertical direction
        if(self.x < 0 + image_width / 2 or self.x > width - image_width / 2): 
            self.hspd *= -1
        if(self.y < 0 + image_height / 2 or self.y > height - image_height / 2):
            self.vspd *= -1 

# make space for some balls lol 
balls = []

# create specified number of balls
for i in range(0, numBalls):
    x = random.uniform(image_width, width - image_width)    # ensures ball spawns within the borders
    y = random.uniform(image_height, height - image_height) # ^^
    vspd = random.uniform(-5, 5)                            # randomly chooses initial speed and direction
    hspd = random.uniform(-5, 5)                            # ^^
    balls.append(Ball(canvas, x, y, vspd, hspd, ball_image))# adds ball to list of balls

# place the ball in the canvas
def draw():
    for ball in balls:
        ball.update(canvas)              # update the balls' positions
    window.after(msBetweenFrames, draw)  # after a short delay
    
window.after(msBetweenFrames, draw)      # initial placement of all balls
window.mainloop()
