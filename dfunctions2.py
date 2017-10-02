# -*- coding: cp1252 -*-
from __future__ import division

import pygame
import math
import pygame.gfxdraw
import pygame.font
import random
import copy

RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0, 255)
BRIGHT_BLUE = (150,150,255)
BLUE_2 = (0,0,160)
BLUE_3 = (0,0,100)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (100,100,100)
GOLD = (255,215,0)
MAGENTA = (255,0,255)
PURPLE = MAGENTA
MAGENTA_2 = (160,0,160)
RED_2 = (160,0,0)
ORANGE = (255,165,0)
SILVER = (192,192,192)
PINK = (255,193, 203)
GREEN_2 = (0,170,0)
BLUE_WHITE = (150,230,255)


pygame.font.init ()
clock = pygame.time.Clock ()
screen_x = 1100
screen_y = 700

# if __name__ != "__main__": screen_x, screen_y = 1,1

screen = pygame.display.set_mode((screen_x, screen_y))# , pygame.FULLSCREEN)


test_variable = 2 

#########################################

def rect_points (position, x_size, y_size):
    point_1 = position
    point_2 = vadd (position, (x_size,0))
    point_3 = vadd (position, (x_size,y_size))
    point_4 = vadd (position, (0,y_size))
    return (point_1,point_2,point_3,point_4) 

def success_box (position, colour, success, **wargs):
    if 'surface' in wargs: surface = wargs.get ('surface')
    else: surface = screen 
    seize = wargs.get ('seize')
    if seize == None: seize = 20

    right_upper = vadd  (position, (seize, 0))

    left_down = vadd (position, (0, seize))

    right_down = vadd (position, (seize, seize ))

    pygame.gfxdraw.aapolygon (surface, ( position, right_upper, right_down, left_down) , colour )

    if success == 'yes':
        pygame.draw.aaline (surface, colour, position, right_down, 1)
        pygame.draw.aaline (surface, colour, right_upper, left_down, 0)



def find_angle_range (start_angle,angle_range, direction): ### direction = 'clock' , 'anticlock'

    if direction == 'clock':
        if start_angle + angle_range <= 2 * 3.14:
            out = [ [start_angle, start_angle + angle_range ] ]
        elif start_angle + angle_range > 2 * 3.14:
            out = [ [start_angle, 2 * 3.14], [0, start_angle + angle_range - 2 * 3.14] ]

    elif direction =='anticlock':
        if start_angle - angle_range >= 0:
            out = [ [start_angle, start_angle - angle_range] ]
        elif start_angle - angle_range < 0:
            out = [ [start_angle, 0], [2 * 3.14,   start_angle - angle_range  + 2 * 3.14] ]

    


    else: raise ValueError ('fucked up')

    for item in out:
        item.sort ()


    return out




def within_range (input_range, value):
    out = False 
    working_range = input_range [:]
    working_range.sort ()
    if value >= working_range [0] and value <= working_range [1] : out = True

    return out

def within_range_list (range_list, value):
    out = False

    for r in range_list:
        if within_range (r, value) == True: out = True

    return out

def within_angle_range (start_angle,angle_range, direction, value):

    # print 'test 33 ', angle_range ( 3, 2, 'clock') 

    range_list = find_angle_range (start_angle,angle_range, direction)

    

    out = within_range_list (range_list, value)

    return out








    


def x_add (vector, x):
    return (vector [0] + x, vector [1] )

def y_add (vector, y):
    return (vector [0], vector [1] + y ) 

def darken_colour (colour_1): # verdunkelt eine Farbe
    r,g,b = colour_1
    r = int (r / 2)
    g = int (g / 2)
    b = int (b / 2)
    colour_2 = (r,g,b)
    return colour_2

def brighten_colour (colour_1):
    r,g,b = colour_1
    r = min (255, 2 * r)
    g = min (255, 2 * g)
    b = min (255, 2 * b)
    colour_2 = (r,g,b)
    return colour_2 


def round_vector (vector, digits):   ### rounds the elements of a 2-vector to digits 
    new_vector = ( round (vector [0], digits), round (vector [1], digits))
    return new_vector 

def create_intermediate_points (startpunkt, endpunkt, **wargs):
    out_dot_list = []
    grain_seize = 2
    if 'grain_seize' in wargs: grain_seize = wargs.get ('grain_seize')
    x1,y1 = startpunkt
    x2, y2 = endpunkt 
    d = math.atan2 ((x2-x1),(y2-y1))

    lenght = (  (x1 -x2) ** 2 + (y1 - y2) ** 2 ) ** 0.5
    for i in range (1, int (lenght / grain_seize)):
        out_dot = fextrapolate_line (d, startpunkt, i * grain_seize, 10000) [0] 

        out_dot_list.append ( (int (out_dot [0]), int (out_dot [1])))

    return out_dot_list


def listify_tuple_list (input_list):
    new_list = []
    for t in input_list:
        new_list.append ( list (t) )
    return new_list

def tuplify_list_list (input_list):
    new_list = []
    for l in input_list:
        new_list.append ( tuple (l) )
    return new_list 



def collide2 (s, b, height, lenght): # s ist die linke obere ecke des Rechtecks ! 
    out = 0

    s_x, s_y = s
    s_x_u = s_x 
    s_x_o = s_x + lenght 

    s_y_u = s_y 
    s_y_o = s_y + height 
    
    xb, yb = b 

    if ( s_x_o > xb > s_x_u ) and ( s_y_o > yb > s_y_u ): out = 1

    return out   # 1 = treffer ; 0 = kein treffer


def target_brackets (position, radius):
    ### left bracket:
    pl_u = vadd (position, (- int (radius * 1.5), - int (radius * 1.5)))
    pl_u_2 = vadd (pl_u, (int (radius * 0.7), 0))
    pl_d = vadd (position, (- int (radius * 1.5), int (radius * 1.5)))
    pl_d_2 = vadd (pl_d, (int (radius * 0.7), 0))

    pygame.draw.aaline (screen, RED,vadd ( pl_u ,  (0 , 1)    )  ,vadd ( pl_d, (0, 1)      ), 1)
    pygame.draw.aaline (screen, RED, pl_u, pl_u_2,1)
    pygame.draw.aaline (screen, RED, pl_d, pl_d_2, 1) 

    ### right bracket:

    pr_u = vadd (position, (int (radius * 1.5), - int (radius * 1.5)))
    pr_u_2 = vadd (pr_u, (-int (radius * 0.7), 0))
    pr_d = vadd (position, (int (radius * 1.5), int (radius * 1.5)))
    pr_d_2 = vadd (pr_d , (-int (radius * 0.7), 0))


    pygame.draw.aaline (screen, RED,vadd ( pr_u ,  (0 , 0)    )  ,vadd ( pr_d, (0, 1)      ), 1)
    pygame.draw.aaline (screen, RED, pr_u, pr_u_2,1)
    pygame.draw.aaline (screen, RED, pr_d, pr_d_2, 1) 

    

def back_frame (position, x_seize, y_seize, colour,d, number, back_colour, **wargs):
    surface = screen
    if 'surface' in wargs: surface = wargs ['surface'] 
    x,y = position
    pygame.draw.polygon (surface, back_colour, ( (position), (x + x_seize ,y), (x + x_seize,y + y_seize), (x,y + y_seize)), 0)
    for n in range (0, number):
        pygame.gfxdraw.aapolygon (surface, ( (x + d * n, y +d *n ), (x + x_seize  - d * n ,y + d * n), (x + x_seize + - d * n,y + y_seize + - d * n), (x + d * n,y + y_seize - d * n)), colour)


