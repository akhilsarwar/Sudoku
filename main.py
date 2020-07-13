import numpy as np
import pygame as pg
import threading
import math
from solution import Backtrack

pg.init()
Font = pg.font.SysFont("impact", 45)


threads = []
grid = np.array([[0,0,0,0,0,1,2,0,0],
                 [0,0,0,0,0,0,3,4,0],
                 [0,0,0,0,0,0,0,5,6],
                 [0,0,0,0,0,0,0,0,7],
                 [0,0,0,0,0,0,0,0,0],
                 [1,0,0,0,0,0,0,0,0],
                 [7,2,0,0,0,0,0,0,0],
                 [0,4,8,0,0,0,0,0,0],
                 [0,0,6,3,0,0,0,0,0]
                 ])
sub_grid = {"a" : (0,1,2),"b" : (3,4,5),"c" : (6,7,8)}


class Grid:
    def __init__(self, n):
        self.n = n
        self.cell_length = round(600/n)

    def draw(self, WIN):
        for i in range(self.n):
            pg.draw.line(WIN, (178,34,34), (0, round((600/self.n)*(i+1))), (600, round((600/self.n)*(i+1))), 1)
            pg.draw.line(WIN, (178,34,34), (round((600/self.n)*(i+1)), 0), (round((600/self.n)*(i+1)), 600), 1)
        


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
                    print(grid[i,j])
                    return centre_x, centre_y, i, j
        


    def draw_selection_grid(self, WIN):
        try:
            centre_x, centre_y, i, j = self.selection_grid()
            x, y = centre_x - self.cell_length/2, centre_y - self.cell_length/2
            pg.draw.rect(WIN, (0,255,0), (x, y, self.cell_length, self.cell_length), 1)
        
        except TypeError:
            pass


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



def display_all(WIN, grids, button1):

     grids.draw(WIN)
     grids.set(WIN, grid)
     grids.draw_selection_grid(WIN)
     button1.draw(WIN)


     
def solve():
    if Backtrack(grid, check):
        print(grid)
    else:
        print("solution not possible")


def gameplay(grids):
    try:
        _, _, cell_x, cell_y,  = grids.selection_grid()
    except TypeError:
        return False

    get_input = True
    while get_input:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6 ,pg.K_7 ,pg.K_8 ,pg.K_9]:
                    num=int(chr(event.key))
                    grid[cell_x, cell_y] = num
                    return True
                else:
                    return False
    
        

def solve_button():
    global threads
    threads.append(threading.Thread(target=solve, daemon=True))
    threads[-1].start()





def main():


    display = (600,700)
    WIN = pg.display.set_mode(display)
    global grid
    play = True


    grids = Grid(9)
    button1 = Button(10, 610, 150, 80, (0,0,255), "solve")
    gameover = False

    #game loop
    while play:
        
        WIN.fill((0,0,0))

        for event in pg.event.get():

            if event.type == pg.QUIT:
                play = False

            if event.type == pg.MOUSEBUTTONDOWN and not gameover:
                if not gameplay(grids):
                    if button1.state == "Active":
                        gameover = True
                        solve_button()
                        break
                    else:
                        break
                else:
                    break

        
        display_all(WIN, grids, button1)
        
        pg.display.update()

    pg.quit()    
    quit()
    



if __name__ == "__main__":
    main()
    
