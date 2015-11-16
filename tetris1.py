# from random import randint
import random
import pygame
import sys
from queue import Queue
from pygame.locals import *


class Mino:
#    queue = Queue(8)
    next1 = [] #  ネクストブロック7種を入れる
    next2 = [] #  ネクストブロック7種を入れる

    hold1 = [] #  ホールド時にhold2の内容を移す
    hold2 = [] #  落下中のminoのパターンを入れておく

    fix_time = 3

    def __init__(self, process):
        self.create()
        if process == 'drop':
            self.pattern = Mino.next1.pop(0)
            Mino.next1.append(Mino.next2.pop(0)) #  next2からnext1へブロック１つを移す
        elif process == 'hold':
            self.pattern = Mino.hold1
        self.loc = [6, 0]  # mino配列のfield配列内での位置を表す[x, y]
        self.state = [0, 0]  # [今の状態, 移行したい状態]
        self.fix_time = Mino.fix_time

    def create(self):
        if len(Mino.next1) == 0:
            #next1 next2ともに空なので両方にappend
            index_list = [1, 2, 3, 4, 5, 6, 7]
            random.shuffle(index_list)
            for i in index_list:
                pattern = self.pattern_create(i)
                Mino.next1.append(pattern)
            index_list = [1, 2, 3, 4, 5, 6, 7]
            random.shuffle(index_list)
            for i in index_list:
                pattern = self.pattern_create(i)
                Mino.next2.append(pattern)
        elif len(Mino.next2) == 0:
            #next2が空なのでnext2にappend
            index_list = [1, 2, 3, 4, 5, 6, 7]
            for i in index_list:
                pattern = self.pattern_create(i)
                Mino.next2.append(pattern)

    def pattern_create(self, index):
        if index == 1:  # I
            return ([[0, 0, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0], ])
        if index == 2:  # O
            return ([[2, 2],
                     [2, 2], ])
        if index == 3:  # S
            return ([[0, 3, 3],
                     [3, 3, 0],
                     [0, 0, 0], ])
        if index == 4:  # Z
            return ([[4, 4, 0],
                     [0, 4, 4],
                     [0, 0, 0], ])
        if index == 5:  # J
            return ([[5, 0, 0],
                     [5, 5, 5],
                     [0, 0, 0], ])
        if index == 6:  # 2
            return ([[0, 0, 6],
                     [6, 6, 6],
                     [0, 0, 0], ])
        if index == 7:  # T
            return ([[0, 7, 0],
                     [7, 7, 7],
                     [0, 0, 0], ])

    def rotate(self, direct):
        pattern_len = len(self.pattern)
        pattern_copy = [[0 for col in range(pattern_len)] for row in range(pattern_len)]
        if direct == 'left':
            for y in range(pattern_len):
                for x in range(pattern_len):
                    pattern_copy[pattern_len - 1 - x][y] = self.pattern[y][x]
            self.state[1] -= 1
            self.state[1] %= 4
        if direct == 'right':
            for y in range(pattern_len):
                for x in range(pattern_len):
                    pattern_copy[x][pattern_len - 1 - y] = self.pattern[y][x]
            self.state[1] += 1
            self.state[1] %= 4
        for y in range(pattern_len):
            for x in range(pattern_len):
                self.pattern[y][x] = pattern_copy[y][x]

    def control(self, direct):
        if direct == 'left':
            self.loc[0] -= 1
        if direct == 'right':
            self.loc[0] += 1
        if direct == 'down':
            self.loc[1] += 1

    def held_already(self):
        for y in self.pattern:
            for x in y:
                if x != 0:
                    mino_index = x
                    break
        if Mino.hold2:
            Mino.hold1 = Mino.hold2
            pattern = self.pattern_create(mino_index)
            Mino.hold2 = pattern
            return True
        else:
            pattern = self.pattern_create(mino_index)
            Mino.hold2 = pattern
            return False

    def fix_check(self, process):
        if process == 'count':
            self.fix_time -= 1
        if process == 'reset':
            self.fix_time = Mino.fix_time
        if self.fix_time == 0:
            return True
        elif self.fix_time == 0:
            return False


