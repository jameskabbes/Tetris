### Tetris
import pygame

import numpy as np
import time
import copy
import random
####### Set game intro variables

hard_black = (0,0,0)
dark_grey = (58,58,58)
light_grey = (120, 120, 120)
off_white = (237,237,237)
lime_green = (53, 242, 106)
blue = (53, 84, 242)
red = (242, 53, 53)
yellow = (242, 239, 53)
purple = (201, 53, 242)
orange = (242, 138, 53)
light_blue = (46, 219, 213)

placed_color_adder = -20

square_pixel_length = 25
x_squares = 10 #10 sqaures along the x direction
y_squares = 20 #10 sqaures along the y direction

grid_lines_width = 3
score_width = 100
grid_size = ((grid_lines_width + x_squares * (square_pixel_length + grid_lines_width) + score_width), (grid_lines_width + y_squares * (square_pixel_length + grid_lines_width)))

background_color = hard_black
empty_square_color = dark_grey
cleared_line_color = off_white

left_of_playing_field = 0 # pixel
top_of_playing_field = 0  #pixel

max_refresh_time = .4   #in seconds
min_refresh_time = .05 #in seconds
lines_to_get_max_refresh = 500 #refresh time will linearly decrease until it reaches the min number at x number of lines
line_clear_delay = .2
sticky_keys_hold_time = .12
sticky_keys_windback = .03

#############################

#Build game environment


def rectangle(place, color ,x, y, l, w):
    pygame.draw.rect(place, color, [x, y, l ,w])

def update_grid(grid):
    whole_screen.fill(background_color)
    score_surface.blit(font.render(str(lines), False, off_white), [0,0])

    for i in range(x_squares):
        for j in range(y_squares):

            sq = grid[i][j]
            square_color = (sq[2], sq[3], sq[4])

            rectangle(grid_screen, square_color, (left_of_playing_field + i*square_pixel_length + (i+1)*grid_lines_width), (top_of_playing_field + j*square_pixel_length + (j+1)*grid_lines_width), square_pixel_length, square_pixel_length)

def turn_square_color(grid, i, j, color):
    grid[i][j] = (grid[i][j][0], grid[i][j][1], color[0], color[1], color[2])
    return grid

def get_line_refresh_time(lines):

    proportion_of_max = lines / lines_to_get_max_refresh
    return max(min_refresh_time, (max_refresh_time - proportion_of_max*(max_refresh_time-min_refresh_time)))

def check_line_cleared(grid, lines):

    #loop through lines
    cleared_lines = []
    for i in range(y_squares):

        cleared = True
        for x in range(x_squares):

            if not grid[x][i][0]: #if there is not a block there
                cleared = False
                break

        if cleared:
            cleared_lines.append(i)

    lines += len(cleared_lines)
    if cleared_lines != []:
        grid = clear_lines(grid, cleared_lines)
        print (lines)

    return grid, lines

def write_row_to_grid(grid, row, row_ind):

    for i in range(len(row)):
        grid[i][row_ind] = row[i]

    return grid

def get_row_from_grid(grid, row_ind):

    row = []
    for i in range(len(grid)):

        row.append(grid[i][row_ind])

    return row

def clear_lines(grid, cleared_lines):

    #flash the cleared_line_color once or twice and then disappear
    for j in cleared_lines:
        for i in range(x_squares):

            turn_square_color(grid, i, j, cleared_line_color)

    update_grid(grid)
    pygame.display.flip()
    time.sleep(line_clear_delay / 4)

    for j in cleared_lines:
        for i in range(x_squares):

            turn_square_color(grid, i, j, empty_square_color)

    update_grid(grid)
    pygame.display.flip()
    time.sleep(line_clear_delay / 4)
    ##########################################################33

    how_many_to_shift_down = [0,] * y_squares
    #16,17,19
    for row in range(y_squares):
        for line in cleared_lines:
            if row < line:
                how_many_to_shift_down[row] = how_many_to_shift_down[row] + 1

    shifted_grid = copy.deepcopy(grid)
    blank_row = [empty_square,] * x_squares

    for i in range(len(cleared_lines)): #Add x number of blank rows to the top
        shifted_grid = write_row_to_grid(shifted_grid, blank_row, i)

    for i in range(y_squares):

        if i not in cleared_lines:
            row_to_use = get_row_from_grid(grid, i)
            shifted_grid = write_row_to_grid(shifted_grid, row_to_use, (i + how_many_to_shift_down[i]) )


    time.sleep(line_clear_delay / 2)
    update_grid(shifted_grid)
    pygame.display.flip()
    return shifted_grid