def back_frame_2 (surface, position, x_seize, y_seize, colour,d, number, back_colour):  ### like back frame, but draws on surface instead on screen 
    x,y = position
    pygame.draw.polygon (surface, back_colour, ( (position), (x + x_seize ,y), (x + x_seize,y + y_seize), (x,y + y_seize)), 0)
    for n in range (0, number):
        pygame.gfxdraw.aapolygon (surface, ( (x + d * n, y +d *n ), (x + x_seize  - d * n ,y + d * n), (x + x_seize + - d * n,y + y_seize + - d * n), (x + d * n,y + y_seize - d * n)), colour)


def info_box (text, position, text_colour, back_colour, frame_colour):
    back_frame (position, 100, 30, frame_colour,1,2,back_colour)
    myfont = pygame.font.SysFont("Comic Sans MS", 15)
    label = myfont.render ( str (text) , 1, text_colour)
    screen.blit (label, vadd (position, ( 2, 4)))

def info_box2 (text, position, text_colour, back_colour, frame_colour,x_seize, y_seize,left_mouse,mpos):
    out = 0
    back_frame (position, x_seize, y_seize, frame_colour,1,2,back_colour)
    myfont = pygame.font.SysFont("Comic Sans MS", 15)
    label = myfont.render ( str (text) , 1, text_colour)
    screen.blit (label, vadd (position, ( 2, 4)))
    if left_mouse == 1:
            if collide2 (position, mpos, y_seize, x_seize) == 1: 
                out = 1
    return out


def switch_list_membership (x, list_1):
    if x in list_1: condition = 1
    if x not in list_1: condition = 2
    if condition == 1: list_1.remove (x)
    if condition == 2: list_1.append (x)
    return list_1

def write (text,position, text_colour, font_seize):
    myfont = pygame.font.SysFont("TIMES NEW ROMAN", font_seize) ### "Comic Sans MS"
    label = myfont.render ( str (text) , 1, text_colour)
    screen.blit (label, position)

def write_1b ( text,position, text_colour, font_seize, **wargs):          ### like normal 'write', but draws on surface instead of screen
    surface = wargs ['surface'] 
    myfont = pygame.font.SysFont("Times New Roman", font_seize)
    label = myfont.render ( str (text) , 1, text_colour)
    surface.blit (label, position)

def write_1c ( position,text, text_colour, font_seize, **wargs):          ### like normal 1b, but : - position and text exchanged ;;;  - returns the label instead of blitting it  

    myfont = pygame.font.SysFont("Times New Roman", font_seize)
    label = myfont.render ( str (text) , 1, text_colour)
    return label 


def write_vertical (text, position, colour, font_seize):
    key_list = list (text)
    for e, key in enumerate (key_list):
        write (key, vadd (position, (0, (e-1) * font_seize)), colour, font_seize)



def invert_y ( input_tuple):
    output_tuple = ( input_tuple [0], -1 * input_tuple [1] )
    return output_tuple




def angel_seize (distance, diameter):
    alpha = math.atan (diameter / distance)
    return alpha



def one_or_minus_one (x):
    if x == 0 : out = 0
    if x < 0 : out = -1
    if x > 0 : out = 1
    return out


def inner_octagon (old_octagon, x): # beginnt mit Punkt links ganz oben
    new_octagon = []
    new_0 = vadd (old_octagon [0], (0, -x))
    new_1 = vadd (old_octagon [1], (0, -x))
    new_2 = vadd (old_octagon [2], (-x, 0))
    new_3 = vadd (old_octagon [3], (-x, 0))
    new_4 = vadd (old_octagon [4], (0, x))
    new_5 = vadd (old_octagon [5], (0,x))
    new_6 = vadd (old_octagon [6], (x, 0))
    new_7 = vadd (old_octagon [7], (x,0))
    new_octagon.append (new_0)
    new_octagon.append (new_1)
    new_octagon.append (new_2)
    new_octagon.append (new_3)
    new_octagon.append (new_4)
    new_octagon.append (new_5)
    new_octagon.append (new_6)
    new_octagon.append (new_7)
    return new_octagon

def multi_octagon_200 (position, distance, n, colour):
    position = (100,100) 
    frame = pygame.Surface ( (200,200)) 
    
        
    octagon_list = []
    octagon_1 = [ (-60,100), (60,100), (100,60), (100,-60), (60, -100), (-60,-100), (-100,-60), (-100,60) ]
    octagon_list.append (octagon_1)
    for i in range (1,n):
        octagon_list.append ( inner_octagon (octagon_1, i * distance))
    for octagon in octagon_list:
        pygame.gfxdraw.aapolygon (frame, move_normalized_polygon (position, octagon), colour)

    return frame 

    

def dot ( position, colour, **wargs):
    surface = screen
    if 'surface' in wargs: surface = wargs ['surface']
    pygame.draw.circle (surface, colour, (int (position [0]), int (position [1])), 3, 0)

def dot_2 ( position, colour):
    pygame.draw.circle (screen, colour, (int (position [0]), int (position [1])), 2, 0)






def switch (a):  # macht 1 zu 0 und umgekehrt
    if a == 1: out = 0
    if a == 0: out = 1
    return out

def merge_into_tuples (list_1, list_2):
    new_list = []
    for i in range (0, len (list_1)):
        element = (list_1 [i], list_2 [i])
        new_list.append (element)
    return new_list

def hit_direction (shot_angle):
    angle = aa (shot_angle, 3.14)
    if angle > 5.5 or angle <= 0.79: out = 'front'
    if angle > 0.79 and angle <= 2.37 : out = 'left'
    if angle > 2.37 and angle <= 3.95 : out = 'aft'
    if angle > 3.95 and angle <= 5.5 : out = 'right'
    return out

def hit_direction_2 (ship_direction, shot_direction):
    angle = relative_direction (ship_direction, shot_direction)
    out = hit_direction (angle)
    return out




def range_overlap ((a0,ae),(b0,be)):  # testet, ob zwei linien in einer dimension sich überschneiden # 1 falls ja ;;  null falls nein
    result = 1
    if a0 > be : result = 0
    if ae < b0 : result = 0
    return result

def vadd (vector_1, vector_2, *args):   ### addiert vektoren beliebiger länge 
    l_1 = list (vector_1)
    l_2 = list (vector_2)
    new_list = []
    for i in range (0, len (vector_1)):
        new_value = l_1 [i] + l_2 [i]
        for ar in args:
            new_value += ar [i] 

        
        new_list.append (new_value)
    return tuple (new_list)




def triple_line_horizontal (middle, lenght, outer_colour, **vargs):    ### inner_colour = inner_colour, outer_lines = outer_lines, inner_lines=inner_lines)
    inner_colour = vargs.get ('inner_colour')
    inner_lines = vargs.get ('inner_lines')
    outer_lines = vargs.get ('outer_lines')

    surface = screen
    if 'surface' in vargs: surface = vargs ['surface'] 
    # print ' test 66  ', inner_lines, outer_lines 
    
    lines = outer_lines + inner_lines 
    for i in range (0,lines ):
        a = int ((i + 1 ) / 2)
        if i %2 == 1: a *= (-1)
        

        if i < inner_lines: colour = inner_colour
        else: colour = outer_colour

        
        

        pygame.draw.aaline (surface, colour, vadd (middle, (- lenght/2, a )), vadd (middle, (lenght / 2, a)), 1)