class Window:
    _field = [
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99], ]

    _field_height = 25
    _field_width = 16

    def __init__(self):
        self.load_image()
        self.shift_loc = [0, 0]  # 壁蹴り時のシフト幅[x, y]
        self.lines = []

    def mapping(self, mino, process):
        field_x = mino.loc[0]
        field_y = mino.loc[1]
        pattern_len = len(mino.pattern)
        end_x = field_x + pattern_len
        end_y = field_y + pattern_len

        if process == 'line_clear':
            for y in self.lines:
                del Window._field[y]
            for y in self.lines:
                Window._field.insert(2, [99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99])
            return 0

        for y in range(field_y, end_y):
            for x in range(field_x, end_x):
                pattern_x = x - field_x
                pattern_y = y - field_y
                code = mino.pattern[pattern_y][pattern_x]  # patternリストの中を左上から右に向かって走査
                if code:
                    if process == 'drop':
                        Window._field[y][x] = code
                    elif process == 'clear':
                        Window._field[y][x] = 0
                    elif process == 'fix':
                        Window._field[y][x] = code + 10


    def draw(self, screen):
        screen.fill((0, 0, 0))

        # field描画用
        for y in range(2, Window._field_height - 2):
            for x in range(2, Window._field_width - 2):
                code = Window._field[y][x]
                self.blit_img(code, x, y, 72, 24)

        # next描画用
        nexts_len = len(Mino.next1)
        for z in range(nexts_len):
            next_len = len(Mino.next1[z])
            for y in range(next_len):
                for x in range(next_len):
                    if Mino.next1[z][y][x]:
                        code = Mino.next1[z][y][x]
                        self.blit_img(code, x, y, 450, 24+80*z)

        # hold描画用
        for y in range(len(Mino.hold2)):
            for x in range(len(Mino.hold2)):
                if Mino.hold2[y][x]:
                    code = Mino.hold2[y][x]
                    self.blit_img(code, x, y, 24, 24)

