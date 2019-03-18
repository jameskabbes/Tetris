### Tetris
import pygame
import numpy as np
import time
import copy
####### Set game intro variables

hard_black = (0,0,0)
dark_grey = (58,58,58)
light_grey = (120, 120, 120)

square_pixel_length = 25
x_squares = 10 #10 sqaures along the x direction
y_squares = 20 #10 sqaures along the x direction

grid_lines_width = 3
grid_size = ((grid_lines_width + x_squares * (square_pixel_length + grid_lines_width)), (grid_lines_width + y_squares * (square_pixel_length + grid_lines_width)))

background_color = hard_black
empty_square_color = dark_grey

left_of_playing_field = 0 # pixel
top_of_playing_field = 0  #pixel

max_refresh_time = 1   #in seconds
min_refresh_time = .05 #in seconds
lines_to_get_max_refresh = 500 #refresh time will linearly decrease until it reaches the min number at x number of lines

#############################

#Build game environment


def rectangle(place, color ,x, y, l, w):
    pygame.draw.rect(place, color, [x, y, l ,w])

def update_grid(squares):

    for i in range(x_squares):
        for j in range(y_squares):

            sq = grid[i][j]
            square_color = (sq[2], sq[3], sq[4])

            rectangle(screen, square_color, (left_of_playing_field + i*square_pixel_length + (i+1)*grid_lines_width), (top_of_playing_field + j*square_pixel_length + (j+1)*grid_lines_width), square_pixel_length, square_pixel_length)


def turn_square_color(grid, i, j, color):
    grid[i][j] = (grid[i][j][0], grid[i][j][1], color[0], color[1], color[2])
    return grid

def get_line_refresh_time(lines):

    proportion_of_max = lines / lines_to_get_max_refresh
    print (proportion_of_max)
    return max(min_refresh_time, (max_refresh_time - proportion_of_max*(max_refresh_time-min_refresh_time)))

def check_line_cleared(grid):

    return False

def clear_lines(grid):

    return grid

def check_lowest_point(grid, object_xys):

    a = False
    for i in object_xys:
        if 19 in i:
            a = True

    return a

def place_object(grid, object_xys):

    for coords in object_xys:

        grid[coords[0]][coords[1]][0] = True
        grid[coords[0]][coords[1]][1] = False

    return grid

def move_object(grid, how, object_xys):

    #check collision

    print (object_xys)
    new_xys = copy.deepcopy(object_xys)


    if how == 'down':
        for i in range(len(new_xys)):
            new_xys[i][1] = new_xys[i][1] + 1

    elif how == 'up':

        for i in range(len(new_xys)):
            new_xys[i][1] = new_xys[i][1] - 1


    elif how == 'left':

        for i in range(len(new_xys)):
            new_xys[i][0] = new_xys[i][0] - 1

    elif how == 'right':

        for i in range(len(new_xys)):
            new_xys[i][0] = new_xys[i][0] + 1

    print ('new xys')
    print (new_xys)
    print ('ob xys')
    print (object_xys)
    grid = change_squares_to_new_coords(grid, object_xys, new_xys)
    return grid, new_xys

def print_values_at_coords(grid, coords):

    for i in coords:
        print (grid[i[0]][i[1]])

def check_collision():

    #use this new one
    pass

def change_squares_to_new_coords(grid, old_coords, new_coords):

    placed = []
    active = []
    colors = []

    for i in old_coords:

        placed.append( grid[i[0]][i[1]][0]  )
        active.append( grid[i[0]][i[1]][1]  )
        colors.append( grid[i[0]][i[1]][2:5].copy() )

        grid[i[0]][i[1]] = empty_square

    for i in range(len(new_coords)):
        coords = new_coords[i]
        grid[coords[0]][coords[1]] = [placed[i], active[i], colors[i][0], colors[i][1], colors[i][2]]


    return grid

def drop_object(grid, object_xys):

    ###Make sure the line is able to be dropped first
    if not check_lowest_point(grid, object_xys):

        grid, object_xys = move_object(grid, 'down', object_xys)

        placed = False

    else:
        placed = True
        grid = place_object(grid, object_xys)

    return grid, placed, object_xys
        ## PLACE the object

def rotate_object():

    pass



############################33
#prepare

pygame.init()
screen = pygame.display.set_mode(grid_size)
pygame.display.set_caption('Tetris')
screen.fill(background_color)

grid = np.zeros((x_squares, y_squares, 5)) #3D numpy array
empty_square = (False, False, empty_square_color[0], empty_square_color[1], empty_square_color[2])

for i in range(x_squares):
    for j in range(y_squares):
        #print (grid[i][j])
        grid[i][j] = (False, False, 0, 0,0) #(Occupied non active, occupied active, r,g,b)
        grid = turn_square_color(grid, i,j, empty_square_color)

###################################

#Main Game Loop
lines = 0
refresh_time = get_line_refresh_time(lines)
i = 0
drop = False
start_time = time.time()

grid[0][0] = (False, True, 0,0,0)
grid = turn_square_color(grid, 0,0, light_grey)
grid[0][1] = (False, True, 0,0,0)
grid = turn_square_color(grid, 0,1, light_grey)
grid[1][0] = (False, True, 0,0,0)
grid = turn_square_color(grid, 1,0, light_grey)
grid[1][1] = (False, True, 0,0,0)
grid = turn_square_color(grid, 1,1, light_grey)

object_xys = [[0,0], [0,1], [1,0], [1,1]]

for i in object_xys:
    print (grid[i[0]][i[1]])


while True:

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            pygame.quit()
            exit()
            break  # Flag that we are done so we exit this loop
    #show the snake
    '''
    if (time.time() - start_time) > refresh_time:
        current_time = time.time()
        start_time = time.time()
        grid, placed, object_xys = drop_object(grid, object_xys)
        print ('drop object')
    '''

    if pygame.key.get_focused():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            grid, object_xys = move_object(grid, 'up', object_xys)
        elif keys[pygame.K_LEFT]:
            grid, object_xys = move_object(grid, 'left', object_xys)
        elif keys[pygame.K_RIGHT]:
            print ('moving right')
            grid, object_xys = move_object(grid, 'right', object_xys)
        elif keys[pygame.K_DOWN]:
            grid, object_xys = move_object(grid, 'down', object_xys)
        #elif keys[pygame.K_SPACE]:
        #    grid, object_xys = move_object(grid, 'up', object_xys)


    line_cleared = check_line_cleared(grid)
    if line_cleared:
        grid = clear_lines(grid)

    update_grid(grid)
    pygame.display.flip()