def triple_line_vertical (middle, lenght, outer_colour, **vargs):    ### inner_colour = inner_colour, outer_lines = outer_lines, inner_lines=inner_lines)
    inner_colour = vargs.get ('inner_colour')
    inner_lines = vargs.get ('inner_lines')
    outer_lines = vargs.get ('outer_lines')

    surface = screen
    if 'surface' in vargs: surface = vargs ['surface'] 
    # print ' test 66  ', inner_lines, outer_lines 
    
    lines = outer_lines + inner_lines 
    for i in range (0,lines ):
        a = int ((i + 1 ) / 2)
        if i %2 == 1: a *= (-1)

        if i < inner_lines: colour = inner_colour
        else: colour = outer_colour 
        

        pygame.draw.aaline (surface, colour, vadd (middle, ( a , - lenght/2)), vadd (middle, ( a, lenght / 2)), 1)


    

def count_down_to_zero (actual_value):
    if actual_value > 0 : actual_value -= 1
    if actual_value < 0 : actual_value = 0
    return actual_value

def determine_x_y_range (point_list):   ### gibt ausserdem als drittes die position der linken oberen ecken an
    x_list = []
    y_list = []
    for point in point_list:
        x_list.append (point [0])
        y_list.append (point [1])
   
    x_list.sort ()
    y_list.sort ()

    x_range = (abs ((x_list [0]) - (x_list [-1])))
    y_range = (abs ((y_list [0]) - (y_list [-1])))
    return x_range, y_range , (x_list [0], y_list [0])

def hitbox_collision (  direction, hitbox_in, bullet_position_in, bullet_radius):
    hitbox, bullet_position = adjust_hitbox ((300,300), direction,  hitbox_in, bullet_position_in)
    
    bullet_position = (bullet_position [0] - bullet_radius, bullet_position [1] - bullet_radius)
    bullet_x_seize = 2 * bullet_radius
    bullet_y_seize = 2 * bullet_radius

    hitbox_x_seize , hitbox_y_seize, hitbox_position = determine_x_y_range (hitbox)  
    result = rect_collide ( (hitbox_position, hitbox_x_seize, hitbox_y_seize), (bullet_position, bullet_x_seize, bullet_y_seize))
   
    return result 
        


def rect_collide (rect_1, rect_2): # nimmt die rects entgegen in der Form: (position, x_seize, y_seize)
    p_1, p_2 = rect_1 [0], rect_2 [0]
    x_seize_1, x_seize_2 = rect_1 [1], rect_2 [1]
    y_seize_1, y_seize_2 = rect_1 [2], rect_2 [2]

    x_range_1 = (p_1 [0], p_1 [0] + x_seize_1)
    x_range_2 = (p_2 [0], p_2 [0] + x_seize_2)
    
    y_range_1 = (p_1 [1], p_1 [1] + y_seize_1)
    y_range_2 = (p_2 [1], p_2 [1] + y_seize_2)

    result = 0 ### falls keine Kollission
    if range_overlap (x_range_1,x_range_2) == 1 and range_overlap (y_range_1,y_range_2) == 1: result = 1
    return result

def rect_collide_list (rect_1, rect_list): ### testet ein rect auf kollission mit einer ganzen Liste von rects; gibt treffer als objekt_id_liste aus;
    ## Input : rect_1 : ((position, x_seize, y_seize), [ (object_id, ((position, x_seize, y_seize)), ... ]
    out_list = []
    for other_rect in rect_list:
        rect_2 = other_rect [1]
        if rect_collide (rect_1, rect_2) == 1:
            out_list.append (other_rect [0])
    return out_list


def angle_difference (a1, a2):
    d = a1 - a2
    d= math.fabs (d)
    if d > 3.14: d = d - 2 * 3.14
    d = math.fabs (d)
    return d



    


def relative_direction (dir_ship, bearing): # berechnet, ob das Ziel links oder rechts vom schiff liegt, und wie weit
    bearing = normalize_angle (bearing)
    dir_ship = normalize_angle (dir_ship)
    correction = 3.14 - dir_ship
    bearing = aa (correction, bearing)
    return  (bearing - 3.14)  # ergebnis in Pi

def assign_angle_factor (angle): ### gibt zu jedem Winkel einen Distanzfaktor aus <=> der Abstand nach oben sollte kleiner sein, als nach unten
    factor = 1
    if  0 <= angle < 30  : factor = 0.5
    if 30 <= angle < 60 : factor = 0.75
    if 60 <= angle < 120: factor = 1
    if 120 <= angle < 150: factor = 0.75
    if 150 <= angle < 210: factor = 0.5
    if 210 <= angle < 240: factor = 0.75 ### test, echter wert === 0.75
    if 240 <= angle < 300: factor = 1
    if 300 <= angle < 330: factor = 0.75
    if 330 <= angle : factor = 0.5
    return factor


def skalar_multi (x, vector):
    old_list = list (vector)
    new_list = []
    for o in old_list:
        o = o * x
        new_list.append (o)
    return tuple (new_list)

def out_of_list (tuple_list, x):
    out_list = []
    for t in tuple_list:
        out_list.append (t [x])
    return out_list 





def triangle (position, direction, lenght, widht):
    thaw, tip_point = fextrapolate_line (direction, position, 1, lenght / 2)
    thaw, point_g = fextrapolate_line (aa (direction, 3.14), position, 1, lenght / 2)
    thaw, point_2 = angle_line (point_g, direction, widht / 2, 90)
    thaw, point_3 = angle_line (point_g, direction, widht / 2, 270)
    return tip_point, point_2, point_3

def triangle_middle ((point_1, point_2, point_3)): # berechnet den Mittelpunkt
    l_ground = dis (abs_pos (point_2, point_3))
    dir_ground = ftarget_direction (abs_pos (point_2, point_3))
    throwaway, point_g = fextrapolate_line (point_2, dir_ground, 1, l_ground / 2)
    direction = l_ground + 270 / 57
    lenght = dis (abs_pos (point_g, point_1))
    throwaway, point_m = fextrapolate_line (point_g, direction, 1, lenght / 2)
    return point_m

def triangle_middle_2 (point_1, direction, lenght):
    wegwerf, point_m = fextrapolate_line ( aa (direction, 3.14), point_1 , 1, lenght / 2)
    return point_m 
    

def triangle_tip (position, direction, lenght, widht): # berechnet Dreieck; "position" = position der Spitze
    point_g = fextrapolate_line (aa (direction, 3.14), position, 1, lenght) [1]
    point_2 = angle_line (point_g, direction, widht / 2, 90) [1]
    point_3 = angle_line (point_g, direction, widht / 2, 270) [1]
    # print 'test 800  ', position, '  ', point_2,'   ',  point_3
    return  round_vector ((position),0),round_vector ( (point_2),0) ,round_vector ( ( point_3 ), 0) 

def rect_tip (position, direction, lenght, widht ):
    wegwerf, point_1 = fextrapolate_line ( aa (direction, 1.57), position, 1, widht / 2)
    wegwerf, point_2 = fextrapolate_line ( aa (direction, 4.71), position, 1, widht / 2)
    wegwerf, point_3 = fextrapolate_line ( aa (direction, 3.14), point_1,1, lenght)
    wegwerf, point_4 = fextrapolate_line ( aa (direction, 3.14), point_2,1, lenght)
    return point_1, point_3, point_4, point_2

