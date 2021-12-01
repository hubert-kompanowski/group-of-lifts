import time

import pygame

from pygame.locals import (
    K_KP0,
    K_KP1,
    K_KP2,
    K_KP3,
    K_KP4,
)

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 1000

c1 = (250, 235, 215)  # beż jasny
c2 = (139, 131, 120)  # szary
c3 = (127, 255, 212)  # turkusowy
c4 = (156, 102, 31)  # brązowy
c5 = (139, 115, 85)
white = (255, 255, 255)
black = (0, 0, 0)
turkus = (122, 197, 205)
yellow = (255, 215, 0)
b = 48

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

up_down_plates = [
    (int(0.5 * b), b + 2 * b * x, 3 * b, int(1.5 * b))
    for x in range(5)
]

doors = [
    ((int(7.5 * b), b + 2 * b * x, int(1.25 * b), int(1.5 * b)),
     (int(10.25 * b), b + 2 * b * x, int(1.25 * b), int(1.5 * b)))
    for x in range(5)
]

building = (int(5.5 * b), int(0.5 * b), 8 * b, 10 * b)

separators = [
    (int(5.5 * b), int(0.5 * b + 2 * b * x), 8 * b, int(0.25 * b))
    for x in range(6)
]
separators += [
    (int(5.5 * b), int(0.5 * b), int(0.25 * b), 10 * b),
    (int(13.25 * b), int(0.5 * b), int(0.25 * b), 10 * b)
]

triangles_down = [
    ((int(0.75 * b), int(1.25 * b + 2 * b * x)),
     (int(1.75 * b), int(1.25 * b + 2 * b * x)),
     (int(1.25 * b), int(2.25 * b + 2 * b * x)))
    for x in range(4)
]

triangles_up = [
    ((int(2.25 * b), int(2.25 * b + 2 * b * x)),
     (int(2.75 * b), int(1.25 * b + 2 * b * x)),
     (int(3.25 * b), int(2.25 * b + 2 * b * x)))
    for x in range(1, 5)
]

buttons_down = [
    (int(0.5 * b), b + 2 * b * x, int(1.5 * b), int(1.5 * b))
    for x in range(4)
]

buttons_up = [
    (int(2 * b), b + 2 * b * x, int(1.5 * b), int(1.5 * b))
    for x in range(1, 5)
]

lift_plates = [
    (7 * b, 12 * b, 2 * b, 5 * b),
    (10 * b, 12 * b, 2 * b, 5 * b),
]

left_lift_buttons = {
    0: (7 * b, 16 * b, b, b),
    1: (8 * b, 15 * b, b, b),
    2: (7 * b, 15 * b, b, b),
    3: (8 * b, 14 * b, b, b),
    4: (7 * b, 14 * b, b, b)
}

right_lift_buttons = {
    0: (10 * b, 16 * b, b, b),
    1: (11 * b, 15 * b, b, b),
    2: (10 * b, 15 * b, b, b),
    3: (11 * b, 14 * b, b, b),
    4: (10 * b, 14 * b, b, b)
}

floor_tops = {
    0: 9 * b,
    1: 7 * b,
    2: 5 * b,
    3: 3 * b,
    4: b
}

buttons = {
    "buttons_down": [
        pygame.Rect(left_top, (w, h))
        for *left_top, w, h in reversed(buttons_down)
    ],
    "buttons_up": [
        pygame.Rect(left_top, (w, h))
        for *left_top, w, h in reversed(buttons_up)
    ],
    "left_lift": [
        pygame.Rect(left_top, (w, h))
        for *left_top, w, h in left_lift_buttons.values()
    ],
    "right_lift": [
        pygame.Rect(left_top, (w, h))
        for *left_top, w, h in right_lift_buttons.values()
    ]
}


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def draw_button(scr, name, cords):
    border = 2
    pygame.draw.rect(scr, black, cords)
    x, y, w, h = cords
    pygame.draw.rect(scr, c1, (x + border, y + border, w - 2 * border, h - 2 * border))
    scr.blit(my_font.render(name, True, (255, 0, 0)), (x + 18, y + 16))


