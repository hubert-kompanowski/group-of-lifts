import time

import pygame

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 1000

c1 = (250, 235, 215)  # beż jasny
c2 = (139, 131, 120)  # szary
c3 = (127, 255, 212)  # turkusowy
c4 = (156, 102, 31)  # brązowy
c5 = (139, 115, 85)
orange = (255, 165, 0)
red = (255, 0, 0)
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
    ],

}

action_buttons = {
    "R_Line": pygame.Rect((int(2.5 * b), 12 * b), (2 * b, 2 * b)),
    "L_Line": pygame.Rect((int(0.5 * b), 12 * b), (2 * b, 2 * b)),
    "R_KG": pygame.Rect((int(2.5 * b), 15 * b), (2 * b, 2 * b)),
    "L_KG": pygame.Rect((int(0.5 * b), 15 * b), (2 * b, 2 * b))
}

emergency_buttons = {
    'emerg_left': pygame.Rect((7 * b, 13 * b), (2 * b, b)),
    'emerg_right': pygame.Rect((10 * b, 13 * b), (2 * b, b)),
}

action_buttons_draw = {
    "R Line": [
        int(2.5 * b), 12 * b, 2 * b, 2 * b,
    ],
    "L Line": [
        int(0.5 * b), 12 * b, 2 * b, 2 * b,
    ],
    "R KG": [
        int(2.5 * b), 15 * b, 2 * b, 2 * b,
    ],
    "L KG": [
        int(0.5 * b), 15 * b, 2 * b, 2 * b,
    ],
}

emergency_buttons_draw = [
    [7 * b, 13 * b, 2 * b, b],
    [10 * b, 13 * b, 2 * b, b],
]


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