def filled_triangle_tip (position, direction, lenght, widht, colour):
    point_m = triangle_middle_2 (position, direction, lenght)
    z = 20
    wegwerf, new_pos = fextrapolate_line ( aa (direction, 3.14), position,1,2)
    # pygame.draw.polygon (screen, colour, triangle_tip (new_pos, direction, lenght - 4, widht - 4), 0)
    for i in range (0, z ):
        wegwerf, pos_2 = fextrapolate_line ( aa (direction, 3.14), position,0,i)
        if (lenght - i > 0) and (widht - i > 0):
            pygame.gfxdraw.aapolygon (screen, triangle_tip(pos_2, direction, lenght - i, widht - i) , colour)

def filled_triangle (position, direction, lenght, widht, colour):
    direction = aa (direction, 3.14)
    point_m = triangle_middle_2 (position, direction, lenght)
    z = 20
    wegwerf, new_pos = fextrapolate_line ( aa (direction, 3.14), position,1,2)
    # pygame.draw.polygon (screen, colour, triangle_tip (new_pos, direction, lenght - 4, widht - 4), 0)
    for i in range (0, z ):
        wegwerf, pos_2 = fextrapolate_line ( aa (direction, 3.14), position,0,i)
        if (lenght - i > 0) and (widht - i > 0):
            pygame.gfxdraw.aapolygon (screen, triangle_tip(pos_2, direction, lenght - i, widht - i) , colour)

def draw_triangle (position, direction, lenght, widht, colour, **wargs):
    surface = screen
    if 'surface' in wargs: surface = wargs ['surface']
    direction = aa (direction, 3.14)
    
    pygame.gfxdraw.aapolygon (screen, triangle_tip(position, direction, lenght , widht) , colour)






    


    

def vector_int ((a,b)):
    return int (a), int (b)


def int_2_tuple (number_tuple): # verwandelt eine Liste von Zahlen in eine List von integers
    number_list = list (number_tuple)
    list_new = []
    for n in number_list:
        list_new.append (int (n))
    tuple_new = tuple (list_new)
    return tuple_new

def int_4 (tuple_list): # nimmt eine Liste von Tupeln und verwandelt alle Zahlen darin in Integers
    new_list = []
    for t in tuple_list:
        t_new = int_2_tuple (t)
        new_list.append (t_new)
    return new_list

def int_5_tuple (tuple_list): # wie 4, gibt aber tuple aus
    return tuple (int_4 (tuple_list))
        
    
    

def turn_polygon (position, direction,point_list, turn_angle): # turn_angle in Grad! ; direction in Pi! 
    pl = list (point_list)
    new_list = []
    for p in pl:
        dis_p, angle_p = vector_point (position, direction, p)
        p_new = fextrapolate_line (aa (direction + turn_angle / 57 , angle_p), position, 1, dis_p) [1]
        new_list.append (p_new)
    return tuple (new_list)

def adjust_hitbox (position, direction,  hitbox, bullet_position):
    hitbox_plus = list (copy.deepcopy (hitbox))
    
    hitbox_plus.append (bullet_position)

    turned = turn_polygon (position, 0, hitbox_plus  , -direction * 57.3)
    bullet_new = turned [-1]
    hitbox_new = turned [:-1]
    pygame.gfxdraw.aapolygon (screen, hitbox_new, GREEN)
    dot ( bullet_new, WHITE)
    # pygame.time.wait (2000)
    return hitbox_new, bullet_new




def move_normalized_polygon (move_position, point_list): # bewegt ein Polygon mit Mittelpunkt (0,0) auf eine angegebene Position
    new_list = []
    for point in list (point_list):
        new_point = vadd (move_position, point)
        new_list.append (new_point)
    return tuple (new_list)

def turn_normalized_polygon (point_tuple, turn_angle): ## turn_angle in pi
    point_list = list (point_tuple)
    new_list = []
    for point in point_list:
        dis_p, angle_p = vector_point ( (0,0), 0, point)
        p_new = fextrapolate_line (aa (turn_angle, angle_p), (0,0),1, dis_p) [1]
        new_list.append (p_new)
    return tuple (new_list)


def set_to_90 (position, direction, point_list):
    turn_angle = relative_direction (1.57, direction) * (- 57)
    return turn_polygon (position, direction, point_list, turn_angle)
        
        



def normalize_angle (a):
    while a < 0 : a += 2 * 3.141
    while a > 2 * 3.141 : a -= 2 * 3.141
    return a

def aa (a,b): # winkeladdition: addiert die Winkel a und b, so dass ein ergebniss zwischen 0 und 2 * 3.141 herauskommt
    x = normalize_angle (a + b)
    return x

print 'test 209.000   ', aa (0.3 ,-0.2 ) 

def angle_sub (a,b): # substrahiert winkel b von a
    x = normalize_angle (a - b)
    return x
    



def rel_pos ( (x1,y1), (x2,y2)): # gibt die relative Position von objekt 2 zu objekt 1
    x = x2 - x1
    y = y2 - y1
    return (x,y)

def abs_pos ( (xo,yo), (xr, yr)): # errechnet aus der position von Objekt A und der relativen Position eines Objektes B zu A => die absolute Position von B
    x2 = xo + xr
    y2 = yo + yr
    return (x2,y2)

pobject = 10,20
prelativ = -5, -2
pos = abs_pos (pobject, prelativ)
# print ' absolute position  :', pos


def fextrapolate_line (direction, object_position, start_distance, end_distance):
    xo, yo = object_position
    xs = xo + math.sin (direction) * start_distance
    xe = xo + math.sin (direction) * end_distance
    ys = yo + math.cos (direction) * start_distance
    ye = yo + math.cos (direction) * end_distance
    return (xs,ys), (xe,ye) # startpunkt, endpunkt 


def ftarget_direction ((x,y)): # input: relative position des Ziels zum Schiff; Output: die Richtung, in der das Ziel vom Schiff aus liegt
    d = math.atan2 (x,y)
    return d



def ftarget_direction_2 (a,b): # input: position schiff ,, position ziel
    x = rel_pos (a,b)
    return ftarget_direction (x)


def distance ((x,y)):
    dis = (x * x + y * y)**0.5
    return dis

def distance_2 (p_1, p_2):
    r_pos = rel_pos (p_1, p_2)
    return distance (r_pos)

# print 'd test ' , distance_2 ((200,200,), (200,100))




def fline_direction ( startpunkt, endpunkt): # input: zwei punkte einer Linie => Output: die Richtung der Linie
    x1,y1 = startpunkt
    x2, y2 = endpunkt 
    d = math.atan2 ((x2-x1),(y2-y1))
    return d

def middle_line (p_1, p_2, dis_1, dis_2, colour): # zieht eine Linie zwischen zwei Punkten, die aber in einer bestimmten Entfernung vor den Punkten aufhört
    direction = fline_direction (p_1, p_2)
    lenght = distance_2 (p_1, p_2)
    p_s, p_e = fextrapolate_line (direction, p_1, dis_1, lenght - dis_2)
    pygame.draw.aaline (screen, colour, p_s, p_e, 1)

