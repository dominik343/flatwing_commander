# -*- coding: cp1252 -*-

### version 153     :: changed the main loop into a function 
### version 153d    :: removed variable "log_mode"
### version 153e    :: solved lead ship crash bug :: there need to be two different variables for lead_ship and for autopilot_lead_ship
### version 153g    :: solved: missile kills did not count as kills
### version 153i    :: solved: custom missions crashed if no player ship was selected
### version 154     :: solved: GetSystemMetrics works now (on windows only)
### version 154xx   :: Make the Menues less colourful, fewer borders
### version 155     :: solved bug: custom mission screen > most of the display buttons did not work
### version 155a    :: custom mission screen: added ship details to display
### version 155b    :: renamed "constructor___ship_button_command" to "constructor___ship_select_command"
### version 155c    :: removed all images and image references  ;;;  made briefing screen less colourful and fewer borders

### version 156     :: changed Radar Colour to self.colour  ;;; changed enemy colour from Orange to RED
### version 157     :: deleted "linux" switch
### version 158     :: changed player ship colour to White ;;; added function : "complete_half_ship"  ;;; changed Drahlthi ship model ;;; changed Talon ship model 
### version 159     :: added ship model: Dragon Missile Boat
### version 160     :: custom mission: when player ship has been selected, player-enemy-wingman - radiobutton automatically switches to 'enemy' 
### version 160a    :: removed nonfunctional Buttons from Main Menu
### version 160b    :: added ship model: SHRIKE
### version 160c    :: changed function "complete half ship" to eliminate points that are doubles
### version 160d    :: de-coloured debriefing screen
### version 160e    :: changed MESSERSCHMIDT Model
### version 160f    :: enlarged target_brackets by factor 1.5
### version 160g    :: Custom_Mission_Menus: small improvements
### version 160i    :: added DEMON to Pirate Fighters
### version 160j    :: split SCYLLA into Empire version and outdated pirate version
### version 161     :: small change to "hit" method: turrets are only hit if the shields are already down or the bullet/missile is shieldbreaking
### version 161a    :: enhanced HAMMERHEAD's turret hitpoints to 4.
### version 162b    :: mission_running now has values '0' for 'no', ;; '1' for 'campaign_mission' ;; '2' for 'custom_mission'    ;;;; >>> solved the bugs : 1) Campaign Debriefing for Custom Missions , 2) Campaign count increased by playing custom missions
### version 162c    :: moved target ship name 100 pixels up
### version 162d    :: using numpad 1-3 for primary, secondary, tertiary goals works again
### version 162e    :: added descriptions to cannons
### version 162f    :: ship blinks while cloaking / decloaking
### version 162g    :: solved bug: cloaked, cloaking and decloaking ships now properly cannot shoot missiles or torpedoes anymore. 
##############################      

from __future__ import division

import pygame
import math
import copy
import random
import re
import os

import dfunctions2 as dfunctions



try:
    from win32api import GetSystemMetrics
except: pass 

import Tkinter


INCLUDE_IMAGES = 'no'
DEBUG_MODE = 'no'



pygame.init ()
pygame.joystick.init()
joystick = 'no'
if pygame.joystick.get_count () > 0:
    joy_1 = pygame.joystick.Joystick (0)
    joy_1.init ()
    joystick = 'yes'



pygame.font.init ()
clock = pygame.time.Clock ()




try:
    import ctypes
    user32 = ctypes.windll.user32
    SCREEN_X = user32.GetSystemMetrics (0)
    SCREEN_Y = user32.GetSystemMetrics (1) -50
except:
    SCREEN_X = 1500
    SCREEN_Y = 1100







screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y),)  ###         , pygame.FULLSCREEN











SCREEN_SPLIT = SCREEN_X - 400

SCREEN_SPLIT_Y = 400 
LEFT_LIMIT = 1
RIGHT_LIMIT = SCREEN_SPLIT
MIDDLE = ( int (SCREEN_SPLIT / 2), int (SCREEN_Y / 2))
NEGATIVE_MIDDLE = dfunctions.skalar_multi (-1, MIDDLE)
SECOND_MIDDLE = ( int (( SCREEN_X + SCREEN_SPLIT) / 2), int ( SCREEN_Y / 2) )
SECOND_MIDDLE = ( int (( SCREEN_X + SCREEN_SPLIT) / 2), 200) 
PLAYER_SAS_POSITION = (100,100)
TARGET_SAS_POSITION = (100, SCREEN_Y - 95)
PI_FACTOR = 180 / math.pi
LEFT_MAIN_BORDER = 250
LEFT_MISSILE_DISPLAY_BORDER = 130

RIGHT_FIELD_SEIZE = 340
LEFT_TOP_FIELD_Y = 295
LEFT_BOTTOM_FIELD_Y = 300 


UPPER_RIGHT_WINDOW = {'position': ( SCREEN_X - 400, 0), 'x_seize': 340, 'y_seize': 400 }
LOWER_RIGHT_WINDOW = {'position': (SCREEN_X - 340, SCREEN_Y - 400), 'x_seize': 340, 'y_seize': 400 }



### defines the screen area that is updated EVERY frame and the border fields, only to be updated each 10th frame:
CENTRAL_FIELD = [ (255,40,SCREEN_X - 255 - RIGHT_FIELD_SEIZE, SCREEN_Y - 40), (131, 295, 124,SCREEN_Y - LEFT_TOP_FIELD_Y - LEFT_BOTTOM_FIELD_Y)  ]


###

DISPLAY_MISSILE_CONE = 'no' ### 'yes' ;;; 'no'
DISPLAY_SHIELD_AXIS = 'no' ### 'yes' ;;; 'no'

GOAL_DISPLAY_POSITION = (1000,300) 


radar_factor = 20           ### +++  global in mainloop
speed_factor = 0.03         ### ---  needs not be in mainloop 




start_debriefing_screen = 'no'  ### +++  global in mainloop 

autopilot_destination = None  ### +++  global in mainloop
running_mission_info = None  ### +++  global in mainloop 




log_factor = 1 ### verkleinerungsfaktor des Hauptschirms   /// +++ global in mainloop 




target_count = 1 ### +++ global in mainloop 

recreate_stars = 'no' ### +++ global in mainloop 



shield_recharge_per_frame = 1 / 100



object_list = ['dummy']
master_object_counter = 0
master_frame_counter = 0
ship_list = []
trigger_point_list = []
bullet_list = []
asteroid_list = [] 
missile_list = []
explosion_list = []
turret_list = []
cannon_list = []
debris_list = []
global_target_object_id = None
display_heat_cones = 0
manual_turrets = 'no'    ### if 'yes': player controls his turrets manually
persistant_dot_list = []
mission_goal_results = {}
success_level = None




frame_rate = 10
speed_loss_turn = 0 
ship_accel_factor = 0.1
AFTERBURNER_ACTIVATION_TIME = 180
AFTERBURNER_ACCELERATION_TIME = 150
AFTERBURNER_GLIDING_TIME = 300
AFTERBURNER_COOLDOWN = 1200

MISSILE_COOLDOWN = 800
ENERGY_POINTS_CHARGE_TIME = 1200
BOOSTER_DURATION = 300
GLIDING_DURATION = 450

SHIELD_SUPERCHARGE_ACTIVATION_TIME = 500
SHIELD_SUPERCHARGE_DURATION = 300 



RED = (255, 0, 0)
GREEN = (0,255,0)
LIGHT_GREEN = (40,255,40)
BLUE = (0,0, 255)
LIGHT_BLUE = (80,80,255)
LIGHT_BLUE_2 = (120,120,255) 
BLUE_2 = (0,0,160)
BLUE_3 = (0,0,100)
BROWN = (139,69,19)
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
BLUE_WHITE = BRIGHT_BLUE = (150,230,255)
FAINT_WHITE = (50,50,50)

player_sas_graphics = None
target_sas_graphics = None

PILOT_QUALITY = {'ace': [0,0], 'excellent' : [0.1, 1 ], 'good' : [0.2,3], 'average': [0.4, 4.5], 'poor' : [1, 6] , 'abysmal': [2, 10]}



### Definition of Weapons


TOKEN = {'name': 'token', 'range': 500, 'velocity': 250, 'damage': 1.5, 'cooldown': 1, 'maximum_load': 0, 'ammo_weapon': 'no', 'colour': ORANGE}

LASER = {'name': 'laser', 'range': 500, 'velocity': 250, 'damage': 1.5, 'cooldown': 1, 'maximum_load': 7, 'ammo_weapon': 'no', 'colour': ORANGE, 'description': 'The most common fighter weapon. Decent combination of range,muzzle velocity and damage per time.'}
PARTICLE = {'name': 'particle', 'range': 650, 'velocity': 350, 'damage': 6, 'cooldown': 7, 'maximum_load': 4, 'ammo_weapon': 'no', 'colour': MAGENTA, 'description': 'Sniper Weapon. Long range; A single shot does high damage, but damage per time is low due to low rate of fire.'}

SF_LASER = {'name': 'sf_laser', 'range': 300, 'velocity': 250, 'damage': 1.5, 'cooldown': 1, 'maximum_load': 7, 'ammo_weapon': 'no', 'colour': ORANGE}
OLD_LASER = {'name': 'old_laser', 'range': 400, 'velocity': 250, 'damage': 1.5, 'cooldown': 1, 'maximum_load': 7, 'ammo_weapon': 'no', 'colour': ORANGE}
# ION = {'name': 'ion', 'range': 300, 'velocity': 200, 'damage': 0.5, 'cooldown': 1, 'maximum_load': 10, 'ammo_weapon': 'no', 'colour': GOLD, 'ion_damage': 'yes'}
MASS = {'name': 'mass', 'range': 300, 'velocity': 170, 'damage': 2.2, 'cooldown': 3, 'burst': 4, 'maximum_load': 5, 'ammo_weapon': 'no', 'colour': GREY , 'description': 'The Mass Driver Cannon inflicts insane amounts of damage at medium range. It fires bursts of four shots each.'}
NEUTRON = {'name': 'neutron', 'range': 220, 'velocity': 120, 'damage': 4, 'cooldown': 2.5, 'maximum_load': 3, 'ammo_weapon': 'no', 'colour': BLUE, 'ion_damage': 'yes', 'description': 'The Neutron Cannon is a powerful short- range weapon. A single hit is enough to kill the shields of a light fighter, but its low muzzle velocity and rate of fire make it difficult to hit with. It circumvents Armor: All damage that bypasses the shields goes directly to the internal systems.'}
STARFIRE = {'name': 'starfire', 'range': 800, 'velocity': 500, 'damage': 10, 'cooldown': 4, 'maximum_load': 4, 'ammo_weapon': 'no', 'colour': YELLOW, 'shield_piercing': 'yes', 'description': 'Extreme Range. Extreme Firepower. Shield- Piercing. The largest and most powerful fighter Weapon ever.'}
PLASMA = {'name': 'plasma', 'range': 120, 'velocity': 70, 'damage': 12, 'cooldown': 5, 'maximum_load': 2, 'ammo_weapon': 'no', 'colour': RED, 'description': 'In many ways a more extreme version of the Neutron Cannon: A single hit deals insane amounts of damage, but you will have a hard time hitting a moving target.'}

AM_10 = {'name': 'antimatter 10', 'range': 2500, 'velocity': 100, 'damage': 100, 'cooldown': 10, 'maximum_load': 1, 'ammo_weapon': 'no', 'colour': BLUE, 'second_colour': WHITE, 'antimatter': 'yes', 'display_radius': 4}
AM_20 = {'name': 'antimatter 20', 'range': 5000, 'velocity': 100, 'damage': 500, 'cooldown': 20, 'maximum_load': 1, 'ammo_weapon': 'no', 'colour': BLUE, 'second_colour': WHITE, 'antimatter': 'yes', 'display_radius': 6}
AM_40 = {'name': 'antimatter 40', 'range': 10000, 'velocity': 100, 'damage': 2000, 'cooldown': 30, 'maximum_load': 1, 'ammo_weapon': 'no', 'colour': BLUE, 'second_colour': WHITE, 'antimatter': 'yes', 'display_radius': 8}

PHASE_TRANSIT = {'name': 'phase transit', 'range': 20000, 'velocity': 1000, 'damage': 20000, 'cooldown': 60, 'maximum_load': 1, 'ammo_weapon': 'no', 'colour': BLUE, 'second_colour': MAGENTA, 'antimatter': 'yes', 'display_radius': 12}

AK_80MM_20S = {'name': 'ak_80mm_20s', 'range': 500, 'velocity': 250, 'damage': 1.5, 'cooldown': 1, 'maximum_load': 20, 'ammo_weapon': 'yes', 'colour': GREY }

FLAK = {'name': 'flak', 'range': 1500, 'velocity': 300, 'damage': 8, 'cooldown': 1, 'maximum_load': 1, 'ammo_weapon': 'no', 'colour': GOLD, 'explosion': 'yes', 'explosion_radius': 40 }


### Definition der Raketen und Torpedos
HEAT_SEEKING = [ 'heatseeking', [110,50,10,1], RED, {'damage': 'm1' } ]
RADAR = [ 'radar', [70,30,6,1], BLUE, {'damage': 'm1' } ]
DUMBFIRE = [ 'dumbfire', [150,0,15,10], GREEN , {'damage': 'm1' , 'explosion_radius': 5}]
DUMB_DELAYED = ['dumb_delayed', [60,0,1,15], ORANGE, {'damage': 'm1' , 'explosion_radius': 10} ]
HEAVY_DUMB = [ 'heavy_dumb', [60,0,1,10], GOLD, {'damage': 'm2', 'explosion_radius': 1 } ] 
MINE = [ 'mine', [0,0,10,0], YELLOW, {'damage': 'm1' }]
DELAYED_EXPLOSION = [ 'delayed', [0,0,0,30], WHITE , {'damage': 'm1' }]
DUMB_DELAY = 6 ### time: delayed explosion of dumb2 missile
MICRO = ['micro', [60,40,1,1], GREEN, {'damage': 5 }]

TORPEDO = ['torpedo', [20,1,0.2,0], BLUE, {'range': 4000, 'damage': 't' } ]



ALL_LETHAL = {
    'm1': 'lethal',
    'm2': 'lethal',
    't': 'lethal'
    }

MISSILE_DAMAGE_MATRIX = {
    'mine':ALL_LETHAL,
    'fighter': ALL_LETHAL,
    'bomber': {
        'm1': 3,
        'm2': 'lethal',
        't': 'lethal'
        },
    'light_capital': {
        'm1': 0,
        'm2': 20,
        't': 'lethal'
        },
    'large_capital': {
        'm1': 0,
        'm2': 20,
        't': 1000
        },
    'asteroid': {
        'm1': 20,
        'm2': 50,
        't': 1000
        }
    }


def complete_half_ship (input_list):  ### ship graphics : takes the left side of the ship graphic dots and adds the symmetric right half 
    reversed_list = input_list [::-1]

    mirror_points = [ (-x [0], x [1]) for x in reversed_list ]

    out_list = input_list + mirror_points

    ### remove double points
    compare_list = []
    for p in out_list:
        if p in compare_list:
            out_list.remove (p) 
        compare_list.append (p) 

    return out_list 









SALTHI = {'name': 'salthi', 'movement': (70,70,2,170), 'sas': [[2,1,1,1],[2,1,1,1],[1],[0,0,0,0] ], 'guns':  [ (LASER, 5, -1), (LASER, 5, 1) ], 'missile_launchers': 0, 'graphics': ['polygon', (  (-2.5, -4), (-6.5,-1), (-6.5,1), (-2.5,-1), (-2.5,2), (-1.5, 4), (1.5,4), (2.5,2), (2.5, -1), (6.5,1), (6.5, -1), (2.5, -4)   )], 'hitbox':  ['standart', 3], 'turrets': [], 'ship_class': 'fighter', 'description': 'Very fast and maneuverable, extremely fragile' }