def place_object(grid, object_xys):

    for coords in object_xys:


        grid[coords[0]][coords[1]][0] = True
        grid[coords[0]][coords[1]][1] = False
        grid[coords[0]][coords[1]][2] = grid[coords[0]][coords[1]][2] + placed_color_adder
        grid[coords[0]][coords[1]][3] = grid[coords[0]][coords[1]][3] + placed_color_adder
        grid[coords[0]][coords[1]][4] = grid[coords[0]][coords[1]][4] + placed_color_adder


    return grid

def move_object(grid, how, object_xys):
    #check collision

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

    if not check_collision(grid, new_xys): #no collosion
        grid = change_squares_to_new_coords(grid, object_xys, new_xys)

    else:
        if how == 'down':
            #place
            grid = place_object(grid, object_xys)
            return grid, None
        else:
            return grid, object_xys
    return grid, new_xys

def print_values_at_coords(grid, coords):

    for i in coords:
        print (grid[i[0]][i[1]])

def check_collision(grid, new_xys):

    # (Placed, Object, r,g,b)
    for i in new_xys:
        if i[0] < 0:
            return True
        if i[0] > (x_squares - 1):
            return True
        if i[1] < 0:
            return True
        if i[1] > (y_squares - 1):
            return True
        if grid[i[0]][i[1]][0]: #There is already a piece there
            return True

    return False

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

def get_vectors_wrt_rotate_point(object_xys, rotate_point_index):

    #Get vectors from rotate point to each point in the object

    vectors = copy.deepcopy(object_xys)
    for i in range(len(object_xys)):

        vectors[i][0] = object_xys[i][0] - object_xys[rotate_point_index][0]
        vectors[i][1] = object_xys[i][1] - object_xys[rotate_point_index][1]
        vectors[i] = vectors[i] + [0] #MAke it 3 dimensions

    return vectors

def rotate_object(grid, object_xys, object_type, how = 'clock'):

    if object_type == 0: #Dont change for the square
        return grid, object_xys
    elif object_type == 1:
        rotate_point_index = 1

    elif object_type == 2:
        rotate_point_index = 1

    elif object_type == 3:
        rotate_point_index = 1

    elif object_type == 4:
        rotate_point_index = 1

    elif object_type == 5:
        rotate_point_index = 1

    elif object_type == 6:
        rotate_point_index = 1

    ###Use Cross Product for rotation
    vectors = get_vectors_wrt_rotate_point(object_xys, rotate_point_index)

    if how == 'clock':
        vec = [0,0,-1]
    else: #counterclockwise
        vec = [0,0,1]

    new_shift_coords = []
    for i in vectors:
        new = np.cross(vec, i)
        new_shift_coords.append(new)

    new_object_xys = []
    for i in range(len(new_shift_coords)):
        new_object_xys.append([object_xys[rotate_point_index][0] + new_shift_coords[i][0], object_xys[rotate_point_index][1] + new_shift_coords[i][1] ])


    if not check_collision(grid, new_object_xys):
        grid = change_squares_to_new_coords(grid, object_xys, new_object_xys)
        return (grid, new_object_xys)
    else:
        return (grid, object_xys)

def hard_drop(grid, object_xys):

    new_xys = copy.deepcopy(object_xys)

    while True:

        grid, object_xys = move_object(grid, 'down', object_xys)
        if object_xys == None:
            return grid, object_xys

        update_grid(grid)
        time.sleep(.005)

def object_generator(grid):

    choice = random.randint(0, 6)
    if choice == 0:
        #   ________
        #  |   |   |
        #  |___|___|
        #  |   |   |
        #  |___|___|
        object_xys = [[4,0], [4,1], [5,0], [5,1]]
        object_color = lime_green

    elif choice == 1:
        #  ____
        # |   |
        # |___|
        # |   |
        # |___|
        # |   |
        # |___|
        # |   |
        # |___|
        #
        object_xys = [[3,0], [4,0], [5,0], [6,0]]
        object_color = blue

    elif choice == 2:

        #  ____
        # |   |
        # |___|
        # |   |
        # |___|____
        # |   |   |
        # |___|___|
        #
        object_xys = [[3,0], [4,0], [5,0], [3,1]]
        object_color = red

    elif choice == 3:

        #  _______
        # |   |   |
        # |___|___|
        # |   |
        # |___|
        # |   |
        # |___|

        object_xys = [[3,0], [4,0], [5,0], [5,1]]
        object_color = orange

    elif choice == 4:

        #  ____
        # |   |
        # |___|____
        # |   |   |
        # |___|___|
        # |   |
        # |___|

        object_xys = [[3,0], [4,0], [5,0], [4,1]]
        object_color = light_blue

    elif choice == 5:

        #  ____
        # |   |
        # |___|____
        # |   |   |
        # |___|___|
        #     |   |
        #     |___|

        object_xys = [[3,1], [4,0], [4,1], [5,0]]
        object_color = yellow

    elif choice == 6:

        #      ____
        #     |   |
        #  ___|___|
        # |   |   |
        # |___|___|
        # |   |
        # |___|

        object_xys = [[3,0], [4,0], [4,1], [5,1]]
        object_color = purple



    #check for collision among the new object_xys
    if not check_collision(grid, object_xys):

        for i in object_xys:

            grid[i[0]][i[1]] = [False, True, 0,0,0]
            grid = turn_square_color(grid, i[0], i[1], object_color)

        return grid, object_xys, choice

    else:
        #game over
        return grid, None, choice