def draw_info_crosshairs (start_point, direction, lenght, colour, number, **wargs):
    secondary = wargs.get ('secondary') 
    background_colour = (60,60,60)
    if 'background_colour' in wargs: background_colour = wargs.get ('background_colour')
    sub_start_point = start_point 
    for i in range (1, int (lenght / 20)):
        sub_start_point, sub_middle_point = fextrapolate_line (direction, start_point, i * 20, i * 20 + 10)
        
        sub_end_point = fextrapolate_line (direction, start_point, i * 20, i * 20 + 20) [1] 
        
        
        if number >= i: pygame.draw.aaline (screen, colour, sub_start_point, sub_middle_point, 1)
        pygame.draw.aaline (screen, background_colour, sub_middle_point, sub_end_point, 1)
            
        
    

def display_missile_cone (position, direction, angle):
    point_a_1, point_a_2 = angle_line (position, direction, 200, angle)
    point_b_1, point_b_2 = angle_line (position, direction, 200, - angle)
    pygame.draw.aaline (screen, BLUE, point_a_1, point_a_2, 1)
    pygame.draw.aaline (screen, BLUE, point_b_1, point_b_2, 1)

def display_engine_flame (position, direction, speed_mode, **wargs):
    if speed_mode == 's': lenght = 5
    elif speed_mode == 'm' : lenght = 12
    elif speed_mode == 'h' : lenght = 21
    elif speed_mode == 'off' : lenght = 0
    else:
        print 'test 440  ', speed_mode 
        raise ValueError ('fucked up') 
    point_1, point_2 = fextrapolate_line (direction, position, 5, 5 + lenght)
    
    pygame.draw.aaline (screen, ORANGE, point_1, point_2, 1) 
    

def middle_line_arrow (p_1, p_2, dis_1, dis_2, colour): # wie middle_line, mit einem zusätzlichen Pfeil 
    direction = fline_direction (p_1, p_2)
    lenght = distance_2 (p_1, p_2)
    p_s, p_e = fextrapolate_line (direction, p_1, dis_1, lenght - dis_2)
    p_t = fextrapolate_line (direction, p_1, dis_1, lenght - dis_2 + 5) [1] ### triangle_point
    pygame.draw.aaline (screen, colour, p_s, p_e, 1)
    pygame.gfxdraw.aapolygon (screen, triangle (p_t, direction, 10, 6), colour)


def line_middle_point (p_1,p_2):
    direction = fline_direction (p_1, p_2)
    lenght = distance_2 (p_1, p_2)
    p_s, p_m = fextrapolate_line (direction, p_1, 0, lenght / 2)
    p_m = (vector_int (p_m))
    return p_m


def display_charge_bar (position, colour, length, charge_status, **wargs):

    surface = screen
    if 'surface' in wargs: surface = wargs ['surface'] 
    charged_point_end = vadd (position, ( math.ceil(charge_status * length) + 1  ,0 ))   #  int (charge_status * length)
    end_point = vadd (position, (length, 0))

    pygame.draw.aaline (surface, BLACK, charged_point_end, end_point, 1)
    pygame.draw.aaline (surface, colour, position, charged_point_end, 1)

    pygame.draw.aaline (surface, BLACK, vadd (charged_point_end ,(0,1)) , vadd (end_point, (0,1)), 1)
    pygame.draw.aaline (surface, colour, vadd (position, (0,1)), vadd (charged_point_end, (0,1)) , 1)

    pygame.draw.aaline (surface, BLACK, vadd (charged_point_end ,(0,-1)) , vadd (end_point, (0,-1)), 1)
    pygame.draw.aaline (surface, colour, vadd (position, (0,-1)), vadd (charged_point_end, (0,-1)) , 1) 
    

    
    

    

def forthogonal_line (startpunkt, richtung, laenge): # gibt zu einer Linie mit einem Startpunkt und einer Richtung eine Orthogonale Linie aus von diesem Startpunkt aus aus
    ro = richtung + 3.141 / 2
    return fextrapolate_line (ro, startpunkt, 0, laenge) # gibt Startpunkt und Endpunkt der orthogonalen Linie aus

def angle_line (startpunkt, richtung, laenge, alpha): # (alpha in GRAD !!!) gibt zu einer Linie mit einem Startpunkt und einer Richtung eine Linie im Winkel alpha aus von diesem Startpunkt aus aus
    ra = aa (richtung, alpha / 57)
    return fextrapolate_line (ra, startpunkt, 0, laenge) # gibt Startpunkt und Endpunkt der neuen Linie aus

def draw_line_direction (startpunkt, direction, length, colour):
    endpunkt = fextrapolate_line (direction, startpunkt, 0, length) [1]
    pygame.draw.aaline  (screen, colour, startpunkt, endpunkt, 1) 


def vector_point (mpoint, direction, outer_point): # berechnet winkel und vektorlaenge, in der ein Punkt von einem Mittelpunkt entfernt liegt
    a = rel_pos (mpoint, outer_point)
    d = ftarget_direction (a)
    dis  = distance (a)
    angle = angle_sub (d,direction)
    return dis, angle

print 'distanz + winkel  ', vector_point ( (10,10), 1.57, (7, 5))

    

def fparralel_start (startpunkt, endpunkt, distanz, laenge): # start- und endpunkt einer parralellen Linie der gleichen Laenge
    xs, ys = startpunkt
    xs, ys = endpunkt
    d = fline_direction (startpunkt, endpunkt)
    throwaway, start_parralel = forthogonal_line (startpunkt, d, distanz)
    start_parralel,end_parralel = fextrapolate_line ( d, start_parralel, 0, laenge)
    return start_parralel, end_parralel # gibt start- und endpunkte der parralelen aus 
    ## ### ### unvollstaendig, es fehlt eine funktion zur errechnung orthogonaler Linien

