import os
import numpy as np
import pygame as pg
import threading
import math
from solution import Backtrack
from matrix import matrix

pg.init()
IMG = pg.transform.smoothscale(pg.image.load(os.path.join("icons", "undo_64.png")), (35,35))
Font = pg.font.SysFont("impact", 45)
Font_2 = pg.font.SysFont("arial", 25)


threads = []
grid = np.copy(matrix)
sub_grid = {"a" : (0,1,2),"b" : (3,4,5),"c" : (6,7,8)}
data = []



class Grid:
    def __init__(self, n):
        self.n = n
        self.cell_length = round(600/n)

    def draw(self, WIN):
        for i in range(self.n):
            if i not in [2,5,8]:
                pg.draw.line(WIN, (178,34,34), (0, round((600/self.n)*(i+1))), (600, round((600/self.n)*(i+1))), 1)
                pg.draw.line(WIN, (178,34,34), (round((600/self.n)*(i+1)), 0), (round((600/self.n)*(i+1)), 600), 1)
            else:
                pg.draw.line(WIN, (220,140,0), (0, round((600/self.n)*(i+1))), (600, round((600/self.n)*(i+1))), 3)
                pg.draw.line(WIN, (220,140,0), (round((600/self.n)*(i+1)), 0), (round((600/self.n)*(i+1)), 600), 3)


    def set(self, WIN, grid):
        for i in range(9):
            for j in range(9):
                num = grid[i,j]
                if num!=0:
                    text = Font.render(f'{num}',True, (0, 255, 255))
                    WIN.blit(text, (round((j+0.5)*(600/self.n))-10,round((i+0.5)*(600/self.n))-28) )
                    

    def selection_grid(self):
        m_x, m_y = pg.mouse.get_pos()
        for i in range(9):
            for j in range(9):
                centre_x, centre_y = round((j+0.5)*(600/self.n)), round((i+0.5)*(600/self.n))
                if abs(m_x - centre_x) in range(0, round((600/self.n)*0.5)) and abs(m_y - centre_y) in range(0, round((600/self.n)*0.5)):
                    return centre_x, centre_y, i, j
        


    def draw_selection_grid(self, WIN):
        try:
            centre_x, centre_y, i, j = self.selection_grid()
            x, y = centre_x - self.cell_length/2, centre_y - self.cell_length/2
            pg.draw.rect(WIN, (0,255,0), (x, y, self.cell_length, self.cell_length), 1)
        
        except TypeError:
            pass

class Image:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.img = image
        self.mask = self.create_mask()

    def create_mask(self):
        return pg.mask.from_surface(self.img)

    def show(self, WIN):
        if self.selection() == 1:
            WIN.blit(pg.transform.smoothscale(self.img, (44,44)), (self.x, self.y))
        else:
            WIN.blit(self.img, (self.x, self.y))
    
    def selection(self):
        pos_x, pos_y = pg.mouse.get_pos()
        try:
            mask_val = self.mask.get_at((pos_x-self.x, pos_y-self.y))
        except IndexError:
            return 0
        return mask_val




class Button:
    def __init__(self, x, y, l, b, color, text):
        self.length = l
        self.breadth  = b
        self.color = color
        self.x = x
        self.y = y
        self.text = text
        self.state = "Inactive"

    def draw(self, WIN):
        pos_x, pos_y = pg.mouse.get_pos()
        if pos_x in range(self.x, self.x+self.length) and pos_y in range(self.y, self.y+self.breadth):
            pg.draw.rect(WIN, self.color, (self.x, self.y, self.length, self.breadth), 0)
            self.state = "Active"
        else:
            pg.draw.rect(WIN, self.color, (self.x, self.y, self.length, self.breadth), 2)
            self.state = "Inactive"
        text = Font.render(self.text, True, (255,255,255))
        WIN.blit(text, (self.x + (self.length-text.get_width())/2, self.y + (self.breadth - text.get_height())/2)) 



class Warnings:
    def __init__(self, text, x, y):
        self.txt = text
        self.x = x
        self.y = y
        self.state = "Inactive"

    def show(self, WIN):
        if self.state == "Active":
            text = Font_2.render(self.txt, True, (210, 0, 0))
            WIN.blit(text, (self.x, self.y))



def check(grid, num, x, y):

    global sub_grid
    key_x = ""
    key_y = ""

    try:
        if grid[x,y] == 0:

            for i in range(9):
                if grid[x,i] == num:
                    return False
                if grid[i,y] == num:
                    return False
            for key in sub_grid:
                selected_set = sub_grid[key]
                if x in selected_set:
                    key_x = key
                if y in selected_set:
                    key_y = key

            for i in sub_grid[key_x]:
                for j in sub_grid[key_y]:
                    if grid[i,j] == num:
                        return False
            return True
        else:
            return False

    except IndexError :
        print("sorry error reported")
        return False







def gameplay(grids, warning1):

    #function takes an input from keyboard 
    #assign the new value to grid after calling check()

    global data
    try:
        _, _, cell_x, cell_y,  = grids.selection_grid()
    except TypeError:
        return False

    warning1.state = "Inactive"
    get_input = True

    while get_input:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6 ,pg.K_7 ,pg.K_8 ,pg.K_9]:
                    num=int(chr(event.key))
                    if check(grid, num, cell_x, cell_y):
                        grid[cell_x, cell_y] = num
                        data.append([num, cell_x, cell_y])
                        
                    else:
                        warning1.state = "Active"
                    return True    
                        
                else:
                    return False

def undo(image, grid):
    global data
    if image.selection():
        try:
            undo_num, undo_x, undo_y = data[-1]
        except IndexError:
            return 
        grid[undo_x, undo_y] = 0
        data.pop(-1)
        return True
    return   



 
def solve():

    #solves the sudoku using backtracking algo

    if Backtrack(grid, check):
        print(grid)
    else:
        print("solution not possible")        



def solve_button():

    # assign the thread for backtracking

    global threads
    threads.append(threading.Thread(target=solve, daemon=True))
    threads[-1].start()


def display_all(WIN, grids, button1, button2, warning1, image):

     grids.draw(WIN)
     grids.set(WIN, grid)
     grids.draw_selection_grid(WIN)
     button1.draw(WIN)
     warning1.show(WIN)
     button2.draw(WIN)
     image.show(WIN)




def main():


    display = (600,700)
    WIN = pg.display.set_mode(display)
    pg.display.set_caption("SUDOKU")

    global grid
    play = True
    grids = Grid(9)
    button1 = Button(10, 610, 150, 80, (0,0,255), "solve")
    button2 = Button(440, 610, 150, 80, (180, 40, 40), "Reset")
    warning1 = Warnings("Not possible!!!", 250, 630)
    image = Image(180, 634, IMG)
    gameover = False

    #game loop
    while play:
        
        WIN.fill((0,0,0))

        for event in pg.event.get():

            if event.type == pg.QUIT:
                play = False

            if event.type == pg.MOUSEBUTTONDOWN and not gameover:


                if not gameplay(grids, warning1):
                    if button1.state == "Active":
                        gameover = True
                        solve_button()
                        break
                    elif button2.state == "Active":
                        grid = np.copy(matrix)
                        break
                    else:
                        undo(image, grid)
                        break
                
                

        
        display_all(WIN, grids, button1, button2, warning1, image)
        
        pg.display.update()

    pg.quit()    
    quit()
    



if __name__ == "__main__":
    main()
    
