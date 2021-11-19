import cv2 as cv
import numpy as np
import imutils
import pyautogui
import time
import math
from matplotlib import pyplot as plt


def resMatch(image, match, out):
    img = cv.cvtColor(np.array(image), cv.COLOR_RGB2GRAY)
    w, h = match.shape[::-1]
    method = eval("cv.TM_CCOEFF_NORMED")
    # Apply template Matching
    res = cv.matchTemplate(img,match,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img,top_left, bottom_right, 255, 2)
    cv.imwrite(out,img)
    return [top_left, bottom_right]

def resMatchMult(image, match, thresh, out, list):
    img_full = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    img_gray = cv.cvtColor(img_full, cv.COLOR_BGR2GRAY)
    w, h = match.shape[::-1]

    res = cv.matchTemplate(img_gray,match,cv.TM_CCOEFF_NORMED)
    threshold = thresh
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_full, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        list.append(pt)
    cv.imwrite(out,img_full)

time.sleep(3)
image = pyautogui.screenshot()

#scMatch = cv.imread("images/sc-match1.png", 0)
scMatch = cv.imread("images/grid_tl.png", 0)
top_l = resMatch(image, scMatch, "imagesOut/res1.png")

#scMatch2 = cv.imread("images/sc-match2.png", 0)
scMatch2 = cv.imread("images/grid_br.png", 0)
bot_r = resMatch(image, scMatch2, "imagesOut/res2.png")

game_coords = [top_l[0], bot_r[1]]


#main loop time
game_sc = pyautogui.screenshot(region=(game_coords[0][0],game_coords[0][1], game_coords[1][0]-game_coords[0][0], game_coords[1][1]-game_coords[0][1]))
game_sc1 = cv.cvtColor(np.array(game_sc), cv.COLOR_RGB2BGR)
cv.imwrite("imagesOut/game_sc.png",game_sc1)

print(game_coords[1][0]-game_coords[0][0])

if game_coords[1][0]-game_coords[0][0] > 800:
    grid = np.full((16,30), "0",  dtype=str)
elif game_coords[1][0]-game_coords[0][0] < 800:
    grid = np.full((16,16), "0",  dtype=str)

def numOCR():
    
    one_list = []
    ones = cv.imread("images/ones.png", 0)
    resMatchMult(game_sc, ones, .93, "imagesOut/onesOut.png", one_list)

    one_coords = []
    for one in one_list:
        x = math.ceil(one[0] / 48)
        y = math.ceil(one[1] / 48)
        one_coords.append([x, y])
    
    for x in one_coords:
        grid[x[1]-1][x[0]-1] = "1"


    two_list = []
    twos = cv.imread("images/twos.png", 0)
    resMatchMult(game_sc, twos, .93, "imagesOut/twosOut.png", two_list)

    two_coords = []
    for two in two_list:
        x = math.ceil(two[0] / 48)
        y = math.ceil(two[1] / 48)
        two_coords.append([x, y])
    
    for x in two_coords:
        grid[x[1]-1][x[0]-1] = "2"


    three_list = []
    threes = cv.imread("images/threes.png", 0)
    resMatchMult(game_sc, threes, .93, "imagesOut/threesOut.png", three_list)

    three_coords = []
    for three in three_list:
        x = math.ceil(three[0] / 48)
        y = math.ceil(three[1] / 48)
        three_coords.append([x, y])

    for x in three_coords:
        grid[x[1]-1][x[0]-1] = "3"


    four_list = []
    fours = cv.imread("images/fours.png", 0)
    resMatchMult(game_sc, fours, .93, "imagesOut/foursOut.png", four_list)

    four_coords = []
    for four in four_list:
        x = math.ceil(four[0] / 48)
        y = math.ceil(four[1] / 48)
        four_coords.append([x, y])
    
    for x in four_coords:
        grid[x[1]-1][x[0]-1] = "4"


    five_list = []
    fives = cv.imread("images/fives.png", 0)
    resMatchMult(game_sc, fives, .93, "imagesOut/fivesOut.png", five_list)

    five_coords = []
    for five in five_list:
        x = math.ceil(five[0] / 48)
        y = math.ceil(five[1] / 48)
        five_coords.append([x, y])
    
    for x in five_coords:
        grid[x[1]-1][x[0]-1] = "5"


    six_list = []
    sixes = cv.imread("images/sixes.png", 0)
    resMatchMult(game_sc, sixes, .93, "imagesOut/sixesOut.png", six_list)

    six_coords = []
    for six in six_list:
        x = math.ceil(six[0] / 48)
        y = math.ceil(six[1] / 48)
        six_coords.append([x, y])
    
    for x in six_coords:
        grid[x[1]-1][x[0]-1] = "6"

    flag_list = []
    flags = cv.imread("images/flags.png", 0)
    resMatchMult(game_sc, flags, .93, "imagesOut/flagsOut.png", flag_list)

    flag_coords = []
    for flag in flag_list:
        x = math.ceil(flag[0] / 48)
        y = math.ceil(flag[1] / 48)
        flag_coords.append([x, y])

    for x in flag_coords:
        grid[x[1]-1][x[0]-1] = "f"
    
    zero_list = []
    zeros = cv.imread("images/zero1.png", 0)
    resMatchMult(game_sc, zeros, .93, "imagesOut/zerosOut.png", zero_list)

    zero_coords = []
    for zero in zero_list:
        x = math.ceil(zero[0] / 48)
        y = math.ceil(zero[1] / 48)
        zero_coords.append([x, y])

    for x in zero_coords:
        grid[x[1]-1][x[0]-1] = "x"
numOCR();

print(grid)