def display_triangles (position, lenght, widht, distance, colour, angle, content, **wargs):
    surface = screen
    if 'surface' in wargs: surface = wargs ['surface']
    
   

    for e, con in enumerate (content):
        angle_2 = round (aa (3.14, e * angle / 57.3),2) # winkel in 2_Pi 
        
        pos_3 = fextrapolate_line (angle_2, position, 1, distance) [1]

        actual,maximum = con

        primary_factor = int (math.ceil (maximum / 5 ))

        
        
        if primary_factor <= 1:
            secondary_factor, factor_count  = 1, 0
            inner_lines = 0
            outer_lines = 3
            inner_colour = WHITE
            outer_colour = BLUE
            
        elif primary_factor <= 2:
            secondary_factor, factor_count = 2,1
            inner_lines = 0
            outer_lines = 6
            inner_colour = WHITE
            outer_colour = BLUE

            
        elif primary_factor <= 5:
            secondary_factor, factor_count  = 5,2
            inner_lines = 0
            outer_lines = 3
            inner_colour = PURPLE
            outer_colour = PURPLE
            
        elif primary_factor <= 10:
            secondary_factor, factor_count = 10,3
            inner_lines = 0
            outer_lines = 6
            inner_colour = PURPLE
            outer_colour = PURPLE
        elif primary_factor <= 20:
            secondary_factor, factor_count = 20,4
            inner_lines = 1
            outer_lines = 2
            inner_colour = GOLD
            outer_colour = GOLD
        
        elif primary_factor <= 50:
            secondary_factor, factor_count = 50,5
            inner_lines = 1
            outer_lines = 4
            inner_colour = outer_colour = SILVER
        elif primary_factor <= 100:
            secondary_factor, factor_count = 100,6
            inner_lines = 3
            outer_lines = 4
            inner_colour = outer_colour = SILVER
        elif primary_factor <= 500:
            secondary_factor, factor_count = 500, 7
            inner_lines = 0
            outer_lines = 3
            inner_colour = outer_colour = GOLD
        elif primary_factor <= 2500:
            secondary_factor, factor_count = 2500, 8
            inner_lines, outer_lines = 0,6
            inner_colour = outer_colour = GOLD
        else: raise ValueError ('fucked up')

        factor_count = inner_lines + outer_lines - 3 

        actual = int (actual /secondary_factor)
        maximum = int (maximum /secondary_factor)  

        

        shield_list = []

        for i in range (1, maximum + 1):
            if i <= actual: shield_list.append ( 1) 
            else: shield_list.append (0)

        shield_list = shield_list [:5] 

        pos_4 = pos_3
        if e == 3: pos_4 = vadd (pos_4, (-1,0))   ### correction, because the right shield was of 1 pics to the right
        if e == 2: pos_4 = vadd (pos_4 , (0,-1))    ### correction, because the back shield was 1 pic to low
        for f, item in enumerate (shield_list):
            
            
            if shield_list [f] == 0 : shield_colour = WHITE
            elif shield_list [f] == 1: shield_colour = outer_colour
            else: raise ValueError ('fucked up')

            

            pos_4 = fextrapolate_line (angle_2,pos_4, 1, 7 + factor_count) [1]

    

             
            if e in [0, 2] : triple_line_horizontal ( pos_4, (2 + f) * 5, shield_colour, inner_colour = inner_colour, outer_lines = outer_lines, inner_lines=inner_lines, surface = surface)
            elif e in [1,3]: triple_line_vertical ( pos_4, (2 + f) * 5, shield_colour, inner_colour = inner_colour, outer_lines = outer_lines, inner_lines=inner_lines, surface = surface)
            else: raise ValueError ('fucked up') 
            
            

            
        

def display_rects (position, lenght, widht, distance, colour, angle, content, **wargs):
    surface = screen
    if 'surface' in wargs: surface = wargs ['surface']
    # c_list = list (content)
    zaehler_ = - 1 
    for con in content:
        zaehler_ += 1
        a, m = con
        ratio = a / m 
        angle_2 = aa (3.14, zaehler_ * angle / 57.3) # winkel in 2_Pi 
        # throwaway, pos_2 = fextrapolate_line (angle_2, position, 1, (distance + lenght / 2))
        throwaway, pos_3 = fextrapolate_line (angle_2, position, 1, distance)

        lenght_2 = int (ratio * lenght)

        pygame.gfxdraw.aapolygon (surface, rect_tip (pos_3 , aa (angle_2, 3.14), lenght, widht), colour)
        pygame.gfxdraw.aapolygon (surface, rect_tip (pos_3 , aa (angle_2, 3.14), lenght_2, widht), colour)


        
        for i in range (1, lenght_2): pygame.gfxdraw.aapolygon (surface, rect_tip (pos_3 , aa (angle_2, 3.14), i , widht ), colour)


def display_sas_3 ( position,colour, actual_shields,full_shields, actual_armor, full_armor, actual_structure, full_structure, **vargs):
    x = 200
    if 'expand_x' in vargs: x = vargs ['expand_x']
    position = (int (x/2), int (x/2)) 
    shield_generator_damage = vargs.get ('shield_generator_damage')
    engine_damage = vargs.get ('engine_damage') 
    armor = merge_into_tuples (actual_armor, full_armor)
    shields = merge_into_tuples (actual_shields, full_shields)
    guns = vargs.get ('guns')   ### (overall number , damaged guns )
    missiles = vargs.get ('missiles')
    damage_threshold = vargs ['damage_threshold']

    surface = pygame.Surface ( (x,x) )
    # surface = pygame.display.set_mode ( (500,500 ))



    
    #m = multi_octagon_200 ((50,50), 2, 5, colour) 
    #surface.blit (m, (0,0))

    display_rects ( (position), 25,25, 20, GREEN, 90 , armor, surface = surface)
    display_triangles ( (position), 40, 25, 40, BLUE, 90 , shields, surface = surface)

    structure_value = actual_structure / full_structure
    structure_colour = GOLD
    if structure_value == 1: structure_colour = GOLD
    if 1 > structure_value >= 0.8 : structure_colour = YELLOW
    if 0.8 > structure_value >= 0.5 : structure_colour = ORANGE
    if 0.5 > structure_value >= 0.25 : structure_colour = RED_2
    if 0.25 > structure_value: structure_colour = RED

    pygame.gfxdraw.aacircle(surface, position [0], position [1], 19, structure_colour)
    pygame.gfxdraw.aacircle(surface, position [0], position [1], 18, structure_colour)

    if shield_generator_damage >= damage_threshold: generator_colour = RED
    else: generator_colour = GREEN

    engine_colour = GREEN 
    if engine_damage >= damage_threshold: engine_colour = ORANGE
    if engine_damage >= 2 * damage_threshold: engine_colour = RED

    
    write_1b ( 'S', vadd (position, (-4, -16)), generator_colour, 12, surface = surface)
    write_1b ( 'E', vadd (position, (-4, 0)), engine_colour, 12, surface = surface)

    

    for i in range (1, guns [0] + 1):
        dot_colour = RED
        if i > guns [1]: dot_colour = GREEN
        dot ( vadd (position, (-8, -10 + (i - 1) * 7)), dot_colour , surface = surface)

    for i in range (1, missiles [0] + 1):
        dot_colour = RED
        if i > missiles [1] : dot_colour = GREEN
        draw_triangle (vadd (position, ( 9, -12 + (i - 1) * 7)), 0, 5, 6, dot_colour , surface = surface)
    '''
    screen.blit (surface, (0,0))
    pygame.display.update ()
    pygame.time.wait ( 10 * 1000)
    '''

    return surface 
    




#########################################################################################################