def draw_led(scr, name, cords):
    border = 2
    pygame.draw.rect(scr, black, cords)
    x, y, w, h = cords
    pygame.draw.rect(scr, c1, (x + border, y + border, w - 2 * border, h - 2 * border))
    pygame.draw.circle(scr, red, (x + w // 2, y + h // 2), int(0.5 * b - 2))
    scr.blit(my_font.render(name, True, (0, 0, 0)), (x + 8, y + 16))


def draw_action_button(scr, name, cords):
    border = 2
    pygame.draw.rect(scr, black, cords)
    x, y, w, h = cords
    pygame.draw.rect(scr, c1, (x + border, y + border, w - 2 * border, h - 2 * border))
    scr.blit(my_font.render(name, True, (255, 0, 0)), (x + 15, y + 40))


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

    for n, c in action_buttons_draw.items():
        draw_action_button(scr, n, c)

    for c in emergency_buttons_draw:
        draw_button(scr, 'EMERG', c)

    if show_line_led_left:
        draw_led(scr, 'Line', (8 * b, 12 * b, b, b))

    if show_line_led_right:
        draw_led(scr, 'Line', (11 * b, 12 * b, b, b))

    if show_kg_led_left:
        draw_led(scr, 'KG', (7 * b, 12 * b, b, b))

    if show_kg_led_right:
        draw_led(scr, 'KG', (10 * b, 12 * b, b, b))


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
        self.prev_state = 'no_action'

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            topleft=(self.x, self.y)
        )

    def move(self):

        if self.state == "no_active":
            self.compute_direction()
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
            self.compute_direction()
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
                    abs(self.dest_floor - self.curr_floor) and \
                    self.lift_list[self.get_closest(self.curr_floor)] in \
                    self.get_possible_floors_in_curr_direction() and \
                    (
                            (self.direction == -1 and self.lift_list[self.get_closest(self.curr_floor, on_path=True)] < self.dest_floor)
                            or
                            (self.direction == 1 and self.lift_list[self.get_closest(self.curr_floor, on_path=True)] > self.dest_floor)
                    ):
                self.lift_list.append(self.dest_floor)
                i = self.get_closest(self.curr_floor, on_path=True)
                self.dest_floor = self.lift_list.pop(i)
                self.lift_list = unique(self.lift_list)


            if len(self.waiting_lift_list) > 0 and \
                    abs(self.waiting_lift_list[
                            self.get_closest(self.curr_floor, 'waiting_lift_list')] - self.curr_floor) < \
                    abs(self.dest_floor - self.curr_floor) and \
                    self.waiting_lift_list[self.get_closest(self.curr_floor, 'waiting_lift_list')] in \
                    self.get_possible_floors_in_curr_direction() and \
                    (
                            (self.direction == -1 and self.waiting_lift_list[self.get_closest(self.curr_floor, 'waiting_lift_list', on_path=True)] < self.dest_floor)
                            or
                            (self.direction == 1 and self.waiting_lift_list[self.get_closest(self.curr_floor, 'waiting_lift_list', on_path=True)] > self.dest_floor)
                    ):

                self.lift_list.append(self.dest_floor)
                i = self.get_closest(self.curr_floor, 'waiting_lift_list', on_path=True)
                self.dest_floor = self.waiting_lift_list.pop(i)
                self.waiting_lift_list = unique(self.waiting_lift_list)

            # if (self.direction == -1 and floor_tops[self.dest_floor] <= self.rect.top) or \
            #         (self.direction == 1 and floor_tops[self.dest_floor] >= self.rect.top):
            if floor_tops[self.dest_floor] != self.rect.top:
                self.rect.move_ip(0, self.direction * 2)
            else:
                self.curr_floor = self.dest_floor
                self.state = 'break'
                self.wait_till = time.time() + 1

        if self.state == 'broken_line':
            if floor_tops[0] > self.rect.top:
                self.rect.move_ip(0, 2)

    def clear_list(self):
        to_pop = []
        for i, el in enumerate(self.waiting_lift_list):
            if el in self.lift_list:
                to_pop.append(i)
        for i in to_pop:
            self.waiting_lift_list.pop(i)
        self.compute_direction()

    def get_possible_floors_in_curr_direction(self):
        if self.direction == 1:
            return list(range(self.curr_floor, -1, -1))
        elif self.direction == -1:
            return list(range(0, self.curr_floor))

    def get_closest(self, curr, list='lift_list', on_path=False):
        idx, closest = (None, 1000)
        if list == 'lift_list':
            for i, el in enumerate(self.lift_list):
                if abs(el - curr) < abs(closest - curr) and (
                        not on_path or el in self.get_possible_floors_in_curr_direction()):
                    idx, closest = (i, el)
        elif list == 'waiting_lift_list':
            for i, el in enumerate(self.waiting_lift_list):
                if abs(el - curr) < abs(closest - curr) and (
                        not on_path or el in self.get_possible_floors_in_curr_direction()):
                    idx, closest = (i, el)
        return idx

    def compute_direction(self):
        # if self.curr_floor > self.dest_floor:
        if self.rect.top < floor_tops[self.dest_floor]:
            self.direction = 1
        # elif self.curr_floor < self.dest_floor:
        elif self.rect.top > floor_tops[self.dest_floor]:

            self.direction = -1
        # else:
        #     raise Exception()

    def update_color(self):
        if self.state in ['no_active', 'break']:
            self.color = yellow
            self.surf.fill(self.color)
        elif self.state == "emergency":
            self.color = red
            if int(time.time() * 10) % 3 == 0:
                self.surf.fill(red)
            else:
                self.surf.fill(yellow)
        elif self.state == 'broken_line':
            self.color = black
            self.surf.fill(self.color)
        elif self.state == 'overload':
            self.color = orange
            self.surf.fill(self.color)
        else:
            self.color = turkus
            self.surf.fill(self.color)

    def emergency(self):
        if self.state != 'broken_line':
            if self.state != 'emergency':
                self.prev_state = self.state
                self.state = 'emergency'
            else:
                self.state = self.prev_state

    def overload(self):
        if self.state != 'broken_line':
            if self.state != 'overload':
                self.prev_state = self.state
                self.state = 'overload'
            else:
                self.state = self.prev_state

    def break_line(self):
        self.state = 'broken_line'


def button_read_action(pos):
    for btn_type, btns in buttons.items():
        for idx, btn in enumerate(btns):
            if btn.collidepoint(pos):
                return btn_type, idx
    return None, None


def button_read_action_action(pos):
    for btn_type, btn in action_buttons.items():
        if btn.collidepoint(pos):
            return btn_type
    return None


def button_read_action_emerg(pos):
    for btn_type, btn in emergency_buttons.items():
        if btn.collidepoint(pos):
            return btn_type
    return None


def xor(a, b):
    return (a and not b) or (not a and b)


class LiftsManager:
    def __init__(self):
        self.l_lift = Lift(0, 5, int(7.5 * b), 9 * b)
        self.r_lift = Lift(1, 5, int(10.25 * b), 9 * b)
        self.main_list = []
        self.waiting_list = []

    def update_dest(self, b_type, i):
        if b_type == 'left_lift' and self.l_lift.state != 'emergency':
            if i not in self.l_lift.lift_list and i not in self.l_lift.waiting_lift_list:
                if i in self.l_lift.get_possible_floors_in_curr_direction():
                    self.l_lift.lift_list.append(i)
                    self.l_lift.lift_list = unique(self.l_lift.lift_list)
                else:
                    self.l_lift.waiting_lift_list.append(i)
                    self.l_lift.lift_list = unique(self.l_lift.lift_list)
            else:
                return

        if b_type == 'right_lift' and self.r_lift.state != 'emergency':
            if i not in self.r_lift.lift_list and i not in self.r_lift.waiting_lift_list:
                if i in self.r_lift.get_possible_floors_in_curr_direction():
                    self.r_lift.lift_list.append(i)
                    self.r_lift.lift_list = unique(self.r_lift.lift_list)
                else:
                    self.r_lift.waiting_lift_list.append(i)
                    self.r_lift.lift_list = unique(self.r_lift.lift_list)
            else:
                return

        if b_type == 'buttons_down' or b_type == 'buttons_up':
            if b_type == 'buttons_down':
                i = i + 1

            self.main_list.append(i)
        self.l_lift.lift_list = unique(self.l_lift.lift_list)
        self.l_lift.waiting_lift_list = unique(self.l_lift.waiting_lift_list)
        self.r_lift.lift_list = unique(self.r_lift.lift_list)
        self.r_lift.waiting_lift_list = unique(self.r_lift.waiting_lift_list)
        self.main_list = unique(self.main_list)
        self.waiting_list = unique(self.waiting_list)
        self.l_lift.clear_list()
        self.r_lift.clear_list()

    def update(self):
        self.l_lift.clear_list()
        self.r_lift.clear_list()
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
                        self.l_lift.waiting_lift_list.append(el)  # może do waiting?
                        to_del_id.append(idx)
                        break
                    elif self.r_lift.state != 'no_active' and el in self.r_lift.get_possible_floors_in_curr_direction():
                        self.r_lift.waiting_lift_list.append(el)  # może do waiting?
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


show_line_led_left = False
show_kg_led_left = False
show_line_led_right = False
show_kg_led_right = False

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

            btn_type = button_read_action_action(position)
            if btn_type is not None:
                if btn_type == 'L_Line':
                    lifts_manager.l_lift.break_line()
                    show_line_led_left = True
                if btn_type == 'R_Line':
                    lifts_manager.r_lift.break_line()
                    show_line_led_right = True
                if btn_type == 'L_KG':
                    if lifts_manager.l_lift.state in ['break', 'no_active', 'overload']:
                        lifts_manager.l_lift.overload()
                        show_kg_led_left = not show_kg_led_left
                if btn_type == 'R_KG':
                    if lifts_manager.r_lift.state in ['break', 'no_active', 'overload']:
                        lifts_manager.r_lift.overload()
                        show_kg_led_right = not show_kg_led_right

            btn_type = button_read_action_emerg(position)
            if btn_type is not None:
                if btn_type == 'emerg_left':
                    lifts_manager.l_lift.emergency()
                if btn_type == 'emerg_right':
                    lifts_manager.r_lift.emergency()

    lifts_manager.update()
    lifts_manager.move()

    draw_stable(screen)

    lifts_manager.draw(screen)

    pygame.display.flip()
