# created on Python 3.5.1 :: Anaconda 4.0.0 (64-bit)
# run: python thing.py

import tkinter as tk
import math

#default
NUMBER_OF_CIRCLES=6


# max density of packings up to 72. {number_circles: max_density ceiling with sig .001}
DENSITY_DICT={1:0.786,2:0.555,3:0.654,4:0.715,5:0.732,6:0.759,7:0.769,8:0.772,9:0.785,10:0.809,11:0.82,12:0.824,13:0.828,14:0.822,15:0.832,16:0.84,17:0.844,18:0.845,19:0.847,20:0.851,21:0.849,22:0.853,23:0.852,24:0.852,25:0.854,26:0.856,27:0.856,28:0.857,29:0.86,30:0.86,31:0.859,32:0.86,33:0.859,34:0.86,35:0.861,36:0.862,37:0.861,38:0.863,39:0.861,40:0.862,41:0.861,42:0.863,43:0.863,44:0.862,45:0.864,46:0.863,47:0.86,48:0.863,49:0.859,50:0.863,51:0.864,52:0.86,53:0.862,54:0.864,55:0.863,56:0.861,57:0.863,58:0.864,59:0.865,60:0.866,61:0.867,62:0.865,63:0.868,64:0.866,65:0.866,66:0.864,67:0.871,68:0.867,69:0.866,70:0.868,71:0.868,72:0.871}


#fonts and margins
WORK_AREA_SIZE=500 #side length (px) of the square where you're putting the circles. The window size is approx this + 20 high, and 2*this wide
CIRCLE_OUTLINE_COLOR="#f6d55c"
CIRCLE_ACTIVE_COLOR="#ed553b"
CIRCLE_INACTIVE_COLOR="#3caea3"
SQUARE_COLOR="#20639b"
CANVAS_BACKGROUND_COLOR="#173f5f"
BORDER=10
CIRCLE_OUTLINE_WIDTH=2


# get the radius of the circle based on area
def get_radius(area): 
   return math.sqrt(area/math.pi)

# monkey patch Canvas to make circles
def _create_circle(self, x,y,r,**kwargs): 
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle=_create_circle


# note: manipulates global canvas
class Selector(): 
    def __init__(self): 
        self.x=-1
        self.y=-1
        self.selected=[]

    def click(self, event):
        selected_tmp=canvas.find_overlapping(event.x, event.y, event.x+1, event.y+1)
        selected_tmp2=[]
        for item in selected_tmp:
            if "circle" in canvas.gettags(item):
                if item not in selected_tmp2:
                    selected_tmp2.append(item)

        # if you're clicking nothing, unselect all
        if len(selected_tmp2)<1:
            self.x=event.x
            self.y=event.y
            self.selected=[]
            for item in canvas.find_withtag("circle"):
                    canvas.itemconfig(item, fill=CIRCLE_INACTIVE_COLOR)
        else: 
            self.x=event.x
            self.y=event.y

            top=max(selected_tmp2)
            #if the top selected item is a cirlce
            if top in canvas.find_withtag("circle"):
                # and it's not already selected
                if top not in self.selected:
                    # it becomes the only selected item
                    self.selected = [item]
                    for item in canvas.find_withtag("circle"):
                        canvas.itemconfig(item, fill=CIRCLE_INACTIVE_COLOR)
                    canvas.itemconfig(top, fill=CIRCLE_ACTIVE_COLOR)
                    self.x=event.x
                    self.y=event.y


    def unclick(self, event): 
        if self.x>0:
            overlapping=canvas.find_overlapping(self.x, self.y, event.x, event.y)
            for item in canvas.find_withtag("circle"):
                if item in overlapping:
                    canvas.itemconfig(item, fill=CIRCLE_ACTIVE_COLOR)
                    if item not in self.selected:
                        self.selected.append(item)
    
    def drag(self, event): 
        if len(self.selected)>0:
            dx=event.x-self.x
            dy=event.y-self.y
            for item in self.selected:
                canvas.move(item, dx, dy)
            self.x=event.x
            self.y=event.y



# return multiplier (p ST the area of the cirlces are 1p,2p,...,np)
def get_multiplier(number_of_circles, density, square_size): 
    sum_i=0.0
    for i in range(1,number_of_circles+1):
        sum_i+=i
    return density*(square_size**2)*(1/sum_i)


#uses constants set at the top
def draw_the_puzzle(number_of_circles):
    NUMBER_OF_CIRCLES=number_of_circles
    canvas.delete("circle")

    max_density=DENSITY_DICT.get(NUMBER_OF_CIRCLES)
    p=get_multiplier(NUMBER_OF_CIRCLES,max_density, WORK_AREA_SIZE)

    rect=canvas.create_rectangle(BORDER, BORDER, WORK_AREA_SIZE+BORDER, WORK_AREA_SIZE+BORDER, fill=SQUARE_COLOR, outline=SQUARE_COLOR)

    myx=WORK_AREA_SIZE+(2*BORDER)+(get_radius(NUMBER_OF_CIRCLES*p))
    myy=BORDER+(get_radius(NUMBER_OF_CIRCLES*p))
    circle_outline_width=2 #needs to be subtracted from the circle radius
    for i in range(NUMBER_OF_CIRCLES,0,-1):
        myr=get_radius(p*i)-(circle_outline_width/2)
        circ=canvas.create_circle(myx,myy,myr, fill=CIRCLE_INACTIVE_COLOR, outline=CIRCLE_OUTLINE_COLOR, width=circle_outline_width, tags=("circle"))




def settings_popup(): 
    win=tk.Toplevel()
    win.wm_title("Settings")

    l=tk.Label(win, text="Number of Circles")
    l.grid(row=0, column=0)

    s=tk.Scale(win, from_=1, to=72, orient="horizontal")
    s.grid(row=0, column=1)

    b=tk.Button(win, text="Apply", command=lambda:draw_the_puzzle(s.get()))
    b.grid(row=3,column=2)

    o=tk.Button(win, text="Close", command=win.destroy)
    o.grid(row=3, column=3)



if __name__=='__main__':

    # root
    window = tk.Tk()
    window.title("pack the things")


    # create the menu bars
    menubar=tk.Menu(window)
    filemenu=tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Settings", command=settings_popup)
    filemenu.add_separator()
    filemenu.add_command(label="Close", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    window.config(menu=menubar)


    #create the canvas
    canvas = tk.Canvas(window, width=2*WORK_AREA_SIZE+(2*BORDER), height=WORK_AREA_SIZE+(2*BORDER), bg=CANVAS_BACKGROUND_COLOR)
    canvas.grid()

    #draw the things
    draw_the_puzzle(NUMBER_OF_CIRCLES)

    # handle moving the circles
    selector=Selector()
    canvas.bind("<ButtonPress-1>", selector.click)
    canvas.bind("<ButtonRelease-1>", selector.unclick)
    canvas.bind("<B1-Motion>", selector.drag)

    window.mainloop()