def display_engine_status (position, counter, max_counter, current_state_in, set_state_in , **wargs):
    
    position = (0,0)    
    x_seize = 140
    full_x_seize = x_seize * 3 
    expand_x = 'no'
    if 'expand_x' in wargs: expand_x = wargs ['expand_x']
    if expand_x != 'no':
        if expand_x > 1 :
            
            x_seize = int (expand_x / 3)
            full_x_seize = expand_x

    length = x_seize
    circle_radius = 2 

    surface = pygame.Surface ( (full_x_seize, 40 )) 
            
    

    current_state = {'off':0, 's': 1, 'm': 2, 'h': 3}.get (current_state_in)
    set_state = {'off':0, 's': 1, 'm': 2, 'h': 3}.get (set_state_in)

    
    

    if type (current_state) is not int:
        print 'test 120  ', set_state_in, current_state_in 
        raise ValueError ('fucked up')
    
    if type (set_state) is not int:
        print 'test 121  ', set_state_in, current_state_in 
        raise ValueError ('fucked up')


    back_frame (position, full_x_seize, 20, WHITE,2, 2, BLACK, surface = surface)
    write_1b ('Engine Mode', (vadd (position, (10,1))), WHITE, 15,  surface = surface) 
    position = vadd (position, (0,20)) 

    
    
   
    colour_select = {1: RED, 2: ORANGE, 3: GREEN } 
    for i in range (1,4):



        
        colour = colour_select.get (i)


        if i != current_state: colour = darken_colour (colour)
        if i != 1 :  position = vadd (position, (x_seize, 0)) 
    
        ### surrounding_box
        back_frame (position, x_seize, 20, colour,2, 2, WHITE, surface = surface)

        increment_distance = int (length / 12 ) 



        ##### normal active
        if i <= current_state and not ( i == current_state and (i - 1) == set_state ):
            for j in range (1,11):
                pygame.draw.circle (surface, colour, vadd (position, (j * increment_distance, 10)), circle_radius, 0)
                


        ##### normal dark
        if i > current_state and not ( (i - 1) == current_state and i == set_state):
            for j in range (1,11):
                pygame.draw.circle (surface, BLACK, vadd (position, ( j * increment_distance, 10)), circle_radius, 0)
                
            
            
        
        ##### powering down from <i>
        if i == current_state and (i - 1) == set_state: 


        
            for j in range (1,11):

                if j <= ( 10 * counter / max_counter):
                    pygame.draw.circle (surface, colour, vadd (position, ( j * increment_distance, 10)), circle_radius, 0)
                else:
                    pygame.draw.circle (surface, BLACK, vadd (position, ( j * increment_distance, 10)), circle_radius, 0)
        
                

        ##### powering up from i - 1:
        if (i - 1) == current_state and i == set_state:
            colour = brighten_colour (colour)
            for j in range (1,11):
        
                


                if j - 1  <= 10 - ( 10 * counter / max_counter):
                    pygame.draw.circle (surface, colour, vadd (position, ( j * increment_distance, 10)), circle_radius, 0)
                else:
                    pygame.draw.circle (surface, BLACK, vadd (position, ( j * increment_distance, 10)), circle_radius, 0)
            
                    


        ### big circles
        
        if current_state >= i:
            
            pygame.draw.circle (surface, colour, vadd (position, (length - 8,10)), 6, 0)
        else:
            pygame.draw.circle (surface, BLACK, vadd (position, (length -  8,10)), 6, 0)


    return surface 

##################################################################################################




def display_missile_launchers (position, launcher_list, max_counter, **wargs):
    y_space = 0 
    colour = BRIGHT_BLUE
    name = 'MISSILE' 
    if wargs.get ('torpedo') == 'yes' :
        colour = PURPLE
        name = 'TORPEDO'

    height = max (40, 20 + 20 * len (launcher_list)) 

    surface = pygame.Surface ( (100, height)) 


    
    ### Name Box 
    back_frame (position, 100, 20, BLUE,2, 2, WHITE, surface = surface)
    write_1b(name,vadd (position, (8,2 )), colour, 15, surface = surface)
    y_space += 20 

    if len (launcher_list) == 0:
        position = vadd (position, (0,20))
        back_frame (position, 100, 20, BLUE,2, 2, WHITE, surface = surface)
        write_1b('None',vadd (position, (8,2 )), colour, 15, surface = surface)
        y_space += 20 
    
    


    
    for e, launcher in enumerate (launcher_list):
        y_space += 20 

        position = vadd (position, (0, 20))

        ### background 
        back_frame (position, 100, 20, BLUE,2, 2, WHITE, surface = surface)

        

        ### big circle
        if launcher == 0: pygame.draw.circle (surface, colour, vadd (position, (85,10)), 8, 0)
        else: pygame.draw.circle (surface, BLACK, vadd (position, (85,10)), 8, 0)


        ### bar
        display_charge_bar (vadd (position, (5,10)), colour, 60, 1 -  launcher / max_counter, surface = surface)

    return surface 

######################################################################################################
def display_energy_points (position, energy_points, max_energy_points , charge_ratio, **wargs):

    length = 100
    expand_x = 'no'
    if 'expand_x' in wargs: expand_x = wargs ['expand_x']
    length = 100
    if expand_x != 'no':
        if expand_x > 1: length = expand_x

    surface = pygame.Surface ( (length, 60)) 
    
    colour = GOLD

    back_frame (position, length, 20, GOLD, 2,2, WHITE, surface = surface)
    write_1b ( 'Engergy Points', (vadd (position, (3,1))), GOLD, 15, surface = surface) 

    position = vadd (position , (0,20)) 

    back_frame (position, length, 40, GOLD, 2,2, WHITE, surface = surface )

    for i in range (1, max_energy_points + 1):
        if i <= energy_points:display_colour = colour
        else: display_colour = BLACK 
        pygame.draw.circle (surface, display_colour, vadd (position, (20 + (i-1) * 30,15)), 8, 0)


    display_charge_bar (vadd (position, (10,30)), GOLD, length - 20, charge_ratio, surface = surface )

    return surface 

########################################################################################################
def display_booster (position, active, timer_ratio, *args, **wargs):    ### also used for the gliding mechanic
    length = 100
    expand_x = 'no'
    if 'expand_x' in wargs: expand_x = wargs ['expand_x']
    if expand_x != 'no':
        if expand_x > length: length = expand_x

    surface = pygame.Surface ( (length, 40 )) 
    
    colour = GREEN
    name = 'Booster' 

    if 'yes' in args:
        colour = PURPLE
        name = 'Gliding' 

   
    back_frame (position, length, 20, WHITE,2, 2, BLACK, surface = surface)
    write_1b (name, vadd (position, (10,1)), colour, 15, surface = surface) 

    position = vadd (position, (0,20)) 
    
   
    back_frame (position, length, 20, colour, 2,2, WHITE, surface = surface )

    if active == 'yes':
        pygame.draw.circle (surface, colour, vadd (position, (length - 15,10)), 8, 0)
        display_charge_bar (vadd (position, (10,10)), colour, length - 40, timer_ratio , surface = surface)

    elif active == 'no':
        pygame.draw.circle (surface, BLACK, vadd (position, (length - 15,10)), 8, 0)

    return surface 

#######################################################################################################

'''
def display_shield_supercharge (position, phase, timer_ratio, **wargs ):
    surface = screen
    if 'surface' in wargs: surface = wargs ['surface'] 
    colour = GOLD 
    length = 100

    back_frame (position, 200, 20, WHITE,2, 2, BLACK, surface = surface)
    write_1b ('Shield Supercharge' , vadd (position, (5,1)), GOLD, 15, surface = surface) 


    position = vadd (position, (0,20)) 

    

    for i in range (1,3):
        if i != 1: position = vadd (position, (100,0))
        back_frame (position, length, 20, colour, 2,2, WHITE, surface = surface )
        if i == phase: display_charge_bar (vadd (position, (10,10)), colour, length - 40, timer_ratio, surface = surface )

        if i == 2:
            if phase == 2:
                pygame.draw.circle (surface, colour, vadd (position, (85,10)), 8, 0)
            else:
                pygame.draw.circle (surface, BLACK, vadd (position, (85,10)), 8, 0)
                
'''            
        
        
def display_shield_supercharge_b (position,  **wargs ):


   

    player_shield_supercharge_phase = wargs ['player_shield_supercharge_phase']
    player_shield_supercharge_timer = wargs ['player_shield_supercharge_timer']
    shield_supercharge_activation_time = wargs ['shield_supercharge_activation_time']
    shield_supercharge_duration = wargs ['shield_supercharge_duration'] 
    colour = GOLD

    expand_x = 'no'
    if 'expand_x' in wargs: expand_x = wargs ['expand_x']
    length = 100
    full_length = 200
    if expand_x != 'no':
        if expand_x > 1 :
            length = int (expand_x / 2)
            full_length = expand_x 

    surface = pygame.Surface ( (full_length, 40)) 
    
    if player_shield_supercharge_phase == 1: player_shield_supercharge_ratio = player_shield_supercharge_timer / shield_supercharge_activation_time
    elif player_shield_supercharge_phase == 2: player_shield_supercharge_ratio = player_shield_supercharge_timer / shield_supercharge_duration
    elif player_shield_supercharge_phase == 0: player_shield_supercharge_ratio = 0
    else: raise ValueError ('fucked up')

    phase = player_shield_supercharge_phase
    timer_ratio = player_shield_supercharge_ratio

    back_frame (position, full_length, 20, WHITE,2, 2, BLACK, surface = surface)
    write_1b ('Shield Supercharge' , vadd (position, (5,1)), GOLD, 15, surface = surface) 


    position = vadd (position, (0,20)) 

    

    for i in range (1,3):
        if i != 1: position = vadd (position, (length,0))
        back_frame (position, length, 20, colour, 2,2, WHITE, surface = surface )
        if i == phase: display_charge_bar (vadd (position, (10,10)), colour, length - 40, timer_ratio, surface = surface )

        if i == 2:
            if phase == 2:
                pygame.draw.circle (surface, colour, vadd (position, (length - 15,10)), 8, 0)
            else:
                pygame.draw.circle (surface, BLACK, vadd (position, (length - 15,10)), 8, 0)

    return surface 
                
            
        
                
        