DRAHLTI = {'name': 'drahlti', 'movement': (50,50,2,120), 'sas': [[6,4,4,4],[4,3,3,3],[10],[0,0,0,0] ], 'guns':  [ (LASER, 5, -1), (LASER, 5, 1) ], 'missile_launchers': 0, 'graphics': ['polygon', complete_half_ship ( [ (-2,-3), (-4,-2), (-4,0), (-3,2), (-1,3), (-1,1) ])], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter' , 'description': 'the Empire\' s standart light fighter. Has a lower turn rate than the hornet, but stronger shields.'}
HORNET = {'name': 'hornet', 'movement': (50,60,2,150), 'sas': [[5,3,3,3],[4,3,3,3],[10],[0,0,0,0] ], 'guns':  [ (LASER, 5, -1), (LASER, 5, 1) ], 'missile_launchers': 0, 'graphics': ['polygon',( (0,-4), (-2,-4), (-2,-5), (-3,-5), (-3,-4), (-6,-4), (-1,1), (-3,3), (0,6), (3,3), (1,1), (6,-4), (3,-4), (3,-5), (2,-5), (2,-4))  ], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter', 'description': 'The Federations standart light fighter ist fast and agile. Its Firepower is not impressive, but enough to get the job done.' }
TIE = {'name': 'tie', 'movement': (30,30,1,50), 'sas': [[0.1,0.1,0.1,0.1],[0.5,0.5,0.5,0.5],[0.1],[0,0,0,0] ], 'guns':  [ (SF_LASER, 3, 0) ], 'missile_launchers': 0, 'graphics': ['polygon', ( (-1,3), (-1, - 1),(-2,1), (-1,3), (1,3), (2,1), (1,-1), (1,-3)     )], 'hitbox':  ['standart', 2], 'turrets': [], 'ship_class': 'fighter' , 'decription': 'Micro- Fighter. These tiny spacecraft are just big enough to carry a pilot, engines, and a gun. Slow and fragile, only dangerous in great numbers.' }

RAPIER = {'name': 'rapier', 'movement': (55,60,2,150), 'sas': [[10,5,10,5],[4,3,3,3],[10],[0,0,0,0] ], 'guns':  [ (LASER, 5, -1), (LASER, 5, 1), (LASER, 5, 0) ], 'missile_launchers': 2, 'graphics': ['polygon', ( (-2,-6), (-2,-5), (-5,-5), (-3,-1),(-1,-1), (-1,2), (-3,2), (0,6), (3,2), (1,2), (1,-1), (3,-1), (5,-5), (2,-5), (2,-6)               )], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter' , 'description': 'The Federations newest Heavy Fighter. The best Mix of Agility, Armament and Protection available.' }
RAPIER_B = copy.deepcopy (RAPIER)
RAPIER_B ['name'] = 'rapier B'

RAPIER_B ['guns'] = [  (NEUTRON, 20, 0) ] 
SABRE = {'name': 'sabre', 'movement': (40,40,2,100), 'sas': [[15,8,15,8],[10,10,10,10],[15],[0,0,0,0] ], 'guns':  [ (LASER, 5, -1), (LASER, 5, 1),(LASER, 7, -1), (LASER, 7, 1) ], 'missile_launchers': 2, 'torpedo_launchers': 1, 'graphics': ['polygon', (          (-4,-10),(-6,-9),(-6,-6),(-5,-4),(-3,-2),(-1,-1),(-1,1),(-2,5),(-2,7),(-1,10),(1,10),(2,7),(2,5),(1,1),(1,-1),(3,-2),(5,-4),(6,-6),(6,-9),(4,-10)        )], 'hitbox':  ['standart', 6], 'turrets': [{'guns': [(LASER,-1), (LASER, 1)],
                  'vertical_position': -3,
                  'horizontal_position': 0,
                  'alignment': 3.14,
                  'left_area': 1.57,
                  'right_area': 1.57}], 'ship_class': 'bomber',
         'description': 'Light Bomber'}

SCYLLA = {'name': 'scylla', 'movement': (20,20,2,50), 'sas': [[15,10,15,10],[10,10,10,10],[15],[0,0,0,0] ], 'guns':  [ (LASER, 5, 4), (LASER, 5, 3),(LASER, 5, 2), (LASER, 8, 1),(LASER, 8, 0), (LASER, 8, -1) ], 'missile_launchers': 0, 'torpedo_launchers': 0, 'graphics': ['polygon', [ (-5,-10), (-11,-5),(-8,0), (-8,6), (-6,8), (-4,6),(-4,3),(-2,2),(-2,0),(1,0),(1,2),(2,3),(7,3),(9,0),(9,-3),(6,-10)      ]], 'hitbox':  ['standart', 10], 'turrets': [{'guns': [(LASER,-2),(LASER,-1),(LASER,0),(LASER,1)],
                  'vertical_position': 0,
                  'horizontal_position': - 5,
                  'alignment': 4.71,
                  'left_area': 1.57,
                  'right_area': 1.57}], 'ship_class': 'bomber',
          'description': 'The Scylla\' s quad laser turret covers the entire right hemissphere, but the Scylla is vulnerable to attacks from the left'}

SCYLLA_P = {'name': 'scylla P', 'movement': (20,20,2,50), 'sas': [[15,10,15,10],[10,10,10,10],[15],[0,0,0,0] ], 'guns':  [ (OLD_LASER, 5, 4), (OLD_LASER, 5, 3),(OLD_LASER, 5, 2), (OLD_LASER, 8, 1),(OLD_LASER, 8, 0), (OLD_LASER, 8, -1) ], 'missile_launchers': 0, 'torpedo_launchers': 0, 'graphics': ['polygon', [ (-5,-10), (-11,-5),(-8,0), (-8,6), (-6,8), (-4,6),(-4,3),(-2,2),(-2,0),(1,0),(1,2),(2,3),(7,3),(9,0),(9,-3),(6,-10)      ]], 'hitbox':  ['standart', 10], 'turrets': [{'guns': [(OLD_LASER,-2),(OLD_LASER,-1),(OLD_LASER,0),(OLD_LASER,1)],
                  'vertical_position': 0,
                  'horizontal_position': - 5,
                  'alignment': 4.71,
                  'left_area': 1.57,
                  'right_area': 1.57}], 'ship_class': 'bomber',
          'description': 'The Pirates use an outdated version of the Scylla with outdated (shorter range) Weapons'}



SHRIKE = {'name': 'shrike', 'movement': (65,30,2,150), 'sas': [[25,15,15,15],[10,10,10,10],[15],[0,0,0,0] ], 'guns':  [ (LASER, 5, -1), (LASER, 5, 1) ], 'missile_launchers': 0, 'torpedo_launchers': 1,  'graphics': ['polygon', complete_half_ship ([ (-5,-8), (-3,-4), (-3,1), (-4,7),(-2,9), (0,7)  ])], 'hitbox':  ['standart', 6], 'turrets': [], 'ship_class': 'bomber', 'description': 'Hyperspeed Bomber. It can easily outrun any enemy fighter except the salthi' }


KOMET = {'name': 'komet', 'movement': (30,60,2,150), 'sas': [[5,3,3,3],[4,3,3,3],[10],[0,0,0,0] ], 'guns':  [ (NEUTRON, 5, -1), (NEUTRON, 5, 1),(NEUTRON, 3, -1), (NEUTRON, 3, 1) ], 'missile_launchers': 0, 'graphics': ['polygon', ( (-2,-5), (-5,-3),(-5,1),(-3,5),(-2,-1),(2,-1),(3,5),(5,1),(5,-3),(2,-5)         )], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter', 'afterburner_gliding_multiplicator': 2, 'afterburner_activation_modificator': 0.2, 'afterburner_acceleration_modificator': 0.2, 'afterburner_cooldown_modificator': 0.2 , 'description': 'The Komet features an improved afternburner system with reduced acceleration and cooldown time, and increased gliding time. It is designed for gliding drive- by shootings'}

TEST = {'name': 'test', 'movement': (50,60,2,150), 'sas': [[500,300,300,300],[4,3,3,3],[10],[0,0,0,0] ], 'guns':  [ (LASER, 5, -1), (LASER, 5, 1) ], 'missile_launchers': 0,'torpedo_launchers': 2,  'graphics': ['polygon', ( (-2,-5), (-5,-3),(-5,1),(-3,5),(-2,-1),(2,-1),(3,5),(5,1),(5,-3),(2,-5)         )], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter' }

TALON = {'name': 'talon', 'movement': (50,40,2,120), 'sas': [[3,2,2,2],[3,2,2,2],[10],[0,0,0,0] ], 'guns':  [ (OLD_LASER, 5, 0) ], 'missile_launchers': 0, 'graphics': ['polygon', complete_half_ship ( [ (-3,-6),(-3,-3), (-1,-1), (-1,2), (-2,3), (-2,5), (-1,6) ]) ], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter' , 'damage_threshold': 2, 'kill_value': 300, 'description': 'Outdated. Fast, but poorly armed and protected'}
DEMON = {'name': 'demon', 'movement': (35,60,2,100), 'sas': [[5,2,2,2],[3,2,2,2],[10],[0,0,0,0] ], 'guns':  [ (AK_80MM_20S, 5, 0) ], 'missile_launchers': 0, 'graphics': ['polygon', ((-4,-6), (-4,-5), (-8,-4), (-8,-2), (-5,-1), (-5,0), (-4,2), (-4,4), (-3,6), (-2,6), (-2,4), (2,4), (2,6), (3,6), (4,4), (4,2), (5,0), (5,-1), (8,-2), (8,-4), (4, -5), (4,-6) )], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter' , 'damage_threshold': 2, 'description': 'Outdated. Slow, but more maneuverable than the Talon. The single gun carries only limited ammo'}

SCIMITAR = {'name': 'scimitar', 'movement': (40,40,2,120), 'sas': [[8,5,5,5],[8,6,6,6],[3],[0,0,0,0] ], 'guns':  [ (MASS, 5, -1), (MASS, 5, 1) ], 'missile_launchers': 1, 'graphics': ['polygon', ( (-4,-6), (-4,4), (-3,4), (-3,-3), (-2,-1), (-2,6), (-1,8), (1,8),(2,6),(2,-1),(3,-3), (3,4), (4,4), (4,-6)              )], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter', 'description': 'Medium Fighter. Slow and ungainly, but its powerful mass driver cannons and the missile launcher make up for it.' }

JALTHI = {'name': 'jalthi', 'movement': (35,30,2,100), 'sas': [[15,10,10,10],[10,5,5,5],[6],[0,0,0,0] ], 'guns':  [ (LASER, 5, -1), (LASER, 5, 1),(LASER, 7, 1),(LASER, 7, -1),(LASER, 5, 2),(LASER, 5, -2) ], 'missile_launchers': 0, 'graphics': ['polygon', ( (-4,-5), (-7,0), (-5,3), (-5,6), (-4,6), (-4,3), (-3,3), (-2,2), (-2,5), (-1,5), (-1,2), (1,2), (1,5), (2,5), (2,2), (3,3), (4,3), (4,6), (5,6), (5,3), (7,0), (4,-5)                   )], 'hitbox':  ['standart', 5], 'turrets': [], 'ship_class': 'fighter' , 'description': 'Heavy Fighter. Its six laser cannons can take on any fighter head-on, but once the enemy gets behind, the Jalthi is screwed'}

HAMMERHEAD = {'name': 'hammerhead',
              'movement': (50,60,2,150),
              'sas': [[5,3,3,3],[4,3,3,3],[3],[0,0,0,0] ],
              'guns':  [ ], 'missile_launchers': 0,
              'graphics': ['polygon',[ (- 2,-4), (-8,-1), (-8,3), (-3,0), (-2,4), (-3,5), (-3,7), (-2,6), (2,6), (3,7), (3,5), (2,4), (2,1), (3,0), (8,3), (8,-1), (2, -4)        ]],
              'hitbox':  ['standart', 4],
              'turrets': [{'guns': [ (LASER, -1), (LASER, 1) ],
                           'vertical_position': 2,
                           'horizontal_position': 0,
                           'alignment': 1.57,
                           'left_area': 3.14,
                           'right_area': 3.14,
                            'hit_points': 4}],
              'ship_class': 'fighter' }

DEADMAN =   {'name': 'deadman',
              'movement': (10,1,1,0),
              'sas': [[30,30,30,30],[25,25,25,25],[1],[0,0,0,0] ],
              'guns':  [ ], 'missile_launchers': 0,
              'graphics': ['polygon', [ [ 3 * x [0], 3 * x [1]] for x in    [[-1, -6], [-3, -5], [-5, -3], [-6, -1], [-6, 1], [-5, 3], [-3, 5], [-1, 6], [-1,7], [0,8],  [1,7], [1, 6], [3, 5], [5, 3], [6, 1], [6, -1], [5, -3], [3, -5], [1, -6]]] ],
              'hitbox':  ['standart', 18],
              'turrets': [{'guns': [ (AK_80MM_20S, -1), (AK_80MM_20S, 1) ],
                           'vertical_position': 2,
                           'horizontal_position': 18,
                           'alignment': 1.57,
                           'left_area': 1.8,
                           'right_area': 1.8},
                          {'guns': [ (AK_80MM_20S, -1), (AK_80MM_20S, 1) ],
                           'vertical_position': 2,
                           'horizontal_position': -18,
                           'alignment': 4.7,
                           'left_area': 1.8,
                           'right_area': 1.8}], 
              'ship_class': 'light_capital',
             'description': 'Light Tanker. Vulnerable, Combustible, Expendable' }

claw_box = ['nonstandart', 160, [[ (-80,-140), (-80, -20), (80, -20),(80, -140) ] , [ (-40,-20), (-40,120),(40,120),(40, -20) ] ] ] 
moron_box = ['nonstandart', 40,  [[(-10,-35), (-30,-35), (-30,35), (-10,35)] ,[ (10,-35), (30,-35), (30,35), (10,35)]]]
ralari_box = ['nonstandart', 52,  [[(-9,-52), (-9,52), (9,52), (9,-52)] ]]
MORONIR =   {'name': 'moronir',
              'movement': (10,1,1,0),
              'sas': [[50,50,50,50],[100,100,100,100],[50],[0,0,0,0] ],
              'guns':  [ ], 'missile_launchers': 0,
              'graphics': ['multipolygon', [[ (-10,-5), (-10, -35), (-20,-35), (-30,-25), (-30, 25), (-20,35), (-10,35), (-10,5)],[ (10,5), (10,35), (20,35), (30,25), (30,-25), (20,-35), (10,-35), (10,-5) ] ]],
              'hitbox': moron_box ,
              'turrets': [{'guns': [ (LASER, -1), (LASER, 1) ],
                           'vertical_position': 2,
                           'horizontal_position': 30,
                           'alignment': 1.57,
                           'left_area': 1.6,
                           'right_area': 1.6},
                          {'guns': [ (LASER, -1), (LASER, 1) ],
                           'vertical_position': 2,
                           'horizontal_position': -30,
                           'alignment': 4.7,
                           'left_area': 1.6,
                           'right_area': 1.6}],
             'description': 'Well armed and armored for a civilian ship.',
             'special_hit_boxes': [
                 [ 'nonstandart', 12,[ [ (-10, -5), (-10,5), (10,5), (10,-5) ]],  10, 'ship_destroyed', 'exists',[ (-9, -5), (-9,5), (-3, 5), (-3, 8), (3,8), (3,5),  (9,5), (9,-5) ]  ] #  0: standart (circle) vs nonstandart (box);;; 1: radius ;;; 2: box points ;;; 3: hit points ;;; 4: effect ;;; 5: exists or is it already destroyed ? 
                 ],
              'ship_class': 'light_capital' }



RALARI =   {'name': 'ralari',
              'movement': (20,5,3,0),
              'sas': [[500,500,500,500],[1000,1000,1000,1000],[500],[0,0,0,0] ],
              'guns':  [ ], 'missile_launchers': 0, 'torpedo_launchers': 10, 
              'graphics': ['polygon', [(-4, -52), (-8, -48), (-8, -28), (-3, -8), (-3, 32), (-7, 40), (-7, 48), (-3, 52), (2, 52), (6, 48), (6, 40), (2, 32), (2, -8), (8, -28), (8, -48), (4, -52)]
],
              'hitbox': ralari_box ,
              'turrets': [{'guns': [ (FLAK, 0) ],
                           'vertical_position': - 40,
                           'horizontal_position': 0,
                           'alignment': 3.14,
                           'z_dimension': 'yes',
                           'radius': 5, 
                           'hit_points': 40, 
                           'left_area': 3,
                           'right_area': 3},
                          {'guns': [ (AM_10, 0) ],
                           'vertical_position': 45 ,
                           'horizontal_position': 0,
                           'hit_points': 200,
                           'radius': 7,
                           'alignment': 0,
                           'z_dimension': 'yes',
                           'left_area': 3,
                           'right_area': 3}],
             'description': 'Destroyer. \n Fast and deadly.',
         
              'ship_class': 'light_capital' }

FRALTHI =   {'name': 'fralthi',
              'movement': (15,5,2,0),
              'sas': [[2000,2000,2000,2000],[3000,3000,3000,3000],[2000],[0,0,0,0] ],
              'guns':  [ ], 'missile_launchers': 0, 'torpedo_launchers': 20, 
              'graphics': ['polygon', [(-20, -120), (-40, -100), (-40, -40), (-20, -20), (-20, 40), (-40, 80), (-40, 100), (-20, 120), (20, 120), (40, 100), (40, 80), (20, 40), (20, -20), (40, -40), (40, -100), (20, -120)]
],
              'hitbox': ralari_box ,
              'turrets': [{'guns': [  (AM_20, -3), (AM_20,3)  ],
                           'vertical_position': - 40,
                           'horizontal_position': 0,
                           'alignment': 3.14,
                           'left_area': 3,
                           'right_area': 3},
                          {'guns': [ (AM_20, -3), (AM_20,3) ],
                           'vertical_position': 45 ,
                           'horizontal_position': 0,
                           'alignment': 0,
                           'left_area': 3,
                           'right_area': 3}],
             'description': 'Cruiser',
         
              'ship_class': 'large_capital' }


SIVAR =   {'name': 'sivar',
              'movement': (12,3,2,0),
              'sas': [[5000,5000,5000,5000],[8000,8000,8000,8000],[10000],[0,0,0,0] ],
              'guns':  [(PHASE_TRANSIT, 200,0) ], 'missile_launchers': 0, 'torpedo_launchers': 20, 
              'graphics': ['polygon', [(-20, -160), (-60, -180), (-120, -160), (-120, -120), (-100, -100), (-100, -80), (-100, -60), (-100, -20), (-60, -40), (-20, 20), (-20, 80), (-40, 120), (-40, 160), (-20, 180), (20, 180), (40, 160), (40, 120), (20, 80), (20, 20), (60, -40), (100, -20), (100, -60), (100, -80), (100, -100), (120, -120), (120, -160), (60, -180), (20, -160)]
],
              'hitbox': ralari_box ,
              'turrets': [{'guns': [  (AM_40, -3), (AM_40,3)  ],
                           'vertical_position': - 40,
                           'horizontal_position': 0,
                           'alignment': 3.14,
                           'left_area': 3,
                           'right_area': 3},
                          {'guns': [ (AM_40, -3), (AM_40,3) ],
                           'vertical_position': 40 ,
                           'horizontal_position': 0,
                           'alignment': 0,
                           'left_area': 3,
                           'right_area': 3}],
             'description': 'Battleship. The most powerful warship ever built. Its main weapon, the Phase Transit Cannon, will kill literally anything in a single blast',
         
              'ship_class': 'large_capital' }






BROADAXE = { 'name': 'broadaxe',
             'movement':(30,20,1,80),
             'sas': [[25,25,25,25],[25,25,25,25],[20],[0,0,0,0] ],
             'guns': [(PARTICLE,5,0),(PARTICLE,3,-2),(PARTICLE,3,2)],
             'missile_launchers': 0,
             'torpedo_launchers': 3,
             'missile_launchers' : 2,
             'turrets': [
                 {'guns': [(LASER,-1), (LASER, 1) ],
                  'vertical_position': -5,
                  'horizontal_position': 10,
                  'hitpoints': 4,
                  'alignment': 1.57,
                  'left_area': 1.57,
                  'right_area': 1.57,},
                 {'guns': [(LASER,-1), (LASER, 1)],
                  'vertical_position': -5,
                  'horizontal_position': -10,
                  'hitpoints':4,
                  'alignment': 4.7,
                  'left_area': 1.57,
                  'right_area': 1.57},
                 {'guns': [(LASER,-1), (LASER, 1)],
                  'vertical_position': -10,
                  'horizontal_position': 0,
                  'hitpoints': 4,
                  'alignment': 3.14,
                  'left_area': 1.57,
                  'right_area': 1.57}],
             'hitbox': ['standart', 10],
             'graphics': ['polygon', (      (-6,-10), (-9,-8), (-8, -3), (-3,2), (-4,5), (-4,9), (-2, 11), (2,11), (4,9), (4,3), (3,2), (8,-3), (9, -8), (6, -10)         )],  ### (          (-4,-10),(-6,-9),(-6,-6),(-5,-4),(-3,-2),(-1,-1),(-1,1),(-2,5),(-2,7),(-1,10),(1,10),(2,7),(2,5),(1,1),(1,-1),(3,-2),(5,-4),(6,-6),(6,-9),(4,-10)        )
             'ship_class': 'bomber',
             'description': 'Heavy Bomber. If you want to take out something big, this is the ship for you. It can defend itself against fighters.'}

DRAGON = { 'name': 'dragon',
             'movement':(25,20,1,80),
             'sas': [[25,25,25,25],[25,25,25,25],[20],[0,0,0,0] ],
             'guns': [],
             'torpedo_launchers': 0,
             'missile_launchers' : 10,
             'turrets': [
                 {'guns': [(LASER,-1), (LASER, 1) , (LASER,0), (LASER, 2)],
                  'vertical_position': -5,
                  'horizontal_position': 10,
                  'alignment': 1.57,
                  'left_area': 1.6,
                  'right_area': 1.6},
                 {'guns': [(LASER,-1), (LASER, 1) , (LASER,0), (LASER, 2)],
                  'vertical_position': -5,
                  'horizontal_position': -10,
                  'alignment': 4.7,
                  'left_area': 1.6,
                  'right_area': 1.6},
                ],
             'hitbox': ['standart', 10],
             'graphics': ['polygon', complete_half_ship ([ (-4,-8),(-4,-10),(-9,-10),(-12,-8),(-12,-2),(-10,1),(-10,4),(-7,4),(-4,2),(-4,6),(-2,8)  ])],  ### (          (-4,-10),(-6,-9),(-6,-6),(-5,-4),(-3,-2),(-1,-1),(-1,1),(-2,5),(-2,7),(-1,10),(1,10),(2,7),(2,5),(1,1),(1,-1),(3,-2),(5,-4),(6,-6),(6,-9),(4,-10)        )
             'ship_class': 'bomber' ,
           'description': 'Missile Boat'}

CHARYBDIS = { 'name': 'charybdis',
             'movement':(20,20,1,80),
             'sas': [[10,10,10,10],[25,25,25,25],[20],[0,0,0,0] ],
             'guns': [],
             'missile_launchers': 0,
             'torpedo_launchers': 0,
   
             'turrets': [ {'guns': [(FLAK,0)],
                  'vertical_position': -5 ,
                  'horizontal_position': 0,
                           
                  'alignment': 4.7,
                  'z_dimension': 'yes',
                  'left_area': 3.2,
                  'right_area': 3.2} ],
             'hitbox': ['standart', 10],
             'graphics': ['polygon', (      (-6,-10), (-9,-8), (-8, -3), (-3,2), (-4,5), (-4,9), (-2, 11), (2,11), (4,9), (4,3), (3,2), (8,-3), (9, -8), (6, -10)         )],  ### (          (-4,-10),(-6,-9),(-6,-6),(-5,-4),(-3,-2),(-1,-1),(-1,1),(-2,5),(-2,7),(-1,10),(1,10),(2,7),(2,5),(1,1),(1,-1),(3,-2),(5,-4),(6,-6),(6,-9),(4,-10)        )
             'ship_class': 'bomber' , 'description': 'The Charybdis Gunboat carries a powerful flak, whose explosive shells can hit even the most agile fighter at great distances. Its greatest weakness is the extremely vulnerable gun turret.' }

STRAKHA = {'name': 'Strakha', 'movement': (50,30,2,150), 'sas': [[2,2,2,2],[0.1,0.1,0.1,0.1],[4],[0,0,0,0] ], 'guns':  [ (LASER, 5, -1), (LASER, 5, 1) ], 'missile_launchers': 1, 'graphics': ['polygon', ( (-2,-5), (-5,-3),(-5,1),(-3,5),(-2,-1),(2,-1),(3,5),(5,1),(5,-3),(2,-5)         )], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter' , 'stealth_device': 'yes', 'description': 'Stealth fighter. [press "r" to activate / deactivate stealth]'}
STRAKHA_N = {'name': 'Strakha N', 'movement': (50,30,2,150), 'sas': [[2,2,2,2],[0.1,0.1,0.1,0.1],[4],[0,0,0,0] ], 'guns':  [ (PLASMA, 5,-1), (PLASMA, 5,1)], 'missile_launchers': 1, 'graphics': ['polygon', ( (-2,-5), (-5,-3),(-5,1),(-3,5),(-2,-1),(2,-1),(3,5),(5,1),(5,-3),(2,-5)         )], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter' , 'stealth_device': 'yes', 'description': 'This Version has Neutron Cannons instead of lasers' }

MESSERSCHMIDT = {'name': 'messerschmidt', 'movement': (80,35,2,220), 'sas': [[5,3,3,3],[4,3,3,3],[3],[0,0,0,0] ], 'guns':  [ (STARFIRE, 5,0) ], 'missile_launchers': 2, 'graphics': ['polygon',complete_half_ship ([(-1,-6),(-3,-5),(-5,-1),(-7,-3),(-7,1),(-6,4),(-4,6),(-4,4),(-3,1),(-2,0),(0,2)   ]) ], 'hitbox':  ['standart', 4], 'turrets': [], 'ship_class': 'fighter', 'radar': 3500, 'description': 'Hyperspeed Interceptor. Build for one Purpose: Kill enemy bombers, as fast as possible' } ### old model: ( (0, -3), (-2,-3), (-2,-5), (-5,-5), (-5,2), (-4,4), (-3,4), (-2,2), (-2,0), (-1,2), (-1,8), (0,9), (1,8), (1,2), (2,0), (2,2), (4,3), (4,4), (5,2), (5,-5), (2,-5), (2, -3) )


RAPTOR = {'name': 'raptor', 'movement': (45,50,2,130), 'sas': [[10,7,8,7],[10,8,8,8],[10],[0,0,0,0] ], 'guns':[ (MASS,5,1), (MASS, 5,-1), (MASS, 2,-2), (MASS, 2,2)], 'missile_launchers': 4 ,'turrets' : [], 'graphics': [ 'polygon', (    (-1,-5), (-3,-4),(-5,-4), (-5,0),(-2,2), (-2,5), (-1,6), (1,6), (2,5), (2,2), (5,0), (5,-4),( 3,-4),(1,-5)         )],'hitbox': ['standart', 5], 'ship_class': 'fighter', 'description': 'The most powerful fighter on the Battlefield. Nothing short of a capital ship will survive a barrage of its four mass drivers and missile launchers. And it is more agile than the scimitar. '  }
RAPTOR_B = copy.deepcopy ( RAPTOR) 
RAPTOR_B ['name'] = 'raptor B' 
RAPTOR_B ['guns'] = [  (PARTICLE, 5,-1), (PARTICLE,5,-1), (PARTICLE, 2,2), (PARTICLE, 2,-2) ] 
PSYCHO = { 'name': 'psycho', 'movement': (35,100,6,120), 'sas': [[30,1,1,1],[10,1,1,1],[3],[0,0,0,0] ],'guns': [ (NEUTRON,5,1), (NEUTRON,5,-1), (NEUTRON,3,1),(NEUTRON,3,-1)], 'missile_launchers': 0, 'graphics':[ 'polygon', (    (-1,-5), (-3,-4),(-5,-4), (-5,0),(-2,2), (-2,5), (-1,6), (1,6), (2,5), (2,2), (5,0), (5,-4),( 3,-4),(1,-5)         )], 'hitbox':['standart', 5], 'turrets': [], 'ship_class': 'fighter' }
PSYCHO_B = copy.deepcopy (PSYCHO)
PSYCHO_B ['name'] = 'psycho B'
PSYCHO_B ['guns'] = [ (PLASMA,5,1), (PLASMA,5,-1), (NEUTRON,3,1),(NEUTRON,3,-1)]



LASER_MINE = {'name': 'laser_mine', 'movement': (0.001,0.001,0.001,0.001), 'sas': [[0.1,0.1,0.1,0.1],[0.1,0.1,0.1,0.1],[0.5],[0,0,0,0] ], 'guns':  [ (TOKEN,0,0) ], 'missile_launchers': 0, 'graphics': ['polygon', (  (-2, 1), (-1,2), (1,2), (2,1), (2,-1), (1,-2), (-1,-2),(-2,-1)       )], 'hitbox':  ['standart', 2], 'turrets': [{'guns': [  (LASER, 0) ], 'vertical_position': 2, 'horizontal_position': 0,'z_dimension': 'yes', 'alignment': 1.57, 'left_area': 3.14, 'right_area': 3.14}], 'ship_class': 'mine' }

TARGET_DUMMY = {'name': 'target_dummy', 'movement': (0.001,0.001,0.001,0.001), 'sas': [[10,10,10,10],[10,10,10,10],[10],[0,0,0,0] ], 'guns':  [ (TOKEN,0,0) ], 'missile_launchers': 0, 'graphics': ['polygon', (  (-2, 1), (-1,2), (1,2), (2,1), (2,-1), (1,-2), (-1,-2),(-2,-1)       )], 'hitbox':  ['standart', 5], 'turrets': [], 'ship_class': 'mine' }
SMALL_SUPPLY_DEPOT = {'name': 'small_supply_depot', 'movement': (0.00001,0.00001,0.00001,0.00001), 'sas': [[0.001,0.0001,0.001,0.001],[20,20,20,20],[15],[0,0,0,0] ], 'guns':  [ (TOKEN,0,0) ], 'missile_launchers': 0, 'graphics': ['polygon', (  (-10, 5), (-5,10), (5,10), (10,5), (10,-5), (5,-10), (-5,-10),(-10,-5)       )], 'hitbox':  ['standart', 10], 'turrets': [], 'ship_class': 'fighter' }


# CLAW = [ 'claw',  (5,1,0,1), ((1,1,1,1),(1000,800,600,800),(500),(0,0,0,0)), [ ], [],  [(LASER_T, -100, 80, 1.57, 1.57,1.57),(LASER_T, -40,80,1.57,1.57,1.57),(LASER_T, -40, -80, 4.6,1.57,1.57),(LASER_T, -100,- 80,4.6,1.57,1.57), (LASER_T,0,40, 1.57, 1.57 , 0.4), (LASER_T,60,40, 1.57,1.57,1)], [ 'polygon', (    (- 40,0), (-80,-40), (-80, -120), (-60, -140),(60,- 140), (80, -120), (80, -40), (40, 0), (40, 100), (20,120), (-20,120),(-40,100)    )], ['nonstandart', 160, [ (-80,-140), (-80, -20), (80, -20),(80, -140) ] , [ (-40,-20), (-40,120),(40,120),(40, -20) ] ] ]   
ship_type_list = [ TEST, MESSERSCHMIDT, PSYCHO, RAPTOR, BROADAXE, HAMMERHEAD,DEADMAN, LASER_MINE,TALON, TARGET_DUMMY, JALTHI, SCIMITAR, DRAHLTI, STRAKHA, KOMET ]

fed_cap_ships = []
fed_fighters = [ HORNET,SCIMITAR, RAPTOR,RAPTOR_B, RAPIER, KOMET, MESSERSCHMIDT, PSYCHO, PSYCHO_B, HAMMERHEAD]
fed_corvettes = [SABRE, BROADAXE, CHARYBDIS, SHRIKE, DRAGON]
fed_civs = [DEADMAN]

empire_cap_ships = [RALARI,FRALTHI, SIVAR]
empire_fighters = [JALTHI,DRAHLTI,STRAKHA,STRAKHA_N, TIE, SALTHI]
empire_corvettes = [SCYLLA] 
empire_civs = [MORONIR]

pirate_cap_ships = []
pirate_fighters = [TALON, DEMON]
pirate_corvettes = [SCYLLA_P] 

neutral_stuff = [LASER_MINE, TARGET_DUMMY]




campaign_state = 0
promotion_points = 0
promotion_point_matrix = {'failure': -2, 'basic': 1, 'bronze': 2, 'silver': 4, 'gold': 6 } 
rank = 'Flight Officer'

rank_list = ['Flight Officer', 'Second Lieutenant', 'First Lieutenant' ]

rank_dict = {
    'Flight Officer': {
        'level': 0,
        'points_required': 0,
        'wingmen': 0,
        'ships': [HORNET]
        },
    'Second Lieutenant': {
        'level': 1,
        'points_required': 2,
        'wingmen': 1,
        'ships': [HORNET, SCIMITAR]
        },
    'First Lieutenant': {
        'level': 2,
        'points_required': 4,
        'wingmen': 2,
        'ships': [HORNET, SCIMITAR, RAPTOR, RAPIER, SABRE ]
        }
    }
    
#### Functions
####
####



#######################################
def cleanup_old_mission ():   ### resets the game states that where changed by the previous mission run
    global end_game
    global master_frame_counter
    master_frame_counter = 0 
    global mission_timer
    global pause
    global global_message_list
    global star_list
    star_list = []
    global pressed
    global screen
    global autopilot_destination
    global log_factor
    global global_target_object_id
    target_object_id = None
    global recreate_stars
    global campaign_state
    global ship_list
    ship_list = []
    global bullet_list
    bullet_list = []
    global missile_list
    missile_list = []
    global asteroid_list
    asteroid_list = []
    global explosion_list
    explosion_list = [] 
    global target_count
    target_count = [] 
    global enemy_ship_list
    enemy_ship_list = []
    global killed_ship_list
    killed_ship_list = []
    global killed_ships_team2
    killed_ships_team2 = [0,0,0]
    global object_list
    object_list = ['dummy']
    global master_object_counter
    master_object_counter = 0
    global trigger_point_list
    trigger_point_list = []
    global turret_list
    turret_list = []
    global cannon_list
    cannon_list = []
    global debris_list
    debris_list = []
    global mission_goal_results
    mission_goal_results = {} 
    global success_level 
    success_level = None
    global mission_goal_list
    mission_goal_list = []
    global mission_event_list
    mission_event_list = []
    global delayed_effects_list
    delayed_effects_list = []
    global custom_mission
    custom_mission = {'ships': [] } 
    


###############################################


##############################################
def accepts (vtype_list):
    def decorator (some_func):

        def inner (*args, **wargs):
            for x in list (args) + wargs.values ():
                if type (x).__name__ not in vtype_list:
                    raise ValueError ('fucked up') 
            
            ret = some_func (*args, **wargs)
            return ret 

        return inner

    return decorator
#############################################

#############################################
def input_paras (test_number):

    def decorator (some_func):
        def wrapper (*args, **wargs):
            for x in list (args) + wargs.values ():
                print 'test ' + str (test_number) + '   ', x
            print '\n'
            ret = some_func (*args,**wargs)
            return ret

        return wrapper
    return decorator 
################################################

################################################
def input_paras_2 (test_number):

    def decorator (some_func):
        def wrapper (*args, **wargs):
            for x in list (args) + wargs.values ():
                print 'test ' + str (test_number) + '   ', x
            print 'args :  ', locals ()  
            print '\n'
            ret = some_func (*args,**wargs)
            return ret

        return wrapper
    return decorator 
##################################################        

##################################################
def check_all_list_items_in_other_list (small_list, big_list):
    out = 'no'
    result_list = []
   

    for item in small_list:
        if item in big_list: result_list.append ('yes')
        else: result_list.append ('no')

    if 'no' not in result_list: out = 'yes'

    return out

def check_if_list_items_in_at_least_one_element_of_list (small_list, big_list_list):
    out = 'no'
    for li in big_list_list:
        if check_all_list_items_in_other_list (small_list, li) == 'yes': out = 'yes'
    return out




def split_list_by_key (input_list, key):
    out_list = []
    key_item_list = []
    
    for item in input_list:
        item_transformed = key (item) 
        key_item_list.append (item_transformed )
    key_item_list = list (set (key_item_list))

    for item in key_item_list:
        sublist = []
        for i in input_list:
            if key (i) == item:
                sublist.append (i)
        out_list.append (sublist) 


    return out_list 



def check_on_screen (obj):
    out = 'no'
    x,y = obj.position
    if x > LEFT_MAIN_BORDER and x < SCREEN_SPLIT:
        if y > 0 and y < SCREEN_Y:
            out = 'yes'

    return out 

    
    

def print_stuff_x (x):
    print ('test 300.100  ' + str (x))
    return x 


def setify_list (some_list):
    new_list = [] 
    for item in some_list:
        if item not in new_list: new_list.append (item)
    return new_list 




class BetweenDict(dict):
    def __init__(self, d ):
        for k,v in d.items():
            self[k] = v
        

    def __getitem__(self, key):
        for k, v in self.items():
            
            if type ( k [0] ).__name__ in ['int', 'float']:
                if key >= k [0] and key < k [1]:
                    return v
            elif k [0] == '<':
                if key < k [1]: return v
            elif k [0] == '>':
                if key >= k [1]: return v 
        raise KeyError("Key '%s' is not between any values in the BetweenDict" % key)
###########################################################################################

def add_frame (border, colour):
    def decorator (some_func):

        def inner (*args, **wargs):
           
            ret = some_func (*args, **wargs)
          
            x = ret.get_width ()
            y = ret.get_height () 
            

            f = pygame.Surface ((x + 2 * border,y + 2 * border))
            f.fill (colour) 
            f.blit (ret, (border,border))

            return f
        return inner
    return decorator 


def add_frame_2 (old_frame,border,colour):
    #if type (border).__name__ != int: raise ValueError ('fucked up')
    #if type (colour).__name__ != tuple: raise ValueError ('fucked up')
    h = old_frame.get_height ()
    w = old_frame.get_width ()
    new_frame = pygame.Surface ( (w + border * 2 , h + border * 2 ))
    new_frame.fill (colour) 
    new_frame.blit (old_frame, (border,border))
    return new_frame 
    
            
            
            










def vadd (vector_1, vector_2):   ### addiert vektoren beliebiger länge 
    l_1 = list (vector_1)
    l_2 = list (vector_2)
    new_list = []
    for i in range (0, len (vector_1)):
        new_value = l_1 [i] + l_2 [i]
        new_list.append (new_value)
    return tuple (new_list)

def vsub (vector_1, vector_2):
    new_list = []
    for i in range (0, len (vector_1)):
        new_value = vector_1 [i] - vector_2 [i]
        new_list.append (new_value)
    return new_list



# @accepts ( ['tuple', 'list'])

def dot (position, **wargs):
    colour = wargs.get ('colour')
    if colour == None: colour = RED
    pygame.draw.circle  (screen, colour, vint (position), 3, 0) 

def points_distance (p1, p2):
    d = vector_sub (p1, p2)

    return vector_length (d) 


def error ():
    raise ValueError ('fucked up: Variable exists already') 


def xget (input_list, key):
    out = None

    for item in input_list:
        if type (item) is dict:
            out = (item.get (key) if item.get (key) != None else out )

    return out

def extract_from_dict_list (input_list, selection_key, selection_value, return_key ):
    out = None
    for l in input_list:
        if l.get (selection_key) == selection_value:
            out = l.get (return_key)

    return out



def vector_sub (v1, v2):
    return (v1 [0] - v2 [0], v1 [1] - v2 [1] )


def vector_length (v):
    return ( ( v [0] ** 2 + v [1] ** 2) ** 0.5)


def middle_point (p1,p2):
    m = ( p1 [0] / 2 + p2 [0] / 2, p1 [1] /2 + p2 [1] / 2 )
    return m



def y_n_switch (x):
    if x == 'yes': out = 'no'
    if x == 'no' : out = 'yes'
    return out


def get_out_of_list_3 ( input_list , matrix ):
    new_list = []
    for item in input_list:
        new_item = item 
        for e in range (0, len (matrix)):
            new_item = new_item [ matrix [e]]
        
        new_list.append (new_item)
    return new_list


def out_of_dictionary (dict_list, key):
    out_list = []
    for d in dict_list:
        out_list.append (d.get (key))
    return out_list


                        


def vint (input_vector):
    return (int (input_vector [0]), int (input_vector [1]))



def split_stack (stack, increment):
    if stack >= increment:
        out = (stack - increment, increment)
    elif stack > 0 and stack < increment:
        out = (0, stack)
    elif stack == 0:
        out = (0,0)
    else:
        print 'test 31. 000 ', stack , increment
        raise ValueError ('fucked up')
    return out [0], out [1]  






def key_selector ():
    global key_selected
    global keydown
    out = None

    if key_selected == 0:
        global key_1
        global key_2
        global key_3
        global key_4
        global key_5
        global key_6
        global key_7
        global key_8
        global key_9
        global key_0

        if key_1 == 1: out = 1
        if key_2 == 1: out = 2
        if key_3 == 1: out = 3
        if key_4 == 1: out = 4
        if key_5 == 1: out = 5
        if key_6 == 1: out = 6
        if key_7 == 1: out = 7
        if key_8 == 1: out = 8
        if key_9 == 1: out = 9
        if key_0 == 1: out = 0
        if keydown [97] == 1: out = 10
        if keydown [98] == 1: out = 11
        if keydown [99] == 1: out = 12
        if keydown [100] == 1: out = 13
        if keydown [102] == 1: out = 14
        if keydown [103] == 1: out = 15

    return out

def change_text_in_list_front ( input_list, change_place, to_add):
    original_text = input_list [change_place]
    new_text = to_add + original_text
    
    new_list = []
    for i, item in enumerate (input_list):
        if i != change_place : new_list.append (item)
        if i == change_place : new_list.append (new_text)

    return new_list
        
    


def add_limit ( x, y, limit):
    x += y
    if x > limit: x = limit
    return x

def substract_limit ( x, y, limit):
    x -= y
    if x < limit: x = limit
    return x 


def cut_string (input_string, key):
    input_list = list (input_string)
    position = None

    

    for e, x in enumerate (input_list):
        if position == None:
            if x == key :
                position = e
                
        
    output_list = list (input_list)
    if position != None: output_list = input_list [:position]
    return list_to_string (output_list)


def list_to_string ( input_list):
    out = ''
    for i in input_list:
        out += i
    return out



def collide (x_s, y_s, b):
    out = 0

    x_s_u, x_s_o = x_s
    y_s_u, y_s_o = y_s
    b_x, b_y = b 

    if x_s_u <= b_x <= x_s_o and y_s_u <= b_y <= y_s_o: out = 1
    return out

def extract_from_dictionary ( dictionary, key ):
    out = None
    for item in dictionary:
        if item [0] == key: out = item [1]
    return out




def shrink_ship ( ship, factor ): ### makes ship graphics smaller
    ship = list (ship)
    new_ship = []
    factor = 1 / factor 
    for s in ship:
        new_ship.append ( skalar_multi (factor, s))
    return tuple (new_ship)


def skalar_multi ( skalar, vector):
    vector = list (vector)
    new_vector = []
    for v in vector:
        new_vector.append ( skalar * v )
    return tuple (new_vector)



                                                     
def thick_vertical_line ( point_1, point_2, thickness, colour ):
    pygame.draw.aaline ( screen, colour, point_1, point_2, 1)
    for i in range (1, thickness + 1):
        pygame.draw.aaline ( screen, colour, dfunctions.vadd (point_1, (i,0)),dfunctions.vadd ( point_2, (i,0)), 1)
        i = i * (-1)
        pygame.draw.aaline ( screen, colour, dfunctions.vadd (point_1, (i,0)),dfunctions.vadd ( point_2, (i,0)), 1)
        

def thick_horizontal_line (point_1, point_2, thickness, colour):
    pygame.draw.aaline (screen, colour, point_1, point_2, 1)
    for i in range (1, thickness + 1):
        pygame.draw.aaline ( screen, colour, dfunctions.vadd (point_1, (0,i)),dfunctions.vadd ( point_2, (0,i)), 1)
        i = i * (-1)
        pygame.draw.aaline ( screen, colour, dfunctions.vadd (point_1, (0,i)),dfunctions.vadd ( point_2, (0,i)), 1)
      
        

def log_value (x):
    out = 0
    if x <= 100: out = x
    if x > 100:
        y = x / 100
        z = math.log (y,10)
        out = 100 + ( 100 * z )
    return out

def log_vector ( (x,y)):

    x_normalized = x - MIDDLE [0]
    x_n_direction = dfunctions.one_or_minus_one (x_normalized)
    x_n_abs = abs (x_normalized)
    x_neu = ((log_value (x_n_abs)) * x_n_direction ) + MIDDLE [0]

    
    y_normalized = y - MIDDLE [1]
    y_n_direction = dfunctions.one_or_minus_one (y_normalized)
    y_n_abs = abs (y_normalized)

    
    y_neu = ((log_value (y_n_abs)) * y_n_direction ) + MIDDLE [1]
    return (int (x_neu),int (y_neu))


def collide_2 (ship_position, ship_seize, missile_position, missile_seize):
    out = 0
    combined_seize = ship_seize + missile_seize
    distance = dfunctions.distance_2 (ship_position, missile_position)
    if combined_seize > distance: out = 1
    return out

def damage_calc (armor, damage):
    if armor == damage: condition = 1
    if armor > damage: condition = 2
    if armor < damage: condition = 3

    if condition == 1: armor, damage = 0,0
    
    if condition == 2:
        armor = armor - damage
        damage = 0
        
    if condition == 3:
        damage -= armor
        armor = 0
    return armor, damage 
        

def write (text,position, text_colour, font_seize):
    myfont = pygame.font.SysFont("Times New Roman", font_seize)
    label = myfont.render ( str (text) , 1, text_colour)
    screen.blit (label, position)

def write_2 (text, position):
    write (text, position, RED, 15)


def write_1b (surface, text,position, text_colour, font_seize):          ### like normal 'write', but draws on surface instead of screen 
    myfont = pygame.font.SysFont("Times New Roman", font_seize)
    label = myfont.render ( str (text) , 1, text_colour)
    surface.blit (label, position)

def write_list (text_list, position, text_colour, font_seize):
    for e, text in enumerate (text_list):
        write (text, dfunctions.vadd (position, (0,e * 1.5 * font_seize)), text_colour, font_seize)

def write_double_list (text_double_list, position, text_colour, font_seize):
    for e, double_text in enumerate (text_double_list):
        write (str (double_text [0]) + '  ' + str (double_text [1]), dfunctions.vadd (position, (0,e * 1.5 * font_seize)), text_colour, font_seize)

        

def target_in_crosshairs (heading, bearing, target_distance, weapon_range):
    out = 0
    condition_1 = 0
    condition_2 = 0
    
    in_crosshairs = dfunctions.relative_direction (heading, bearing)
    if abs (in_crosshairs) < 0.1 : condition_1 = 1
    if weapon_range > target_distance : condition_2 = 1
    if condition_1 == 1 and condition_2 == 1: out = 1
    return out

def target_in_crosshairs_2 (self_position, target_position, self_direction, weapon_range):   ## so ähnlich wie crosshairs, aber mit anderen eingabeparametern
    heading = self_direction
    out = 0 
    bearing = dfunctions.ftarget_direction_2 (self_position, target_position)
    target_distance = dfunctions.distance_2 (self_position, target_position)
    out = target_in_crosshairs (heading, bearing, target_distance, weapon_range)
    return out , bearing



######################################################################################################################################
######################################################################################################################################
##################################              Start:          Class Definitions                                   ##################
######################################################################################################################################
######################################################################################################################################


##########################################################################################################################################

DEBRIS_GRAPHICS_LIST = [  lambda x, colour: pygame.draw.line (screen, colour, x, dfunctions.vadd (x, (0,4)))  ] 


class debris (object):
    def __init__ (self, position, speed, direction, **wargs ):
        self.ship_id = None
        self.radius = 0
        self.superclass = 'debris'
        self.z_dimension = 'no' 
        self.position = position
        self.speed = speed
        self.direction = direction
        self.life_timer = 300
        self.graphics = DEBRIS_GRAPHICS_LIST [random.randint (0, len (DEBRIS_GRAPHICS_LIST) - 1 ) ]
        debris_list.append (self)
        self.vertical_direction = dfunctions.aa ( self.direction, 1.57 * random.uniform (1,3) )
        self.vertical_speed = 50
        self.vertical_speed_timer = 10 + random.randint (1,20)
        self.colour = WHITE
        if 'colour' in wargs: self.colour = wargs ['colour']
        self.damage = wargs.get ('damage') 


    def update (self):
      
        self.update_speed ()
        self.update_position ()
        self.do_graphics ()

        self.life_timer -= 1
        if self.life_timer <= 0: debris_list.remove (self) 
          


    def update_speed (self):
        self.speed -= 0.1
        if self.speed <= 0: self.speed = 0 
        

    def update_position (self):
        
        
       
        x,y = self.position
        x = x + self.speed * math.sin (self.direction) / 30 
        y = y + self.speed * math.cos (self.direction) / 30
        
        if self.vertical_speed_timer > 0:
            self.vertical_speed_timer -= 1
            x += self.vertical_speed * math.sin (self.vertical_direction) / 30
            y += self.vertical_speed * math.cos (self.vertical_direction ) / 30 
        
        self.position = x,y
       

        self.normalized_position = dfunctions.vadd (self.position, NEGATIVE_MIDDLE) #       ??? what is this good for ???

    def do_graphics (self):
        self.graphics (vint (self.position), self.colour)

    def adjust_position (self, x,y ):
        self.position = dfunctions.vadd ((x,y), self.position)
      









############################################################################################################################################




            

###########################################################################################################################################
class display_stuff_class (object):
    def __init__ (self, function, **wargs):
        self.x = 250
        self.y = 200
        self.colour = WHITE 
        self.picture = None
        if 'colour' in wargs: self.colour = wargs ['colour'] 
        self.information = [[],[]]
        self.function = function
        self.border = 10
        if 'border' in wargs: self.border = wargs ['border'] 

    def update (self, new_args, new_wargs, **wargs):
        new_stuff = new_args + new_wargs.values ()
        new_stuff = copy.deepcopy (new_stuff) 
 
        self.information.insert (0, new_stuff)

        self.information = self.information [:2]
        if self.information [0] != self.information [1]:

            if self.border != 0: function_2 = add_frame (self.border, dfunctions.darken_colour (self.colour)) (self.function)
            else: function_2 = self.function
 
            # new_wargs.update ({'expand_x' : self.x})
            result = function_2 ((0,0),*new_args , **new_wargs)
 


            self.picture = pygame.Surface ( (result.get_width (), result.get_height () ))
            self.picture.blit (result, (0,0))

#############################################################################################################################################


            


class window (object):

    def second_init (self):
        pass 
    def __init__ (self):
        self.outer_frame = None
        self.x_seize = 500
        self.y_seize = 400
        self.position = (300,300) 
        self.outer_colour = BROWN
        self.name = None
        self.counter = 0
        self.outer_border = 10 



        self.second_init ()
   




    def update (self):
        # if self.outer_frame == None:
            #self.outer_frame = self.create_outer_frame ()
        self.counter += 1
        if self.counter >= 10:
            self.counter = 0 

            inner_frame = self.create_inner_frame ()
            if self.outer_border != 0 : inner_frame = add_frame_2 (inner_frame, self.outer_border , self.outer_colour) 
            #self.outer_frame = pygame.Surface ((inner_frame.get_width () , inner_frame.get_height () ))
            #pygame.Surface.blit (self.outer_frame, inner_frame, (0,0))
            

            # self.frame.fill ( (0,0,0 ))

            

            pygame.Surface.blit (screen, inner_frame, self.position)
            pygame.display.update ( [self.position [0], self.position [1], inner_frame.get_width (), inner_frame.get_height () ] )
            




    



#####################################################################################################################################

class top_right_window (window):

    def second_init (self):
        self.x_seize = 340
        self.y_seize = 400
       
        self.position = (SCREEN_X - self.x_seize, 0) 

    
    def create_inner_frame (self):
        frame = pygame.Surface ( (self.x_seize - 16, self.y_seize - 16))
        frame.fill (BLACK)
        middle = ( int (self.x_seize / 2), int (self.y_seize / 2))

        for t in trigger_point_list:
         
            
            t.radar_graphics (surface = frame, middle = middle)

        for y in ship_list:
            if ship.output_player (y) == 1: ship.radar_graphics (y, surface = frame, middle = middle)
            if ship.output_player (y) == 0:
                if y in (ship.output_ships_on_radar ( ship_list [0] )) : ship.radar_graphics (y, surface = frame, middle = middle)

        return frame 
        


######################################################################################################################################

class bottom_right_window (window):
    def second_init (self):
        self.x_seize = 340
        self.y_seize = 400
        
        self.colour = GREEN 

        self.position = (SCREEN_X - self.x_seize, SCREEN_Y - self.y_seize)
        self.tabs = ['goals']



    ###########################################################################
    def create_inner_frame (self):
        frame = pygame.Surface ( (self.x_seize - 16, self.y_seize - 16))
        frame.fill (BLUE) 

        position = (0,0) 
        ### def upper tab frame
        tab_position = position 
        for item in self.tabs:
            tab_length = int (self.x_seize / len (self.tabs))
            dfunctions.back_frame_2 (frame, tab_position, tab_length, 20 , self.colour,2, 2, WHITE)
            write_1b (frame, item, dfunctions.vadd (tab_position, (10, 1)), self.colour, 15)
            tab_position = vadd (tab_position, (tab_length,0))
            
        position = dfunctions.vadd (position, (10,30))






        global mission_goal_results
        mission_goal_results = {}
        mission_points = 0
        e = 0 ### in case of empty goal list :   writing the points needs 'e'
       
        for e, g in enumerate (mission_goal_list [:]) :
            goal_acc = 'no'
            goal_id = g.get ('goal_id') 
            goal_event = g.get ('goal_event')
            
            for item in mission_event_list:
                if check_all_list_items_in_other_list (goal_event, item) == 'yes':
                    goal_acc = 'yes'
            mission_goal_results [goal_id] = goal_acc                  #append ( [goal_id, goal_acc]) 
          
            if goal_acc == 'yes': 
                for g_2 in running_mission_info.get ('goals') [::-1]:
                    if g_2.get ('super_goal') == g.get ('goal_name') and g_2 not in mission_goal_list: mission_goal_list.insert (e + 1, g_2)   ###   why does the list need to be reversed ? => because the sub_goals are always inserted directly after the super_goal: without inversing, first sub_alpha is inserted after the super goal, then sub_beta is inserted after the super goal- before sub_alpha !
                   
            
            tab_modificator = 0 
            if g.get ('super_goal') != None: tab_modificator = 20 
            
            
            dfunctions.success_box (dfunctions.vadd (position, ( tab_modificator, e * 27)        ), WHITE, goal_acc , surface = frame)
            
            write_1b (frame, g.get ('goal_name'), dfunctions.vadd ( position, (tab_modificator + 30 , e * 27)), WHITE, 12 )
            points = g.get ('points')
            if goal_acc == 'yes' and points != None:
                mission_points += points
        for item in mission_event_list:
            if item [1] == 'destroyed':
                if len (item) >= 4 and item [3] is int: 
            
            
                    mission_points += item [3]
            
        

        # write_1b (frame, 'Points  ' + str (mission_points), dfunctions.vadd (position, (10, (e + 1) * 27 + 10)), RED, 12) 


        
        return frame

    ############################################################################

#################################################################################

class middle_right_window (window):
    def second_init (self):
        self.x_seize = 200
        self.y_seize = 200
        self.position = (SCREEN_X - self.x_seize , 400)
        self.aft = display_stuff_class (dfunctions.display_afterburner, colour = BLUE)
        self.es = display_stuff_class (dfunctions.display_engine_status, colour = MAGENTA)
        self.ss = display_stuff_class (dfunctions.display_shield_supercharge_b, colour = GOLD)
        self.name = 'middle'

    #########################################################
    
    def create_inner_frame (self):
        inner_position = (0,0)

        middle = ( int (self.x_seize / 2), int (self.y_seize / 2))

        if mission_running == 0:
            frame = pygame.Surface ( (self.x_seize - 16, self.y_seize - 16))
            frame.fill (BLACK)


        if mission_running in [1,2]:

            #       afteburner
            self.aft.update ([(ship.output_afterburner_delay_counter (object_list [1]) / (object_list [1]).AFTERBURNER_ACTIVATION_TIME ), (ship.output_afterburner_delay_counter (object_list [1]) / (object_list [1]).AFTERBURNER_ACCELERATION_TIME ),(ship.output_afterburner_delay_counter (object_list [1])) / ship.output_AFTERBURNER_GLIDING_TIME (object_list [1] ),(ship.output_AFTERBURNER_COOLDOWN (object_list [1]) / (object_list [1]).AFTERBURNER_COOLDOWN ), ship.output_afterburner_activation (object_list [1]) ], {'expand_x': self.x_seize - 36})
             
            #       engine_status
            '''
            es = dfunctions.display_engine_status ( inner_position, ship.output_engine_counter (object_list [1]), ship.output_engine_counter_max (object_list [1]), ship.output_speed_mode (object_list [1]), ship.output_set_speed_mode (object_list [1]), expand_x = 250)
            es = add_frame_2 (es, 10, dfunctions.darken_colour (PURPLE))
            '''
            self.es.update ([ship.output_engine_counter (object_list [1]), ship.output_engine_counter_max (object_list [1]), ship.output_speed_mode (object_list [1]), ship.output_set_speed_mode (object_list [1])], {'expand_x': self.x_seize - 36})
 
            

            #       shield supercharge
            '''
            ss = dfunctions.display_shield_supercharge_b ( (0,0),player_shield_supercharge_phase = ship.output_shield_supercharge_phase (object_list [1]) , player_shield_supercharge_timer = ship.output_shield_supercharge_timer (object_list [1] ),shield_supercharge_activation_time = SHIELD_SUPERCHARGE_ACTIVATION_TIME,shield_supercharge_duration = SHIELD_SUPERCHARGE_DURATION, expand_x = 250)
            ss = add_frame_2 (ss, 10,dfunctions.darken_colour ( GREEN))
            '''
            self.ss.update ( [],{ 'player_shield_supercharge_phase' : ship.output_shield_supercharge_phase (object_list [1]) , 'player_shield_supercharge_timer' : ship.output_shield_supercharge_timer (object_list [1] ),'shield_supercharge_activation_time' : SHIELD_SUPERCHARGE_ACTIVATION_TIME, 'shield_supercharge_duration' : SHIELD_SUPERCHARGE_DURATION , 'expand_x': self.x_seize - 36} ) 
           



            ###         blit stuff
            ss = self.ss.picture 
            es = self.es.picture
           
            self.y_seize = self.aft.picture.get_height () + es.get_height () + ss.get_height () 
            frame = pygame.Surface (( self.x_seize - 20, self.y_seize   ))
            frame.fill (BLACK)
            frame.blit (self.aft.picture, (0,0))
            frame.blit (es , (0,self.aft.picture.get_height ()) )
            frame.blit ( ss, (0,self.aft.picture.get_height () + es.get_height ()))
        return frame 

    
           
        
############################################################################################################################################

class window_4 (window):  #     Energy, Gliding, Booster

    def second_init (self):
        self.x_seize = 200
        self.y_seize = 200
        self.position = (SCREEN_X  - 340, 400)
        self.en = display_stuff_class (dfunctions.display_energy_points, colour = GOLD)
        self.gl = display_stuff_class (dfunctions.display_booster, colour = MAGENTA )
        self.bo = display_stuff_class (dfunctions.display_booster, colour = GREEN )
 

    def create_inner_frame (self):
        inner_position = (0,0)

        
        if mission_running == 0:
            frame = pygame.Surface ( (self.x_seize - 16, self.y_seize - 16))
            frame.fill (BLACK)


        if mission_running in [1,2]:


        #       energy_points 
            '''
            en = dfunctions.display_energy_points ( (0,0), ship.output_energy_points (object_list [1]), ship.output_max_energy_points (object_list [1]), ship.output_energy_points_charge_ratio (object_list [1]), surface = frame )
            frame.blit (en, (0,0))
            '''
            self.en.update ( [ ship.output_energy_points (object_list [1]), ship.output_max_energy_points (object_list [1]), ship.output_energy_points_charge_ratio (object_list [1]) ], {} )
            en = self.en.picture

        #       Gliding
      
            '''
            gl = dfunctions.display_booster ( (0,0), ship.output_gliding_phase (object_list [1]), ship.output_gliding_timer (object_list [1]) / GLIDING_DURATION , gliding = 'yes', surface = frame)
            '''
            self.gl.update ( [ ship.output_gliding_phase (object_list [1]), ship.output_gliding_timer (object_list [1]) / GLIDING_DURATION, 'yes' ], {})
            gl = self.gl.picture 
          
           
        #       Booster
      
            # bo =  dfunctions.display_booster ( (0, 0), ship.output_booster_active (object_list [1]), ship.output_booster_timer (object_list [1]) / BOOSTER_DURATION,surface = frame)
            self.bo.update ( [ship.output_booster_active (object_list [1]), ship.output_booster_timer (object_list [1]) / BOOSTER_DURATION ], {} ) 
            bo = self.bo.picture
            
          
            
            self.y_seize = en.get_height () + gl.get_height () + bo.get_height () + 20 
            frame = pygame.Surface ( ( max (en.get_width (), gl.get_width (), bo.get_width () )     ,en.get_height () + gl.get_height () + bo.get_height ()  ))
            frame.fill (BLACK)
            frame.blit (en, (0,0))
            frame.blit (gl, (0, en.get_height () ))
            frame.blit (bo, (0, en.get_height () + gl.get_height () ))




        return frame

###################################################################################################################################


        
############################################################################################################################################

class window_5 (window): ### player_shields + speed 

    def second_init (self):
        self.x_seize = 250
        self.y_seize = 200
        self.position = (0,0)
        self.sd = display_stuff_class (dfunctions.display_sas_3, colour = GREEN)
        self.player_speed = display_stuff_class (dfunctions.write_1c, colour = BLUE, border = 3 )
        self.player_man = display_stuff_class (dfunctions.write_1c, colour = BLUE, border = 3 )
        self.name = 5 




    def create_inner_frame (self):
        inner_position = (0,0)

        
        if mission_running == 0:
            frame = pygame.Surface ( (self.x_seize - 16, self.y_seize - 16))
            frame.fill (BLACK)


        if mission_running in [1,2]:

            


        #       display_player_speed
            s = object_list [1]
            self.player_speed.update ( ['Speed :  ' + str (round (s.speed,0)), WHITE, 12 ], {'expand_x': self.x_seize - 36} )

            # player man

            s = object_list [1]
            self.player_man.update ( ['Turn Rate :  ' + str (round (s.man, 0 )), WHITE, 12 ], {'expand_x': self.x_seize - 36} ) 

        #       shield display
            s = object_list [1]
            self.sd.update  ( [GREEN, s.actual_sas [0], s.full_sas [0], s.actual_sas [1], s.full_sas [1], s.actual_sas [2] [0], s.full_sas [2] [0] ], { 'missiles' : (len (s.missile_cooldowns) ,s.missile_damage / s.damage_threshold ) , 'guns' : (len (s.cannon_ids),s.cannon_damage / s.damage_threshold          ), 'shield_generator_damage' : s.shield_generator_damage, 'engine_damage' : s.engine_damage, 'damage_threshold' : s.damage_threshold ,'expand_x': self.x_seize - 36} , show_info = 'yes', )




            frame = pygame.Surface ( ( max (self.sd.picture.get_width (), self.player_speed.picture.get_width (), self.player_man.picture.get_width () )     ,self.sd.picture.get_height () + self.player_speed.picture.get_height () + self.player_man.picture.get_height ()  ))
            frame.fill (BLACK)
   
            frame.blit (self.sd.picture ,(0,0))

            frame.blit (self.player_speed.picture , (0,200))
            frame.blit (self.player_man.picture, (0, 225))



        return frame


        
############################################################################################################################################

class window_6 (window): # target shields and stuff 

    def second_init (self):
        self.x_seize = 250
        self.y_seize = 300
        self.position = (0,SCREEN_Y - self.y_seize)
        self.sd = display_stuff_class (dfunctions.display_sas_3, colour = ORANGE )
        self.target_name = display_stuff_class (dfunctions.write_1c, colour = BLUE, border = 3 )
        self.target_speed = display_stuff_class (dfunctions.write_1c, colour = BLUE, border = 3 )
        self.target_man = display_stuff_class (dfunctions.write_1c, colour = BLUE, border = 3 )
        self.target_dis = display_stuff_class (dfunctions.write_1c, colour = BLUE, border = 3 )






    def create_inner_frame (self):
        inner_position = (0,0)

        
        if mission_running == 0 or global_target_object_id == None:
            frame = pygame.Surface ( (self.x_seize - 16, self.y_seize - 16))
            frame.fill (BLACK)


        if mission_running in [1,2]:

            if global_target_object_id != None:
                s = object_list [global_target_object_id]

                # target name
                self.target_name.update ( [s.name.upper (), ORANGE, 15], {} ) 

                # target speed
                self.target_speed.update ( ['Speed :  ' + str (round (s.speed,0)), GOLD, 12 ], {} )

                # target man
                self.target_man.update ( ['Turn Rate :  ' + str (round (s.man, 0 )), WHITE, 12 ], {} )

                # target dis
                self.target_dis.update ( [  'Distance : ' + cut_string (str ( dfunctions.distance_2 (ship.output_position (object_list [1]), ship.output_position (object_list [global_target_object_id]))), '.'), MAGENTA, 12 ], {} )

            
            


                #   shield display
   
                self.sd.update  ( [GREEN, s.actual_sas [0], s.full_sas [0], s.actual_sas [1], s.full_sas [1], s.actual_sas [2] [0], s.full_sas [2] [0] ], { 'missiles' : (len (s.missile_cooldowns) ,s.missile_damage / s.damage_threshold ) , 'guns' : (len (s.cannon_ids),s.cannon_damage / s.damage_threshold          ), 'shield_generator_damage' : s.shield_generator_damage, 'engine_damage' : s.engine_damage, 'damage_threshold' : s.damage_threshold ,'expand_x': self.x_seize - 36} , show_info = 'yes' )


                speed = self.target_speed.picture
                man = self.target_man.picture
                dis = self.target_dis.picture
                sd = self.sd.picture
                name = self.target_name.picture 

                frame = pygame.Surface ( ( max (sd.get_width (), speed.get_width (), man.get_width (), dis.get_width () )     ,sd.get_height () + speed.get_height () + man.get_height () + dis.get_height () + name.get_height () ))
                frame.fill (BLACK)
       
                frame.blit (sd ,(0,0))

                frame.blit (speed, (0,200))
                frame.blit (man, (0, 225))
                frame.blit (dis, (0,250))
                frame.blit (name, (0,175))



        return frame

###################################################################################################################################

############################################################################################################################################

class window_7 (window): # missiles and torpedos 

    def second_init (self):
        self.x_seize = 150
        self.y_seize = 300
        self.position = (0,int (SCREEN_Y / 2 )   - int (self.y_seize / 2 ))
        self.sd = display_stuff_class (dfunctions.display_sas_3, colour = RED )
        self.m = display_stuff_class (dfunctions.display_missile_launchers, colour = BLUE, border = 3 )
        self.t = display_stuff_class (dfunctions.display_missile_launchers, colour = MAGENTA, border = 3 ) 

    def create_inner_frame (self):
        inner_position = (0,0)

        
        if mission_running == 0:
            frame = pygame.Surface ( (self.x_seize - 16, self.y_seize - 16))
            frame.fill (BLACK)


        if mission_running in [1,2]:

            s = object_list [1]
            self.m.update ([ s.output_missile_cooldowns (), MISSILE_COOLDOWN ], {})

            self.t.update ( [s.output_torpedo_cooldowns (), MISSILE_COOLDOWN ], {'torpedo': 'yes'} )
            
            m = self.m.picture
            t = self.t.picture
            
            frame = pygame.Surface ( (max (m.get_width (), t.get_width ()), m.get_height () + t.get_height () )) 
            frame.fill (BLACK)

            self.y_seize = frame.get_height ()

            self.position = (0,int (SCREEN_Y / 2 )   - int (self.y_seize / 2 ))


   
            frame.blit (m ,(0,0))
            frame.blit (t, (0,m.get_height ()))


        return frame

###################################################################################################################################

############################################################################################################################################

class window_8 (window): # killed ships list  

    def second_init (self):
        self.x_seize = 150
        self.y_seize = 300
        self.position = (251,0)
        self.outer_border = 2 
        self.k = display_stuff_class (dfunctions.display_killed_ships, colour = MAGENTA, border = self.outer_border  )# killed = dfunctions.display_killed_ships ( killed_ship_list, 300, WHITE)
     

    def create_inner_frame (self):
        inner_position = (0,0)

        
        if mission_running == 0:
            frame = pygame.Surface ( (self.x_seize - 16, self.y_seize - 16))
            frame.fill (BLACK)


        if mission_running in [1,2]:

           
            self.k.update ([ killed_ship_list, 300, WHITE], {})

           
            
            frame = pygame.Surface ( (500,20)) 
            frame.fill (BLACK)
            frame.blit (self.k.picture, (0,0)) 

            self.y_seize = frame.get_height ()

            


   

        return frame

###################################################################################################################################




#####################################################################################################################################

    
    

# # # Klassendefinition         trigger_point

class trigger_point (object):
    def __init__ (self, **wargs):
        self.position = wargs.get ('position')
        self.ships = wargs.get ('ships')
        self.triggered = 0
        self.radar_position = (0,0)
        self.list_position = None
        self.goal_name = wargs.get ('goal_name') 
     
        self.mission_id = wargs.get ('mission_id')

        self.triggered_goals = wargs.get ('trigger')
        self.name = wargs.get ('name') 
       
        


    

    def output_position (self): return self.position

    def adjust_position (self, x,y ):
        self.position = dfunctions.vadd ((x,y), self.position)
        self.normalized_position = dfunctions.vadd (self.position, NEGATIVE_MIDDLE)
        self.radar_position = dfunctions.skalar_multi ( 1 / radar_factor, self.normalized_position)

    def set_list_position (self,x): self.list_position = x           ### position of this object in the mission_goal_list   #### this changes when new subgoals are insertet into the list! 
        


    def circle (self):
        pygame.draw.circle (screen, WHITE, vint (self.position), 20, 2)
        write (str (self.name) , vint (vadd ((self.position), (-10, -7))), WHITE, 15)

    def trigger (self):
        if self.ships != None and self.triggered == 0:
  

            if dfunctions.distance_2 (self.position, ship.output_position (object_list [1])) < 100:
                for s in self.ships:
                    create_fighter (s)
                self.triggered = 1
                if self.mission_id != None: mission_event_list.append ([self.mission_id, 'visited'] )
                goals = running_mission_info ['goals']

        if master_frame_counter % 30 == 0:
            for s in ship_list:
                if s.mission_id != None:
                    # print 'test 881  ', dfunctions.distance_2 (self.position, s.position) 
                    if dfunctions.distance_2 (self.position, s.position) <= 300: 
                        new_event = [self.mission_id, 'visited', s.mission_id ]
                        if new_event not in mission_event_list: mission_event_list.append (new_event) 
                        
                
                    

    def radar_graphics (self, **wargs):
        surface = screen
        middle = (100,100)
        if 'middle' in wargs: middle = wargs ['middle'] 
        if 'surface' in wargs:
            surface = wargs ['surface']
         
        x,y = self.radar_position
        radar_display_position = ( int (x) + SECOND_MIDDLE [0] , int (y) + SECOND_MIDDLE [1])
        radar_name = ( self.name if len (self.name.split ('_') ) == 1 else self.name.split ('_') [1])  
        write_1b (surface, radar_name, dfunctions.vadd (middle, self.radar_position,(-2, -6)), WHITE, 10)
    
       
        pygame.draw.circle ( surface,FAINT_WHITE, dfunctions.vadd (middle,vint (self.radar_position)), 7, 1)
        pass 

        
        # pygame.draw.circle ( screen,FAINT_WHITE,  ( int (x) + SECOND_MIDDLE [0] , int (y) + SECOND_MIDDLE [1]), int (self.radar_actual_range / radar_factor), 1)
                

    
    


# # # Klassendefinition Explosion
class explosion (object):
    def __init__(self, e_type, special_radius, **vargs):
        self.object_id = 0
        self.position = 100,100
        self.colour = 255,255,0 
        
        self.destruct = 0
        self.type = e_type
        self.radius = special_radius
        self.special_radius = special_radius + 5
        self.start_radius = vargs.get ('start_radius')
        self.end_radius = vargs.get ('end_radius')
        self.zaehler = 2
        if self.type == 4: self.zaehler = self.start_radius
        if self.type == 4: self.parent_id = vargs.get ('parent_id')
        if self.type == 5: self.colour = BROWN

        if 'colour' in vargs: self.colour = vargs ['colour']
        if 'position' in vargs: self.position = vargs ['position'] 

        explosion_list.append (self)

    #######################################     End : __Init__ 

    def set_position (self, x,y):
        self.position = x,y

    def adjust_position (self, x,y ):
        # self.position = dfunctions.vadd ((x,y), self.position)
        if self.type == 4:
            self.position = ship.output_position (object_list [self.parent_id] ) 
             

    def circle (self):
        
        
        
        x,y = self.position
        if self.type == 1:    ### ship explosion 
            if self.zaehler < self.radius * 0.67: pygame.draw.circle (screen, self.colour, (int(x),int(y)), int(self.zaehler),2)  ### inner explosion circle
            pygame.draw.circle (screen, self.colour, (int(x),int(y)), int(self.zaehler * 1.5),1)    ### outer explosion circle ;; expands faster 
            self.zaehler +=  1.5
            if self.zaehler > self.radius: self.destruct = 1

        if self.type == 2:
            if self.zaehler < 4: pygame.draw.circle (screen, self.colour, (int(x),int(y)), int(self.zaehler),2)
            pygame.draw.circle (screen, self.colour, (int(x),int(y)), int(self.zaehler * 1.5),1)
            self.zaehler = self.zaehler + 1.5
            if self.zaehler > 5: self.destruct = 1

        if self.type == 3:
            
            if self.zaehler < self.special_radius / 2 : pygame.draw.circle (screen, BLUE, (int(x),int(y)), int(self.zaehler),2)
            pygame.draw.circle (screen, BLUE, (int(x),int(y)), int(self.zaehler * 1.5),1)
            self.zaehler = self.zaehler + 2.5
            if self.zaehler > self.special_radius : self.destruct = 1

        if self.type == 4:    ### shield breakdown
            
            pygame.draw.circle (screen, BLUE, (int(x),int(y)), int (self.zaehler), 2)
            self.zaehler += 1.5  
        
            if self.zaehler > self.end_radius: self.destruct = 1 


                

    def output_destruct (self):
            return self.destruct


# # # Class definition delayed_effect ## Start
class delayed_effect (object):
    def __init__ (self, effect_type, timer, additional_information, **wargs):
        self.effect_type = effect_type
        self.timer = int (timer)
        self.additional_information = additional_information
        self.ship_id = wargs ['ship_id'] 
        

    def update (self):
        
        out = 1 
        self.timer -= 1
        if self.timer == 0:
            if self.effect_type == 1: delayed_effect.create_delayed_missile (self)
        if self.timer < 0: out = 0
        return out ### 0 is the kill signal 
            



    def create_delayed_missile (self):
        m = missile (DELAYED_EXPLOSION, 0, 0, 0, self.ship_id)
        missile.set_position ( m, self.additional_information [0] [0], self.additional_information [0] [1] )
        missile_list.append (m)
        
        
        
    


# # # Klassendefinition # # bullet # # Beginn 

class bullet (object):
    def __init__(self,ship_id, information):
        self.object_id = 0
        self.position = information ['position'] 
        self.speed = 200
        self.direction = 2
        self.travelled = 0
        self.damage = 0
        self.radius = 0 
        self.display_position = self.position
        self.normalized_position = self.position
        self.radar_position = self.position
        self.log_position = self.position
        self.last_frame_position = None
        self.shield_piercing = information.get ('c_type').get ('shield_piercing')
        if self.shield_piercing == None: self.shield_piercing = 'no' 
        self.type = 'bullet'
        self.type = information ['name']

        self.ion_damage = information ['ion_damage'] 
        self.ship_id = ship_id   ### the id of the ship that fired the bullet
        self.second_colour = None
        self.damage_taken = 0    ### in case of asteroids: they can be destroyed
        self.destroy = 'no'      ### if 'yes', the object will be removed from list the next turn
        self.c_type = information ['c_type']



        self.display_radius = None
        self.explosion = 'no'
        self.explosion_radius = 1
        self.range = 100 
        if self.c_type != None:
            self.explosion = self.c_type.get ('explosion')
            self.explosion_radius = self.c_type.get ('explosion_radius')  
            self.display_radius = self.c_type.get ('display_radius')
            self.range = self.c_type.get ('range')
            
        self.explosion_distance = information.get ('explosion_distance')
        if self.display_radius == None: self.display_radius = 2
        
        self.superclass = 'bullet'
        if self.ship_id == None : self.ship_id = 1000 * 1000 

        

        ###         z- dimension
        
    
        
        self.z_dimension = ('yes' if (pressed [304] == 1 and self.ship_id == 1) else 'no')
        if self.z_dimension == 'yes': self.colour = RED


       
        

    ###############################
    ####### End     __init__
    ###############################

    def set_second_colour (self,x): self.second_colour = x 

    def set_type (self,x): self.type = x
    def output_type (self): return self.type

    def output_ship_id (self): return self.ship_id

 

    def output_destroy (self): return self.destroy 

    

    def adjust_position (self, x,y ): self.position = dfunctions.vadd ((x,y), self.position)

    def output_last_frame_position (self): return self.last_frame_position

    def set_shield_piercing (self): self.shield_piercing = 'yes'

    def output_shield_piercing (self): return self.shield_piercing 

        
    # input - Methoden:
    def set_velocity (self, x):
        self.speed = x

    def set_range (self,x): self.range = x

    def set_damage (self, x): self.damage = x


    def set_position (self, x,y):
        self.position = x,y

    def set_direction (self, x):
        self.direction = x

    def set_colour (self, x,y,z):
        self.colour = x,y,z
        if self.z_dimension == 'yes': self.colour = MAGENTA

    def set_radius (self, x): self.radius = x
    def output_radius (self): return self.radius
          
                            

        
    

    #interne aktualisierung/ Verrechnung
    def update_position (self):
        
      
       
        
        if self.speed >= 200: self.last_frame_position = self.position
        x,y = self.position
        x = x + self.speed * speed_factor * math.sin (self.direction)
        y = y + self.speed * speed_factor * math.cos (self.direction)
        self.position = x,y
        self.travelled = self.travelled + math.fabs (self.speed * speed_factor)

        self.normalized_position = dfunctions.vadd (self.position, NEGATIVE_MIDDLE)
        self.radar_position = dfunctions.skalar_multi ( 1 / radar_factor, self.normalized_position)
        self.log_position = dfunctions.skalar_multi ( 1 / log_factor, self.normalized_position)

        if self.explosion_radius != None and self.explosion_distance != None and self.travelled >= self.explosion_distance:
            for ship in ship_list:
                if collide_2 (self.position, self.explosion_radius, ship.position, ship.radius) == 1: ship.process_damage (self.damage, ['front', 'left', 'right', 'back'] [random.randint (0,3)], 'no', self.ship_id)
            e = explosion ( 1, self.explosion_radius, colour = ORANGE, position = self.display_position)
            self.destroy = 'yes' 
        

    def update_direction (self,x):
        self.direction = self.direction + x
    #graphik output
    def circle (self):
        
        
      
        if log_factor == 1: self.display_position = self.position
        if log_factor != 1: self.display_position = dfunctions.vadd (MIDDLE, self.log_position)
        if (0 < self.display_position [0] < SCREEN_SPLIT ) and ( 0 < self.display_position [1] < SCREEN_Y):
            x,y = self.display_position
            pygame.draw.circle (screen, self.colour, (int(x),int(y)), self.display_radius,0)
            if self.second_colour != None and master_frame_counter % 10 in [1,2,3]:  pygame.draw.circle (screen, self.second_colour, (int(x),int(y)), max (1, self.display_radius),0)
          

    # output - Methoden

    def output_position (self): return (self.position)

    def output_range (self): return (self.range)
    def output_damage (self): return (self.damage)

    def output_speed (self): return (self.speed)

    def output_direction (self): return (self.direction)  
        
    def output_travelled (self): return (self.travelled)

    
#########################################################
# # # ##  Klassendefinition ## bullet ## ende
#########################################################



##########################################################
##################  Klassendefinition Asteroid Beginn
##########################################################

# # # Klassendefinition # # bullet # # Beginn 

class asteroid (object):
    def __init__(self,position, radius):
        self.speed = 0 
        self.ship_id = None 
        self.z_dimension = 'no' 
        self.position = position
       
        self.radius = radius
        self.display_position = self.position
        self.normalized_position = self.position
        self.radar_position = self.position
        self.log_position = self.position
       
        self.damage_taken = 0    ### in case of asteroids: they can be destroyed
        self.destroy = 'no'
        self.colour = BROWN 
        


        self.superclass = 'asteroid'

        asteroid_list.append (self) 

        

        ###         z- dimension

    ###############################
    ####### End     __init__
    ###############################

    def update (self):
        self.circle ()
        self.check_asteroid_bullets ()

    def adjust_position (self, x,y ): self.position = dfunctions.vadd ((x,y), self.position)

    def explode (self):
        for i in range (0, self.radius ** 2 ):
            debris  (self.display_position, 100, 1.57 * random.uniform (0,4), colour = BROWN, damage = 1  )
                            
        



    def check_asteroid_bullets (self):   ### is the asteroid beeing hit by bullets 


        for bull in (bullet_list + missile_list) [:]:
            
            
            hit_1 = collide_2 (self.position,self.radius,bull.position,bull.radius)
            
            
        
            if hit_1 == 1:
                damage = bull.damage
                if type (damage) is str:
                    damage = MISSILE_DAMAGE_MATRIX ['asteroid'] [damage] 
            
                
               
                # write (str (hit_direction), (100,100), BLUE, 50)
             
                if bull.superclass == 'bullet': bullet_list.remove (bull)
                if bull.superclass == 'missile': missile_list.remove (bull)
                self.damage_taken  += damage
                if self.damage_taken >  0.25 *  self.radius ** 2 :
                    try:
                        asteroid_list.remove (self)
                      
                    except:
                        pass 
                    e = explosion (1,int (self.radius * 1.5), position = self.display_position, colour = BROWN)
                    self.explode ()    
                
                  
                
                e = explosion (2, 0, position = bull.display_position)
                
   

 
    


       

    def update_direction (self,x):
        self.direction = self.direction + x
    #graphik output
    def circle (self):
        
        
       
        if log_factor == 1: self.display_position = self.position
        if log_factor != 1: self.display_position = dfunctions.vadd (MIDDLE, self.log_position)
        if (0 < self.display_position [0] < SCREEN_SPLIT ) and ( 0 < self.display_position [1] < SCREEN_Y):
            x,y = self.display_position
            pygame.draw.circle (screen, self.colour, (int(x),int(y)), self.radius,0)
          
    



##########################################################
##########################################################



########################################################
# # # ## Klassendefinition ## cannon ## beginn
########################################################

class cannon (object):
    def __init__(self,info, carrier_id, **wargs):
        

        c_type = info [0]
        if len (info) == 3: 
            fore = info [1]
            side = info [2]
        if len (info) == 2:
            fore = 0
            side = info [1]
            
        global master_object_counter
        master_object_counter += 1
        object_list.append (self)
        self.object_id = len (object_list) - 1
        cannon_list.append (self)
        
    
        self.position = 100,100
        self.c_type = c_type
        
        self.direction = 2
        self.colour = 255,0,0
        self.radius = 2
        self.carrier_id = carrier_id
        
        self.fore = fore   # wie weit ist die kanone nach vorne versetzt vom Schiffsmittelpunkt aus
        self.side = side    # wie weit ist die Kanone zur Seite versetzt vom Schiffsmittelpunkt aus
        self.name = c_type.get ('name')
        self.range = c_type.get ('range') 
        self.velocity = c_type.get ('velocity')
        self.damage = c_type.get ('damage')
        self.cooldown = c_type.get ('cooldown')
        self.maximum_load = c_type.get ('maximum_load')
        self.ammo_weapon = ('yes' if c_type.get ('ammo_weapon') == 'yes' else 'no')
        self.ion_damage = ('yes' if c_type.get ('ion_damage') == 'yes' else 'no') 
        self.speed = self.velocity
        self.cooldown_counter = 0
        self.load = self.maximum_load
        self.load_counter = self.cooldown * frame_rate * 5
        self.turret = 'no'    # is this cannon built into a turret? # if yes: object_number of the turret
        if 'turret' in wargs and wargs.get ('turret') == 'yes': self.turret = 'yes'

        ###
        if self.turret == 'no': self.ship_id = self.carrier_id
        elif self.turret == 'yes': self.ship_id = object_list [self.carrier_id].ship_id
        else: raise ValueError ('fucked up') 


        ###
        self.colour = c_type.get ('colour')
        self.second_colour = c_type.get ('second_colour')
        self.burst = c_type.get ('burst')
        self.burst_timer = 0
        self.burst_counter = 0
        self.burst_delay = 4       # Number of frames between shots of the same burst
        self.explosion = c_type.get ('explosion')
        self.explosion_radius = c_type.get ('explosion_radius')
        self.explosion_distance = None
        

        
    # input - Methoden:
    def set_speed (self, aa):
        self.speed = aa

    def output_range (self): return self.range 

    def output_load (self): return self.load 

    def set_turret (self,x): self.turret = x 

    def set_position (self, x,y):
        self.position = x,y

    def set_direction (self, x):
        self.direction = x

        

    def set_colour (self, x,y,z):
        self.colour = x,y,z

    def set_object_id (self,x): self.object_id = x

    # def set_ship_id (self,x): self.ship_id = x 
    

    #interne aktualisierung/ Verrechnung

    ######################################################################### 
    def update_position (self):
        if self.turret == 'no': 
            self.position = dfunctions.forthogonal_line ( dfunctions.fextrapolate_line (ship.output_direction (object_list [self.carrier_id]),ship.output_position (object_list [self.carrier_id]),0,self.fore) [1], ship.output_direction (object_list [self.carrier_id]), self.side) [1]
            
            self.direction = ship.output_direction (object_list [self.carrier_id])

        if self.turret != 'no': 

            self.position = dfunctions.forthogonal_line ( dfunctions.fextrapolate_line (turret.output_direction (object_list [self.carrier_id]),turret.output_position (object_list [self.carrier_id]),0,self.fore) [1], turret.output_direction (object_list [self.carrier_id]), self.side) [1]
            
            self.direction = turret.output_direction (object_list [self.carrier_id])
    #############################################################################


        ### update_burst_cooldown

    def update (self):
        

        if self.burst != None:
            if self.burst_timer > 0 :
                self.burst_timer -= 1
            if self.burst_counter > 0 and self.burst_timer == 0:
                self.create_bullet ()
                self.burst_counter -= 1
                self.burst_timer = self.burst_delay


        

    def update_cooldown (self):
        self.cooldown_counter = dfunctions.count_down_to_zero (self.cooldown_counter)
        if self.load < self.maximum_load and self.ammo_weapon == 'no':
            self.load_counter -= 1
            if self.load_counter == 0:
                self.load += 1
                self.load_counter = self.cooldown * frame_rate * 5 
        if self.ship_id == 1:
            global crosshairs_colour
            crosshairs_colour = FAINT_WHITE
            if self.load >0:
                
                crosshairs_colour = GREEN
                
                

        
    
    #graphik output
    def circle (self):
        x,y = self.position
        pygame.draw.circle (screen, self.colour, (int(x),int(y)), self.radius,0)

    # output - Methoden

    def output_position (self): return (self.position)

    def output_speed (self): return (self.speed)

    def output_direction (self): return (self.direction)

    def shoot (self, **wargs):

        if self.cooldown_counter <= 0 and self.load > 0:
            cannon.create_bullet (self, **wargs)
            self.cooldown_counter = int (self.cooldown * frame_rate )
            self.load -= 1
            if self.burst != None:
                self.burst_counter = self.burst - 1
                self.burst_timer = self.burst_delay 
        

            
            

    def create_bullet (self, **wargs):
        x,y = self.position
        x1 = math.sin (self.direction)
        y1 = math.cos (self.direction)
            

        b = bullet (self.ship_id, {'name': self.name,'position': ( x + 10 * x1,y + 10 * y1),  'ion_damage': self.ion_damage, 'c_type': self.c_type, 'explosion_distance': wargs.get ('explosion_distance')})
      
        bullet.set_range (b, self.range)
        bullet.set_velocity (b, self.velocity)
        bullet.set_damage (b, self.damage)
        bullet.set_colour (b, self.colour [0],self.colour [1],self.colour [2])
        bullet.set_second_colour (b, self.second_colour) 

 
        
        x = self.direction
        bullet.set_direction (b,x)
        bullet_list.append (b)
        


    
########## Klassendefinition cannon Ende 

# # # Klassendefinition # # missile # # Beginn 

class missile (object):
    def __init__(self, m_type, target_id, direction, speed,ship_id, **wargs):
        self.object_id = 0
        self.position = 100,100
        self.speed = 250
        self.direction = direction
        self.set_direction = direction
        # self.colour = 0,0,255
 
 
        self.range = 1500 ### vor-festlegung!!! der echte wert wird spaeter gesetzt
        
        self.travelled = 0
        self.target_position = 0
        self.target_rel_pos = 0
        self.type_info = m_type
        self.type = self.type_info [0]
        self.move_info = self.type_info [1]
        self.colour = self.type_info [2]
        self.top_speed = self.move_info [0]
        
        self.accel = self.move_info [2]
        self.explosion_radius = self.move_info [3]
        self.speed = speed
        self.top_man = self.move_info [1]   # man = maneuverability
        self.man = self.top_man
        self.target_id = target_id
        self.cone_angle = 30
        self.turn_amount = 0
        self.missile_vorhalt = 0
        self.display_position = self.position
        self.normalized_position = self.position
        self.radar_position = self.position
        self.log_position = self.position
        self.timer = 1
        self.damage = xget (m_type, 'damage')
        self.display_radius = 2
        self.ship_id = ship_id
        self.explosion_radius = xget (m_type, 'explosion_radius')
        if self.explosion_radius == None: self.explosion_radius = 1 
        self.radius = self.explosion_radius 
        if self.explosion_radius == None: self.explosion_radius = 1
        self.superclass = 'missile'
        self.ion_damage = 'no'
        self.shield_piercing = 'yes'

        global pressed
        
        self.z_dimension = ('yes' if pressed [304] == 1 else 'no')
        if self.z_dimension == 'yes': self.second_colour = GREEN


    ######          END:    Init

        

    
    def output_damage (self): return self.damage 

    def output_explosion_radius (self): return self.explosion_radius

    def set_missile_vorhalt (self,x): self.missile_vorhalt = x

    def adjust_position (self, x,y ): self.position = dfunctions.vadd ((x,y), self.position)

    def output_range (self): return self.range    
    # input - Methoden:
    def set_speed (self, aa):
        self.speed = aa

    def set_position (self, x,y):
        self.position = x,y

    def set_direction (self, x):
        self.direction = x

    def set_colour (self, x,y,z):
        self.colour = x,y,z

    def set_radius (self, x):
        self.radius = x

    def set_target_position (self,x,y):
        self.target_position = x,y

    def output_timer (self): return self.timer
        
    

    #interne aktualisierung/ Verrechnung
    def update_position (self):
        if self.type == 'delayed' :
            self.timer -= 1
            

        if self.speed < self.top_speed: self.speed = add_limit (self.speed, self.accel / frame_rate, self.top_speed)
        if self.speed > self.top_speed: self.speed = substract_limit (self.speed, 10 / frame_rate, self.top_speed)
        
        x,y = self.position
        x = x + self.speed * speed_factor * math.sin (self.direction)
        y = y + self.speed * speed_factor * math.cos (self.direction)
        self.position = x,y
        self.travelled = self.travelled + math.fabs (self.speed * speed_factor)

        self.normalized_position = dfunctions.vadd (self.position, NEGATIVE_MIDDLE)
        self.radar_position = dfunctions.skalar_multi ( 1 / radar_factor, self.normalized_position)
        self.log_position = dfunctions.skalar_multi ( 1 / log_factor, self.normalized_position)
        

        

    def update_direction (self):
        self.turn_amount = self.man / ( 360 * frame_rate)
        
        if self.type in ['radar', 'heatseeking' ] and self.target_id not in [None, 'na']: 

            if dfunctions.fradar_cone (self.direction, self.position, ship.output_position (object_list [self.target_id]) , self.cone_angle) == 1:
                xs,ys = self.position
                xt,yt = ship.output_position (object_list [self.target_id])
                global master_frame_counter
                if master_frame_counter % 3 == 0: pygame.draw.aaline ( screen, BLUE, (xs,ys), (xt,yt), 1)
                # self.target_rel_pos = (xt - xs, yt -ys)
                bearing = math.atan2 ((xt - xs),(yt - ys))
                bearing += self.missile_vorhalt

                heading = self.direction
                rel_dir = dfunctions.relative_direction (heading, bearing)
                rel_dir_norm = dfunctions.one_or_minus_one (rel_dir)
                self.direction = dfunctions.aa (self.direction, rel_dir_norm * self.turn_amount)

        if self.type == 'heatseeking':
            # write (self.target_id, (400,100), BLUE, 15)

            if dfunctions.fradar_cone (self.direction, self.position, ship.output_position (object_list [self.target_id]) , self.cone_angle) == 1:
                
                if dfunctions.fheat_cone (ship.output_direction (object_list [self.target_id]), ship.output_position (object_list [self.target_id]), self.position, ship.output_heat_cone (object_list [self.target_id])) == 1:
                    xs,ys = self.position
                    xt,yt = ship.output_position (object_list [self.target_id])
                    global master_frame_counter
                    if master_frame_counter % 3 == 0: pygame.draw.aaline ( screen, RED, (xs,ys), (xt,yt), 1)
                    # self.target_rel_pos = (xt - xs, yt -ys)
                    bearing = math.atan2 ((xt - xs),(yt - ys))
                    bearing += self.missile_vorhalt 

                    heading = self.direction
                    rel_dir = dfunctions.relative_direction (heading, bearing)
                    rel_dir_norm = dfunctions.one_or_minus_one (rel_dir)
                    self.direction = dfunctions.aa (self.direction, rel_dir_norm * self.turn_amount)


                
        
    #graphik output
    def circle (self):
        global log_factor
        if log_factor == 1: self.display_position = self.position
        if log_factor != 1: self.display_position = dfunctions.vadd (MIDDLE, self.log_position)
    
        x,y = self.display_position
        pygame.draw.circle (screen, self.colour, (int(x),int(y)), self.display_radius,0)

        line_end, line_start = dfunctions.fextrapolate_line (self.direction, self.display_position, -2, -8) 
        if self.type != 'mine': pygame.draw.line (screen, WHITE, line_start, line_end)
        
        if DISPLAY_MISSILE_CONE == 'yes':
            if self.type == 'heatseeking' or self.type == 'radar' :
                dfunctions.display_missile_cone (self.position, self.direction, self.cone_angle )

    # output - Methoden

    def output_position (self): return (self.position)

    def output_speed (self): return (self.speed)

    def output_direction (self): return (self.direction)  
        
    def output_travelled (self): return (self.travelled)

    def output_type (self):return self.type
# # # ##  Klassendefinition ## missile ## ende
##################################################
###################################################
###################################################
# # # Klassen - Definition : Ship # # Anfang # # 
class ship (object): 
    def __init__(self, s_type, **wargs):
        ###         I       initial stuff 
        global master_object_counter 
        master_object_counter = master_object_counter + 1
        self.object_id = master_object_counter
        object_list.append (self)
        self.ship_id = self.object_id   ### wahrscheinlich veraltet 

        ### 

        self.complete_information = wargs ['complete_information']

        ### 


        
        self.autopilot_destination = xget (self.complete_information, 'autopilot_destination') 
   
        self.position = wargs ['position']
        self.direction = ( 1.57 if wargs.get ('direction') == None else wargs ['direction'] ) 
        self.damage = 0
        self.death_delay = -1   ###     -1 = ship is healthy ## 0: destroy immediately   ### > 0 : death countdown
        self.player = wargs ['player']

        ###         cannons
        
    
        self.cannon_ids = []
        self.cannons_sorted = []

        

        for item in s_type ['guns']:
            c = cannon (item, self.object_id )
            self.cannon_ids.append (c.object_id)

        self.sort_guns ()
      

        ### turrets 
        self.turrets = []
        for t in s_type ['turrets']:
            tur = turret (t, self.object_id)
            self.turrets.append (tur)
            

        self.turret_ids = []
        for t in self.turrets:
            self.turret_ids.append (t.object_id) 
        ###
        
        self.type_info = s_type
        
        self.weapon_info = s_type.get ('guns')
        self.move_info = s_type.get ('movement')
        self.top_speed = self.move_info [0]
        self.turret_info = s_type.get ('turrets')
        self.top_accel = self.move_info [2]
        self.accel = self.top_accel
        self.speed = self.top_speed
        self.top_man = self.move_info [1]   # man = maneuverability
        self.man = self.top_man
        self.set_speed = self.top_speed 
        self.turn_amount = 0
        ## ai - variablen
        self.ai_shoot = 0
        self.target = None
        self.target_direction = 0
        self.target_bearing = 0
        self.graphics = copy.deepcopy (s_type.get ('graphics'))
        if self.graphics [0] == 'polygon': self.graphics [1] = [self.graphics [1]] 
        
        self.hitbox = s_type.get ('hitbox')
       
        self.radius = self.hitbox [1]
   
        
        self.missile_launchers = s_type.get ('missile_launchers')
        self.torpedo_launchers = s_type.get ('torpedo_launchers')
        if self.torpedo_launchers == None: self.torpedo_launchers = 0
        
        self.torpedo_cooldowns = []
        for i in range (0, self.torpedo_launchers):
            self.torpedo_cooldowns.append (0)
            
        self.missile_cooldowns = []
        for i in range (0, self.missile_launchers):
            self.missile_cooldowns.append (0)  ### schiffe starten mit cooldown von null
       
        
        self.speed_setting = 10
        self.full_sas = s_type.get ('sas') ### shields, armor, structure , damage_reduction
        self.actual_sas = copy.deepcopy (self.full_sas)
        self.heat_cone = 40
        self.moved = (0,0)
        self.normalized_position = (0,0)
        self.fadenkreuz_direction = 0
        self.fadenkreuz_size = 5
        self.radar_position = (0,0)

        ###         Afterburner

        self.AFTERBURNER_GLIDING_TIME = AFTERBURNER_GLIDING_TIME 
        self.afterburner_gliding_multiplicator = s_type.get ('afterburner_gliding_multiplicator')
        if self.afterburner_gliding_multiplicator != None : self.AFTERBURNER_GLIDING_TIME *= self.afterburner_gliding_multiplicator
        
        self.AFTERBURNER_COOLDOWN = AFTERBURNER_COOLDOWN
        self.AFTERBURNER_COOLDOWN *= ( 1 if s_type.get ('afterburner_cooldown_modificator') == None else s_type.get ('afterburner_cooldown_modificator'))

        self.AFTERBURNER_ACCELERATION_TIME = AFTERBURNER_ACCELERATION_TIME
        self.AFTERBURNER_ACCELERATION_TIME *= ( 1 if s_type.get ('afterburner_acceleration_modificator') == None else s_type.get ('afterburner_acceleration_modificator'))

        self.AFTERBURNER_ACTIVATION_TIME = AFTERBURNER_ACTIVATION_TIME
        self.AFTERBURNER_ACTIVATION_TIME *= (1 if s_type.get ('afterburner_activation_modificator') == None else s_type.get ('afterburner_activation_modificator') ) 
        
        
        
        #

        self.AFTERBURNER_COOLDOWN_timer = self.AFTERBURNER_COOLDOWN 
        self.afterburner_speed = 0
        self.afterburner_direction = self.direction
        self.afterburner_activation = 0
     
        self.afterburner_delay_counter = 0
        self.afterburner_frame_counter = 0
        self.afterburner_top_speed = self.move_info [3]
        self.afterburner_acceleration = self.afterburner_top_speed  / (frame_rate * self.AFTERBURNER_ACCELERATION_TIME)   
        self.afterburner__gliding_frame_time = self.AFTERBURNER_GLIDING_TIME * frame_rate
        self.afterburner_nac = 2 * self.afterburner_top_speed / (math.pow (self.AFTERBURNER_GLIDING_TIME * frame_rate , 2) )               # negative acceleration constant
        self.afterburner_negative_acceleration = self.afterburner_nac * self.afterburner_frame_counter
        ###
       
      
        ###         End : Afterburner 
        
        self.missile_vorhalt = 0
        self.display_position = self.position
        self.log_position = self.position
        
        if self.player == 1: self.colour = BLUE
        if self.player == 0: self.colour = RED
        self.radar_top_range = 2000
        if 'radar' in s_type: self.radar_top_range = s_type.get ('radar')
        self.radar_actual_range = self.radar_top_range
        self.ships_on_radar = []
        self.speed_mode = 'm'
        self.set_speed_mode = 'm'
        self.speed_mode_timer = - 100   ### timer for switching between speed modes
        self.speed_mode_timer_max = 400    ### frames it takes to switch speed 
        if 'speed_mode' in wargs: self.speed_mode = wargs.get ('speed_mode')
        if xget (self.complete_information, 'speed_mode') != None: self.speed_mode = xget (self.complete_information, 'speed_mode')

        ###         Energy_Points
        self.energy_points = 3
        self.energy_points_decay_timer = - 100
        self.energy_points_reload_timer = 0
        self.max_energy_points = 3 


        
        self.gliding_phase = 'no'
        self.gliding_timer = 0 
        self.micro_missile_counter = []
        self.ship_class = s_type.get ('ship_class')
        self.stealthed = 'no'
        #self.stealth_device = 'no'
        self.stealth_device = xget (self.complete_information, 'stealth_device')
        #if self.stealth_device == None: self.stealth_device = 'no' 
        self.stealthed_activation_timer = - 100
        self.stealthed_deactivation_timer = - 100
        self.team = 0
        if 'team' in wargs: self.team = wargs.get ('team')
        if self.team == 0 and self.player == 1: self.colour = WHITE
        if self.team == 0 and self.player == 0: self.colour = BLUE
        if self.team == 1: self.colour = RED
        self.vorhalt_direction = 0
        
        self.shield_supercharge = 0
        self.shield_supercharge_timer = 0
        self.enemy_ship_list = []
        self.shield_down_timer = 0
        self.shield_generator_damage = 0
        self.engine_damage = 0
        self.cannon_damage = 0
        self.missile_damage = 0
        self.turret_damage = 0 
        self.ship_class = s_type.get ('ship_class')
        self.pilot_quality = xget (self.complete_information, 'pilot_quality') 
        if self.pilot_quality == None : self.pilot_quality = 'average'
        
        self.pilot_clock = 0
        self.pilot_vorhalt_modificator = None
        self.pilot_inaccuracy_modificator = None
        self.real_vorhalt_direction = 0
        self.booster_timer = 0
        self.booster_active = 'no'

        self.mission_id = xget (self.complete_information, 'mission_id')
       
        
        self.damage_threshold = s_type.get ('damage_threshold')
        if self.damage_threshold == None: self.damage_threshold = 2

        ####        Autopilot
        
        self.autopilot_destination = xget (self.complete_information,'autopilot_destination')
        self.autopilot_position = (0,0)
        
        self.destination_object_id = None

        self.lead_ship = xget (self.complete_information, 'lead_ship')
        self.autopilot_lead_ship = xget (self.complete_information, 'autopilot_lead_ship') 
        self.destination = xget (self.complete_information, 'destination')

         
        self.name = s_type.get ('name')
        self.enemy_ship_list = []
        self.enemy_ship_list_tvalues = []
        self.target_object_id = None
        self.target_priorities = xget (self.complete_information, 'target_priorities')
        self.maneuver_mode = 'normal'
        self.maneuver_dict = {}
        self.kill_value = s_type.get ('kill_value')
        ###     ship disabled: 
        self.ion_damage = 0
        self.disabled = 'no'
        self.shield_blink = 0
        self.delayed_death = -1 

        self.just_jumped_in = ( 'yes' if xget (self.complete_information, 'just_jumped_in') == 'yes'   else 'no' )
       
        self.special_hitboxes = copy.deepcopy (xget (self.complete_information, 'special_hit_boxes'))

        self.z_dimension = 'no'

        self.shrink_factor = 1 

        
   
        
        

    ###############
    ###############
    ###############     End     __init__
    ###############
    ###############


        
    ##################################################################
    def update (self):
        self.update_functions ()
        self.update_stuff ()
    ##################################################################


    #############################################
    def update_functions (self):

        ship.update_enemy_ship_list (self)
        ship.select_target (self) 

        ship.update_stealthed (self)
        ship.update_micro_missile (self)
        ship.update_gliding_phase (self)
        ship.update_speed_mode (self)
        ship.update_energy_points (self)
        
    
        ship.update_booster (self) 
        ship.update_shield_supercharge (self)

                
        ship.display_stuff_if_player (self)
        ship.display_stuff_for_debug (self)
        ship.display_stuff_if_target (self)
        self.update_fadenkreuz ()
        self.update_man ()

    ####################################################

        
    ####################################################
    def update_stuff (self):
        ###     I       initiates jumped-in flash 
        if self.just_jumped_in == 'yes':
            self.just_jumped_in = 'no'
            e = explosion ( 1, 40, colour = WHITE, position = (self.display_position if self.display_position != None else self.position))
            

        
       

            
        ###     III     initiates shield supercharge 
        if self.player == 1 and pressed [pygame.K_s] == 1 and pressed [308] == 1: ship.initiate_shield_supercharge (self)

        ###     IV      handles delayed death 
        if self.delayed_death > 0:
            self.delayed_death -= 1
        if self.delayed_death == 0:
            self.damage = 1
            self.delayed_death = -1 
     ################################################################       




    ##################################################################
    def update_enemy_ship_list (self):
        self.enemy_ship_list = []
        self.enemy_ship_list_tvalues = []
        for s in ship_list:
            if s != self:
               
                
                if s.team != self.team:
                    target_value = ship.determine_target_value (self,s)
                    
                    self.enemy_ship_list.append (s) 
                    self.enemy_ship_list_tvalues.append ((s,target_value))


    #############################################
    def sort_guns (self):
        self.cannons_sorted = split_list_by_key (self.cannon_ids, lambda x: object_list [x].name )
    #############################################
                       
    ############################################################
    def determine_relative_bearing (self,target, **wargs):
        relative_position = vector_sub (target.position, self.position)
        absolute_bearing = math.atan2 (*relative_position)
        relative_bearing = absolute_bearing - self.direction
        
        relative_bearing = math.fabs (relative_bearing)
        if relative_bearing > 3.14: relative_bearing = math.fabs (relative_bearing - 2 * 3.14)

        direction = 'right'
        if dfunctions.within_angle_range (self.direction, 3.14, 'clock', absolute_bearing) == True: direction = 'left'
        if 'output_direction' in wargs: return direction 

        return relative_bearing
    ##############################################################

    ##############################################################
    def determine_relative_inverserd_direction (self,target):
        target_direction = target.direction
        inversed_target_direction = dfunctions.aa (target_direction, 3.14)
        d = dfunctions.angle_difference (self.direction, inversed_target_direction)
        return d
    ##############################################################

    def determine_target_distance (self,target):
        rel_pos = vector_sub (target.position, self.position) 
        d = vector_length (rel_pos) 
        return d
    

    ################################################################
    def determine_target_value (self,target):
        
        
        ###
        relative_bearing = ship.determine_relative_bearing (self, target)
        bearing_dict = BetweenDict ( {
            ('<', 10 / 57) : 15,
            (10 / 57, 30 / 57) : 10,
            (30 / 57, 60 / 57) : 5,
            (60 / 57, 90 / 57) : 2,
            ('>', 90 / 57) : 1
            } )

        bearing_points = bearing_dict [relative_bearing]

       

        
        ###
        target_direction_inv = ship.determine_relative_inverserd_direction (self,target)

        direction_dict = BetweenDict ( {
            ('<', 10 / 57) : 7,
            (10 / 57, 30 / 57) : 5,
            (30 / 57, 60 / 57) : 2,
            (60 / 57, 90 / 57) : 1,
            ('>' ,90 / 57) : 0
            } )

        direction_points = direction_dict [target_direction_inv] 

        ###
        distance = ship.determine_target_distance (self,target)

        distance_dict = BetweenDict ({('<',500):15, (500,1000): 10, (1000,1500):5, (1500, 2000):2, ('>', 2000): 0} )
        distance_points = distance_dict [distance]

       
        point_sum = bearing_points   + distance_points

        target_priority = None 
        if target.mission_id != None and self.target_priorities != None: target_priority = self.target_priorities.get (target.mission_id)
        if target_priority != None: point_sum += target_priority 

        return point_sum
    ###########################################################################


    

    def get_cannon_speed (self):
        cannon_speed = cannon.output_speed (object_list [self.cannon_ids [0]])
        return cannon_speed

    def get_cannon_range (self):
        if self.cannon_ids != []: cannon_range = cannon.output_range (object_list [self.cannon_ids [0]])
        else: cannon_range = 200
        return cannon_range 
   
    ########################################################
    def select_target (self):
        if self.target not in [None, 'na']:

            self.enemy_ship_list_tvalues.sort (key = lambda x: - 1 * x [1])
            
       
        if self.enemy_ship_list != []:
            self.target = self.enemy_ship_list_tvalues [0] [0]
            self.target = self.target.object_id
            self.target_object_id = self.target
    #########################################################
           
        
        

    def output_mission_id (self): return self.mission_id 

    def set_mission_id (self, x):
        self.mission_id = x
        

    def output_team (self): return self.team 

    def output_AFTERBURNER_GLIDING_TIME (self): return self.AFTERBURNER_GLIDING_TIME 

    def output_booster_timer (self): return self.booster_timer

    def output_booster_active (self): return self.booster_active 

    def output_energy_points (self): return self.energy_points

    def output_max_energy_points (self): return self.max_energy_points

    def output_energy_points_charge_ratio (self): return self.energy_points_reload_timer / ENERGY_POINTS_CHARGE_TIME

    ###

    def output_engine_counter (self): return self.speed_mode_timer

    def output_engine_counter_max (self): return self.speed_mode_timer_max

    def output_speed_mode (self): return self.speed_mode

    def output_set_speed_mode (self): return self.set_speed_mode

    ####
    
    def output_display_position (self): return self.display_position

    def output_radius (self): return self.radius 

    def display_shield_axis (self):
        for i in range (0,4):
            angle = 45 + i * 90 
            # absolute_angle == aa ( angle, self.direction)
            point_a_1, point_a_2 = dfunctions.angle_line (self.position, self.direction, 200, angle)
            pygame.draw.aaline (screen, BLUE, point_a_1, point_a_2, 1)


    def display_stuff_if_target (self):
        global global_target_object_id 
        if self.object_id == global_target_object_id:
           
            pass

         
    ############################################################
    def display_stuff_if_player (self):
        if self.player == 1:
       

            
        
            
        
                
            if DISPLAY_SHIELD_AXIS == 'yes': ship.display_shield_axis (self)
       
            if global_target_object_id not in [None, 'na']:
                res = ship.determine_relative_bearing (self,object_list[global_target_object_id]) 
                res = round (res,2)
                target = object_list [global_target_object_id ] 
               
    #################################################################            
            
      
    

    def display_stuff_for_debug (self):
        # write (str (self.object_id), dfunctions.vadd (self.position, (0, -10)), RED, 15)
        pass

    def update_autopilot_position (self):
        pass 
   
        

    def output_enemy_ship_list (self): return self.enemy_ship_list 


    def initiate_shield_supercharge (self):
        self.shield_supercharge = 1
        self.shield_supercharge_timer = 0
        self.actual_sas [0] = [0,0,0,0]

        
    #####################################################################
    def update_shield_supercharge (self):
        self.shield_supercharge_timer += 1 
        if self.shield_supercharge == 1:
            if self.shield_supercharge_timer >= SHIELD_SUPERCHARGE_ACTIVATION_TIME:
                self.shield_supercharge = 2
                self.shield_supercharge_timer = 0
        if self.shield_supercharge == 2:
            if self.shield_supercharge_timer >= SHIELD_SUPERCHARGE_DURATION:
                self.shield_supercharge = 0
                self.shield_supercharge_timer = 0
    ########################################################################

    def output_shield_supercharge_phase (self): return self.shield_supercharge
    def output_shield_supercharge_timer (self): return self.shield_supercharge_timer 


    # ship.output_shield_supercharge_phase (object_list [1])
       # player_shield_supercharge_timer = ship.output_shield_supercharge_timer (object_list [1] )
                
        
        

    def update_test_module (self):
        ### pygame.draw.aaline (screen, self.colour, self.position, dfunctions.fextrapolate_line (self.vorhalt_direction, self.position, 0, 200) [1],1)
        pass 


    def output_team (self): return self.team 

    def output_turret_ids (self): return self.turret_ids
    
    #######################################################################
    def switch_stealthed (self):
        if self.stealth_device == 'yes':
            if self.stealthed == 'yes' and self.stealthed_activation_timer <= 0 and self.stealthed_deactivation_timer <= 0 :
                self.stealthed = 'no'
                self.stealthed_deactivation_timer = 120
            if self.stealthed_activation_timer <= 0 and self.stealthed_deactivation_timer <= 0 and self.stealthed == 'no':
                self.stealthed_activation_timer = 120
    #######################################################################
                

    #######################################################################
    def update_stealthed (self):
        self.stealthed_activation_timer -= 1
        self.stealthed_deactivation_timer -= 1
        if self.stealthed_activation_timer == 0: self.stealthed = 'yes'
    #######################################################################
            
            

    def output_stealthed (self): return self.stealthed
    
    #########################################################################
    def initiate_gliding_phase (self):
        if self.energy_points >= 1:
            self.energy_points -= 1 
            self.gliding_phase = 'yes'
            self.gliding_timer = 0
            self.gliding_direction = self.direction
    #########################################################################
            
            
    #########################################################################
    def update_gliding_phase (self):
        if self.gliding_phase == 'yes':
            if self.gliding_timer >= GLIDING_DURATION: 
                self.gliding_phase = 'no'
                self.gliding_timer = 0 
            else: self.gliding_timer += 1
    #########################################################################
            
    def output_gliding_phase (self): return self.gliding_phase

    def output_gliding_timer (self): return self.gliding_timer

    
            

    def output_speed_mode_timer (self): return self.speed_mode_timer

    def output_speed_mode (self): return self.speed_mode
    
    #########################################################################
    def set_speed_mode (self, new_mode):
        speed_mode_ranking = ['off', 's', 'm' , 'h' ]
        new_mode_rank = speed_mode_ranking.index (new_mode)
        old_mode_rank = speed_mode_ranking.index (self.speed_mode)

        if new_mode_rank > old_mode_rank + 1 :
            new_mode = speed_mode_ranking [old_mode_rank + 1]

        if new_mode_rank < old_mode_rank - 1:
            new_mode = speed_mode_ranking [old_mode_rank -1] 

        if new_mode != self.speed_mode:
            if new_mode != None:  
                self.speed_mode_timer = self.speed_mode_timer_max
                self.set_speed_mode = new_mode
    #########################################################################
                
    #########################################################################
    def update_speed_mode (self):
        self.speed_mode_timer -= 1 
        if self.speed_mode_timer == 0:
            if self.set_speed_mode != 'none':
                self.speed_mode = self.set_speed_mode
            
                self.speed_mode_timer = -100
    #########################################################################


    #########################################################################                
    def update_energy_points (self):
        if self.energy_points < self.max_energy_points: self.energy_points_reload_timer += 1
            
        if self.energy_points_reload_timer == ENERGY_POINTS_CHARGE_TIME:
            if self.energy_points < self.max_energy_points:
                self.energy_points += 1
                self.energy_points_reload_timer = 0
    #########################################################################

    def output_energy_points (self): return self.energy_points

    
    #########################################################################
    def use_energy_sphere (self):
        if self.energy_points > 0:
            self.energy_points -= 1
            if self.energy_points == 0: self.energy_points_reload_timer = 1000
            if self.energy_points > 1: self.energy_points_decay_timer = 1000
    #########################################################################
    
        

    def output_set_speed_mode (self): return self.set_speed_mode 
        
        
    #########################################################################
    def output_target (self):
        if self.player == 1: self.target_object_id = global_target_object_id
        return self.target_object_id
    #########################################################################
   

    

    
        
        

    def output_booster (self): return self.booster

    ###### ENDE : löschen
    #       self.booster_timer = 0
    #       self.booster_active = 'no'
    #########################################################################
    def activate_booster (self):
        if self.energy_points >= 1:
            self.energy_points -= 1
            self.booster_active = 'yes'
    #########################################################################


    #########################################################################            
    def update_booster (self):
        if self.booster_active == 'yes':
            if self.booster_timer >= BOOSTER_DURATION :
                self.booster_active = 'no'
                self.booster_timer = 0
            else: self.booster_timer += 1 
     #########################################################################           

    
        
    

    def set_missile_vorhalt (self,x): self.missile_vorhalt += x

    def output_afterburner_speed (self): return self.afterburner_speed
    def output_man (self): return self.man    # man = maneuverability


    ###             Afterburner 

    #########################################################################
    def activate_afterburner (self):
     
        if self.AFTERBURNER_COOLDOWN_timer == self.AFTERBURNER_COOLDOWN and self.energy_points >= 1:
            self.energy_points -= 1 
            self.afterburner_activation = 1
            self.afterburner_delay_counter =  0
    #########################################################################
    
    
    #########################################################################
    def update_afterburner (self):
        if self.player == 1:
            
            #write ('activation  ' +str (self.afterburner_activation), (300,80), GOLD, 15)
            #write ('acceleration ' +str (self.afterburner_acceleration), (300,140), GOLD, 15)
            #write ('afterburner_direction  ' +str (self.afterburner_direction), (300,110), GOLD, 15)
            #write ('activation  ' +str (self.afterburner_activation), (300,80), GOLD, 15)
            #write ('negative_acceleration  ' +str (self.afterburner_negative_acceleration), (600,80), GOLD, 15)
            #write ('frame_counter  ' +str (self.afterburner_frame_counter), (600,50), GOLD, 15)
            #write ('AFTERBURNER_COOLDOWN' +str (self.AFTERBURNER_COOLDOWN), (600,20), BLUE, 15)
            #write (' afterburner_delay_counter ' + str (self.afterburner_delay_counter), (700,150), BLUE, 15)
            
          
          
            pass

        #       PHASE 0 
        if self.afterburner_activation == 0 and self.AFTERBURNER_COOLDOWN_timer != self.AFTERBURNER_COOLDOWN: self.AFTERBURNER_COOLDOWN_timer += 1 

        
        #       PHASE 1         : Activation 
        if self.afterburner_activation == 1:
            if self.afterburner_delay_counter >= self.AFTERBURNER_ACTIVATION_TIME:
                ### activate acceleration phase:
                self.afterburner_direction = self.direction
                self.afterburner_activation = 2
                self.afterburner_delay_counter = 0 
            if self.afterburner_delay_counter < self.AFTERBURNER_ACTIVATION_TIME: self.afterburner_delay_counter += 1 

            
        #       PHASE 2         : Acceleration 
        elif self.afterburner_activation == 2:
            afterburner_acceleration = self.afterburner_top_speed / self.AFTERBURNER_ACCELERATION_TIME
            
            if self.afterburner_delay_counter >= self.AFTERBURNER_ACCELERATION_TIME:
                self.afterburner_activation = 3
                self.afterburner_delay_counter = 0 
            else:
                self.afterburner_speed += afterburner_acceleration
                self.afterburner_delay_counter += 1 
            



            
        #       PHASE 3         : Decelleration + Gliding 
        if self.afterburner_activation == 3:   
            if self.afterburner_delay_counter >= self.AFTERBURNER_GLIDING_TIME:
                self.afterburner_activation = 0
                self.afterburner_delay = 0
                self.AFTERBURNER_COOLDOWN_timer = 0
                self.afterburner_speed = 0 

            else:
                self.afterburner_delay_counter += 1 
                neg_afterburner_acceleration = self.afterburner_top_speed / (0.5 * self.AFTERBURNER_GLIDING_TIME)
                if self.afterburner_delay_counter >= self.AFTERBURNER_GLIDING_TIME / 2 :
                    # self.afterburner_speed -= neg_afterburner_acceleration
                    self.afterburner_speed -= 2 * self.afterburner_top_speed / (self.AFTERBURNER_GLIDING_TIME )         
    ##################################################################

                    

        
    def output_AFTERBURNER_COOLDOWN (self): return self.AFTERBURNER_COOLDOWN_timer
    def output_afterburner_delay_counter (self): return self.afterburner_delay_counter
    def output_afterburner_activation (self): return self.afterburner_activation 
    
        
    ################################################
    def recharge_shields (self):
        
        self.shield_down_timer -= 1 
        global shield_recharge_per_frame
        if self.shield_supercharge == 0 and self.shield_down_timer <= 0 and self.shield_generator_damage < 2 :
            for i in range (0,4):
                if self.actual_sas [0] [i] < self.full_sas [0] [i] : self.actual_sas [0] [i] += shield_recharge_per_frame
    #################################################

    def output_missile_cooldowns (self): return self.missile_cooldowns
    def output_torpedo_cooldowns (self): return self.torpedo_cooldowns 

    ###################################################
    def recharge_missiles (self):
        
        for i in range (0,len (self.missile_cooldowns)):
            self.missile_cooldowns [i] = dfunctions.count_down_to_zero (self.missile_cooldowns [i])
        for i in range (0, len (self.torpedo_cooldowns)):
            self.torpedo_cooldowns [i] = dfunctions.count_down_to_zero (self.torpedo_cooldowns [i] ) 
    ###################################################
    ###################################################            
    def missile_cooldown (self):
        out = 0
        for i in range (0, len (self.missile_cooldowns)):
            if self.missile_cooldowns [i] == 0:
                self.missile_cooldowns [i] = MISSILE_COOLDOWN
                out = 1
                break
        return out   
    ###################################################       r
        
    ###################################################
    def torpedo_cooldown (self):
        
        out = 0
        for i in range (0, len (self.torpedo_cooldowns)):
            if self.torpedo_cooldowns [i] == 0:
                self.torpedo_cooldowns [i] = MISSILE_COOLDOWN
                out = 1
                break
        return out 
    ###################################################
    
    def output_ships_on_radar (self): return self.ships_on_radar
    
    ###################################################
    def update_radar (self):
        self.ships_on_radar = [] 


        speed_rate = self.speed / self.top_speed
        
        if speed_rate <= 0.5 : self.radar_actual_range = self.radar_top_range
        if speed_rate > 0.5: self.radar_actual_range = self.radar_top_range 
        global ship_list

        for sx in ship_list:
            if ship.output_object_id (sx) != self.object_id:
                if dfunctions.distance_2 ( self.position, ship.output_position (sx)) < self.radar_actual_range : self.ships_on_radar.append (sx)
    ###################################################                
            
            
        

    
    def adjust_position (self, x,y ): self.position = dfunctions.vadd ((x,y), self.position)
    def output_fadenkreuz_size (self): return self.fadenkreuz_size

    def output_normalized_position (self): return self.normalized_position
    def output_radar_position (self): return self.radar_position
        # self.target_distance_passive = 0
        
    def output_moved (self): return self.moved
    def __del__(self): running

    def set_death_delay (self,x): self.death_delay = x

    def output_heat_cone (self): return self.heat_cone

    def output_actual_sas (self): return self.actual_sas
    def output_full_sas (self): return self.full_sas

    def output_weapon_info (self): return self.weapon_info
    def output_turret_info (self): return self.turret_info
    
        
    # input - Methoden:
    def set_player (self, x):
        self.player = x

   
    # def set_target_object_id (self, x): self.target_object_id = x

    def set_graphics (self,x): self.graphics = list (x)



    def set_object_id (self, x):
        self.object_id = x 
    
    def set_speed (self, aa):
        self.speed = aa

    def set_position (self, x,y):
        self.position = x,y

    def set_direction (self, x):
        self.direction = x

    def set_colour (self, x,y,z):
        self.colour = x,y,z

    def set_speed_setting (self, x): self.speed_setting = x

    def set_radius (self, x): self.radius = x

 
        


    #########################################################################
    def update_position (self):

        ###     I       update speed 
        
        
       
        speed_multiplier_list = {'off': 0, 's': 0.3 , 'm': 0.65, 'h': 1 }
        self.speed = self.top_speed * speed_multiplier_list.get (self.speed_mode) 
        
        if self.engine_damage >= self.damage_threshold: self.speed = self.speed / 2
        if self.engine_damage >= self.damage_threshold * 2: self.speed = 0
       

        
        ###     II      execute movement
        
            ##      A       normal 
        
        x,y = self.position
        if self.gliding_phase == 'no':
            x = x + self.speed * speed_factor * math.sin (self.direction) + self.afterburner_speed * speed_factor * math.sin (self.afterburner_direction)
            y = y + self.speed * speed_factor * math.cos (self.direction) + self.afterburner_speed * speed_factor * math.cos (self.afterburner_direction)
            self.position = x,y

            moved_x = self.speed * speed_factor * math.sin (self.direction) + self.afterburner_speed * speed_factor * math.sin (self.afterburner_direction)
            moved_y = self.speed * speed_factor * math.cos (self.direction) + self.afterburner_speed * speed_factor * math.cos (self.afterburner_direction)
            self.moved = (moved_x, moved_y)

            ##      B       gliding
            
        if self.gliding_phase == 'yes':
            
            moved_x =  self.speed * speed_factor * math.sin (self.gliding_direction)
            moved_y =self.speed * speed_factor * math.cos (self.gliding_direction)
            x += moved_x
            y += moved_y
            self.moved = (moved_x, moved_y)
            self.position = (x,y)


        ###     III         update  - normalized  , - radar , - log positions 

        
        self.normalized_position = dfunctions.vadd (self.position, NEGATIVE_MIDDLE)
        self.radar_position = dfunctions.skalar_multi ( 1 / radar_factor, self.normalized_position)
        self.log_position = dfunctions.skalar_multi ( 1 / log_factor, self.normalized_position)
    #######################################################################


        
    #######################################################################
    def update_man (self):  # updates maneuverability

        ###     I       damage factor 
        damage_man_factor = 1   # healthy enging 
   
        if self.engine_damage >= self.damage_threshold: damage_man_factor = 0.5  
        if self.engine_damage >= self.damage_threshold * 2: damage_man_factor = 0


        ###     II      speed factor
        
        speed_rate = self.speed / self.top_speed
    
        if speed_rate <= 0.5: man_rate = 2 *  speed_rate
        
        if speed_rate > 0.5 :
            man_rate = 1.5 - speed_rate

        if speed_rate <= 0.3:
            self.accel = self.top_accel / 5
            man_rate = 0.5

        if speed_rate <= 0.5 > 0.3 : self.accel = self.top_accel
        if speed_rate > 0.5: self.accel = self.top_accel / 5

        ###     III         booster factor 
        booster_factor = 1
        if self.booster_active == 'yes': 
            booster_factor = 2
            
            
        ###     IV          calculate result     
        self.man = self.top_man * man_rate * booster_factor * damage_man_factor 
    ###################################################
        

    
    ###################################################
    def update_fadenkreuz (self): 
        global manual_turrets 
        if self.player == 0:
            self.fadenkreuz_direction = dfunctions.relative_direction (ship.output_direction (object_list [1]),     dfunctions.ftarget_direction_2 (ship.output_position (object_list [1]),self.position))
            if manual_turrets == 'yes':
                turrets = ship.output_turret_ids (object_list [1])
            
                if turrets != []: 
                    self.fadenkreuz_direction = dfunctions.relative_direction (turret.output_direction (object_list [turrets [0]]),     dfunctions.ftarget_direction_2 (ship.output_position (object_list [1]),self.position))
            self.fadenkreuz_size = math.atan (5 / dfunctions.distance_2 (self.position, ship.output_position (object_list [1])))     
    ###################################################
        

    def output_fadenkreuz_direction (self): return self.fadenkreuz_direction
    
    ###################################################
    def check_capital_collision (self):
        if self.target != None:
            target = object_list [self.target]
            if target.ship_class in ['light_capital', 'capital', 'large_capital']:
                if ship.determine_target_distance (self, target) < ship.get_cannon_range (self) / 2 :
                    
                    if self.determine_relative_bearing (target) < 30 / 57 :
                        self.maneuver_mode = 'evade_capital_timer'
    ###################################################
                        

    ###################################################                        
    def evade_capital (self):
        turning_time = 200 + random.randint (1,80) 
        fly_straight_time = 400 
        enemy_direction = self.determine_relative_bearing ( object_list [self.target], output_direction = 'yes')
        if 'evade_capital_direction' not in self.maneuver_dict: 
            if enemy_direction == 'right': direction = 'left'
            if enemy_direction == 'left' : direction = 'right'
            self.maneuver_dict ['evade_capital_direction'] = direction
        else: direction =  self.maneuver_dict ['evade_capital_direction']

        if 'evade_capital_timer' not in self.maneuver_dict.keys ():
            self.maneuver_dict ['evade_capital_timer'] = 0
        else: self.maneuver_dict ['evade_capital_timer'] = self.maneuver_dict ['evade_capital_timer'] + 1

        timer = self.maneuver_dict ['evade_capital_timer']

        if timer < turning_time:
            if enemy_direction == 'right': direction = -1
            if enemy_direction == 'left' : direction = 1 

            self.direction = dfunctions.aa (self.direction, direction * self.turn_amount)

        if timer >= turning_time + fly_straight_time:
            self.maneuver_mode = 'normal'
            del self.maneuver_dict ['evade_capital_timer']
            del self.maneuver_dict ['evade_capital_direction']

    ###################################################
            
        
    ###################################################
    def update_direction (self,x):


        ######          I           move to destination

        ###                 1           determine if destination mode applies

        if self.maneuver_mode == 'normal' and self.destination != None:
            self.maneuver_mode = 'move_to_destination'


        ###                 2           determine destination position
        if self.destination != None:
            if self.destination [0] == 'trigger_point':
                for item in trigger_point_list:
                    if item.mission_id == self.destination [1]:
                        destination_position = item.position
            dot (destination_position) 


        ###                 3

        if self.maneuver_mode == 'move_to_destination':
            relative_position_to_destination = vsub (destination_position, self.position)
            relative_direction = math.atan2 (*relative_position_to_destination)
            relative_direction = dfunctions.normalize_angle (relative_direction)
            destination_direction = relative_direction

        ###                 4       determine jump_out
        if self.maneuver_mode == 'move_to_destination':
            distance_from_destination = dfunctions.distance_2 (self.position, destination_position)
            if distance_from_destination <= 200 :
                self.position = ( 1000 * 1000 , 1000 * 1000 )
                ship_list.remove (self)
                mission_event_list.append ( ['jumped_out', self.mission_id ] )
                explosion ( 1, 40, colour = WHITE, position = (self.display_position if self.display_position != None else self.position))


        ######          II           follow lead ship

        ###                 1           determine if follow mode applies 
        if self.maneuver_mode == 'normal' and self.lead_ship != None:
            self.maneuver_mode = 'follow_lead'
            lead_ship_id = 'fucked up  7818' 


        ###                 2           get lead_ship
        if self.maneuver_mode == 'follow_lead':
            for item in ship_list:
                if item.mission_id == self.lead_ship [0]: lead_ship = item
            if 'lead_ship' not in locals (): self.maneuver_mode = 'normal' 


        ###                 3           determine escort point          # the point near the lead ship where the ship tries to go to
        if self.maneuver_mode == 'follow_lead':
            print 'test 9381000 ', lead_ship.position, lead_ship.direction, self.lead_ship 
            lead_point = dfunctions.angle_line (lead_ship.position, lead_ship.direction, self.lead_ship [1], 57.3 * self.lead_ship [2]) [1]
            dot (lead_point)

        ###                 4           determine distance and direction of lead point
        if self.maneuver_mode == 'follow_lead':
            distance_from_lead_point = dfunctions.distance_2 (self.position, lead_point)
            relative_position_to_lead = ( lead_point [0] - self.position [0], lead_point [1] - self.position [1] ) 
            direction_to_lead_point = math.atan2 ((lead_point [0] - self.position [0]),(lead_point [1] - self.position [1]))
            direction_to_lead_point = dfunctions.normalize_angle (direction_to_lead_point) 
      
            

            # lead_point_bearing = dfunctions.normalize_angle (direction_to_lead_point - self.direction) 
            if distance_from_lead_point > 100: destination_direction = direction_to_lead_point
            else: destination_direction = None 
                


        #####################
        
        old_direction = self.direction

        if self.afterburner_activation in [1,2]: self.man = 0
        if self.afterburner_activation == 3: self.man = 2 * self.top_man

        self.turn_amount = self.man / ( 360 * frame_rate)

        if self.player == 0: ship.check_capital_collision (self) 

        
        
        
        if self.player == 1: self.direction = dfunctions.aa (self.direction, x * self.turn_amount)
        if self.player == 0:
            if self.maneuver_mode == 'evade_capital_timer':
                self.evade_capital ()

            
            
            if self.maneuver_mode == 'normal': 
            
                destination_direction = None 
                
                if self.target not in [ 'na', None]:
                    
                    if collide_2 (self.position, self.radar_actual_range, ship.output_position (object_list [self.target]), 0) == 1 and ship.output_stealthed (object_list [self.target]) == 'no':
                    
                        xs,ys = self.position
                        xt,yt = ship.output_position (object_list [self.target])
                        target_direction = ship.output_direction (object_list [self.target])
                        target_speed = ship.output_speed (object_list [self.target])
                        if self.cannon_ids != []: cannon_speed = cannon.output_speed (object_list [self.cannon_ids [0]])
                        else: cannon_speed = 5
                        bearing =  dfunctions.normalize_angle (math.atan2 ((xt - xs),(yt - ys)))
                        heading = self.direction
                        # rel_dir = dfunctions.relative_direction (heading, bearing)
                        beta_angle = dfunctions.relative_direction (bearing, target_direction)

                        
                        if self.cannon_ids != []: 
                            vorhalt_angle = math.asin ( math.sin (beta_angle) * target_speed / cannon.output_speed (object_list [self.cannon_ids [0]]) )
                            pilot_quality_mod = PILOT_QUALITY.get (self.pilot_quality)
                            

                            if self.pilot_vorhalt_modificator == None or self.pilot_inaccuracy_modificator == None or (pygame.time.get_ticks () - self.pilot_clock ) > random.randint (3000,15000):
                                self.pilot_vorhalt_modificator = pilot_quality_mod [0] * random.uniform (-1,1)
                                self.pilot_inaccuracy_modificator = ( pilot_quality_mod [1] / 57.3 ) * random.uniform (-1,1)
                                self.pilot_clock = pygame.time.get_ticks () 
                            
                            self.vorhalt_direction = dfunctions.normalize_angle (bearing + self.pilot_inaccuracy_modificator + vorhalt_angle * (1 + self.pilot_vorhalt_modificator))
                            self.real_vorhalt_direction = dfunctions.normalize_angle (bearing  + vorhalt_angle )   ### perfect vorhalt 
                            
                            

                        elif self.cannon_ids == []: self.vorhalt_direction = bearing 
                            

                        else: raise ValueError (' fucked up ' ) 
                        
                        if self.team == 0:
                            factor = 180 / 3.14

                            
                            
                        destination_direction = self.vorhalt_direction

                

            if destination_direction != None:
        
                heading = self.direction
                rel_dir = dfunctions.relative_direction (heading, destination_direction)
                rel_dir_abs = abs (rel_dir)
                rel_dir_norm = dfunctions.one_or_minus_one (rel_dir)
                if rel_dir_abs >= self.turn_amount : self.direction = dfunctions.aa (self.direction, rel_dir_norm * self.turn_amount)
                else: self.direction = destination_direction
                
        

        turned = abs ( dfunctions.relative_direction (old_direction, self.direction))
    ###################################################


        

        

        
    #graphik output
    def circle (self):
        x,y = self.position
        pygame.draw.circle (screen, self.colour, (int(x),int(y)), self.radius,0)

    def triangle (self, **wargs):
        surface = (screen if 'surface' not in wargs else wargs ['surface'] )
        pygame.gfxdraw.aapolygon (surface, dfunctions.triangle (self.display_position, self.direction, 10,6)       , self.colour)
        

    ###################################################
    def graphics (self):
        ###     I       preliminaries : determine display_position 
        global log_factor
        if log_factor == 1: self.display_position = self.position
        if log_factor != 1: self.display_position = dfunctions.vadd (MIDDLE, self.log_position)

        self.shrink_factor = min (log_factor, max (1, self.radius / 5 ))

        ###     II      do the graphics 
        self.ship_graphics ()
        self.graphics_small_stuff () 
    ###################################################

    ###################################################        
    def graphics_small_stuff (self):
        ###     I       crosshairs
        if self.player == 1: 
            startpos, endpos = dfunctions.fextrapolate_line (self.direction, self.position, 10, 500 )  
            global crosshairs_colour
            if self.cannon_ids != []: dfunctions.draw_info_crosshairs (self.position, self.direction, cannon.output_range (object_list [self.cannon_ids [0]]), GREEN, cannon.output_load (object_list [self.cannon_ids [0]]))   
            if self.cannon_ids == []:  dfunctions.draw_info_crosshairs (self.position, self.direction, 200, WHITE, 0)
            
        ###     II      shield graphics
        if self.shield_supercharge == 1: pygame.draw.circle (screen, GREEN, (int (self.display_position[0]), int (self.display_position [1])), self.radius + 7, 1)
        elif self.shield_supercharge == 2: pygame.draw.circle (screen, GOLD, (int (self.display_position[0]), int (self.display_position [1])), self.radius + 7, 1)
        elif self.shield_down_timer <= 0 and self.shield_generator_damage <= 2:
            if self.shield_blink > 0:
                self.shield_blink -= 1
                shield_colour = LIGHT_BLUE
            else: shield_colour = BLACK
            pygame.draw.circle (screen, shield_colour, (int (self.display_position[0]), int (self.display_position [1])), self.radius + 7, 1)

        ###     III     engine graphics
        if log_factor == 1:  dfunctions.display_engine_flame (self.display_position, dfunctions.aa (self.direction, 3.14), self.speed_mode )

        ###     IV      heat cone 
        if display_heat_cones == 1: dfunctions.display_missile_cone (self.display_position, dfunctions.aa (3.14, self.direction), self.heat_cone )

        ###     V       missile vorhalt
        if self.player == 1:
            if self.missile_vorhalt > 0.03 or self.missile_vorhalt < - 0.03:
                vorhalt_line = dfunctions.fextrapolate_line (dfunctions.aa (self.direction, self.missile_vorhalt), self.position, 5, 80) 
                pygame.draw.aaline (screen, LIGHT_BLUE, vorhalt_line [0], vorhalt_line [1], 1)

        ###     VI      disabled 
        if self.disabled == 'yes':
            write ('disabled', dfunctions.vadd (self.position, (- 20, - 25)), BRIGHT_BLUE, 12 ) 
        

                
    ###################################################



    ###################################################        
    def ship_graphics (self, **wargs):
        surface = screen
        if 'surface' in wargs: surface = wargs ['surface']

        if self.stealthed == 'no' and ( self.stealthed_activation_timer <= 0 or self.stealthed_activation_timer % 10 > 5 ) and (self.stealthed_deactivation_timer <= 0 or self.stealthed_deactivation_timer % 10 > 5):
  

         
            self.draw_ship_polygon (surface = surface, colour = self.colour, shrink_factor = self.shrink_factor, input_polygon = self.graphics [1], position = self.display_position) 
            
                    # pygame.gfxdraw.aapolygon (surface, dfunctions.move_normalized_polygon (self.position,dfunctions.turn_normalized_polygon (g,self.direction)), self.colour)

            #### special hitboxes
            if self.special_hitboxes != None: 
                for e, hit in enumerate (self.special_hitboxes):
                    if hit [5] == 'exists':
                        pygame.gfxdraw.aapolygon (surface, dfunctions.move_normalized_polygon (self.display_position,shrink_ship (dfunctions.turn_normalized_polygon (hit [6] ,self.direction),self.shrink_factor)), self.colour)
    ###################################################

    ###################################################
    def draw_ship_polygon (self, **wargs):
        input_polygon_list = wargs ['input_polygon']  # 
        position = wargs ['position'] #
        colour = wargs ['colour'] # 
        shrink_factor = wargs ['shrink_factor']# 
        surface = wargs ['surface'] #
        if 'test' in wargs:
            print 'test   ', wargs ['test']
            for key in wargs.keys ():
                print key, '    ', wargs [key] 

        for input_polygon in input_polygon_list:

            pygame.gfxdraw.aapolygon (surface, dfunctions.move_normalized_polygon (position,dfunctions.turn_normalized_polygon (shrink_ship (input_polygon,shrink_factor),self.direction)), colour)   
    ###################################################

    



            
    ###################################################       
    def radar_graphics (self, **wargs):
        surface = screen
        middle = (100,100)
        if 'middle' in wargs: middle = wargs ['middle'] 
        if 'surface' in wargs: surface = wargs ['surface']
        shrink_factor = 1.5
        if self.ship_class in [ 'light_capital', 'large_capital', 'large_capital'] : shrink_factor = int (self.radius / 10) 
        
        if self.stealthed == 'no':

           
            self.draw_ship_polygon (surface = surface, colour = self.colour, shrink_factor = shrink_factor, input_polygon = self.graphics [1], position = vadd (self.radar_position, middle)) 
                

            x,y = self.radar_position 
            pygame.draw.circle ( surface,FAINT_WHITE,  ( int (x) + middle [0] , int (y) + middle [1]), int (math.ceil (self.radar_actual_range / radar_factor)), 1)
    ###################################################

                

    def display_sas (self, position, colour):
        return dfunctions.display_sas_3 ( position,colour ,self.actual_sas [0], self.full_sas [0], self.actual_sas [1], self.full_sas [1], self.actual_sas [2] [0], self.full_sas [2] [0],missiles = (len (self.missile_cooldowns) ,self.missile_damage / self.damage_threshold ) , guns = (len (self.cannon_ids),self.cannon_damage / self.damage_threshold          ), shield_generator_damage = self.shield_generator_damage, engine_damage = self.engine_damage, damage_threshold = self.damage_threshold)
        
        

    # output - Methoden

    def output_position (self): return (self.position)

    def output_speed (self): return (self.speed)

    def output_direction (self): return (self.direction)  
        
    def output_player (self): return (self.player)

    def print_id (self): print self.ship_id

    def output_object_id (self): return self.object_id

    def output_id (self): return self.ship_id

    ### Zielfestlegungs- funktion
    

    
            
        

    
        
        
    def trigger (self):
        shoot = 0 
        if self.target != None:
            if self.cannon_ids != []:
                if (abs (dfunctions.relative_direction (self.vorhalt_direction, self.direction)) <= 1 / PI_FACTOR)  and (dfunctions.distance_2 (self.position, ship.output_position (object_list [self.target])) <= cannon.output_range (object_list [self.cannon_ids [0]]))     : shoot = 1 


                
            if shoot == 1:
                ship.shoot (self)
                ship.shoot_missile (self, RADAR)

                    
        
    
    # # Schieß- Funktion: Erzeugt ein bullet- objekt
    def shoot (self, **wargs):
        print 'test 600  ', self.cannons_sorted 
        
        if self.stealthed_activation_timer <= 0 and self.stealthed_deactivation_timer <= 0 and self.stealthed != 'yes': 
            for e, can in enumerate (self.cannon_ids):
                cannon.update_position (object_list [can])
                if (e + 1) * self.damage_threshold > self.cannon_damage: ### the first (damage / 2) cannons do not shoot
                    if wargs.get ('guns') == None:
                        cannon.shoot (object_list [can])
                    elif wargs.get ('guns') == 'primary':
                        if len (self.cannons_sorted) >= 1:
                            if can in self.cannons_sorted [0] :
                                cannon.shoot (object_list [can])
                    elif wargs.get ('guns') == 'secondary':
                        if len (self.cannons_sorted) >= 2:
                            if can in self.cannons_sorted [1] :
                                cannon.shoot (object_list [can])
                    elif wargs.get ('guns') == 'tertiary':
                        if len (self.cannons_sorted) >= 3:
                            if can in self.cannons_sorted [2] :
                                cannon.shoot (object_list [can])
                    
                                
                    
                                                   
                                

            
    # # raketen - Funktion
    def shoot_missile (self,m_type):
        if self.stealthed_activation_timer <= 0 and self.stealthed_deactivation_timer <= 0 and self.stealthed != 'yes':
            if ship.missile_cooldown (self) == 1:
                global target_count
                global enemy_ship_list
                if self.player == 1:
                    if enemy_ship_list != []:
                        self.target_object_id = ship.output_object_id (enemy_ship_list [target_count])
                    else: self.target_object_id = None 
               
                if m_type [0] == 'micro':
                    self.micro_missile_counter.append (20) 
                    
                else:
                    m = missile (m_type, self.target_object_id, self.direction, self.speed, self.object_id)
                    x,y = self.position
                    x1 = math.sin (self.direction)
                    y1 = math.cos (self.direction)
                    missile.set_missile_vorhalt (m, self.missile_vorhalt)
                    if m_type [0] == 'mine': missile.set_position (m, x - 12 * x1, y -12 * y1)
                    else: missile.set_position (m, x +35 * x1,y + 35 * y1)
                    missile_list.append (m)

    def shoot_torpedo (self):
        m_type = TORPEDO
        
        if  self.stealthed_activation_timer < 0 and self.stealthed_deactivation_timer <= 0  and self.stealthed != 'yes':
            if ship.torpedo_cooldown (self) == 1 :
            
            
            
                m = missile (TORPEDO, self.target_object_id, self.direction, self.speed, self.object_id)
                x,y = self.position
                x1 = math.sin (self.direction)
                y1 = math.cos (self.direction)
                missile.set_missile_vorhalt (m, self.missile_vorhalt)
                
                missile.set_position (m, x +( self.radius + 20 ) * x1,y + (self.radius + 20)  * y1)
                missile_list.append (m)

    
    def update_micro_missile (self):
        global master_frame_counter
        if master_frame_counter % 3 == 0:
            self.micro_missile_counter = [x for x in self.micro_missile_counter if x > 0 ] 
            for e, x in enumerate (self.micro_missile_counter):
                
                self.micro_missile_counter [e] -= 1 
                
                if self.micro_missile_counter [e] >= 0: 
            
                    missile_direction = dfunctions.aa (self.direction, random.randint (- 30, 30) * 3.14 / 360)
                    
                    m = missile (MICRO, 0, missile_direction, self.speed, self.ship_id)
                    x,y = self.position
                    x1 = math.sin (self.direction)
                    y1 = math.cos (self.direction)
                
                    
                    missile.set_position (m, x +35 * x1,y + 35 * y1)
                    missile_list.append (m)
                

    def process_damage (self, damage, side_t, shield_piercing,firing_ship_id,  **wargs): 
        
        
        if self.mission_id != None:
            new_event = ( self.mission_id, 'hit' )
            if new_event not in mission_event_list: mission_event_list.append (new_event)
        
        if self.damage == 1: return None

        ###         ___ I ___   Preliminaries 

        if self.shield_supercharge == 2: damage = 0
        
        bullet_type = wargs.get ('bullet_type')
        ion_damage = wargs.get ('ion_damage') 
        if side_t == 'front': side = 0
        if side_t == 'left' : side = 1
        if side_t in  ['back', 'aft']  : side = 2
        if side_t == 'right' : side = 3

        for i in range (0,2):
            if i == 1 and ion_damage == 'yes': break 
            if not ( i == 0 and shield_piercing == 'yes'):   #########   if the shot is shield-piercing, the first cycle (shields) will be skipped

                if i == 1: x = debris (self.position, 20, self.direction )
                
                if i == 0 and self.actual_sas [0] [side] > 0 and damage > 0:
                    self.shield_blink = 4
                   
                
                    
                self.actual_sas [i] [side], damage = damage_calc (self.actual_sas [i] [side], damage)  ### input: raw damage and shield/armor/structure value ;;; output: remaining damage ; remaining s/a/s value

                ### checks if shields are breached => if so, shuts down shields completely 
                if i == 0 and self.actual_sas [0] [side] == 0 and self.shield_down_timer <= 0:
                    self.shield_down_timer = 500
                    e = explosion (4,0, start_radius = self.radius + 5, end_radius = self.radius + 15, parent_id = self.object_id, position = self.display_position )
                    
             
                   
                    
                    for side in [0,1,2,3]:
                        self.actual_sas [0] [side] = 0

                        
                
                        
            if damage == 0 : break
            
        
        ### if the structure takes damage, the same amount of damage ist applied to internal systems
        if damage > 0:
            system_damage = damage
            
            while system_damage > 0:
            
                system_damage, incremental_damage = split_stack (system_damage, self.damage_threshold)
                while incremental_damage > 0: 
                    some_rand = random.randint (0,3)
                    # some_rand = 0   #########  test !!!!!!!!!!!!!1 ändern !!!!!!!!!!
                    if some_rand == 0:
                        if self.shield_generator_damage < self.damage_threshold:
                            self.shield_generator_damage += incremental_damage
                            incremental_damage = 0 
                        
                        
                        
                    elif some_rand == 1:
                        if self.engine_damage < 2 * self.damage_threshold:
                            self.engine_damage += incremental_damage
                            incremental_damage = 0 
                     
                    elif some_rand == 2:
                        if self.cannon_damage < self.damage_threshold * len (self.cannon_ids):
                            self.cannon_damage += incremental_damage
                            incremental_damage = 0 
                    
                    elif some_rand == 3:
                        if self.missile_damage < self.damage_threshold * self.missile_launchers :
                            self.missile_damage += incremental_damage
                            incremental_damage = 0 

                        
                    else: raise ValueError ('fucked up')
                    if random.randint (1,20) == 20: incremental_damage = 0 


        if ion_damage == 'yes':
            self.ion_damage += damage
            if self.ion_damage >= 3 * self.damage_threshold:
                self.disabled = 'yes' 
                self.engine_damage = 1000
                self.shield_damage = 1000
                self.cannon_damage = 1000
                self.missile_damage = 1000
                self.turret_damage = 1000
                for tur in self.turret_ids:
                    object_list [tur].damaged = 'yes'
            damage = 0
            if self.ion_damage >= 20 * self.damage_threshold: self.damage = 1  
        else: self.actual_sas [2] [0] , damage = damage_calc (self.actual_sas [2] [0] , damage)

        if damage > 0 :
            self.damage = 1
            if firing_ship_id == 1:
                killed_graphics = self.type_info ['graphics'] [1]
                killed_colour_list = {'fighter': RED, 'mine': RED,'bomber': GREEN, 'light_capital': ORANGE, 'large_capital': MAGENTA } 
            
                    
               
                killed_ship_list.append ( lambda surface, position: self.draw_ship_polygon (surface = surface, colour = killed_colour_list [self.ship_class], shrink_factor = self.radius / 5 , input_polygon = self.graphics [1], position = position) )
                killed_ships_team2 [0] = killed_ships_team2 [0] + 1
    ###################################################################################################


                
    ###################################################################################################
    def delayed_death (self):
        out = 0
        if self.death_delay == 0: out = 1
        if self.death_delay > 0: self.death_delay -= 1
        return out 
    ###################################################################################################
    


    ###################################################################################################
    def hit_subfunction (self, bull, hitbox, **wargs):
        position = self.position
        if 'position' in wargs: position = wargs ['position']
        radius = self.radius
        if 'radius' in wargs: radius = wargs ['radius']
        z_dimension = ('yes' if wargs.get ('z_dimension') == 'yes' else 'no')
        # print 'test 700  ', z_dimension, bull.z_dimension 
        out = 0
        both_normal = (z_dimension == 'no' and bull.z_dimension == 'no')
        both_z = (z_dimension == 'yes' and bull.z_dimension == 'yes')
      

        if both_normal or both_z :
       
            
            if bull.ship_id != self.object_id:

                ###             I           standart: circular 
              
                if hitbox [0] == 'standart': 
                    out = collide_2 (position,radius,bull.position,bull.radius)
                    if (bull.speed >= 200 or self.ship_class == 'mine') and bull.superclass == 'bullet':
                        if bullet.output_last_frame_position (bull) != None:
                            check_hit_points = dfunctions.create_intermediate_points (bullet.output_last_frame_position (bull), bullet.output_position (bull), grain_seize = 1 )
                            for p in check_hit_points:
                                if collide_2 (self.position, self.radius, p, 0) == 1:
                                    out = 1
                                    break

                ###             II          nonstandart: real hit - BOX 
                if hitbox [0] == 'nonstandart':
                    if dfunctions.distance_2 (ship.output_position (self), bull.position) < hitbox [1]:

                        hitbox_list = hitbox [2]  ### ACHTUNG: zu Testzwecken geändert! in wirklichkeit muss es heissen hitbox [:2]
                        for box in hitbox_list:
                            box_turned_moved = dfunctions.move_normalized_polygon (self.position,dfunctions.turn_normalized_polygon (box,self.direction))
                            pygame.gfxdraw.aapolygon (screen, box_turned_moved, BLUE)
                            
                            if dfunctions.hitbox_collision ( self.direction, box_turned_moved, bull.position, 0) == 1:
                            
                                out = 1
        return out     
    ###################################################################################################


    
        
    ###################################################################################################
    def hit (self):
              
        bm_list = bullet_list + missile_list 
        
              
        for bull in bm_list [:]:
            if bull.ship_id != self.object_id: 
                

                damage = bull.damage
                if self.shield_supercharge == 2: damage = 0 
                if type (damage).__name__ not in ['int', 'float']: damage = MISSILE_DAMAGE_MATRIX [self.ship_class] [damage]


                ### #       ALPHA           turrets

                
                for tur in self.turret_ids:
                    if self.actual_sas [0] [0] == 0 or bull.superclass == 'missile' or bull.shield_piercing == 'yes' or object_list [tur].z_dimension == 'yes': 
                        tur = object_list [tur]
                        if tur.determine_hit (bull, damage) == 1: 
                            ex = explosion (2, 0, position = bull.display_position , colour = RED)
                            try:                       
                                if bull.superclass == 'bullet': bullet_list.remove (bull)
                                if bull.superclass == 'missile': missile_list.remove (bull)
                            except:
                                pass 

                                    
                            break
                                
                        
                      

                
                ### #       BETA           main ship body
                hit_1 = self.hit_subfunction (bull, self.hitbox, z_dimension = self.z_dimension)
                if hit_1 == 1:
                
                  
                    hit_direction = dfunctions.hit_direction_2 (self.direction, bull.direction)
              
                    ###         I           special bullet types


                        ##          B           dumb delayed or delayed explosion 
                    if bull.type == 'dumb_delayed' or 'delayed':
                        hit_2 = collide_2 (self.position,self.radius, bull.position, bull.radius)
                        if bull.type == 'delayed':
                            if hit_2 == 1:
                                self.death_delay = 20
                                e = explosion (3, bull.explosion_radius, position = bull.display_position)
                                
                               
                               
                        if bull.type == 'dumb_delayed':
                            if hit_2 == 1:
                                effect = delayed_effect ( 1, DUMB_DELAY, [bull.position], ship_id = bull.ship_id )
                                delayed_effects_list.append (effect)
                                missile_list.remove (bull)
                                
                                


                    ###         II          finish 
                   
                    try: 
                        if bull.superclass == 'bullet': bullet_list.remove (bull)
                        if bull.superclass == 'missile': missile_list.remove (bull)
                    except: pass 
                    if damage == 'lethal' :
                        self.damage = 1
                        killed_graphics = self.type_info ['graphics'] [1]
                        killed_colour_list = {'fighter': RED, 'mine': RED,'bomber': GREEN, 'light_capital': ORANGE, 'large_capital': MAGENTA } 
                        killed_ship_list.append ( lambda surface, position: self.draw_ship_polygon (surface = surface, colour = killed_colour_list [self.ship_class], shrink_factor = self.radius / 5 , input_polygon = self.graphics [1], position = position) )
                        killed_ships_team2 [0] = killed_ships_team2 [0] + 1
                    else:  ship.process_damage (self, damage, hit_direction, bull.shield_piercing, bull.ship_id, bullet_type = bull.type,  ion_damage = bull.ion_damage)
                    e = explosion (2, 0, position = bull.display_position)
                    

                ### #       GAMMA            special hitboxes 
                if hit_1 == 0 and self.special_hitboxes != None:
                    for e, hit in enumerate (self.special_hitboxes):
                        if hit [5] == 'exists':
                            hit_special = self.hit_subfunction (bull, hit) 
                                               
                            if hit_special == 1: 
                            
                                try: 
                                    if bull.superclass == 'bullet': bullet_list.remove (bull)
                                    if bull.superclass == 'missile': missile_list.remove (bull)
                                except:
                                    pass 
                               
                                ex = explosion (2, 0, position = bull.display_position, colour = RED )

                                if damage != 'lethal': self.special_hitboxes [e] [3] -= damage
                           
                                if self.special_hitboxes [e] [3] <= 0 or damage == 'lethal':
                                    self.delayed_death = 50
                                    self.special_hitboxes [e] [5] = 'destroyed'
                                    print 'test 334  ', hit [2] 
                                    hit_shrinked = shrink_ship (hit [2] [0] , self.shrink_factor)
                                    ex = explosion (1, 20, colour = RED, position = dfunctions.vadd (self.display_position  , middle_point (hit_shrinked [0], hit_shrinked [2] )))
                                   
                                    for i in range (0,10):
                                        d = debris  (self.position, 100, 1.57 * random.uniform (0,4), colour = RED  )
                                        


                                ##          A           asteroids
                    
        for ast in asteroid_list [:] :
            damage = min (self.speed / 5 , (ast.radius ** 2) / 5)
            
           
            hit_direction = dfunctions.hit_direction_2 (self.direction,  dfunctions.aa (self.direction, 3.14))

            if self.hit_subfunction (ast, self.hitbox, z_dimension = 'no') == 1: 

                ship.process_damage (self, damage, hit_direction, 'no', None, bullet_type = 'asteroid',  ion_damage = 'no')
                e = explosion (2, 0, position = ast.display_position)

                try:
                    asteroid_list.remove (ast)
                    ast.explode ()
                except: pass

        ###  ###        debris

        for deb in debris_list [:] :
            
            if deb.damage != None and self.hit_subfunction (deb, self.hitbox, z_dimension = 'no') == 1:
                ship.process_damage (self, deb.damage , dfunctions.hit_direction_2 (self.direction, deb.direction),'no', None, bullet_type = 'debris', ion_damage = 'no')
                try: debris_list.remove (deb)
                except: pass 
          

                                     
                        


        
        if self.damage == 1:
            global turret_list
            try: 
                for tur in self.turret_ids:
                    turret_list.remove (object_list [tur])
                    print 'test 3911  , removed turret   ', tur 
            except: pass 
            global global_target_object_id
            global_target_object_id = None 
                
        return self.damage 
                
######################################################        
###  Klassendefinition Ship ## Ende #####
########################################################
    

#######################################################
###     Klassendefinition   ''      Turret      '' Beginn

class turret (object):
    def __init__(self,  info, ship_id):
        ###         initial stuff 
        self.info = info
        

        global master_object_counter
        master_object_counter += 1
        object_list.append (self)
        self.object_id = len (object_list) - 1

        turret_list.append (self)
        
        ###         ship_id
        
        self.ship_id = ship_id 

        
        ### 

        self.guns = info ['guns']
        self.fore = info ['vertical_position']
        self.side = info ['horizontal_position']

        
      
      
        self.radius = ( 3 if info.get ('radius') == None else info ['radius']) 
 

     
        self.relative_median_alignment = info ['alignment']
        self.absolute_median_alignment = 0
        self.left_angle_limit = info ['left_area']
        self.right_angle_limit = info ['right_area']

        self.z_dimension = ('yes' if 'z_dimension' in info else 'no') 

        ###

        self.cannon_ids = []
        for item in self.guns:
            c = cannon (item, self.object_id , turret = 'yes')
            self.cannon_ids.append (c.object_id) 


        ### 
        
        self.maneuverability = 100       
        self.direction = 2
        self.colour = 100,100,100
        if self.z_dimension == 'yes': self.colour = GREEN 
        self.position = 100,100
     
        
        ###          ai - variables 
        self.ai_shoot = 0
        self.target = None
        self.target_direction = 0
        self.target_bearing = 0
        self.target_object_id = 1
        self.target_bearing = 0

        ###
        
        self.cooldown_counter = 0

        
       
        self.display_position = self.position
        self.normalized_position = self.position
        self.radar_position = self.position
        self.manual_mode = 'no'
        self.enemy_list = []
        self.vorhalt_direction = self.direction
        self.enemies_in_arc = []
        self.cannon_range = 0
        self.median_alignment = 0
        self.damaged = 'no'
        self.hit_points = (info.get ('hit_points') if info.get ('hit_points') != None else 3)       
        self.destroyed = 'no'
        self.ship_class = 'turret'

        
   

    ##############################
    ####### End     __init__
    ##############################

    hit_subfunction = ship.__dict__ ['hit_subfunction']


    def test_signal (self, colour):
        ex = explosion (1,20, colour = colour , position = self.position)
       


    def determine_hit (self,b, damage):
        out = 0 

        if self.destroyed != 'yes': 
            if self.hit_subfunction (b, ['standart', 3, None] , radius = 3, position = self.position, z_dimension = self.z_dimension) == 1:
                
                if damage != 'lethal': self.hit_points -= damage

                if self.hit_points <= 0 or damage == 'lethal':
                    self.destroyed = 'yes'
                    self.damaged = 'yes'
                    
                    turret_list.remove (self)
           
                    ex = explosion (1, 20, position = self.position , colour = GOLD)
                    for i in range (0,10):
                        d = debris  (self.position, 100, 1.57 * random.uniform (0,4), colour = RED  )

                out = 1
                
        return out 

        
        
    def update (self):
       
        self.cannon_range = cannon.output_range (object_list [self.cannon_ids [0] ] ) 
        self.enemy_ship_list = ship.output_enemy_ship_list (object_list [self.ship_id ] )
        self.target = turret.select_target (self)
        if self.enemy_ship_list == [] : self.target = None
        if self.target != None : turret.calculate_vorhalt_direction (self)
        if self.hit_points <= 0: self.destroyed == 'yes'


    def calculate_vorhalt_direction (self):
        self.vorhalt_direction

        xs,ys = self.position
        xt,yt = ship.output_position (object_list [self.target])
        target_direction = ship.output_direction (object_list [self.target])
        target_speed = ship.output_speed (object_list [self.target])
        if self.cannon_ids != []: cannon_speed = cannon.output_speed (object_list [self.cannon_ids [0]])
        else: cannon_speed = 5
        bearing =  dfunctions.normalize_angle (math.atan2 ((xt - xs),(yt - ys)))
        heading = self.direction
        # rel_dir = dfunctions.relative_direction (heading, bearing)
        beta_angle = dfunctions.relative_direction (bearing, target_direction)

        
        if self.cannon_ids != []: 
            vorhalt_angle = math.asin ( math.sin (beta_angle) * target_speed / cannon.output_speed (object_list [self.cannon_ids [0]]) )
            self.vorhalt_direction = dfunctions.normalize_angle (bearing + vorhalt_angle)

 

        

    #def set_target ( self ):
     #   self.target = ship.output_target ( object_list [self.ship_id] )
        

    def __del__(self): running

    def adjust_position (self, x,y ): self.position = dfunctions.vadd ((x,y), self.position)


    def output_weapon_info (self): return self.weapon_info 
        
    # input - Methoden:
    def set_player (self, x):
        self.player = x

    def set_ship_id (self,x): self.ship_id = x

    
    def set_target_object_id (self, x): self.target_object_id = x

    def set_graphics (self,x): self.graphics = list (x)

    def set_id (self, x):
        self.ship_id = x

    def set_object_id (self, x):
        self.object_id = x 
    
    def set_speed (self, aa):
        self.speed = aa

    def set_position (self, x,y):
        self.position = x,y

    def set_direction (self, x):
        self.direction = x

    def set_colour (self, x,y,z):
        self.colour = x,y,z

   

    def set_radius (self, x):
        self.radius = x


    #interne aktualisierung/ Verrechnung
    def update_position (self):
        self.position = dfunctions.forthogonal_line ( dfunctions.fextrapolate_line (ship.output_direction (object_list [self.ship_id]),ship.output_position (object_list [self.ship_id]),0,self.fore) [1], ship.output_direction (object_list [self.ship_id]), self.side) [1]
        self.cooldown_counter = dfunctions.count_down_to_zero (self.cooldown_counter)

        self.normalized_position = dfunctions.vadd (self.position, NEGATIVE_MIDDLE)
        self.radar_position = dfunctions.skalar_multi ( 1 / radar_factor, self.normalized_position)
        
        
        
        
        

    def update_direction (self):
        global pressed 
        global manual_turrets
        if (ship.output_player (object_list [self.ship_id]) == 1  and manual_turrets == 'yes'): self.manual_mode = 'yes'
        else: self.manual_mode = 'no' 
        self.median_alignment = dfunctions.aa (ship.output_direction (object_list [self.ship_id]), self.relative_median_alignment)
        if self.target != None and self.manual_mode == 'no' :
            xs,ys = self.position
            xt,yt = ship.output_position (object_list [self.target])
            bearing =  dfunctions.normalize_angle (math.atan2 ((xt - xs),(yt - ys)))
            heading = self.direction
            rel_dir = dfunctions.relative_direction (heading, self.vorhalt_direction)
            rel_dir_norm = dfunctions.one_or_minus_one (rel_dir)
            self.direction = dfunctions.aa (self.direction, rel_dir_norm * self.maneuverability / ( 360 * frame_rate))

        if self.manual_mode == 'yes':
            rel_dir_norm = 0
            if pressed [276] == 1: rel_dir_norm = 1
            if pressed [275] == 1: rel_dir_norm = -1 
            self.direction = dfunctions.aa (self.direction, rel_dir_norm * self.maneuverability / ( 360 * frame_rate))

        for c in self.cannon_ids:
            cannon.update_position (object_list [c])
    
    
    

       

    def do_graphics (self):
        if check_on_screen (self) == 'yes' and self.destroyed == 'no': 
          
            self.display_position = self.position
            x,y = self.display_position
            pygame.gfxdraw.aapolygon (screen, dfunctions.triangle ((x,y), self.direction, 10,6)       , self.colour)
            if self.manual_mode == 'yes':
                startpos, endpos = dfunctions.fextrapolate_line (self.direction, self.position, 10, 500 )
                if self.cannon_ids != []: dfunctions.draw_info_crosshairs (self.position, self.direction, cannon.output_range (object_list [self.cannon_ids [0]]), GREEN, cannon.output_load (object_list [self.cannon_ids [0]]))

                
            
                


    def create_cannon (self, c_type, fore, side):
        global master_object_counter
        
        can = cannon (c_type, fore, side, self.ship_id)   
        master_object_counter += 1
        cannon.set_object_id (can, master_object_counter)
        object_list.append (can)
        cannon.set_turret (can, self.object_id)
        self.cannon_ids.append (master_object_counter)
        cannon_list.append (can)
        self.c_type = can.c_type
        self.explosion = self.c_type.get ('explosion')
        self.explosion_range = self.c_type.get ('explosion_range') 
        
        
    #graphik output
    def circle (self):
        x,y = self.position
        pygame.draw.circle (screen, self.colour, (int(x),int(y)), self.radius,0)
    '''
    def triangle (self):
        pygame.gfxdraw.aapolygon (screen, dfunctions.triangle (self.position, self.direction, 10,6)       , self.colour)
        if self.player == 1:
            pygame.draw.circle (screen, (255,0,0), dfunctions.int_2_tuple (ship.output_position (object_list [self.target_object_id]))  , 20,2) #
    '''
    
    def graphics (self):
        print 'test 460', self.graphics [0] 
        if self.graphics [0] == 'triangle': ship.triangle (self)
        if self.graphics [0] == 'polygon':
            pygame.gfxdraw.aapolygon (screen, dfunctions.move_normalized_polygon (self.position,dfunctions.turn_normalized_polygon (self.graphics [1],self.direction)), self.colour)
        
                

    def trigger (self):
        if self.damaged == 'no' and self.destroyed == 'no':
            global pressed 
            if self.cooldown_counter == 0 and self.target != None and self.manual_mode == 'no':
               
                shoot, self.target_bearing = target_in_crosshairs_2 (self.position, ship.output_position ( object_list [self.target]), self.direction, self.cannon_range)
                relative_direction = dfunctions.relative_direction (self.median_alignment, self.target_bearing)
                if shoot == 1: #  or (self.manual_mode == 'yes' and pressed [274] == 1)) :
                    if self.right_angle_limit > relative_direction and relative_direction >(( -1) * self.left_angle_limit) :
                        for c in self.cannon_ids:
                            cannon.shoot (object_list [c], explosion_distance = (1 + object_list [self.ship_id].missile_vorhalt / -3 ) * random.uniform (0.9, 1) * dfunctions.distance_2 (self.position, object_list [self.target].position))
            if self.cooldown_counter == 0 and self.manual_mode == 'yes' and pressed [274] == 1 :
                if dfunctions.within_angle_range (self.median_alignment, self.left_angle_limit, 'clock', self.direction) == True or dfunctions.within_angle_range (self.median_alignment, self.right_angle_limit, 'anticlock', self.direction) == True:
                
                    for c in self.cannon_ids:
                        cannon.shoot (object_list [c])
                
                # print 'test 20.000  ', self.median_alignment , '  ', self.right_angle_limit , '   ', self.left_angle_limit 


            
    # output - Methoden

    def output_position (self): return (self.position)

    def output_speed (self): return (self.speed)

    def output_direction (self): return (self.direction)  
        
    def output_player (self): return (self.player)

    def print_id (self): print self.ship_id

    def output_object_id (self): return self.object_id

    def output_id (self): return self.ship_id

    ### Zielfestlegungs- funktion
    def select_target (self):
        enemy_distance_list = []
        
        
    
        for sh in ship_list:
            
        
            # print 'test 50.000 :  ', sh, '      ', ship.output_object_id (sh)  
            if sh in self.enemy_ship_list:
                target_bearing = target_in_crosshairs_2 (self.position, ship.output_position ( sh), self.direction, self.cannon_range) [1]
                relative_direction = dfunctions.relative_direction (self.median_alignment, target_bearing)
                if self.right_angle_limit > relative_direction and relative_direction >(( -1) * self.left_angle_limit):
                    xs,ys = self.position
                    xt,yt = ship.output_position (sh)
                   
                    enemy_distance_list. append  ( [ int(math.hypot (xs - xt, ys - yt)), ship.output_object_id (sh)  ] )
                    enemy_distance_list.sort ( key = lambda x: x [0] )
                    
                    if enemy_distance_list == []: self.target = None
                    else: self.target = enemy_distance_list [0] [1] 
                    

                
                
                
         
       
        return self.target
        
        
                    
                    
 
  
  
        
    

############################################################
###     Klassendefinition       '' Turret   ''  ENDE
############################################################

def create_fighter (input_stuff):
    player = input_stuff [0]
    s_type = input_stuff [1]
    position = input_stuff [2]
    team = input_stuff [3]


  
    
    direction = xget (input_stuff, 'direction')
    if direction == None : direction = 1.57
    
   

    mission_id = xget (input_stuff, 'mission_id')
  
    
  
        
    ###         execute the ship building 

    s = ship (s_type, team = team, complete_information = input_stuff, player = player, direction = direction, position = position)
    ship_list.append (s)
    # object_list


def create_asteroid (position, seize):
        

    asteroid (position, seize) 
    
    

def create_asteroid_field (position, number, seize):
    position = dfunctions.vadd (position, ( - int (seize / 2), - int (seize / 2))) 
    for i in range (0, number):
        create_asteroid ( dfunctions.vadd (position,(random.randint (1,seize), random.randint (1,seize))), random.randint (3,10))



        

def create_mission (mission, custom_or_campaign):
    global running_mission_info
    running_mission_info = mission 
    ships = mission.get ('ships')
    for s in ships:
        create_fighter (s )
     
    trigger_point_info = mission.get ('trigger_points')
    goals = mission.get ('goals')
    global mission_goal_list
    if goals != None: 
        for g in goals:
            if g.get ('super_goal') == None:
                mission_goal_list.append (g) 
        
    if trigger_point_info != None:
        for t in trigger_point_info:
            create_trigger_point (t)
            
    asteroids = running_mission_info.get ('asteroid_fields')
    if asteroids != None:
        for a in asteroids:
      
            create_asteroid_field (a [0], a [1] , a [2])

    global mission_running
    mission_running = {'campaign': 1, 'custom': 2} [custom_or_campaign]      ###  Values for "mission_running":   0 = no  ;; 1 = campaign_mission  ;; 2 = custom_mission 
    global end_game
    end_game = 0 

    root.destroy ()
    mainloop () 

def create_trigger_point (trigger_info):
    global trigger_point_list

    
   
    for k in trigger_info.keys ():
        print k 
   

   
    t = trigger_point (position = trigger_info.get ('position'), ships = trigger_info.get ('ships') , mission_id = trigger_info.get ('mission_id' ), trigger = trigger_info.get ('trigger'), goal_name = trigger_info.get ('goal_name'), name = trigger_info.get ('name'))
    
    trigger_point_list.append (t)
    

campaign_mission_1 = {
    'ships': [
        [1, PSYCHO, MIDDLE,0, {'autopilot_destination' : ['ship', 21] , 'mission_id': 0}],  #    [0, DEMON, (1200, 500), 1 ]
        ],
    'mission_name': '  p1' ,
    'trigger_points': [
        {
            'name': 'nav_1',
            'position': (2000,500),
            'mission_id': 1,
            'ships': [
                [0, TALON, (2200,500), 1, {'direction': 4.75, 'mission_id': 11}]
                ]
        },
        {
            'name': 'nav_2',
            'position': (3000,1500),
            'mission_id': 2,
            'ships': []
            },
        {
            'name': 'nav_3',
            'position': (1500,3500),
            'mission_id': 3,
            'ships': [
                [0, TALON, (2000,700), 1, {'direction': 3.14, 'mission_id': 12}],
                [0, TALON, (2000,800), 1, {'direction': 3.14, 'mission_id': 13}]
                ]
            },
         {
            'name': 'home',
            'position': (500,400),
            'mission_id': 10,
            'ships': []
            }
        
        ] ,
    'goals': [
        {
            'goal_name': 'destroy fighter',
            'trigger_condition': [3, 'visited'],
            'super_goal': 'check nav 3',
            'goal_event': [12, 'destroyed']
            },
        {
            'goal_name': 'destroy fighter',
            'trigger_condition': [3, 'visited'],
            'super_goal': 'check nav 3',
            'goal_event': [13, 'destroyed']
            },
        {
            'goal_name': 'destroy fighter',
            'trigger_condition' : [1, 'visited'],
            'super_goal': 'check nav 1',
            'goal_event': [11, 'destroyed']
            },
        {
            'goal_name': 'check nav 1',
            'goal_event': [1, 'visited']
            },
                         
        {
            'goal_name': 'check nav 2',
            'goal_event': [2, 'visited']
              },
        {
            'goal_name': 'check nav 3',
            'goal_event': [3,'visited']
            }
              ],
    
    'success_levels': {
        'failure': [
            ['impossible']
            ],
        'basic': [],
        'bronze': [
            ['ships_killed', [3]]
            ]
        },
    
    'briefing': 'You are flying a simple 3 point patrol. Hit Nav 1, Nav 2, Nav 3 and return to the claw. Try to kill as many pirate fighters as possible, BUT FIRST an FOREMOST: COME BACK ALIVE!',
    'debriefing': [
        ['Good to have you back alive. \n', []], ### text + conditions, under which the text is displayed ;; None = unconditionall
        ['Congratulations on your first kill. \n',[ ['ships_killed',[1] ]] ],
        ['Congratulations on your first kills. Quite impressive for your first live fire sortie. \n', [['ships_killed', [x for x in range (2,101) ] ]] ],
        ['We have a little party going on in the rec room. Two of the other rookies have made their first kills. You have got my official permission to get trashed.', []]
        ],
    'asteroid_fields': [
        [ (2000,500), 100, 500 ],  # position, number, field seize
        [ (1500, 3500),80, 400 ]
        ]
    }




campaign_mission_2 = {
    'ships': [
        [1, PSYCHO, MIDDLE,0, {'autopilot_destination' : ['ship', 21] , 'mission_id': 0}]
        ### auto_destination targets object with given MISSION_ID
        ],
    'mission_name': '  p1' ,
    'trigger_points': [
                {
            'name': 'nav_0',
            'position': MIDDLE,
            'mission_id': 10,
            'ships': []
            },
        {
            'name': 'nav_1',
            'position': (3000,500),
            'mission_id': 1,
            'ships': [
                [0, TALON, (1500,- 400), 1, {'direction': 4.57, 'mission_id': 11, 'target_priorities': {21:50}}],
                [0, TALON, (1500,- 300),1 ,  {'direction': 4.57, 'mission_id': 12, 'target_priorities': {21:50}}],
                [0, TALON, (1500,- 500),1 ,  {'direction': 4.57, 'mission_id': 12, 'target_priorities': {21:50}}],
                [0, DEADMAN, (500, 300), 0, { 'direction' : 4.57,'autopilot_destination': ['trigger_point', 1], 'mission_id': 21, 'speed_mode': 'h', 'autopilot_lead_ship':( 0, 'c'), 'just_jumped_in': 'yes'} ]
               
                ]
        }
        
        ] ,
    'goals': [
        {
            'goal_name': 'check nav 1',
            'goal_event': [1, 'visited'],
            'goal_id': 1
            },
                         
        {
            'goal_name': 'escort DEADMAN back to nav_0',
            'goal_event': [10, 'visited',21],
            'goal_id': 2 
              }
              ],
    'success_levels': {
        'failure': [],
        'basic': [
            ['goal_id', 2, 'yes'] 
            ],
        'bronze': [
            ['goal_id', 2, 'yes'], 
            ['ships_killed', [3]]
            ]
        },
    'briefing': 'We have got a DEADMAN Tanker coming in. Meet the Tanker at nav point 1 and escort it back here. /n Remember, to couple your Autopilot, you need to be within 500 klicks of the Tanker.',
    'debriefing': [
        ### text + conditions, under which the text is displayed ;; None = unconditionall
        ['Good work bringine the Tanker in', [['goal_id', 2, 'yes'] ]] , 
        ['And you got all of the attackers. Nice job', [['goal_id', 2, 'yes' ],['ships_killed', [3] ]] ],
        ['A pity you couldnt save the Deadman, but 3 fighters killed makes up for it. Those crates are named "Dead - man" for a reason', [  ['goal_id', 2, 'no'],['ships_killed', [3] ]  ]  ],
        ['A pity you couldnt save the Deadman. At least you got some of the fighters.', [  ['goal_id', 2, 'no'],['ships_killed', [1,2] ]  ]  ],
        ['Well, thats a failed mission if I have ever seen one. If its any consolation, Lightspeed and Doomsday did even worse than you. They got themselfes killed.', [  ['goal_id', 2, 'no'],['ships_killed', [0] ]  ]  ],
              ],
    'asteroid_fields': []
    }








campaign_mission_3 = {
    'ships': [
        [1, HORNET, MIDDLE,0, {'autopilot_destination' : ['ship', 21] , 'mission_id': 0}]
        ### auto_destination targets object with given MISSION_ID
        ],
    'mission_name': '  p3' ,
    'trigger_points': [
        {
            'name': 'nav_1',
            'position': (3000,500),
            'mission_id': 1,
            'ships': [
                [0, TALON, (1000,500), 1, {'direction': 4.57, 'mission_id': 11}]
                ]
            },
        {
            'name': 'nav_2',
            'position': (5000,2000),
            'mission_id': 2,
            'ships' : [
                [0, TALON, (1000,500), 1, {'direction': 4.57, 'mission_id': 12}],
                [0, TALON, (1000,700), 1, {'direction': 4.57, 'mission_id': 13}],
                [0, SMALL_SUPPLY_DEPOT, dfunctions.vadd (MIDDLE, (50,50)), 1, {'speed_mode': 'off', 'direction': 4.57, 'mission_id': 14}],
                [0, LASER_MINE, dfunctions.vadd (MIDDLE, (50,0)), 1, {'speed_setting': 'off','direction': 4.57, 'mission_id': 18}],
                [0, LASER_MINE, dfunctions.vadd (MIDDLE, (50, 100)), 1, {'speed_setting': 'off', 'direction': 4.57, 'mission_id': 17}]
                
                ]
            },
        {
            'name': 'nav_3',
            'position': (2500, 4000),
            'mission_id': 3,
            'ships': []
            },
        {
            'name': 'nav_0',
            'position': MIDDLE,
            'mission_id': 10,
            'ships': []
            }
        ] , ### End : Trigger Points 
    'goals': [
        {
            'goal_name': 'destroy supply depot',
            'goal_event': [14, 'destroyed'],
            'goal_id': 1
            },
  
        {
            'goal_name': 'check nav 1',
            'goal_event': [1, 'visited']
            },
                         
        {
            'goal_name': 'check nav 2',
            'goal_event': [2, 'visited']
              },
        {
            'goal_name': 'check nav 3',
            'goal_event': [3, 'visited']
            }
        
              ],
    'success_levels': {
        'failure': [],
        'bronze': [
            ['goal_id', 1, 'yes'], 
            ]
        },
    'briefing': 'We suspect there is a hidden pirate supply cache in the the asteroids. I want it destroyed. You will scout three asteroid fields for the cache. \n Pro Tip: dont run into asteroids. Its bad for your health.  ',
    'debriefing': [
        ['I knew you could do it. The pirates will be running low on supplies now.' , [['goal_id', 1, 'yes'    ] ] ],  
        ['Don\' t take it to hard. Not everyone was meant to be a fighter ace. Well, I guess I\' ll have to give the tough missions to Maverick or Fairy.', [    ['goal_id', 1, 'no']      ] ], 
      
       
        ],
    'asteroid_fields': [
        [ (3000, 500), 100, 400],
        [ (5000,2000), 80, 300],
        [ (2500, 4000), 120, 400] 
        ]
    }



campaign_mission_4 = {
    'ships': [
        [1, PSYCHO, MIDDLE,0, {'autopilot_destination' : ['ship', 21] , 'mission_id': 0}],  #    [0, DEMON, (1200, 500), 1 ]
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, SMALL_SUPPLY_DEPOT, (5000,2000), 1, {'mission_id': 11, 'speed_mode': 'off'} ], 
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ],
        [0, LASER_MINE, dfunctions.vadd ( (5000,2000), ( [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 ),  [-1,1] [random.randint (0,1)] * 10 * random.randint (3 , 15 )) ) , 1 ]
        ],
    'mission_name': '  p1' ,
    'trigger_points': [
        {
            'name': 'nav_1',
            'position': (4500,2000),
            'mission_id': 1,
            'ships': [
                [0, TALON, (2200,500), 1, {'direction': 4.75, 'mission_id': 12}]
                ]
        },
       
        
        ] ,
    'goals': [
        {
            'goal_name': 'destroy the radar station',
            'trigger_condition': [1, 'visited'],
            'super_goal': None ,
            'goal_event': [11, 'destroyed'],
            'goal_id': 1
            },
       
              ],
    'success_levels': {
        'failure': [],
        'basic': [
            ['goal_id', 1, 'yes'] 
            ]
        
        },
    'briefing': 'Destroy the enemy radar station near nav_1. Be careful: The radar station is guarded by laser mines. \n I don\'t care about the mines. Don\'t take risks just to kill them',
    'debriefing': [
        ['Good job taking out the radar station.  I knew I could count on you. \n', [['ship_destroyed', 11 ]]], ############# changed for test purposes !!! needs to be "11", not "12" !!!
        ['Well, minefields can be a real challenge for a rookie. I\'ve sent Maverick to finish the job. I guess you owe him a drink or three for cleaning up after you', [    ['goal_id', 1, 'no']      ] ]
        ],
    'asteroid_fields': [
        ]
    }





campaign_mission_5 = {
    'ships': [
        [1, PSYCHO, MIDDLE,0, {'autopilot_destination' : ['ship', 21] , 'mission_id': 0}],  #    [0, DEMON, (1200, 500), 1 ]
        ],
    'mission_name': '  p5' ,
    'trigger_points': [
        {
            'name': 'nav_1',
            'position': (2000,500),
            'mission_id': 1,
            'ships': [
                [0, TALON, (1500,500), 1, {'direction': 1.57, 'mission_id': 11}],
                [0, TALON, (1500,700), 1, {'direction': 1.57, 'mission_id': 12}],
                [0, TALON, (1500,900), 1, {'direction': 1.57, 'mission_id': 13}],
                [0, TALON, (1500,1100), 1, {'direction': 1.57, 'mission_id': 14}],

                [0, SCYLLA, (2000,900), 1, {'direction': 1.57, 'mission_id': 15, 'lead_ship':( 21, 250, 4.71)}],
                [0, SCYLLA, (2000,300), 1, {'direction': 1.57, 'mission_id': 16, 'lead_ship':( 21, 250, 1.57)}],
                
                
                [0, MORONIR, (2000, 600), 1, { 'direction' : 0.8,'destination': ['trigger_point', 2, 'jump_out'], 'mission_id': 21, 'speed_mode': 'h'} ]
                
                ]
        },
        {
            'name': 'nav_2',
            'position': (4000,1500),
            'mission_id': 2,
            'ships': []
            },
    
         {
            'name': 'home',
            'position': (500,400),
            'mission_id': 10,
            'ships': []
            }
        
        ] ,
    'goals': [
        {
            'goal_name': 'check nav 1',
            'goal_event': [1, 'visited']
            },
                         
        {
            'goal_name': 'destroy moronir',
            'goal_event': [21, 'destroyed'],
            'goal_id': 1
         }
              ],
    'success_levels': {
        'failure': [],
        'silver': [
            ['goal_id', 1, 'yes'], 
            ]
        },
    'briefing': 'We\' ve got the pirates on the run. They have packed up their stuff into an old moronir Transport and they are running for nav point 2 to jump out of system. \n Don\'t let them escape!',
    'debriefing': [
        ['GREAT! You finished them! . \n', [    ['goal_id', 1, 'yes' ]    ]],
        ['You let them escape. Now they can start their business somewhere else. A, well, the next batch of rookies needs some sparring partners, too.', [    ['goal_id',1, 'no'       ]         ]]
        ],
    'asteroid_fields': [
        [ (2000,500), 100, 500 ],  # position, number, field seize
        [ (1500, 3500),80, 400 ]
        ]
    }










    
    
    



test_mission = {
    'briefing': '',
    'ships': [ (1, SABRE, MIDDLE,0),(0, TALON, (1500,300),1)],
    'mission_name': '  test' ,
    'trigger_points': [{'position': (1000,500), 'ships': [ [0, HAMMERHEAD, (1000,100), 1, {'direction': 3.14, 'mission_id': 11}],[0, HAMMERHEAD, (1000,200),1]] }] ,
    'goals': [{'goal_name': 'destroy fighter alpha',
     'goal_event': [11, 'destroyed'] }]
    }
campaign_missions =[ campaign_mission_1, campaign_mission_2, campaign_mission_3, campaign_mission_4, campaign_mission_5] 


m0 = [  [ (1, HORNET, MIDDLE), ( 0, DRAHLTI, (2000,500))], ' scout ' ]

m1 = [  [ (1, RAPTOR, MIDDLE),( 0, SALTHI, (1500,300)), ( 0, HORNET, (1500,400)), ( 0, HORNET, (1500,500))], '  dogfight' ]

m2 = [ [ (1, DRAHLTI, MIDDLE), (0, HORNET, (1500,300)), (0,DRAHLTI, (1600,400)) ], 'bombing run' ]






    
# eigenes Schiff

    





# definition von variablen
r = 0
killed_ships_team2 = [0,0,0]
start_screen = 1
mission_running = 0
campaign_running = 0
speed_setting = 10 ### 0 bedeutet, dass in dieser Runde keine Einstellungen vorgenommen wurden, die Inhalte reichen von 1-10
custom_mission = {'ships': [] } 
custom_player = [DRAHLTI] 
custom_wing_list = [SCIMITAR]
custom_enemy_list = [JALTHI, JALTHI]
pause = 0
'''
f = None
'''
microcontrol_counter = 0 ### counts, how many consecutive frames the 's' or 'd' buttons were pressed



### stars:
def create_stars ():
    global star_list 
    star_list = []
    
    for i in range (1,1000):
        x = random.randint (LEFT_LIMIT, RIGHT_LIMIT)
        y = random.randint (1, SCREEN_Y)
        star_list.append ( (x,y) )

create_stars ()



crosshairs_colour = WHITE

delayed_effects_list = []
mission_event_list = []
mission_goal_list = [] 





    

    ################################################################################################################
    #####################################           END:    Tkinter Stuff       ####################################
    ################################################################################################################

def mainloop ():
    globs = globals ().keys ()
    globs.sort () 
    global killed_ship_list
    killed_ship_list = [] 
    global target_count
    target_count = 1 
    global running_mission_info
    global start_debriefing_screen
    global end_game
    end_game = 0 
    global master_frame_counter
    master_frame_counter = 0 
    global mission_timer
    mission_timer = 0 
    global pause
    pause = 'no'
    global global_message_list
    global_message_list = []
    global star_list
    star_list = []
    global pressed
    pressed = [] 
    global screen
    global autopilot_destination
    autopilot_destination = None
    global log_factor
    log_factor = 1 
    global global_target_object_id
    global_target_object_id = None 
    global recreate_stars
    recreate_stars = 'no' 
    global campaign_state
    global ship_list
    global bullet_list
    bullet_list = [] 
    global missile_list
    missile_list = [] 
    global asteroid_list
    global explosion_list
    explosion_list = [] 
    global target_count
    target_count = [] 
    global enemy_ship_list
    enemy_ship_list = [] 
    global radar_factor
    radar_factor = 20
    global manual_turrets
    global object_list
    global master_object_counter
    global trigger_point_list
    global turret_list
    global cannon_list
    global debris_list

    

 


    ### ###
    #######         local variables
    
    pause = 0 
    position_adjustment = (0,0)
    microcontrol_counter = 0 

    
    global_message_list = []
    win_1 = bottom_right_window ()
    
     
    win_2 = top_right_window ()
    
    win_3 = middle_right_window ()
    win_3.position = (SCREEN_X - 200, win_1.y_seize) 
    win_1.position = (SCREEN_X - win_1.x_seize, win_2.y_seize + win_3.y_seize )
    win_1.position = (SCREEN_X - 340, win_1.y_seize  + win_3.y_seize + 20)  
   

    win_4 = window_4 ()
    win_4.position = (SCREEN_X - 340, win_1.y_seize)

    win_5 = window_5 ()
    win_6 = window_6 ()
    win_7 = window_7 ()
    win_8 = window_8 () 


    
    mission_points = 0 
    joy_button_old = 0

    create_stars ()


    
    running = 1
    if end_game == 1: running = 0
    



    while running:
       

        screen.fill((0, 0, 0))

        for d in persistant_dot_list [:]:
            dot ( d [0], colour = d [1])
            d [2] -= 1
            if d [2] <= 0: persistant_dot_list.remove (d) 
            

        
        
        clock.tick (30)
        

        enemy_ship_list = []
        for s in ship_list:
            if ship.output_team (s) == 1: enemy_ship_list.append (s)

        
        for message in global_message_list [:]:
            message [1] -= 1
            if message [1] <= 0: global_message_list.remove (message)

        

      

        

        

        

        
        
        master_frame_counter += 1
         
        key_selected = 0 ### 0 = no key has been used yet
        adjustment = 0 
        r = 0
        fire = 0
        ai_fire = 0
        fire_torpedo = 0 
        fire_missile = 0
        fire_missile_2 = 0
        fire_missile_3 = 0
        fire_missile_4 = 0
        fire_missile_5 = 0
        target_key = 0
        respawn_key = 0
        activate_afterburner = 0 
        key_1 = 0
        key_2 = 0
        key_3 = 0
        key_4 = 0
        key_5 = 0
        key_6 = 0
        key_7 = 0
        key_8 = 0
        key_9 = 0
        key_0 = 0
        keypad_minus = 0
        keypad_plus = 0
        
        ### Tastatureingabe

        keyup = []
        for i in range (0,400):
            keyup.append (0)

        keydown = []
        for i in range (0,400):
            keydown.append (0)
        
       
        event = pygame.event.poll()
        press = pygame.key.get_pressed ()
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = 0
            exit (screen)
        
        elif event.type == pygame.KEYUP:
            keyup = []
            for i in range (0,400):
                if event.key == i:
                    keyup.append (1)
                else: keyup.append (0) 
        elif event.type == pygame.KEYDOWN:
            keydown = []
            for i in range (0,400):
                if event.key == i:
                    keydown.append (1)
                else: keydown.append (0) 


            if keydown [308] == 0:   
                if event.key == pygame.K_1:
                    key_1 = 1
                    speed_setting = 1
                    
                if event.key == pygame.K_2:
                    key_2 = 1
                    speed_setting = 2
                if event.key == pygame.K_3:
                    key_3 = 1
                    speed_setting = 3
                if event.key == pygame.K_4:
                    key_4 = 1
                    speed_setting = 4
                if event.key == pygame.K_5:
                    key_5 = 1
                    speed_setting = 5
                if event.key == pygame.K_6:
                    key_6 = 1
                    speed_setting = 6
                if event.key == pygame.K_7:
                    key_7 = 1
                    speed_setting = 7
                if event.key == pygame.K_8:
                    key_8 = 1
                    speed_setting = 8
                if event.key == pygame.K_9:
                    key_9 = 1
                    speed_setting = 9
                if event.key == pygame.K_0:
                    key_0 = 1
                    speed_setting = 10

            if event.key == 46:
                fire_torpedo = 1
            
                
            if mission_running in [1,2]:  
                if event.key == pygame.K_z : radar_factor = int (radar_factor / 2)
                if event.key == pygame.K_x : radar_factor *= 2
                if event.key == pygame.K_l : log_factor = log_factor * 2
                if event.key == pygame.K_k :
                    log_factor = int (log_factor / 2)
                    if log_factor == 0: log_factor = 1
                if event.key == pygame.K_p: pause = dfunctions.switch (pause)
                if event.key == pygame.K_TAB: activate_afterburner = 1
                if event.key == pygame.K_KP_MINUS : keypad_minus = 1
                if event.key == pygame.K_KP_PLUS : keypad_plus = 1
                # if event.key == pygame.K_3: speed = 50.0
                #if event.key == pygame.K_a: r = 1
                #if event.key == pygame.K_d: r = -1
                # if event.key == pygame.K_SPACE: fire = 1
                if event.key == pygame.K_m: fire_missile = 1
                if event.key == pygame.K_n: fire_missile_2 = 1
                if event.key == pygame.K_b: fire_missile_3 = 1
                if event.key == pygame.K_v: fire_missile_4 = 1
                if event.key == pygame.K_c: fire_missile_5 = 1

                if event.key == pygame.K_o: manual_turrets = y_n_switch (manual_turrets)
                
                if event.key == pygame.K_t: target_key = 1
                if event.key == pygame.K_x: respawn_key = 1
                if event.key == pygame.K_q:
                    if ship.output_energy_points (ship_list [0]) > 0:
                        ship.activate_booster (ship_list [0])
                        
                        
                        
                
                if event.key == pygame.K_e: ship.initiate_gliding_phase (ship_list [0])


                #
                
                if event.key == 60:     ###         <
                    
                    
                    adjustment = MIDDLE [0] - 220
                    if pressed [306] == 1: adjustment = - ( MIDDLE [0] - 220 )
                    
                    

        
        
        
        if pressed [pygame.K_a]: r = 1
        if pressed [pygame.K_f]: r = -1


        if joystick == 'yes':
            joy_button_old -= 1 
            
            r = -1 * joy_1.get_axis (0)
            if joy_1.get_button (0) == 1:
                fire = 1
            if joy_1.get_button (1) == 1:
                if joy_button_old <= 0 :
                    fire_missile_3 = 1
                    joy_button_old = 10
        
        ### microcontrols 
        if pressed [pygame.K_s]:
            microcontrol_counter += 1
            r = max (0.1, min ( microcontrol_counter / 50, 0.5))
        if keyup [pygame.K_s]: microcontrol_counter = 0
        
        if pressed [pygame.K_d]:
            microcontrol_counter += 1
            r = -1 *  max (0.1, min (microcontrol_counter / 50, 0.5))
        if keyup [pygame.K_d]: microcontrol_counter = 0
        
        if pressed [pygame.K_SPACE]: fire = 1

    
        
        if mission_running in [1,2] and pressed [308] == 0 and mission_timer >= 100:
            if keydown [pygame.K_1]: ship.set_speed_mode (object_list [1], 's' )
            if pressed [pygame.K_2]: ship.set_speed_mode (object_list [1], 'm' )
            if pressed [pygame.K_3]: ship.set_speed_mode (object_list [1], 'h' )
            if pressed [pygame.K_0]: ship.set_speed_mode (object_list [1], 'off' )
            
            if pressed [pygame.K_r]: ship.switch_stealthed (object_list [1])
            

        if press [308] == 1 and press [120] == 1: end_game = 1

        if mission_running == 0: speed_setting = 2


        ###  End Mission
        if pressed [308] == 1  and keydown [113]== 1:
            running = 0
            if mission_running == 1: 
                campaign_state += 1 
                start_debriefing_screen = 'yes'
            elif mission_running == 2: cleanup_old_mission () 
            end_game = 1  

       

        if pressed [308] == 1:
            if keydown [49] == 1:
                autopilot_destination = 1
                keydown [49] = 0 
            if keydown [50] == 1:
                autopilot_destination = 2
                keydown [50]= 0
            if keydown [51] == 1:
                autopilot_destination = 3
                keydown [51] = 0 
            if keydown [52] == 1:
                autopilot_destination = 4
                keydown [52] = 0
            if keydown [48] == 1:
                autopilot_destination = 10
                keydown [48] = 0 

        if pressed [308] == 1 and keydown [91] == 1 :   ### 91 = 'ü'
            persistant_dot_list.append ( [ (0,300), GREEN, 150] )
            persistant_dot_list.append ( [ (500,500), RED, 150] )
            persistant_dot_list.append ( [ (1000,500), BLUE, 150] ) 

        

        
            
                
        ### Ende ## Tastatureingabe


       

        
        while pause == 1:
            write ('GAME PAUSED', (500,300), GREEN, 25 )
            pygame.display.update ( [ (500,300,200,50) ] ) 
            

            
            pygame.time.wait (20)
            event = pygame.event.poll()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: pause = 0
                
        
        if mission_running in [1,2]:
            mission_timer += 1 
            main_screen = 0
            if len (enemy_ship_list) > 0:
                
                if target_count >= len (enemy_ship_list): target_count = 0
                if target_key == 1:
                    if target_count < len (enemy_ship_list) -1 : target_count = target_count + 1
                    else: target_count = 0
                
                
                global_target_object_id = ship.output_object_id (enemy_ship_list [target_count])

        


         # global messages:
        def display_global_messages ():
            global global_message_list
            for e, item in enumerate (global_message_list):
                write_2 (item [0], vadd ( (200,200), (0, e * 100)))

        display_global_messages ()

        

        for star in list(star_list):
            screen.set_at(dfunctions.vector_int (star), WHITE)
            if star [0] >= RIGHT_LIMIT:
                star_list.remove (star)
                star_list.append ( (LEFT_LIMIT + 1, random.randint (  1,SCREEN_Y)))
            elif star [0] < LEFT_LIMIT:
                star_list.remove (star)
                star_list.append ( (RIGHT_LIMIT -1 , random.randint (1, SCREEN_Y)))
            elif star [1] >= SCREEN_Y:
                star_list.remove (star)
                star_list.append ( ( random.randint (LEFT_LIMIT + 1, RIGHT_LIMIT - 1), 1))
            elif star [1] < 1:
                star_list.remove (star)
                star_list.append (( random.randint (LEFT_LIMIT + 1, RIGHT_LIMIT -1), SCREEN_Y))

                
        
        
        # delayed effects update
        for effect in delayed_effects_list [:]:
            if delayed_effect.update (effect) == 0: delayed_effects_list.remove (effect)

        
        
        # Schiff- Aktualisierung und Graphik
        for sh in ship_list:
            ship.update (sh)
            ship.update_afterburner (sh)
            ship.recharge_shields (sh)
            ship.recharge_missiles (sh)
            ship.update_radar (sh)
            ship.update_test_module (sh)
            if sh in enemy_ship_list and target_count == enemy_ship_list.index (sh):
                target_positionx, target_positiony = ship.output_position (sh)
            # Schiff - Aktionen
                # (1) getroffene Schiffe löschen + explosion erzeugen  
            zaehler2 = ship.hit (sh)
            if ship.delayed_death (sh) == 1: zaehler2 = 1
            if zaehler2 == 1:   ### ship is destroyed
                print 'test 345  , ship destroyed' 
                x,y = ship.output_position (sh)
                ship_list.remove (sh)
                
                if sh.mission_id != None :
                    print 'test 370   '
                    mission_event_list.append ([ship.output_mission_id (sh), 'destroyed', sh.name, sh.kill_value, sh.team] )
 
                e = explosion (1, 30 + 2 * sh.radius, position = sh
                               .display_position)
                debris_count = 10
                if sh.ship_class == 'bomber': debris_count = 25
                if sh.ship_class == 'light_capital': debris_count = 100 
                for i in range (0,debris_count):
                    d = debris  ((x,y), 100, 1.57 * random.uniform (0,4) )
                
                # (2) gegner- Schiffe: keine richtungsänderung
            if ship.output_player (sh) == 0:
                r = 100
                fire = 0
                fire_missile = 0
            if ship.output_player (sh) == 1:
                if activate_afterburner == 1: ship.activate_afterburner (sh)
                if keypad_minus == 1: ship.set_missile_vorhalt (sh, 0.15)
                if keypad_plus == 1: ship.set_missile_vorhalt (sh,-0.15)
                # speed_setting_list = {1: 's', 2: 'm', 3: 'h', 0: 'off' }
                if fire_torpedo == 1: ship.shoot_torpedo (sh) 
                if fire_missile == 1: ship.shoot_missile (sh, HEAT_SEEKING)
                if fire_missile_2 == 1: ship.shoot_missile (sh, RADAR)

                if fire_missile_3 == 1: ship.shoot_missile (sh, DUMBFIRE)
                if fire_missile_4 == 1: ship.shoot_missile (sh, DUMB_DELAYED)
                if fire_missile_5 == 1: ship.shoot_missile (sh, HEAVY_DUMB)
                if keydown [44] == 1: ship.shoot_missile (sh, MICRO)
                if pressed [257] == 1: sh.shoot (guns = 'primary')
                if pressed [258] == 1: sh.shoot (guns = 'secondary')
                if pressed [259] == 1: sh.shoot (guns = 'tertiary')
                if joystick == 'yes':
                    if joy_1.get_button (2) == 1: sh.shoot (guns = 'primary')
                    if joy_1.get_button (3) == 1: sh.shoot (guns = 'secondary')
            
            ship.update_direction (sh,r)
            ship.update_position (sh)
            if ship.output_player (sh) == 1:
                position_adjustment = dfunctions.vadd (dfunctions.skalar_multi ( -1, ship.output_moved (sh)) , ( -adjustment, 0)) 
                # write (position_adjustment , (100,300), BLUE, 15)
                if autopilot_destination != None:

                    def check_autopilot ():
                        global global_message_list 
                        out = 'ok'
                        if 's1' in dir (): error ()
                        for s1 in enemy_ship_list:
                            if points_distance (sh.position, s1.position) <= 2000:
                                out = 'denied'
                                global_message_list.append ( ['enemy_near', 90])
                                break 

                        if 'b' in dir (): error ()
                        for b in bullet_list:
                            if points_distance (sh.position, b.position) <= 200:
                                out = 'denied'
                                global_message_list.append ( ['asteroids near', 90])
                                break 

                        return out

                    if check_autopilot () == 'ok':
                                
                        

                        
                        nav_point_position = None
                        for t in trigger_point_list:
                            if t.mission_id == autopilot_destination:
                                nav_point_position = t.position
                        if nav_point_position != None:
                            player_old_position = sh.position
                            nav_point_vector = vector_sub ( nav_point_position, sh.position)
                            nav_point_distance = vector_length (nav_point_vector)
                            travel_distance = nav_point_distance - 500
                            nav_point_direction = math.atan2 (nav_point_vector [0], nav_point_vector [1] )

                            nav_travel_vector = dfunctions.fextrapolate_line (nav_point_direction, (0,0), 0, travel_distance) [1]
                                                      

                         
                            sh.position = dfunctions.vadd (sh.position, nav_travel_vector)
                            position_adjustment = dfunctions.vadd (dfunctions.skalar_multi (-1, nav_travel_vector), position_adjustment)
                            sh.direction = nav_point_direction 
                            
                            for sx in ship_list:
                                
                                if sx != sh:
                                    
                                    if sx.autopilot_lead_ship == (0, 'u'):   ###  'u' == unconditional  // 'c' = conditional: works only if player is closer than 500 
                                        sx.position = dfunctions.vadd (sx.position, nav_travel_vector)
                                        sx.direction = nav_point_direction
                                    if sx.autopilot_lead_ship == (0, 'c') and vector_length ( vector_sub (player_old_position, sx.position)) <= 500         :
                                        sx.position = dfunctions.vadd (sx.position, nav_travel_vector)
                                        sx.direction = nav_point_direction

                            recreate_stars = 'yes' 



                    autopilot_destination = None 
            
            
            ship.select_target (sh)

            
            
            if ship.output_position (sh) [0]  / log_factor < SCREEN_SPLIT  :


                    
                    if ship.output_player (sh) == 1:  ship.graphics (sh)
                    if ship.output_player (sh) == 0:
                        if sh in (ship.output_ships_on_radar ( ship_list [0] )) : ship.graphics (sh)
            if ship.output_player (sh) == 0: ship.trigger (sh)
               # erzeugen von Schüssen
            if fire == 1: ship.shoot (sh)
            if ai_fire == 1: ship.shoot (sh)

            # ship.adjust_position (sh, position_adjustment [0], position_adjustment [1])

        for x in ship_list: ship.adjust_position (x, position_adjustment [0], position_adjustment [1])
        
        

        
        for e, t in enumerate (trigger_point_list):
            trigger_point.adjust_position (t, position_adjustment [0], position_adjustment [1] )
            trigger_point.circle (t)
            trigger_point.set_list_position (t,e) 
            trigger_point.trigger (t)

        '''
        if mission_running in [1,2]:
            if nav_points != None:
            
                for e, nav in enumerate (nav_points):
                    nav_points [e] = (nav [0] + position_adjustment [0], nav [1] + position_adjustment [1])

                    dot (nav, GOLD)
        '''

                
            
            
        
        for tur in turret_list:
            turret.update (tur) 
            turret.update_position (tur)
            turret.update_direction (tur)
            turret.do_graphics (tur)
            turret.trigger (tur)
            turret.adjust_position (tur, position_adjustment [0], position_adjustment [1])

        for can in cannon_list:
            cannon.update_cooldown (can)
            can.update () 
        # Geschoss - Aktualisierung und Graphik
        
        for ast in asteroid_list:
            ast.update ()
            ast.adjust_position (position_adjustment [0], position_adjustment [1])

        
        for bull in bullet_list [:]:
            bullet.update_position (bull)
            bullet.adjust_position (bull, position_adjustment [0], position_adjustment [1])
            bullet.circle (bull)
            if (bullet.output_travelled (bull) > bullet.output_range (bull) or bullet.output_destroy (bull) == 'yes'):
                if bull in bullet_list: bullet_list.remove (bull)

        for d in debris_list:
            d.update ()
            d.adjust_position (position_adjustment [0], position_adjustment [1])  
        
        # missile - aktualisierung und graphik
        for mi in missile_list [:]:
            if missile.output_timer (mi) <= 0: missile_list.remove (mi)
        for m in missile_list:
            # missile.set_target_position (m,target_positionx, target_positiony)
            missile.update_direction (m)
            missile.update_position (m)
            missile.adjust_position (m, position_adjustment [0], position_adjustment [1])
            missile.circle (m)
            if missile.output_travelled (m) > missile.output_range (m): missile_list.remove (m)
        # Exlosionen
        for e in explosion_list:
            explosion.adjust_position (e, position_adjustment [0], position_adjustment [1]) 
            explosion.circle (e)
            if explosion.output_destruct (e) == 1:
                explosion_list.remove (e)

                
       



        #### test windows
       
        win_1.update ()
     
        win_2.update()
      
        win_3.update ()

       
        win_4.update ()
        win_5.update ()
        win_6.update ()
        win_7.update ()
        win_8.update () 

        
        ### ### ### 
        ### ### ###         Display shit 
        if True:

            ###     target brackets 
            if global_target_object_id != None:
                
                target_coordinates = ship.output_display_position (object_list [global_target_object_id] )
                if target_coordinates != None and target_coordinates [0] < SCREEN_SPLIT: dfunctions.target_brackets (( int (target_coordinates [0]),int (target_coordinates [1])),1.5 *  ship.output_radius (object_list [global_target_object_id]))
               
               #  dfunctions.target_brackets ((int (( dfunctions.vadd (SECOND_MIDDLE, ship.output_radar_position ( object_list [global_target_object_id])) ) [0]), int (( dfunctions.vadd (SECOND_MIDDLE, ship.output_radar_position ( object_list [global_target_object_id])) ) [1])), 70)
               

                
            
                

                

                

            ### fadenkreuz- Balken
            FADENKREUZ_X = MIDDLE [0] 
            FADENKREUZ_Y = SCREEN_Y - 20

            

            
                
                    
            pygame.gfxdraw.aapolygon (screen, (( FADENKREUZ_X - 100, FADENKREUZ_Y - 21), (FADENKREUZ_X + 100, FADENKREUZ_Y - 21), (FADENKREUZ_X + 100, FADENKREUZ_Y -1), (FADENKREUZ_X -100, FADENKREUZ_Y -1)), GREEN ) 
            pygame.draw.aaline ( screen, FAINT_WHITE, (FADENKREUZ_X- 99, FADENKREUZ_Y -11), (FADENKREUZ_X + 99, FADENKREUZ_Y -11), 1)
            pygame.draw.aaline ( screen, FAINT_WHITE, (FADENKREUZ_X, FADENKREUZ_Y - 16), ( FADENKREUZ_X, FADENKREUZ_Y -5), 1)

            ship_list_target_sorted = [x for x in ship_list if x.object_id != global_target_object_id] + [x for x in ship_list if x.object_id == global_target_object_id]
            
            
            for ship_x in ship_list_target_sorted:
                colour = RED
                fg_colour = BLUE
                
                if ship_x.object_id == global_target_object_id:
                    colour = ORANGE
                    fg_colour = GOLD 
                if ship.output_player (ship_x) == 0:
                    fadenkreuz_direction = ship.output_fadenkreuz_direction (ship_x)
                    if abs (fadenkreuz_direction) < 0.8:
                        fadenkreuz_zoom = 6
                        
                        dfunctions.triple_line_horizontal ( ( FADENKREUZ_X + fadenkreuz_direction * -57 * 3, FADENKREUZ_Y -11), ship.output_fadenkreuz_size (ship_x) * fadenkreuz_zoom * 2 * 57.3, colour, outer_lines = 3, inner_lines = 0)
                        dfunctions.triple_line_horizontal ( ( FADENKREUZ_X + fadenkreuz_direction * -57 * 3, FADENKREUZ_Y -11), ship.output_fadenkreuz_size (ship_x) * 1 * 2 * 57.3, fg_colour , outer_lines = 3, inner_lines = 0)
                        if ship_x.object_id == global_target_object_id:
                            pygame.draw.aaline (screen, ORANGE, ( FADENKREUZ_X + fadenkreuz_direction * -57 * 3, FADENKREUZ_Y -2), ( FADENKREUZ_X + fadenkreuz_direction * -57 * 3, FADENKREUZ_Y -20), 1) 
                            #dfunctions.triple_line_horizontal ( ( FADENKREUZ_X + fadenkreuz_direction * -57 * 3, FADENKREUZ_Y -16), ship.output_fadenkreuz_size (ship_x) * 1 * 2 * 57.3, fg_colour , outer_lines = 3, inner_lines = 0)
                            #dfunctions.triple_line_horizontal ( ( FADENKREUZ_X + fadenkreuz_direction * -57 * 3, FADENKREUZ_Y - 13), ship.output_fadenkreuz_size (ship_x) * 1 * 2 * 57.3, fg_colour , outer_lines = 3, inner_lines = 0)
                            
                        # dfunctions.dot ( ( FADENKREUZ_X + fadenkreuz_direction * -57 * 3, FADENKREUZ_Y -11), RED)
                            
               

        ### Stars
       
        new_list = []
        for star in star_list:
            new_star = dfunctions.vadd (star, position_adjustment)
            new_list.append (new_star)
        star_list = new_list [:]

        if adjustment != 0:
            star_list = []
            for i in range (1,1000):
                x = random.randint (LEFT_LIMIT, RIGHT_LIMIT)
                y = random.randint (1, SCREEN_Y)
                star_list.append ( (x,y) )


        if recreate_stars == 'yes':
            
            
            recreate_stars = 'no'
            create_stars ()


         

          
        
        # if pressed [308] == 1  and keydown [60]== 1:
        if 1 == 1: 
            if mission_running in [1,2]:
                if  global_target_object_id != None :
                    player_pos = ship.output_position (object_list [1])
                    target_pos = ship.output_position (object_list [global_target_object_id ])
                    target_rel_pos = dfunctions.rel_pos (ship.output_position (object_list [1]), target_pos)
                    target_distance = dfunctions.distance (target_rel_pos)
                    target_angle = dfunctions.ftarget_direction (target_rel_pos)
                    turning_angle = dfunctions.normalize_angle (target_angle - 1.57)
                    if pressed [308] == 1  and keydown [13]== 1:
                     
                        for s_x in ship_list:
                            ship_pos = ship.output_position (s_x)
                            ship_rel_pos = dfunctions.rel_pos (player_pos, ship_pos)
                            ship_distance = dfunctions.distance (ship_rel_pos)
                            ship_angle = dfunctions.ftarget_direction (ship_rel_pos)

                            
                              
                            # ship_angle_difference = dfunctions.normalize_angle (ship_angle - turning_angle)
                            # print 'test 840   object id:  ', ship.output_object_id (s_x) , ' ship_angle :  ', ship_angle , ' angle_difference :  ', ship_angle_difference
                            new_ship_angle = dfunctions.normalize_angle (ship_angle - turning_angle)
                            print 'test 840   object id:  ', ship.output_object_id (s_x) , ' ship_angle :  ', ship_angle , ' new_ship_angle :  ', new_ship_angle
                            new_pos = dfunctions.fextrapolate_line (new_ship_angle, player_pos, 0, ship_distance) [1]
                            ship.set_position (s_x , new_pos [0], new_pos [1] )



     
        
        pygame.display.update ( CENTRAL_FIELD )

        if end_game == 1: break
    # pygame.display.quit ()

        
    # print 'test 44000   ',   'display.quit' 
    # pygame.display.quit ()



###############################################################################################################
#####################################               Tkinter Stuff           ###################################
###############################################################################################################

running_outer = 1

while running_outer:

    ##############################################################################################################################################
    #######################################         Start:      Tkinter Stuff      ###############################################################
    ##############################################################################################################################################


    root = Tkinter.Tk ()
    # test_image = Tkinter.PhotoImage (file = "c:/test/p1.gif")
   


    def add_none_to_list (input_list, number):
        working_list = input_list [:]

        none_number = number - len (working_list)
        none_list = []
        for i in range (0,none_number):
            none_list.append (None)

        return working_list + none_list


    def split_into_sublists (input_list, number, **wargs ):
        min_sublists = wargs.get ('min_sublists')
        if min_sublists == None: min_sublists = 0

        
        working_list = input_list [:]

        output_list = []

        while working_list != []:
            new_sublist = [] 

            for i in range (0,number):
                if working_list == []: break 
                new_sublist.append (working_list [0] )
            
                working_list = working_list [1:] 

            output_list.append (new_sublist)

            

        return output_list




    def create_print_functions (x):
        def print_function ():
            print x


        return print_function

    def print_stuff (x):
        print x 






    outer_frame= Tkinter.Frame (root, border = 4, relief = 'ridge', bg = "grey" )
    outer_frame.pack ()
    frame_0_a = None


    def smallframe (root):
        f = Tkinter.Frame (root, border = 3, relief = 'ridge')
        f.pack (side = 'left')
        return f

    def bigframe (root):
        f = Tkinter.Frame (root, border = 10, relief = 'ridge')
        f.pack (side = 'left')
        return f


    head1 = ("Helvetica", 20)
    head2 = ("Helvetica", 15)

    def space ():
        l = Tkinter.Label (left_lower_sub_a, bg = fed_colour )
        l.pack ()



            


    def create_menu_screen_2 (menu_info):
        global frame_0_a

        if frame_0_a != None:
        

            frame_0_a.pack_forget ()
            frame_0_a.destroy ()
            
                
        title_text = menu_info ['title']
        button_list = menu_info ['buttons']
        

        #### title_text,button_list,back_image
        
        frame_0_a = Tkinter.Frame (outer_frame, bg = 'white', relief = 'ridge', width = 800, height = 1000 )
        frame_0_a.pack (side = 'left')
        frame_0_a.pack_propagate (0)

        background = Tkinter.Label (frame_0_a, width = 800, height = 1000)
        background.place (x = 0, y = 0 )

        title = Tkinter.Label (frame_0_a, border = 5, bg = "#44f", relief = 'ridge', text = title_text , font=("Helvetica", 30))
        title.pack (side = 'top', fill = 'x', expand = 0)


        frame_0_d = Tkinter.Frame (frame_0_a, border = 10, bg = "#55f", relief = 'raised')
        frame_0_d.pack (expand = 'y')

        for but in button_list:

            b = Tkinter.Button (frame_0_d, text = but ['text'], justify = 'left', border = 6 ,bg = 'white',  relief = 'raised', compound = 'right', command = but ['command'])
            b.pack (side = 'top', fill = 'both', expand = 1)



    class ship_button (object):
        def __init__ (self, **wargs):

            master_frame = Tkinter.Frame (wargs ['root'], border = 0, relief = 'raised')
            master_frame.pack ()

            command = wargs.get ('command')

            display_command = wargs.get ('display_command') 

            
            ###         B       ship name 
            b = Tkinter.Button (master_frame, text = wargs ['text'].capitalize (), width = 10 )
            b.pack (side = 'left')

            
            ###         C       slave frame + buttons 
            slave_frame = Tkinter.Frame (master_frame)
            slave_frame.pack ()

            select_button = Tkinter.Button (slave_frame, text = 'select', border = 4, relief = 'raised', command = command  )
            select_button.pack (side = 'left')

            display_button = Tkinter.Button (slave_frame, text = 'display', border = 4, relief = 'raised', command = display_command)
            display_button.pack ()


         
    def create_between_missions_menu ():
        global frame_0_a

        # ship_list_list = add_none_to_list (split_into_sublists (ship_list, 10), 2) 
        
        

        if frame_0_a != None:
        

            frame_0_a.pack_forget ()
            frame_0_a.destroy ()

        ###         A           Main Frame + Background 
        frame_0_a = Tkinter.Frame (outer_frame, bg = 'white', relief = 'ridge', width = 800, height = 1000 )
        frame_0_a.pack (side = 'left')
        frame_0_a.pack_propagate (0)

        background = Tkinter.Label (frame_0_a, width = 800, height = 1000)
        background.place (x = 0, y = 0 )

        title = Tkinter.Label (frame_0_a,relief = 'raised', text = 'Pirate Campaign' , border = 10, bg = 'grey',  font=("Helvetica", 30))
        title.pack (side = 'top', fill = 'x')

        speech = Tkinter.Label (frame_0_a, relief = 'raised', border = 5,  text = 'Welcome Rookies! In the time- honored Navy tradition, you will test your skills against pirates: Bad pilots in outdated fighters. Those of you who survive this campaign will get the chance to prove themselves against the enemy.' , bg = 'grey',  font=("Helvetica", 14), wraplength = 400 )
        speech.pack () 


        mission_button = Tkinter.Button (frame_0_a, text = 'Next Mission', border = 10, fg = 'red', font = ("Helvetica", 30), command = lambda: create_briefing_menu ())
        mission_button.pack (side = 'bottom', fill = 'x' )

        menu_frame = bigframe (frame_0_a)
        menu_frame.place (x = 0, y = 300)
        main_menu_button = Tkinter.Button (menu_frame, border = 3, relief = 'ridge', text = 'Back to Main', command = lambda: create_menu_screen_2 (menu_dict ['MAIN_MENU']) )
        main_menu_button.pack (fill = 'x')
        save_game_button = Tkinter.Button (menu_frame, border = 3, relief = 'ridge', text = 'Save Game' )
        save_game_button.pack (fill = 'x')


    def create_briefing_menu ():
        global frame_0_a

        # ship_list_list = add_none_to_list (split_into_sublists (ship_list, 10), 2) 
        
        

        if frame_0_a != None:
        

            frame_0_a.pack_forget ()
            frame_0_a.destroy ()

        try: 
            current_mission = campaign_missions [campaign_state]
        except: current_mission = campaign_missions [1] 

        ###         A           Main Frame + Background 
        frame_0_a = Tkinter.Frame (outer_frame, bg = 'white', relief = 'ridge', width = 800, height = 1000 )
        frame_0_a.pack (side = 'left')
        frame_0_a.pack_propagate (0)

        background = Tkinter.Label (frame_0_a, width = 800, height = 1000)
        background.place (x = 0, y = 0 )

        title = Tkinter.Label (frame_0_a,relief = 'raised', text = 'Briefing' , border = 10, bg = 'grey',  font=("Helvetica", 30))
        title.pack (side = 'top', fill = 'x')

        ###         B           Middle Frame

        middle_frame = Tkinter.Frame (frame_0_a, border = 20, bg = ('blue' if DEBUG_MODE == 'yes' else 'grey'), relief = 'raised' )
        middle_frame.pack (fill = 'both', expand = 1 )

        
        ##              1           Left Subframe
        middle_frame_left = Tkinter.Frame (middle_frame, border = ( 20 if DEBUG_MODE == 'yes' else 0 ), bg = 'black', relief = 'raised' )
        middle_frame_left.pack  (side = 'left', fill = 'both', expand = 1 )

        
        subframe_a = Tkinter.Frame (middle_frame_left, border = 20, bg = ('red' if DEBUG_MODE == 'yes' else 'grey'), relief = 'raised' )
        subframe_a.pack (fill = 'both', expand = 1, side = 'left')
        Tkinter.Message (subframe_a, text = current_mission ['briefing']).pack ()

        # subframe_b = Tkinter.Frame (middle_frame_left, border = 20, bg = 'green', relief = 'raised' )
        # subframe_b.pack (fill = 'both', expand = 1, side = 'left')
        # Tkinter.Button (subframe_b, text = 'briefing token').pack ()


        ##              2           Select Ship Subframe
        goal_frame = Tkinter.Frame (middle_frame, border = 20, bg = ('#f0f' if DEBUG_MODE == 1 else 'grey'), relief = 'raised' )
        goal_frame.pack  (fill = 'both', expand = 1 , side = 'right')
        
        select_ship_frame = Tkinter.Frame (goal_frame, border = 5, bg = 'black', relief = 'ridge')
        select_ship_frame.pack ()
        '''
        available_ship_list = [CHARYBDIS, SALTHI,DEMON, HORNET, MESSERSCHMIDT, RAPTOR, SCIMITAR, PSYCHO, RAPIER,RAPIER_B, SABRE, SHRIKE, SCYLLA, BROADAXE, JALTHI, TALON]
        '''
        available_ship_list = rank_dict [rank] ['ships'] 
        ship_selected = Tkinter.IntVar ()
        global ship_selected 
        ship_selected.set (0) 
        for e, ship in enumerate (available_ship_list):
            r = Tkinter.Radiobutton (select_ship_frame, text = ship ['name'], var = ship_selected, value = e)
            r.pack (fill = 'x')
        

        ###         C           Start Button

        
        def start_command ():
            current_mission ['ships'] [0] [1] = available_ship_list [ship_selected.get ()]
            current_mission ['asteroids'] = [] 
            create_mission (current_mission, 'campaign') 
            
        mission_button = Tkinter.Button (frame_0_a, text = 'Start Mission', border = 10, fg = 'red', font = ("Helvetica", 30), command = lambda: start_command ())
        mission_button.pack (side = 'bottom', fill = 'x' )


        
    def create_debriefing_menu ():
        global frame_0_a
        global start_debriefing_screen
        start_debriefing_screen = 'no' 

        # ship_list_list = add_none_to_list (split_into_sublists (ship_list, 10), 2) 
        
        

        if frame_0_a != None:
        

            frame_0_a.pack_forget ()
            frame_0_a.destroy ()

        try: 
            current_mission = campaign_missions [campaign_state -1] 
        except: pass 
        ###         A           Main Frame + Background 
        frame_0_a = Tkinter.Frame (outer_frame, bg = 'white', relief = 'ridge', width = 800, height = 1000 )
        frame_0_a.pack (side = 'left')
        frame_0_a.pack_propagate (0)

        background = Tkinter.Label (frame_0_a, width = 800, height = 1000)
        background.place (x = 0, y = 0 )

        title = Tkinter.Label (frame_0_a,relief = 'raised', text = 'Debriefing' , border = 10, bg = ("blue" if DEBUG_MODE == 'yes' else "grey"),  font=("Helvetica", 30))
        title.pack (side = 'top', fill = 'x')

        ###         B           Middle Frame

        middle_frame = Tkinter.Frame (frame_0_a, border = 4, bg = ("blue" if DEBUG_MODE == 'yes' else "grey"), relief = 'raised' )
        middle_frame.pack (fill = 'both', expand = 1 )

        
        ##              1           Left Subframe
        middle_frame_left = Tkinter.Frame (middle_frame, border = 4, bg = 'black', relief = 'raised' )
        middle_frame_left.pack  (side = 'left', fill = 'both', expand = 1 )

        #                   a           Debriefing Speech 
        subframe_a = Tkinter.Frame (middle_frame_left, border = 4, bg = ("red" if DEBUG_MODE == 'yes' else "grey"), relief = 'raised' )
        subframe_a.pack (fill = 'both', expand = 0, side = 'left')

        ############################################################
        def check_condition (con):
            if con [0] == 'ships_killed':
                if killed_ships_team2 [0] in con [1]:
                    out = 'yes'
                else: out = 'no'

            elif con [0] == 'goal_id':
                if mission_goal_results.get (con [1] ) == con [2]:
                    out = 'yes'
                else: out = 'no'

            elif con [0] == 'ship_destroyed':
                print 'test 5500  ', con 
                if check_if_list_items_in_at_least_one_element_of_list ([con [1]], mission_event_list) == 'yes':
                    out = 'yes'
                else: out = 'no'

            elif con [0] == 'impossible': out = 'no'

            else:
                print 'test 37788   ', con [0] , '   ', con 
                raise ValueError ('fucked up')
            
            return out
        ######################################################################
        

        ##########################################################################
        def check_condition_list (condition_list):
           
            result_list = []
            for con in condition_list:
               
                result_list.append ( check_condition (con) )

            if 'no' in result_list: out = 'no'
            else: out = 'yes'

            return out 
        ########################################################################
                    
            
        
        #####################################################
        def create_debriefing_text (mission):
          
            debriefing_text = '' 
            debriefing_lines = mission.get ('debriefing')

            for item in debriefing_lines:
                condition_list = item [1]
                if condition_list == []:
                    debriefing_text += item [0]
                else:
                    if check_condition_list (condition_list) == 'yes':
                        debriefing_text += item [0]
                
            return debriefing_text 
        #####################################################       
        

        subframe_b = Tkinter.Frame (middle_frame_left, border = 4, bg = ("green" if DEBUG_MODE == 'yes' else "grey"), relief = 'raised' )
        subframe_b.pack (fill = 'both', expand = 1, side = 'left')
        Tkinter.Message (subframe_b,border = 4,  text = create_debriefing_text (current_mission), relief = 'raised').pack ()


        ##              2           Goal Subframe
        goal_frame = Tkinter.Frame (middle_frame_left, border = 4, bg = ('#f0f' if DEBUG_MODE == 'yes' else 'grey'), relief = 'raised' )
        goal_frame.pack  (fill = 'both', expand = 1 , side = 'right')

        ########################################################################
        def create_goal_label (master, goal_name, success):
            f = Tkinter.Frame (master, border = 3, relief = 'ridge')
            f.pack (fill = 'x')
            Tkinter.Label (f, text = goal_name, border = 3, relief = 'ridge', width = 30).pack (side = 'left', fill = 'x')
            Tkinter.Label (f, border = 3,width = 10,  relief = 'ridge', text = ('Completed' if success == 'yes' else 'Failed' ), fg = ('green' if success == 'yes' else 'red')).pack ()
        #########################################################################
       
        

        
        if running_mission_info.get ('goals') != None:
            for e, g in enumerate (running_mission_info.get ('goals')) :
                goal_acc = 'no'
                if check_if_list_items_in_at_least_one_element_of_list (g.get ('goal_event'), mission_event_list) == 'yes':
                
                    goal_acc = 'yes'
                    for g_2 in running_mission_info.get ('goals') [::-1]:
                        if g_2.get ('super_goal') == g.get ('goal_name') and g_2 not in mission_goal_list: mission_goal_list.insert (e + 1, g_2)   ###   why does the list need to be reversed ? => because the sub_goals are always inserted directly after the super_goal: without inversing, first sub_alpha is inserted after the super goal, then sub_beta is inserted after the super goal- before sub_alpha !
                       
                
                tab_modificator = 0 
                if g.get ('super_goal') != None: tab_modificator = 20

                create_goal_label (goal_frame, g.get ('goal_name'), goal_acc) 
                
                # Tkinter.Label (goal_frame, text = g.get ('goal_name'),bg = ('green' if goal_acc == 'yes' else 'red'), border = 3, relief = 'ridge').pack ()
                
                
            
        #                B          success_level
        success_frame = Tkinter.Frame (goal_frame, border = 4,bg = 'blue', relief = 'raised')
        success_frame.pack ()
        

        ########################################################
        def determine_success_level ():
            print 'test 8890  ', running_mission_info.get ('success_levels') 
            if running_mission_info.get ('success_levels') == None:
                success_level = 'basic'
            else:
                success_levels_results = [] 
                levels_dict = running_mission_info ['success_levels']
                for key, value in levels_dict.iteritems ():
                    if check_condition_list (value) == 'yes': success_levels_results.append (key) 

                if 'failure' in success_levels_results: success_level = 'failure'
                for _l in ['basic', 'bronze', 'silver', 'gold' ]:
                    if _l in success_levels_results: success_level = _l


            print 'test 2100 ', success_level
           

            


            return success_level 
        ########################################################
        success_level = determine_success_level ()
        success_text = 'success level:   ' + success_level
        Tkinter.Label (success_frame, text = success_text ).pack ()
        
        global promotion_points
        global rank 
        promotion_points += promotion_point_matrix [success_level]

        if promotion_points > 0:
            current_rank_level = rank_dict [rank] ['level']
            if len (rank_list) - 1 >= current_rank_level + 1:
                next_rank = rank_list [current_rank_level + 1]
                points_required = rank_dict [next_rank] ['points_required']
                if promotion_points >= points_required:
                    promotion_points -= points_required
                    rank = next_rank
                    promotion_text = 'You have been promoted to   ' + rank 
                    Tkinter.Label (success_frame, text = promotion_text ).pack ()
                    
            
            ###mark
     

        ###         C           Start Button 
        mission_button = Tkinter.Button (frame_0_a, text = 'Back to Lobby', border = 10, fg = 'red', font = ("Helvetica", 30), command = lambda: create_between_missions_menu ())
        mission_button.pack (side = 'bottom', fill = 'x' )




        ########            clean up old mission
        cleanup_old_mission () 


        

    ########################################################################################################
    ############################            End Debriefing Menu             ################################
    ########################################################################################################
    
   


         
    def create_custom_mission_menu ():
        global frame_0_a

      
        
        

        if frame_0_a != None:
        

            frame_0_a.pack_forget ()
            frame_0_a.destroy ()

        ###         A           Main Frame + Background 
        frame_0_a = Tkinter.Frame (outer_frame, bg = 'white', relief = 'ridge', width = 800, height = 1000 )
        frame_0_a.pack (side = 'left')
        # frame_0_a.pack_propagate (0)
        
        if INCLUDE_IMAGES == 'yes':
            background = Tkinter.Label (frame_0_a, width = 800, height = 1000)
            background.place (x = 0, y = 0 )

        
        ###         B           Lower Start Bar

        def start_command ():
            global custom_mission


            player_ship_list = []
            
            for item in custom_mission ['ships']:
                
                if item [0] == 1:
                    if player_ship_list == []:
                        player_ship_list.append (item)
            
                    
            if player_ship_list != []: create_mission (custom_mission, 'custom')
            
            
        start_button = Tkinter.Button (frame_0_a, border = 3, relief = 'ridge' , text = 'start mission', fg = 'red', font=("Helvetica", 30), command = lambda : start_command () )
        start_button.pack (side = 'bottom' , fill = 'x')

        ###         C           Left and Right Frames 

        left_meta_frame = Tkinter.Frame (frame_0_a, border = (8 if DEBUG_MODE == 'yes' else 0), bg = ('blue' if DEBUG_MODE == 'yes' else 'grey'), relief = 'ridge')
        left_meta_frame.pack (side = 'left') # , expand = 1, fill = 'both' )

        ###         D           Right Meta Frame
     

        class constructor___container_right_meta_frame (object):
            def __init__ (self):
                print 'test 80.000 '
                self.frame = Tkinter.Frame (frame_0_a, border = 8, bg = ('yellow' if DEBUG_MODE == 'yes' else 'grey'), relief = 'ridge')
                self.frame.pack (side = 'right', expand = 1, fill = 'both' )
                Tkinter.Button (self.frame, text = 'test' ).pack ()
               
                self.update ()


            def update (self):
                
                head1 = ("Helvetica", 20)
                head2 = ("Helvetica", 15)

                for widget in self.frame.winfo_children ():
                    widget.destroy ()
                    
                results = Tkinter.Button (self.frame, text = 'selected ships', border = 5, relief = 'ridge', font=("Helvetica", 20) ) # font = head1
                results.pack (side = 'top')
               
                for name in ['player', 'wingmen', 'enemy' ]:
                    # spacer (self.frame, colour = 'green') 
                    f = smallframe (self.frame)
                    f.pack (side = 'top', expand = 1, fill = 'x')
                    l = Tkinter.Label (f, text = name, font = head2, border = 3, relief = 'ridge')
                    l.pack (side = 'top', expand = 1, fill = 'x' )

                    for s in custom_mission ['ships']:

                        if (name == 'player' and s [0] == 1 ) or (
                            name == 'wingmen' and s [0] == 0 and s [3] == 0 ) or (
                                name == 'enemy' and s [0] == 0 and s [3] == 1):

                            
                            
                            l = Tkinter.Label (f, text = s [1].get ('name') , border = 3, relief = 'ridge')
                            l.pack (expand = 1, fill = 'x')
                        

  
                

        right_meta_frame_container = constructor___container_right_meta_frame () 
        '''
        right_meta_frame = Tkinter.Frame (frame_0_a, border = 8, bg = 'yellow', relief = 'ridge')
        right_meta_frame.pack (side = 'right', expand = 1, fill = 'both' )
        ''' 

        head1 = ("Helvetica", 20)
        head2 = ("Helvetica", 15)

     

       
        ###         D           Left Top Stuff 

        left_upper_frame = Tkinter.Frame (left_meta_frame, border = 4, bg = ('yellow' if DEBUG_MODE == 'yes' else 'black'), relief = 'ridge' )
        left_upper_frame.pack (side = 'top', fill = 'x', expand = 0)

        title = Tkinter.Label (left_upper_frame,relief = 'ridge', text = 'Custom Mission',  font=("Helvetica", 30))
        title.pack (side = 'top', fill = 'x')

        ##                  1           Player / Wingmen / Enemy

        party_selection_frame = Tkinter.Frame (left_upper_frame, border = 5, relief = 'raised' )
        party_selection_frame.pack (expand = 1, fill = 'x')

        pwe = Tkinter.StringVar ()
        global pwe
        pwe.set ('player')

        for p in ['player', 'enemy', 'wingman']:

            f = Tkinter.Frame (party_selection_frame, border = 3, relief = 'ridge')
            f.pack (side = 'left',expand = 1, fill = 'x') 
            r = Tkinter.Radiobutton (f, text = p, variable = pwe , value = p)
            r.pack (side = 'left',expand = 1, fill = 'x')

        

        ##                  2           Pilot Quality Selector

        pilot_quality_frame = Tkinter.Frame (left_upper_frame, border = 5, relief = 'raised' )
        pilot_quality_frame.pack (expand = 1, fill = 'x')

        quality_selector = Tkinter.StringVar ()
        global quality_selector
        quality_selector.set ('average')

        

        # {'ace': [0,0], 'excellent' : [0.1, 1 ], 'good' : [0.2,3], 'average': [0.4, 4.5], 'poor' : [1, 6] , 'abysmal': [2, 10] , 'test': [2,0]}
       
        quality_keys = PILOT_QUALITY.keys ()
        quality_keys.sort (key = lambda x: PILOT_QUALITY [x] )

        for qual in quality_keys:
            f = Tkinter.Frame (pilot_quality_frame, border = 3, relief = 'ridge')
            f.pack (side = 'left', expand = 1, fill = 'x')
            r = Tkinter.Radiobutton (f, text = qual, variable = quality_selector , value = qual)
            r.pack (side = 'left', expand = 1, fill = 'x')
            
            
        
        

        ###         E           Left lower  Frame 
        left_lower_frame = Tkinter.Frame (left_meta_frame, border = 8, bg = "#07f", relief = 'raised' )
        left_lower_frame.pack ()

        ###         F           Left lower subs A, B, C, D

        fed_colour = 'blue' 
        
        left_lower_sub_a = Tkinter.Frame (left_lower_frame, border = 8, bg = (fed_colour if DEBUG_MODE == 'yes' else 'grey'), relief = 'raised' )
        left_lower_sub_a.pack (side = 'left')

        left_lower_sub_b = Tkinter.Frame (left_lower_frame, border = 8, bg = ('red' if DEBUG_MODE == 'yes' else 'grey'), relief = 'raised' )
        left_lower_sub_b.pack (side = 'left', fill = 'y')

        left_lower_sub_c = Tkinter.Frame (left_lower_frame, border = 8, bg = ('green' if DEBUG_MODE == 'yes' else 'grey'), relief = 'raised')
        left_lower_sub_c.pack (side = 'left', fill = 'y')

        left_lower_sub_d = Tkinter.Frame (left_lower_frame, border = 8, bg = ('#06f' if DEBUG_MODE == 'yes' else 'grey'), relief = 'raised', width = 200)
        left_lower_sub_d.pack (side = 'left', fill = 'y')
        left_lower_sub_d.pack_propagate(False)
        
        


        ###         G           Filling in the ship buttons
        ###########################################################
        def constructor___ship_select_command (ship):
            print 'test 4610   ', ship.get ('name')
            def ship_button_command ():
                
                party = pwe.get ()
                player = 0
                if party == 'player':
                    player = 1
                    position = MIDDLE
                
                if party == 'player' or 'wingman':
                    team = 0
                    if party == 'wingman': position = dfunctions.vadd ( MIDDLE, (0,100 * len (custom_mission ['ships']))) 
                if party == 'enemy':
                    team = 1
                    print 'test 26.100' 
                    position = dfunctions.vadd ( (2000, - 100), (0,100 * len (custom_mission ['ships'])))
                    print 'test 26.200'
                    print 'test 26.300' , position 
                    
                custom_mission ['ships'].append  ( [player, ship, position , team, {'pilot_quality': quality_selector.get ()} ] )
                if party == 'player':
                    pwe.set ('enemy')

                
                right_meta_frame_container.update ()
                # right_meta_frame.update () 

                

            return ship_button_command
        ##########################################################
        def constructor___ship_display_command (ship):
            print 'test 5700    ', ship.get ('name') 
            def ship_display_command ():
                print 'test 6710  ', ship.get ('name')
                
                #       clear the frame
                for w in left_lower_sub_d.winfo_children ():
                    w.destroy ()

                #       Ship Name and Description 
                Tkinter.Label (left_lower_sub_d, text = ship.get ('name').capitalize (), border = 10, width = 28,  font=("Helvetica", 20)).pack ( fill = 'x')
                text = ship.get ('description')
                if text == None: text = 'No description available' 
                l = Tkinter.Label (left_lower_sub_d, text = text , border = 10, wraplength = 180 ).pack ()
                

                #       Shields
                Tkinter.Label (left_lower_sub_d, text = "Shields" , border = 4, width = 28, anchor = 'w', font=("Helvetica", 15)).pack ( fill = 'x')
                for item in zip (ship.get ('sas') [0] , ['Front', 'Side', 'Back', 'Left']) [:-1]:
                    Tkinter.Label (left_lower_sub_d, text = item [1] + ' :  ' + str (item [0]), border = 2, width = 28,  font=("Helvetica", 10), anchor = 'w').pack ( fill = 'x')
                    
                #       Armor
                Tkinter.Label (left_lower_sub_d, text = "Armor" , border = 4, width = 28, anchor = 'w', font=("Helvetica", 15)).pack ( fill = 'x')
                for item in zip (ship.get ('sas') [1] , ['Front', 'Side', 'Back', 'Left']) [:-1]:
                    Tkinter.Label (left_lower_sub_d, text = item [1] + ' :  ' + str (item [0]), border = 2, width = 28,  font=("Helvetica", 10),anchor = 'w').pack ( fill = 'x')
                    
                #       Speed and Turn Rate
                Tkinter.Label (left_lower_sub_d, text = 'Speed' + ' :  ' + str (ship.get ('movement') [0]) , border = 4, width = 28, anchor = 'w', font=("Helvetica", 15)).pack ( fill = 'x')
                Tkinter.Label (left_lower_sub_d, text = 'Turn Rate' + ' :  ' + str (ship.get ('movement') [1]) , border = 4, width = 28, anchor = 'w', font=("Helvetica", 15)).pack ( fill = 'x')

                #       Guns
                Tkinter.Label (left_lower_sub_d, text = 'Guns : ' , border = 4, width = 28, anchor = 'w', font=("Helvetica", 15)).pack ( fill = 'x')
                if ship.get ('guns') != None: 
                    for item in ship.get ('guns'): 
                        Tkinter.Label (left_lower_sub_d, text = item [0] ['name'].capitalize () , border = 0, width = 28, anchor = 'w', font=("Helvetica", 10)).pack ( fill = 'x')

                #       Turrets
                Tkinter.Label (left_lower_sub_d, text = 'Turrets : ' , border = 4, width = 28,anchor = 'w',  font=("Helvetica", 15)).pack ( fill = 'x')
                if ship.get ('turrets') != None:
                    for e, item in enumerate (ship.get ('turrets')):
                        Tkinter.Label (left_lower_sub_d, text = 'Turret ' + str (e +1) , border = 0, width = 28, anchor = 'w', font=("Helvetica", 10)).pack ( fill = 'x')
                        for gun in item.get ('guns'): 
                            Tkinter.Label (left_lower_sub_d, text = gun [0].get ('name') , border = 0, width = 28, anchor = 'w', font=("Helvetica", 10)).pack ( fill = 'x')

                #       Missiles and Torpedos
                Tkinter.Label (left_lower_sub_d, text = 'Missile Launchers : ' + str (ship.get ('missile_launchers')) , border = 4, width = 28, anchor = 'w', font=("Helvetica", 12)).pack ( fill = 'x')
                Tkinter.Label (left_lower_sub_d, text = 'Torpedo Launchers : ' +str (ship.get ('torpedo_launchers')) , border = 4, width = 28, anchor = 'w', font=("Helvetica", 12)).pack ( fill = 'x')
                
                        
                        
                



                #       Finish update 
                left_lower_sub_d.update ()
                
            return ship_display_command 
                


        ##########################################################

        #            1       Federation

        head1 = ("Helvetica", 20)
        head2 = ("Helvetica", 15)

        def generate_spacer (parent):
            def spacer ():
                Tkinter.Label (parent, bg = ('yellow' if DEBUG_MODE == 'yes' else 'grey')).pack ()
            return spacer

        f_spacer = generate_spacer (left_lower_sub_a) 
        
                
        '''
        def space (root):
            l = Tkinter.Label (root, bg = 'yellow' )
            l.pack ()
        '''

        def turn_ship_list_into_buttons (root, ship_list):
           for ship in ship_list:
               ship_button (root = root, text = ship ['name'] ,  border = 3, relief = 'raised',command = constructor___ship_select_command (ship), display_command = constructor___ship_display_command (ship) ) 
           

        
        

        l = Tkinter.Label (left_lower_sub_a,fg = fed_colour,  text = 'Federation Ships', border = 3, relief = 'raised', font= head1)
        l.pack ()

        f_spacer ()

        #           a           Capital ships 

        cap_frame = Tkinter.Frame (left_lower_sub_a, border = 5, relief = 'ridge')
        cap_frame.pack ()

        l = Tkinter.Label (cap_frame, text = 'Capital Ships', border = 3, relief = 'ridge', font=head2 )
        l.pack ()


        turn_ship_list_into_buttons (cap_frame, fed_cap_ships)
        '''
        for ship in fed_cap_ships:
            b = ship_button (root = cap_frame, text = ship ['name'] ,  border = 3, relief = 'raised', command = constructor___ship_select_command (ship) ) 
        '''
        f_spacer()

        #           b           Fighters

        
        fighter_frame = Tkinter.Frame (left_lower_sub_a, border = 5, relief = 'ridge')
        fighter_frame.pack ()

        l = Tkinter.Label (fighter_frame, text = 'Fighters', border = 3, relief = 'raised', font = head2 )
        l.pack ()

        turn_ship_list_into_buttons (fighter_frame, fed_fighters)
        '''
        for ship in fed_fighters:
            b = ship_button (root = fighter_frame, text = ship ['name'],  border = 3, relief = 'raised', command = constructor___ship_select_command (ship), display_command = constructor___ship_display_command (ship))
        '''
        
        f_spacer ()

        #           c           Corvettes 


        corvette_frame = Tkinter.Frame (left_lower_sub_a, border = 5, relief = 'ridge')
        corvette_frame.pack ()

        l = Tkinter.Label (corvette_frame, text = 'Corvettes', border = 3, relief = 'raised', font = head2 )
        l.pack ()

        turn_ship_list_into_buttons (corvette_frame, fed_corvettes)

        f_spacer ()
        
        

        #           d           Civil ships

        civ_frame = Tkinter.Frame (left_lower_sub_a, border = 5, relief = 'ridge')
        civ_frame.pack () 

        l = Tkinter.Label (civ_frame, text = 'Civilian Ships', border = 3, relief = 'raised', font = head2 )
        l.pack ()

        turn_ship_list_into_buttons (civ_frame, fed_civs)
        '''
        for ship in fed_civs:
            b = ship_button (root = civ_frame, text = ship ['name'],  border = 3, relief = 'raised', command = constructor___ship_select_command (ship))
        '''


        #            2       Empire

        empire_colour = 'red'


        l = Tkinter.Label (left_lower_sub_b,fg = empire_colour,  text = 'Empire Ships', border = 3, relief = 'raised', font = head1 )
        l.pack ()
        
        e_spacer = generate_spacer (left_lower_sub_b)
        
        e_spacer ()

        #           a           Capital ships 

        cap_frame = Tkinter.Frame (left_lower_sub_b, border = 5, relief = 'ridge')
        cap_frame.pack ()

        l = Tkinter.Label (cap_frame, text = 'Capital Ships', border = 3, relief = 'ridge', font=head2 )
        l.pack ()

        turn_ship_list_into_buttons (cap_frame, empire_cap_ships)
        '''
        for ship in empire_cap_ships:
            b = ship_button (root = cap_frame, text = ship ['name'],  border = 3, relief = 'raised',command = constructor___ship_select_command (ship))
        '''
        e_spacer ()

        #           b           Fighters

        
        fighter_frame = Tkinter.Frame (left_lower_sub_b, border = 5, relief = 'ridge')
        fighter_frame.pack ()

        l = Tkinter.Label (fighter_frame, text = 'Fighters', border = 3, relief = 'raised', font = head2 )
        l.pack ()

        turn_ship_list_into_buttons (fighter_frame, empire_fighters)
        '''
        for ship in empire_fighters:
            b = ship_button (root = fighter_frame, text = ship ['name'],  border = 3, relief = 'raised',command = constructor___ship_select_command (ship))
        '''
        e_spacer ()


        #           c           Corvettes

        corvette_frame = Tkinter.Frame (left_lower_sub_b, border = 5, relief = 'ridge')
        corvette_frame.pack ()

        l = Tkinter.Label (corvette_frame, text = 'Corvettes', border = 3, relief = 'raised', font = head2)
        l.pack ()

        turn_ship_list_into_buttons (corvette_frame, empire_corvettes)

        e_spacer ()

        #           d           Civil ships

        civ_frame = Tkinter.Frame (left_lower_sub_b, border = 5, relief = 'ridge')
        civ_frame.pack () 

        l = Tkinter.Label (civ_frame, text = 'Civilian Ships', border = 3, relief = 'raised' , font = head2)
        l.pack ()

        turn_ship_list_into_buttons (civ_frame, empire_civs)
        '''
        for ship in empire_civs:
            b = ship_button (root = civ_frame, text = ship ['name'],  border = 3, relief = 'raised',command = constructor___ship_select_command (ship))
        '''




        #           3       Pirate and Neutral

        p_spacer = generate_spacer (left_lower_sub_c) 

        pirate_colour = 'green' 

       

        l = Tkinter.Label (left_lower_sub_c, fg = pirate_colour, text = 'Pirate Ships', border = 3, relief = 'raised', font = head1 )
        l.pack ()

        p_spacer ()


        #           a       Capital ships 

        cap_frame = Tkinter.Frame (left_lower_sub_c, border = 5, relief = 'ridge')
        cap_frame.pack ()

          
        

        l = Tkinter.Label (cap_frame, text = 'Capital Ships', border = 3, relief = 'raised', font = head2 )
        l.pack ()
        turn_ship_list_into_buttons (cap_frame, pirate_cap_ships)
        '''
        for ship in pirate_cap_ships:
            b = ship_button (root = cap_frame, text = ship ['name'],  border = 3, relief = 'raised', command = constructor___ship_select_command (ship))
        '''
        p_spacer ()

        #           b       Fighters

        fighter_frame = Tkinter.Frame (left_lower_sub_c, border = 5, relief = 'ridge')
        fighter_frame.pack ()

        l = Tkinter.Label (fighter_frame, text = 'Fighters', border = 3, relief = 'raised', font = head2 )
        l.pack ()

        turn_ship_list_into_buttons (fighter_frame, pirate_fighters)
        '''
        for ship in pirate_fighters:
            b = ship_button (root = fighter_frame, text = ship ['name'],  border = 3, relief = 'raised',command = constructor___ship_select_command (ship))
        '''
        p_spacer ()

        #           c       Corvettes
        corvette_frame = Tkinter.Frame (left_lower_sub_c, border = 5, relief = 'ridge')
        corvette_frame.pack ()

        l = Tkinter.Label (corvette_frame, text = 'Corvettes', border = 3, relief = 'raised', font = head2 )
        l.pack ()

        turn_ship_list_into_buttons (corvette_frame, pirate_corvettes)

        
        p_spacer ()
        p_spacer ()
        

        neutral_frame = Tkinter.Frame (left_lower_sub_c, border = 5, relief = 'ridge')
        neutral_frame.pack ()

        l = Tkinter.Label (neutral_frame, text = 'All Factions', border = 3, relief = 'raised' , font = head1)
        l.pack ()

        turn_ship_list_into_buttons (neutral_frame, neutral_stuff)
        '''
        for ship in neutral_stuff:
            b = ship_button (root = neutral_frame, text = ship ['name'],  border = 3, relief = 'raised', command = constructor___ship_select_command (ship), display_command = constructor___ship_display_command (ship))
        ''' 



        




        
        # b = ship_button (root = left_lower_sub_b, text = 'dies ist ein Schiff' )
        
        


        ###         E           Right Top Bar 
        '''
        results = Tkinter.Button (right_meta_frame, text = 'selected ships', border = 5, relief = 'ridge', font = head1)
        results.pack (side = 'top')
       
        for name in ['player', 'wingmen', 'enemy' ]:
            spacer (right_meta_frame, colour = 'green') 
            f = smallframe (right_meta_frame)
            f.pack (side = 'top', expand = 1, fill = 'x')
            l = Tkinter.Label (f, text = name, font = head2, border = 3, relief = 'ridge')
            l.pack (side = 'top')

            for s in custom_mission ['ships']:

                if (name == 'player' and s [0] == 1 ) or (
                    name == 'wingmen' and s [0] == 0 and s [3] == 0 ) or (
                        name == 'enemy' and s [0] == 0 and s [3] == 1):

                    
                    
                    l = Tkinter.Label (f, text = s [1].get ('name') , border = 3, relief = 'ridge')
                    l.pack (expand = 1, fill = 'x')
        '''

            
        
    def exit_game ():
        global running
        global end_game
        global running_outer

        running = 0
        end_game = 1
        running_outer = 0
        root.destroy ()
        try:
            pygame.display.quit ()
        except:
            pass 



    menu_dict = {
        'MAIN_MENU': {
            'title': 'Main Menu',
            # 'image' : image_1,
            'buttons': [
                # {'text': 'main_menu' , 'command': lambda : create_menu_screen_2 (menu_dict ['MAIN_MENU']) },
                # {'text': 'tutorial', 'command': lambda : create_menu_screen_2 (menu_dict ['TUTORIAL_MENU']) },
                {'text': 'custom mission', 'command': lambda : create_custom_mission_menu ()},
                # {'text': 'load saved game', 'command': lambda: print_stuff ('placeholder_1') },
                {'text': 'start campaign', 'command': lambda: create_between_missions_menu () },
                {'text': 'Exit Game', 'command': lambda: exit_game () }
                ]
            },
        'TUTORIAL_MENU' : {
            'title': 'Tutorials',
            # 'image' : image_1,
            'buttons': [
                {'text': 'tutorial 1', 'command': lambda: print_stuff ('placeholder_1') },
                {'text' : 'tutorial 2', 'command': lambda: print_stuff ('placeholder_2') },
                {'text': 'main_menu' , 'command': lambda : create_menu_screen_2 (menu_dict ['MAIN_MENU'])  }
                ]
            },
        'BETWEEN_MISSIONS' : {
            'title': 'Tutorials',
            # 'image' : image_1,
            'buttons': [
                {'text': 'Next Mission', 'command': lambda: print_stuff ('placeholder_1') },
                {'text': 'main_menu' , 'command': lambda : create_menu_screen_2 (menu_dict ['MAIN_MENU']) }
                ]
            }
           
    }

    if start_debriefing_screen == 'no':
        create_menu_screen_2 (menu_dict ['MAIN_MENU'] )
    elif start_debriefing_screen == 'yes':
        create_debriefing_menu ()

    else: raise ValueError ('fucked up') 
    root.mainloop ()

    


    
    
    
