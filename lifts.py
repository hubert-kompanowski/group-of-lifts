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
        self.is_moving = False
        self.floors_to_visit = []

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            topleft=(self.x, self.y)
        )

    def move(self):
        if not self.is_moving and len(self.floors_to_visit) > 0:
            closest_floor = min([abs(self.curr_floor - f) for f in self.floors_to_visit])
            self.dest_floor = closest_floor

        self.compute_direction()

        if self.curr_floor != self.dest_floor:
            self.is_moving = True
            if floor_tops[self.dest_floor] != self.rect.top:
                self.rect.move_ip(0, self.direction * 2)
            else:
                self.curr_floor = self.dest_floor
        else:
            if len(self.floors_to_visit) > 0:
                self.floors_to_visit.pop(0)
            if len(self.floors_to_visit) > 0:
                closest_floor = min([abs(self.curr_floor - f) for f in self.floors_to_visit])
                self.dest_floor = closest_floor
            else:
                self.is_moving = False

    def get_possible_floors_in_curr_direction(self):
        pass

    def compute_direction(self):
        if self.curr_floor > self.dest_floor:
            self.direction = 1
        elif self.curr_floor < self.dest_floor:
            self.direction = -1

    def update_color(self):
        if self.is_moving:
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


class LiftsManager:
    def __init__(self):
        self.l_lift = Lift(0, 5, int(7.5 * b), 9 * b)
        self.r_lift = Lift(1, 5, int(10.25 * b), 9 * b)

    def update_dest(self, b_type, i):
        if b_type == 'left_lift':
            self.l_lift.floors_to_visit.append(i)
        if b_type == 'right_lift':
            self.r_lift.floors_to_visit.append(i)

        if b_type == 'buttons_down' or b_type == 'buttons_up':
            if b_type == 'buttons_down':
                i = i+1

            if abs(self.l_lift.curr_floor-i) <= abs(self.r_lift.curr_floor-i):
                self.l_lift.floors_to_visit.append(i)
            else:
                self.r_lift.floors_to_visit.append(i)

    def draw(self, scr):
        self.l_lift.update_color()
        self.r_lift.update_color()
        scr.blit(self.l_lift.surf, self.l_lift.rect)
        scr.blit(self.r_lift.surf, self.r_lift.rect)

    def move(self):
        print(self.l_lift.floors_to_visit, self.r_lift.floors_to_visit)
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

    lifts_manager.move()

    draw_stable(screen)

    lifts_manager.draw(screen)

    pygame.display.flip()