################################################################################################################
def display_afterburner (position, activation, acceleration, gliding, cooldown, active_phase, **wargs ):
    border = 0

    expand_x = 'no'
    if 'expand_x' in wargs: expand_x = wargs ['expand_x']
    if expand_x != 'no': expand_x -= border * 2 
    
    
    length = 100
    full_length = 300
    if expand_x != 'no':
        length = int (expand_x / 3)
        full_length = expand_x 
    colour = BRIGHT_BLUE
    surface = pygame.Surface ( (full_length + border * 2, 60 + border * 2 )) 
    

    
    #       frame
    # back_frame (position, full_length + border * 2  , 60 + border * 2 , GREEN, int (border / 1), 1, RED, surface = surface)


    position = vadd (position, (border, border))   ### to account for the 10- points border 
    original_position = position

    #       name 
    back_frame (position, length * 3 , 20, BLUE, 2, 2, BLACK, surface = surface)
    write_1b ('Afterburner', vadd (position, (10,1)), colour, 15, surface = surface ) 

    original_position = vadd (original_position, (0,20))
    position = vadd (position, (0,20)) 

    ### activation

    if active_phase == 1:
        back_colour = WHITE
        display_bar = activation
    else:
        back_colour = BLACK
        display_bar = 0

        
    
    
    
    back_frame (position, length, 20, BLUE,2, 2, back_colour, surface = surface)
    display_charge_bar (vadd (position, (10,10)), BRIGHT_BLUE, length - 20, display_bar, surface = surface)

    ### acceleration

    position = vadd (position, (length, 0))
    if active_phase == 2:
        back_colour = WHITE
        display_bar = acceleration
    else:
        back_colour = BLACK
        display_bar = 0 
    
    back_frame (position, length, 20, BLUE,2, 2, back_colour, surface = surface)
    display_charge_bar (vadd (position, (10,10)), BRIGHT_BLUE, length - 20, display_bar, surface = surface )

    ### gliding_time

    position = vadd (position, (length, 0))
    if active_phase == 3:
        back_colour = WHITE
        display_bar = gliding
    else:
        back_colour = BLACK
        display_bar = 0 
    back_frame (position, length, 20, BLUE,2, 2, back_colour,surface = surface)
    display_charge_bar (vadd (position, (10,10)), BRIGHT_BLUE, length - 20, display_bar,surface = surface)

    ### cooldown

    position = vadd (original_position, (0,20))
    if active_phase == 0:
        back_colour = WHITE
        display_bar = cooldown 
    else:
        back_colour = BLACK
        display_bar = 0 
    back_frame (position, full_length , 20, RED,2, 2, back_colour,surface = surface)
    display_charge_bar (vadd (position, (10,10)), BRIGHT_BLUE, full_length - 40, display_bar,surface = surface)
    if display_bar == 1:
        pygame.draw.circle (surface, colour, vadd (position, (full_length - 15, 10 )), 8, 0)
    else:
         pygame.draw.circle (surface, BLACK, vadd (position, (full_length - 15, 10 )), 8, 0)


    return surface
                            
                            
        
################################################################################################################



################################################################################################################
def display_killed_ships (position, killed_ship_list, x_seize, back_colour): 
    
    frame = pygame.Surface ( (x_seize, 20 )) ### changed !!! 500 instead of "x_seize" !!!
    frame.fill (back_colour)
    write_1b ( 'kills :  ',(10,2), GREEN, 12, surface = frame)

    for e, s in enumerate (killed_ship_list):
        display_position = ((50 + (e + int (e / 5)) * 20, 10)) 
        
        
        s (frame, display_position) 
    return frame 
##################################################################################################################     


###########################################################################################################################  

def fheat_cone (flight_direction, ship_position, missile_position, cone_angle):
    relative_missile_position = rel_pos ( ship_position, missile_position)
    in_cone = 0 # default- ergebnis: target ist nicht in cone
    cone_angle = 1.0 * cone_angle / 57
    # print 'cone_angle  :' , cone_angle
    back_direction = flight_direction - 3.141
    back_direction = normalize_angle (back_direction)
    x,y = relative_missile_position
    t_direction = math.atan2 (x,y)
    t_direction = normalize_angle (t_direction)
    #print 'back direction  :', back_direction
    #print 'target_direction  :', t_direction 
    diff = math.fabs ( back_direction - t_direction)
    #print ' diff  :', diff, 'diff in grad', diff * 57
    if diff <= cone_angle: in_cone = 1
    return in_cone


def fradar_cone (flight_direction, missile_position, target_coordinates, cone_angle): # cone_angel: winkel vom mittelpunkt, in Grad ## returns 0 falls nicht in cone, 1 falls in cone
    in_cone = 0 # default- ergebnis: target ist nicht in cone
    cone_angle = 1.0 * cone_angle / 57
    # print 'cone_angle  :' , cone_angle
    x,y = target_coordinates
    t_direction = ftarget_direction_2 (missile_position,target_coordinates) # input: position schiff ,, position ziel (x,y)
    t_direction = normalize_angle (t_direction)
    # print 'flight direction  :', flight_direction
    #print 'target_direction  :', t_direction 
    diff = math.fabs ( flight_direction - t_direction)
    # print ' diff  :', diff, 'diff in grad', diff * 57
    if diff <= cone_angle: in_cone = 1
    return in_cone

ltest1 = []
ltest2 = [1]
print 'laenge ltest1  :', len (ltest1)
print 'laenge ltest2  :', len (ltest2) 

fd1 = 3.141 / 2 
tc1 = - 50 , 28
ca1 = 35

p1 = 200,250
p2 = 210,400
direc = fline_direction (p1,p2)

par = fparralel_start  (p1, p2, 50, 100)
par1, par2 = par

al1, al2 = angle_line (p1, direc, 100, 90)




############
###### Beginn Graphik
###########

if __name__ == "__main__":

    screen.fill((0, 0, 0))
    m = multi_octagon_200 ((50,50), 3, 5, RED)
    screen.blit (m, (300,300)) 
    

    



##############
pygame.display.flip()
   

    
    