def draw_stable(scr):
    scr.fill(white)
    
    pygame.draw.rect(scr, c5, building)
    
    for left, right in doors:
        pygame.draw.rect(scr, c1, left)
        pygame.draw.rect(scr, c1, right)
    
    for s in separators:
        pygame.draw.rect(scr, black, s)
    
    for cords in up_down_plates:
        pygame.draw.rect(scr, c2, cords)
    
    for t in triangles_down:
        pygame.draw.polygon(scr, c1, t)
    
    for t in triangles_up:
        pygame.draw.polygon(scr, c1, t)
    
    for l in lift_plates:
        pygame.draw.rect(scr, c2, l)
    
    for f, x in left_lift_buttons.items():
        draw_button(scr, str(f), x)
    
    for f, x in right_lift_buttons.items():
        draw_button(scr, str(f), x)


class Lift(pygame.sprite.Sprite):
    def __init__(self, index, floors, init_x, init_y):
        super(Lift, self).__init__()
        
        self.state = "no_active"
        self.index = index
        self.floors = floors
        self.x = init_x
        self.y = init_y
        self.color = turkus
        self.width = int(1.25 * b)
        self.height = int(1.5 * b)
        self.curr_floor = 0
        self.direction = -1  # -1 up 1 down
        self.dest_floor = 0
        
        self.lift_list = []
        self.waiting_lift_list = []
        self.wait_till = 0
        
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            topleft=(self.x, self.y)
        )
    
    def move(self):
        if self.state == "no_active":
            if self.curr_floor == self.dest_floor and len(self.lift_list) > 0:
                i = self.get_closest(self.curr_floor)
                self.dest_floor = self.lift_list.pop(i)
                self.compute_direction()
                self.state = "going"
            
            elif self.curr_floor != self.dest_floor:
                self.compute_direction()
                self.state = "going"
                
            elif len(self.lift_list) == 0 and len(self.waiting_lift_list) > 0:
                self.lift_list.append(self.waiting_lift_list.pop(0))
        
        if self.state == 'break':
            if time.time() >= self.wait_till:
                if len(self.lift_list) > 0:
                    i = self.get_closest(self.curr_floor)
                    self.dest_floor = self.lift_list.pop(i)
                    self.compute_direction()
                    self.state = "going"
                else:
                    self.state = 'no_active'
        
        if self.state == "going":
            if len(self.lift_list) > 0 and \
                    abs(self.lift_list[self.get_closest(self.curr_floor)] - self.curr_floor) < \
                    abs(self.dest_floor - self.curr_floor):
                self.lift_list.append(self.dest_floor)
                i = self.get_closest(self.curr_floor)
                self.dest_floor = self.lift_list.pop(i)
            elif floor_tops[self.dest_floor] != self.rect.top:
                self.rect.move_ip(0, self.direction * 2)
            else:
                self.curr_floor = self.dest_floor
                self.state = 'break'
                self.wait_till = time.time() + 1
        
        ###########333
        # if not self.is_moving and len(self.floors_to_visit) > 0:
        #     closest_floor = min([abs(self.curr_floor - f) for f in self.floors_to_visit])
        #     self.dest_floor = closest_floor
        #
        # self.compute_direction()
        #
        # if self.curr_floor != self.dest_floor:
        #     self.is_moving = True
        #     if floor_tops[self.dest_floor] != self.rect.top:
        #         self.rect.move_ip(0, self.direction * 2)
        #     else:
        #         self.curr_floor = self.dest_floor
        # else:
        #     if len(self.floors_to_visit) > 0:
        #         self.floors_to_visit.pop(0)
        #     if len(self.floors_to_visit) > 0:
        #         closest_floor = min([abs(self.curr_floor - f) for f in self.floors_to_visit])
        #         self.dest_floor = closest_floor
        #     else:
        #         self.is_moving = False
    
    def get_possible_floors_in_curr_direction(self):
        if self.direction == 1:
            return list(range(self.curr_floor, 0, -1))
        elif self.direction == -1:
            return list(range(0, self.curr_floor))
    
    def get_closest(self, curr):
        i, closest = (None, 1000)
        for i, el in enumerate(self.lift_list):
            if abs(el - curr) < abs(closest - curr):
                i, closest = (i, el)
        return i
    
    def compute_direction(self):
        if self.curr_floor > self.dest_floor:
            self.direction = 1
        elif self.curr_floor < self.dest_floor:
            self.direction = -1
    
    def update_color(self):
        if self.state != 'no_active':
            self.color = turkus
            self.surf.fill(self.color)
        else:
            self.color = yellow
            self.surf.fill(self.color)