def game_over_animation():

    print ('game over')

############################33
#prepare

pygame.init()

# Initialize system fonts to use for score counter
pygame.font.init()
font = pygame.font.SysFont("Helvetica", 20)

whole_screen = pygame.display.set_mode(grid_size)
grid_screen = whole_screen.subsurface((score_width, 0, grid_size[0] - score_width, grid_size[1]))
score_surface = whole_screen.subsurface((0, 0, score_width, grid_size[1]))

pygame.display.set_caption('Tetris')
whole_screen.fill(background_color)

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
i = 0
drop = False
start_time = time.time()
pressed = False
object_xys = None
refresh_time = get_line_refresh_time(lines)
last_dir = None
last_pressed = time.time()

while True:

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            pygame.quit()
            exit()
            break  # Flag that we are done so we exit this loop

    if object_xys == None: #Object was placed
        grid, lines = check_line_cleared(grid, lines)
        grid, object_xys, object_type = object_generator(grid)
        if object_xys == None:
            #Game is over
            game_over_animation()
            break

    if (time.time() - start_time) > refresh_time:
        start_time = time.time()
        grid, object_xys = move_object(grid, 'down', object_xys)
        refresh_time = get_line_refresh_time(lines)

    if object_xys == None: #Object was placed
        grid, lines = check_line_cleared(grid, lines)
        grid, object_xys, object_type = object_generator(grid)
        if object_xys == None:
            #Game is over
            game_over_animation()
            break


    if pygame.key.get_focused():
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:

            if last_dir != 'up':
                last_dir = 'up'
                last_pressed = time.time()
                grid, object_xys = rotate_object(grid, object_xys, object_type)

        elif keys[pygame.K_z]:
            if last_dir != 'z':
                last_dir = 'z'
                last_pressed = time.time()
                grid, object_xys = rotate_object(grid, object_xys, object_type, how = 'counter')

        elif keys[pygame.K_LEFT]:
            if last_dir == 'left':
                if (time.time() - last_pressed) > sticky_keys_hold_time:
                    grid, object_xys = move_object(grid, 'left', object_xys)
                    #last_pressed = time.time()
                    last_pressed = time.time() - sticky_keys_hold_time + sticky_keys_windback


            else:
                last_dir = 'left'
                last_pressed = time.time()
                grid, object_xys = move_object(grid, 'left', object_xys)


        elif keys[pygame.K_RIGHT]:
            if last_dir == 'right':
                if (time.time() - last_pressed) > sticky_keys_hold_time:
                    grid, object_xys = move_object(grid, 'right', object_xys)
                    #last_pressed = time.time()
                    last_pressed = time.time() - sticky_keys_hold_time + sticky_keys_windback
            else:
                last_dir = 'right'
                last_pressed = time.time()
                grid, object_xys = move_object(grid, 'right', object_xys)

        elif keys[pygame.K_DOWN]:
            if last_dir == 'down':
                if (time.time() - last_pressed) > sticky_keys_hold_time:
                    grid, object_xys = move_object(grid, 'down', object_xys)
                    #last_pressed = time.time()
                    last_pressed = time.time() - sticky_keys_hold_time + sticky_keys_windback

            else:
                last_dir = 'down'
                last_pressed = time.time()
                grid, object_xys = move_object(grid, 'down', object_xys)

        elif keys[pygame.K_SPACE]:
            if last_dir != 'space':
                last_dir = 'space'
                last_pressed = time.time()
                grid, object_xys = hard_drop(grid, object_xys)

        else:
            last_dir = 'none'

        #elif keys[pygame.K_SPACE]:
        #    grid, object_xys = move_object(grid, 'up', object_xys)
    update_grid(grid)
    pygame.display.flip()
    time.sleep(.001)