#        # line_clear描画用
#        if self.lines:
#            for y in self.lines:
#                for x in range(2, Window._field_width - 2):
#    #                code = Window._field[y][x]
#                    code = 0
#                    self.blit_img(code, x, y, 72, 24)

    def blit_img(self, code, x, y, left_margin, bottom_margin):
        block_size = 24
        if code == 99:
            screen.blit(self.block_img[7], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 1 or code == 11 or code == -1:
            screen.blit(self.block_img[0], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 2 or code == 12 or code == -2:
            screen.blit(self.block_img[1], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 3 or code == 13 or code == -3:
            screen.blit(self.block_img[2], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 4 or code == 14 or code == -4:
            screen.blit(self.block_img[3], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 5 or code == 15 or code == -5:
            screen.blit(self.block_img[4], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 6 or code == 16 or code == -6:
            screen.blit(self.block_img[5], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 7 or code == 17 or code == -7:
            screen.blit(self.block_img[6], (left_margin + x * block_size, bottom_margin + y * block_size))
#        elif code == 0:
#            screen.blit(self.block_img[8], (left_margin + x * block_size, bottom_margin + y * block_size))

    def load_image(self):
        self.block_img = []
        self.block_img.append(pygame.image.load('data/i.bmp'))
        self.block_img.append(pygame.image.load('data/o.bmp'))
        self.block_img.append(pygame.image.load('data/s.bmp'))
        self.block_img.append(pygame.image.load('data/z.bmp'))
        self.block_img.append(pygame.image.load('data/j.bmp'))
        self.block_img.append(pygame.image.load('data/l.bmp'))
        self.block_img.append(pygame.image.load('data/t.bmp'))
        self.block_img.append(pygame.image.load('data/w.bmp'))
        self.block_img.append(pygame.image.load('data/c.bmp'))

    def left_hit(self, mino):
        pattern_len = len(mino.pattern)
        for x in range(pattern_len):
            for y in range(pattern_len):
                if mino.pattern[y][x]:
                    field_x = mino.loc[0] + x
                    field_y = mino.loc[1] + y
                    if Window._field[field_y][field_x - 1] > 10:
                        return True
        return False

    def right_hit(self, mino):
        pattern_len = len(mino.pattern)
        for x in range(pattern_len - 1, -1, -1):
            for y in range(pattern_len):
                if mino.pattern[y][x]:
                    field_x = mino.loc[0] + x
                    field_y = mino.loc[1] + y
                    if Window._field[field_y][field_x + 1] > 10:
                        return True
        return False

    def bottom_hit(self, mino, process):
        pattern_len = len(mino.pattern)

        if process == 'drop':
            for y in range(pattern_len - 1, -1, -1):
                for x in range(pattern_len):
                    if mino.pattern[y][x]:
                        field_x = mino.loc[0] + x
                        field_y = mino.loc[1] + y
                        if Window._field[field_y + 1][field_x] > 10:
                            return True
            return False

    def rotate_hit(self, mino):
        pattern_len = len(mino.pattern)
        collision_list = []
        shift_list = []

        if pattern_len == 4:  # Iミノ用
            # 右回転
            if mino.state == [0, 1]:
                shift_list = [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]]
            if mino.state == [1, 2]:
                shift_list = [[0, 0], [-1, 0], [2, 1], [-1, -2], [2, -1]]
            if mino.state == [2, 3]:
                shift_list = [[0, 0], [2, 0], [-1, 0], [2, -1], [-1, 2]]
            if mino.state == [3, 0]:
                shift_list = [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]]
            # 左回転
            if mino.state == [0, 3]:
                shift_list = [[0, 0], [-1, 0], [2, 0], [-1, -2], [2, 1]]
            if mino.state == [3, 2]:
                shift_list = [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]]
            if mino.state == [2, 1]:
                shift_list = [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]]
            if mino.state == [1, 0]:
                shift_list = [[0, 0], [2, 0], [-1, 0], [2, -1], [-1, 2]]
        else:  # I，O以外のミノ用
            # 右回転
            if mino.state == [0, 1]:
                shift_list = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
            if mino.state == [1, 2]:
                shift_list = [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]
            if mino.state == [2, 3]:
                shift_list = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
            if mino.state == [3, 0]:
                shift_list = [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]
            # 左回転
            if mino.state == [0, 3]:
                shift_list = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
            if mino.state == [3, 2]:
                shift_list = [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]
            if mino.state == [2, 1]:
                shift_list = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
            if mino.state == [1, 0]:
                shift_list = [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]

        for shift_axis in shift_list:
            for y in range(pattern_len):
                for x in range(pattern_len):
                    if mino.pattern[y][x]:
                        field_x = mino.loc[0] + x + shift_axis[0]
                        field_y = mino.loc[1] + y + shift_axis[1]
                        if Window._field[field_y][field_x] > 10:
                            collision_list.append(99)
                        else:
                            collision_list.append(0)
            if not 99 in collision_list:
                mino.loc[0] += shift_axis[0]
                mino.loc[1] += shift_axis[1]
                mino.state[0] = mino.state[1]
                return False
            collision_list = []
        return True

    def line_check(self):
        self.lines = []
        for y in range(Window._field_height - 4, 2, -1):
            zero_cnt = Window._field[y].count(0)
            if zero_cnt == 0:
                self.lines.append(y)
            if zero_cnt == 10:
                break

    def hard_drop(self):
        hard_flag = True
        while hard_flag:
            if not window.bottom_hit(mino, 'drop'):
                window.mapping(mino, 'clear')
                mino.control('down')
                window.mapping(mino, 'drop')
            else:
                hard_flag = False
                window.mapping(mino, 'fix')
                window.line_check()
                window.mapping(mino, 'line_clear')
        return True

    def ghost_block(self):
        window.bottom_hit(mino, 'ghost')
        window.mapping(mino, 'ghost')


# mainループ
pygame.init()
screen_size = (600, 600)
screen = pygame.display.set_mode(screen_size)

# インスタンス生成
mino = Mino('drop')
window = Window()
window.mapping(mino, 'drop')
fixed = False
hold = False
# キー入力用カウンタ
l_cnt = 0
r_cnt = 0
d_cnt = 0
threshold = 1
pygame.key.set_repeat(500, 10)

TIMEREVENT = pygame.USEREVENT
pygame.time.set_timer(TIMEREVENT, 50)
first_collision = False
clock = pygame.time.Clock()

while True:

    time_passed = clock.tick(60)
    time_passed_seconds = time_passed / 1000.0

    if fixed:
        mino = Mino('drop')
        window.mapping(mino, 'drop')
        fixed = False
    window.draw(screen)
    pygame.display.update()

#    pygame.event.pump()
#    pressed = pygame.key.get_pressed()
#    if pressed[K_LEFT]:
#        l_cnt += 1
#        if l_cnt == threshold:
#            if not window.left_hit(mino):
#                window.mapping(mino, 'clear')
#                mino.control('left')
#                window.mapping(mino, 'drop')
#            l_cnt = 0
#
#    if pressed[K_RIGHT]:
#        r_cnt += 1
#        if r_cnt == threshold:
#            if not window.right_hit(mino):
#                window.mapping(mino, 'clear')
#                mino.control('right')
#                window.mapping(mino, 'drop')
#            r_cnt = 0

#    if pressed[K_DOWN]:
#        d_cnt += 1
#        if d_cnt == threshold:
#            if not window.bottom_hit(mino, 'drop'):
#                window.mapping(mino, 'clear')
#                mino.control('down')
#                window.mapping(mino, 'drop')
#            else:
#                if first_collision == False:
#                    first_collision = True
#                else:
#                    mino.fix_time = 2
#                if mino.fix_check('count'):
#                    window.mapping(mino, 'fix')
#                    window.line_check()
#                    window.mapping(mino, 'line_clear')
#                    fixed = True
#                    hold = False
#            d_cnt = 0

#    for event in pygame.key.get_repeat():


    for event in pygame.event.get():
        if event.type == TIMEREVENT:
            if window.bottom_hit(mino, 'drop'):
                if mino.fix_check('count'):
                    window.mapping(mino, 'fix')
                    window.line_check()
                    window.mapping(mino, 'line_clear')
                    fixed = True
                    hold = False
            else:
                mino.fix_check('reset')
                window.mapping(mino, 'clear')
                mino.control('down')
                window.mapping(mino, 'drop')
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.quit()

            if event.key == K_z:
                window.mapping(mino, 'clear')
                mino.rotate('left')
                if window.rotate_hit(mino):
                    mino.rotate('right')
                    window.mapping(mino, 'drop')
                else:
                    window.mapping(mino, 'drop')

            if event.key == K_x:
                window.mapping(mino, 'clear')
                mino.rotate('right')
                if window.rotate_hit(mino):
                    mino.rotate('left')
                    window.mapping(mino, 'drop')
                else:
                    window.mapping(mino, 'drop')

            if event.key == K_LSHIFT:
                if not hold:
                    window.mapping(mino, 'clear')
                    if mino.held_already():
                        mino = None
                        mino = Mino('hold')
                    else:
                        mino = None
                        mino = Mino('drop')
                    hold = True
                    window.mapping(mino, 'drop')

            if event.key == K_UP:
                if window.hard_drop():
                    fixed = True
                    hold = False

            if event.key == K_DOWN:
                if not window.bottom_hit(mino, 'drop'):
                    window.mapping(mino, 'clear')
                    mino.control('down')
                    window.mapping(mino, 'drop')
                else:
                    if first_collision == False:
                        first_collision = True
                    else:
                        mino.fix_time = 2
                    if mino.fix_check('count'):
                        window.mapping(mino, 'fix')
                        window.line_check()
                        window.mapping(mino, 'line_clear')
                        fixed = True
                        hold = False

            if event.key == K_LEFT:
                if not window.left_hit(mino):
                    window.mapping(mino, 'clear')
                    mino.control('left')
                    window.mapping(mino, 'drop')

            if event.key == K_RIGHT:
                if not window.right_hit(mino):
                    window.mapping(mino, 'clear')
                    mino.control('right')
                    window.mapping(mino, 'drop')

    window.draw(screen)
    pygame.display.update()