def button_read_action(pos):
    for btn_type, btns in buttons.items():
        for idx, btn in enumerate(btns):
            if btn.collidepoint(pos):
                return btn_type, idx
    return None, None


def xor(a, b):
    return (a and not b) or (not a and b)


class LiftsManager:
    def __init__(self):
        self.l_lift = Lift(0, 5, int(7.5 * b), 9 * b)
        self.r_lift = Lift(1, 5, int(10.25 * b), 9 * b)
        self.main_list = []
        self.waiting_list = []
    
    def update_dest(self, b_type, i):
        if b_type == 'left_lift':
            if i in self.l_lift.get_possible_floors_in_curr_direction():
                self.l_lift.lift_list.append(i)
                self.l_lift.lift_list = unique(self.l_lift.lift_list)
            else:
                self.l_lift.waiting_lift_list.append(i)
                self.l_lift.lift_list = unique(self.l_lift.lift_list)
        
        if b_type == 'right_lift':
            if i in self.r_lift.get_possible_floors_in_curr_direction():
                self.r_lift.lift_list.append(i)
                self.r_lift.lift_list = unique(self.r_lift.lift_list)
            else:
                self.r_lift.waiting_lift_list.append(i)
                self.r_lift.lift_list = unique(self.r_lift.lift_list)
        
        if b_type == 'buttons_down' or b_type == 'buttons_up':
            if b_type == 'buttons_down':
                i = i + 1
            
            self.main_list.append(i)
    
    def update(self):
        if len(self.main_list) > 0 or len(self.waiting_list) > 0:
            self.main_list = unique(self.main_list)
            self.waiting_list = unique(self.waiting_list)
            
            to_del_id = []
            for idx, el in enumerate(self.waiting_list):
                if self.l_lift.state == 'no_active' and self.r_lift.state == 'no_active':
                    dist_left = abs(self.l_lift.curr_floor - el)
                    dist_right = abs(self.r_lift.curr_floor - el)
                    if dist_left < dist_right:
                        self.l_lift.lift_list.append(el)
                        to_del_id.append(idx)
                        break
                    else:
                        self.r_lift.lift_list.append(el)
                        to_del_id.append(idx)
                        break
                
                elif xor(self.l_lift.state != 'no_active', self.r_lift.state != 'no_active'):
                    if self.l_lift.state == 'brake' and self.l_lift.curr_floor == el or \
                            self.r_lift.state == 'brake' and self.r_lift.curr_floor == el:
                        to_del_id.append(idx)
                        break
                    elif self.l_lift.state != 'no_active' and el in self.l_lift.get_possible_floors_in_curr_direction():
                        self.l_lift.lift_list.append(el)
                        to_del_id.append(idx)
                        break
                    elif self.r_lift.state != 'no_active' and el in self.r_lift.get_possible_floors_in_curr_direction():
                        self.r_lift.lift_list.append(el)
                        to_del_id.append(idx)
                        break
                    elif self.l_lift.state == 'no_active':
                        self.l_lift.lift_list.append(el)
                        to_del_id.append(idx)
                        break
                    elif self.r_lift.state == 'no_active':
                        self.r_lift.lift_list.append(el)
                        to_del_id.append(idx)
                        break
                
                elif self.l_lift.state != 'no_active' and self.r_lift.state != 'no_active':
                    if self.l_lift.state == 'brake' and self.l_lift.curr_floor == el or \
                            self.r_lift.state == 'brake' and self.r_lift.curr_floor == el:
                        to_del_id.append(idx)
                        break
                    
                    elif self.l_lift.state != 'no_active' and el in self.l_lift.get_possible_floors_in_curr_direction() and \
                            self.r_lift.state != 'no_active' and el in self.r_lift.get_possible_floors_in_curr_direction():
                        dist_left = abs(self.l_lift.curr_floor - el)
                        dist_right = abs(self.r_lift.curr_floor - el)
                        if dist_left < dist_right:
                            self.l_lift.lift_list.append(el)
                            to_del_id.append(idx)
                            break
                        else:
                            self.r_lift.lift_list.append(el)
                            to_del_id.append(idx)
                            break
                    elif self.l_lift.state != 'no_active' and el in self.l_lift.get_possible_floors_in_curr_direction():
                        self.r_lift.lift_list.append(el)
                        to_del_id.append(idx)
                        break
                    elif self.r_lift.state != 'no_active' and el in self.r_lift.get_possible_floors_in_curr_direction():
                        self.r_lift.lift_list.append(el)
                        to_del_id.append(idx)
                        break
            for i in to_del_id:
                self.waiting_list.pop(i)

            if len(self.main_list) > 0:
                el = self.main_list.pop(0)
                to_del = None
                
                if self.l_lift.state != 'no_active' and self.r_lift.state != 'no_active':
                    dist_left = abs(self.l_lift.curr_floor - el)
                    dist_right = abs(self.r_lift.curr_floor - el)
                    if dist_left < dist_right:
                        self.l_lift.lift_list.append(el)
                        to_del = el
                    else:
                        self.r_lift.lift_list.append(el)
                        to_del = el
                
                elif xor(self.l_lift.state != 'no_active', self.r_lift.state != 'no_active'):
                    if self.l_lift.state == 'brake' and self.l_lift.curr_floor == el or \
                            self.r_lift.state == 'brake' and self.r_lift.curr_floor == el:
                        to_del = el
                    elif self.l_lift.state != 'no_active' and el in self.l_lift.get_possible_floors_in_curr_direction():
                        self.l_lift.lift_list.append(el)
                        to_del = el
                    elif self.r_lift.state != 'no_active' and el in self.r_lift.get_possible_floors_in_curr_direction():
                        self.r_lift.lift_list.append(el)
                        to_del = el
                    elif self.l_lift.state == 'no_active':
                        self.l_lift.lift_list.append(el)
                        to_del = el
                    elif self.r_lift.state == 'no_active':
                        self.r_lift.lift_list.append(el)
                        to_del = el
                
                elif self.l_lift.state != 'no_active' and self.r_lift.state != 'no_active':
                    if self.l_lift.state == 'brake' and self.l_lift.curr_floor == el or \
                            self.r_lift.state == 'brake' and self.r_lift.curr_floor == el:
                        to_del = el
                    
                    elif self.l_lift.state != 'no_active' and el in self.l_lift.get_possible_floors_in_curr_direction() and \
                            self.r_lift.state != 'no_active' and el in self.r_lift.get_possible_floors_in_curr_direction():
                        dist_left = abs(self.l_lift.curr_floor - el)
                        dist_right = abs(self.r_lift.curr_floor - el)
                        if dist_left < dist_right:
                            self.l_lift.lift_list.append(el)
                            to_del = el
                        else:
                            self.r_lift.lift_list.append(el)
                            to_del = el
                    elif self.l_lift.state != 'no_active' and el in self.l_lift.get_possible_floors_in_curr_direction():
                        self.r_lift.lift_list.append(el)
                        to_del = el
                    elif self.r_lift.state != 'no_active' and el in self.r_lift.get_possible_floors_in_curr_direction():
                        self.r_lift.lift_list.append(el)
                        to_del = el
                if to_del is not None:
                    del to_del
                else:
                    self.waiting_list.append(el)
        
        self.l_lift.lift_list = unique(self.l_lift.lift_list)
        self.r_lift.lift_list = unique(self.r_lift.lift_list)
    
    def draw(self, scr):
        self.l_lift.update_color()
        self.r_lift.update_color()
        scr.blit(self.l_lift.surf, self.l_lift.rect)
        scr.blit(self.r_lift.surf, self.r_lift.rect)
    
    def move(self):
        self.l_lift.move()
        self.r_lift.move()


lifts_manager = LiftsManager()
pos = (0, 0)
run = True
while run:
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos()
            btn_type, idx = button_read_action(position)
            if btn_type is not None:
                lifts_manager.update_dest(btn_type, idx)
    
    lifts_manager.update()
    lifts_manager.move()
    
    draw_stable(screen)
    
    lifts_manager.draw(screen)
    # print(lifts_manager.main_list, lifts_manager.l_lift.lift_list, lifts_manager.r_lift.lift_list)
    # print(lifts_manager.waiting_list, lifts_manager.l_lift.waiting_lift_list, lifts_manager.r_lift.waiting_lift_list)
    # print(lifts_manager.l_lift.state, lifts_manager.r_lift.state)
    pygame.display.flip()
