#!/usr/bin/python3

### Pong ##
#
# EXEC:
# DEPN:
#
# (description)
#
#
# ---
#  ver-0.0
# ---
##


import curses
import random
import time
from curses import wrapper


# Unicode chars
BLOCK_CHR = '\u2588'
CHALF_BLOCK_CHR = '\u2503'
LHALF_BLOCK_CHR = '\u258C'
RHALF_BLOCK_CHR = '\u2590'

# Ball constants
BALL_HEIGHT = 1
BALL_WIDTH = 2
BALL_INIT_SPD = 1

# Player/User paddle constants
PADDLE_HEIGHT = 3
PADDLE_WIDTH = 1
PADDLE_INIT_SPD = 2



## METHODS -----#

def drawBall(stdscr, posvect):
    stdscr.addstr(posvect[1], posvect[0], BLOCK_CHR)
    stdscr.addstr(posvect[1], posvect[0] + 1, BLOCK_CHR)
    #stdscr.addstr(10, 10, "posvect(x, y):  {}, {}".format(posvect[0], posvect[1]))
    #stdscr.addstr(posvect[1], posvect[0], "0")
    #stdscr.addstr(posvect[1], posvect[0] + 1, "0")


def drawDivider(stdscr):
    scrsize = stdscr.getmaxyx()
    x_pos = int(round((scrsize[1] / 2), 0))

    for i in range(scrsize[0]):
        if i % 2 == 0:
            stdscr.addstr(i, x_pos, CHALF_BLOCK_CHR)


def drawPaddle(stdscr, posvect):
    scrsize = stdscr.getmaxyx()

    if (posvect[0] < int(scrsize[0] / 2)):
        padchar = RHALF_BLOCK_CHR
    else:
        padchar = LHALF_BLOCK_CHR

    for i in range(PADDLE_HEIGHT):
        stdscr.addstr(posvect[1] + i, posvect[0], padchar)


def drawScores(stdscr, pscore, cscore):
    y_pos = 1
    stdscr.addstr(y_pos, 1, "{}".format(cscore))
    stdscr.addstr(y_pos, (stdscr.getmaxyx()[1] - 2), "{}".format(pscore))


def getComputerMove(padlposvect, padlvelvect, ballposvect, ballvelvect):
    new_ball_y = ballposvect[1] + ballvelvect[1]
    padl_mid_y = padlposvect[1] + int(round((PADDLE_HEIGHT / 2), 0))

    if padl_mid_y < new_ball_y:
        # increase y
        if padlvelvect[1] < 0:
            padlvelvect[1] *= -1
        elif padlvelvect[1] == 0:
            padlvelvect[1] = PADDLE_INIT_SPD * -1
    elif padl_mid_y > new_ball_y:
        # decrease y
        if padlvelvect[1] > 0:
            padlvelvect[1] *= -1
        elif padlvelvect[1] == 0:
            padlvelvect[1] = PADDLE_INIT_SPD
    else:
        padlvelvect[1] = 0

    return padlvelvect


def startBall(velvect):
    seed = random.randint(0, 16)
    velvect[0] = BALL_INIT_SPD
    velvect[1] = BALL_INIT_SPD

    if seed % 2 != 0:
        velvect[0] *= -1
        velvect[1] *= -1

    return velvect


def updateBall(stdscr, posvect, velvect, ppaddle_vect, cpaddle_vect):
    scrsize = stdscr.getmaxyx()
    new_x = posvect[0] + velvect[0]
    new_y = posvect[1] + velvect[1]

    if new_x <= 0:
        new_x = 0
        velvect[0] *= -1
    elif (new_x + 1) >= (scrsize[1] - 1):
        new_x = scrsize[1] - BALL_WIDTH
        velvect[0] *= -1
    elif (new_x == (ppaddle_vect[0] - BALL_WIDTH)) and (velvect[0] > 0):
        if (ppaddle_vect[1] <= new_y) and (new_y <= (ppaddle_vect[1] + PADDLE_HEIGHT)):
            velvect[0] *= -1
    elif (new_x == (cpaddle_vect[0] + PADDLE_WIDTH)) and (velvect[0] < 0):
        if (cpaddle_vect[1] <= new_y) and (new_y <= (cpaddle_vect[1] + PADDLE_HEIGHT)):
            velvect[0] *= -1

    if new_y <= 0:
        new_y = 0
        velvect[1] *= -1
    elif new_y >= (scrsize[0] - 1):
        new_y = scrsize[0] - BALL_HEIGHT
        velvect[1] *= -1

    new_posvect = [new_x, new_y]
    return (new_posvect, velvect)


def updateComputerPaddle(stdscr, posvect, velvect):
    scrsize = stdscr.getmaxyx()
    new_y = posvect[1] + velvect[1]

    if new_y <= 0:
        new_y = 0
    elif new_y >= (scrsize[0] - PADDLE_HEIGHT):
        new_y = scrsize[0] - PADDLE_HEIGHT

    new_posvect = [posvect[0], new_y]
    return new_posvect


def updatePlayerPaddle(stdscr, posvect, velvect):
    scrsize = stdscr.getmaxyx()
    new_y = posvect[1] + velvect[1]

    if new_y <= 0:
        new_y = 0
    elif new_y >= (scrsize[0] - PADDLE_HEIGHT):
        new_y = scrsize[0] - PADDLE_HEIGHT

    new_posvect = [posvect[0], new_y]
    return new_posvect



'''
def drawPaddleL(stdscr):
    x_pos = 8
    y_pos = int(round((stdscr.getmaxyx()[0] / 2), 0))
    stdscr.addstr(y_pos - 1, x_pos, LH_BLOCK_CHR)
    stdscr.addstr(y_pos, x_pos, LH_BLOCK_CHR)
    stdscr.addstr(y_pos + 1, x_pos, LH_BLOCK_CHR)


def drawPaddleR(stdscr):
    x_pos = stdscr.getmaxyx()[1] - 8
    y_pos = int(round((stdscr.getmaxyx()[0] / 2), 0))
    stdscr.addstr(y_pos - 1, x_pos, RH_BLOCK_CHR)
    stdscr.addstr(y_pos, x_pos, RH_BLOCK_CHR)
    stdscr.addstr(y_pos + 1, x_pos, RH_BLOCK_CHR)
'''



def main(stdscr):
    # set up game
    stdscr.nodelay(True)
    screen_size = stdscr.getmaxyx()
    curses.curs_set(0)
    
    # set up ball
    #curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    #ball_colour = curses.color_pair(1)
    ball_init_x = int(round((screen_size[1] / 2), 0))
    ball_init_y = int(round((screen_size[0] / 2), 0))
    ball_pos_vect = [ball_init_x, ball_init_y]
    ball_vel_vect = [0, 0]

    # set up player paddle (right)
    ppaddle_init_x = int(round((screen_size[1] - (screen_size[1] * 0.13)), 0))
    ppaddle_init_y = int(round((screen_size[0] / 2), 0))
    ppaddle_pos_vect = [ppaddle_init_x, ppaddle_init_y]
    ppaddle_vel_vect = [0, 0]

    # set up computer paddle (left)
    cpaddle_init_x = int(round((screen_size[1] * 0.13), 0))
    cpaddle_init_y = int(round((screen_size[0] / 2), 0))
    cpaddle_pos_vect = [cpaddle_init_x, cpaddle_init_y]
    cpaddle_vel_vect = [0, 0]

    # set up display
    stdscr.clear()
    drawDivider(stdscr)
    drawBall(stdscr, ball_pos_vect)
    drawPaddle(stdscr, ppaddle_pos_vect)
    drawPaddle(stdscr, cpaddle_pos_vect)
    stdscr.refresh()

    # do stuff

    # MAIN LOOP
    player_score = 0
    cmputr_score = 0
    ticker = 0
    play = True

    run = True
    while run:

        # check for events
        try:
            key = stdscr.getkey()
        except:
            key = "none"

        if key == " ":
            run = False
        elif key == "r":
            ball_pos_vect = [ball_init_x, ball_init_y]
        elif key == "s":
            ball_vel_vect = startBall(ball_vel_vect)
            play = True

        if key == "KEY_UP":
            ppaddle_vel_vect = [0, (PADDLE_INIT_SPD * -1)]
        if key == "KEY_DOWN":
            ppaddle_vel_vect = [0, PADDLE_INIT_SPD]
        if key == "none":
            ppaddle_vel_vect = [0, 0]
        ppaddle_pos_vect = updatePlayerPaddle(stdscr, ppaddle_pos_vect, ppaddle_vel_vect)

        if (ball_pos_vect[0] <= (cpaddle_pos_vect[0] - BALL_WIDTH - 1)) and play:
            ball_vel_vect = [0, 0]
            player_score += 1
            play = False
        elif (ball_pos_vect[0] >= (ppaddle_pos_vect[0] + PADDLE_WIDTH + 1)) and play:
            ball_vel_vect = [0, 0]
            cmputr_score += 1
            play = False

        if (ball_vel_vect[0] != 0) and (ball_pos_vect[0] <= (int(round((screen_size[1] / 3), 0)))):
            cpaddle_vel_vect = getComputerMove(cpaddle_pos_vect, cpaddle_vel_vect, ball_pos_vect, ball_vel_vect)
            cpaddle_pos_vect = updateComputerPaddle(stdscr, cpaddle_pos_vect, cpaddle_vel_vect)
        else:
            cpaddle_pos_vect = [cpaddle_init_x, cpaddle_init_y]

        if ticker == 0:
            ball_pos_vect, ball_vel_vect = updateBall(stdscr, ball_pos_vect, ball_vel_vect, ppaddle_pos_vect, cpaddle_pos_vect)
            #if (ball_vel_vect[0] != 0) and (ball_pos_vect[0] <= int(round((screen_size[1] / 2), 0))):
            #    cpaddle_vel_vect = getComputerMove(cpaddle_pos_vect, cpaddle_vel_vect, ball_pos_vect, ball_vel_vect)
            #    cpaddle_pos_vect = updateComputerPaddle(stdscr, cpaddle_pos_vect, cpaddle_vel_vect)
            ticker += 1
        else:
            ticker = 0
                
        stdscr.clear()
        drawDivider(stdscr)
        drawScores(stdscr, player_score, cmputr_score)
        drawBall(stdscr, ball_pos_vect)
        drawPaddle(stdscr, ppaddle_pos_vect)
        drawPaddle(stdscr, cpaddle_pos_vect)
        stdscr.refresh()
        time.sleep(0.021)


wrapper(main)