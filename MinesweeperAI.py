import cv2 as cv
import numpy as np
import pyautogui
import time
import math
import sys

#You must make the first click, use No Guessing Mode

X_GRID_OFFSET = 10 #constant distance between left edge of sc and left edge of grid
Y_GRID_OFFSET = 137 #constant distance between top edge of sc and top edge of grid
CELL_LENGTH = 48 #the length of each indivual square cell in the grid

SCALE_FACTOR = .5 #If your computer has a scale resolution (I.E. Mac Retina Displays) set the scale used here
#For example, if your computer has a pixel resolution of 1920x1080 but you have scaled your screen to be 2x Zoomed in/960*540 resolution, set the scale to .5


#Image Recgonition Portion of the Prorgam
#-----------------------------------------------------------------------------------------------------------------------

def resMatch(image, match, out): #takes and image and a template and returns the coordinates of the matched template in the image
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

def resMatchMult(image, match, thresh, out, list): #takes and image and a template and returns the coordinates of the matched template in the image multiple times
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

print(pyautogui.size())


time.sleep(3) #wait for user to move to minesweeper screen
image = pyautogui.screenshot() #take a screenshot of the screen

scMatch = cv.imread("images/sc-match1.png", 0) #load the template for the top left corner of the playing area (extends past the grid)
#scMatch = cv.imread("images/grid_tl.png", 0)
top_l = resMatch(image, scMatch, "imagesOut/res1.png") #find the top left corner of the playing area using image and scMatch

scMatch2 = cv.imread("images/sc-match2.png", 0) #load the template for the bottom right corner of the playing area (extends past the grid)
#scMatch2 = cv.imread("images/grid_br.png", 0)
bot_r = resMatch(image, scMatch2, "imagesOut/res2.png") #find the bototm right corner of the playing area using image and scMatch2 

game_coords = [top_l[0], bot_r[1]] #using top left corner and bottom right corner of playing area calculate coordinates for playing area



def greenXfunc(game_sc): #check if there is a greenX and click it if it exists
    greenX_list = []
    greenMatch = cv.imread("images/greenX.png", 0) #load the template for the green cross
    resMatchMult(game_sc, greenMatch, 0.93, "imagesOut/greenX.png", greenX_list)

    greenX_coords = [] #define an empty list that will contain the grid coordinates of the green X

    for green in greenX_list: #for screen coordinates of each 1 convert to grid coords
        x = math.floor((green[0] - X_GRID_OFFSET) / CELL_LENGTH) #minus the x offset then divide by 48 to get grid coords, round up to nearest whole number
        y = math.floor((green[1] - Y_GRID_OFFSET) / CELL_LENGTH) #minus the y offset then divide by 48 to get grid coords, round up to nearest whole number
        greenX_coords.append([x, y]) #append the grid coords to the grid cord list

    if greenX_list:
        print("Green X Found")
        print([greenX_coords[0][0], greenX_coords[0][1]])
        click_list.append([greenX_coords[0][0], greenX_coords[0][1]])

def numOCR(game_sc, grid): #takes screenshot of playing area and returns a grid of the numbers in the playing area
    one_list = [] #define an empty list that will contain the screen coordinates of the 1s
    ones = cv.imread("images/ones.png", 0) #load the template for the 1s
    resMatchMult(game_sc, ones, .93, "imagesOut/onesOut.png", one_list) #find the 1s in the playing area using game_sc and ones template, returns multiple

    one_coords = [] #define an empty list that will contain the grid coordinates of the 1s (grid coords start at 0)

    for one in one_list: #for screen coordinates of each 1 convert to grid coords
        x = math.ceil((one[0] - X_GRID_OFFSET) / CELL_LENGTH) #minus the x offset then divide by 48 to get grid coords, round up to nearest whole number
        y = math.ceil((one[1] - Y_GRID_OFFSET) / CELL_LENGTH) #minus the y offset then divide by 48 to get grid coords, round up to nearest whole number
        one_coords.append([x, y]) #append the grid coords to the grid cord list

    for x in one_coords: #for each grid coords in the grid cord list
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0': #if the grid coords are set to an X or 0 (default) then assign to 1, this helps with double calls for the same grid tile
            grid[x[1]-1, x[0]-1] = "1"

    #repeated code for other tile values
    #the accuracy of values may vary depending on the screen resolution and what works best for you
    #P.S. the accuracy value is the .93 above, it ranges from 0 to 1, higher values require more accurate template matching

    two_list = []
    twos = cv.imread("images/twos.png", 0)
    resMatchMult(game_sc, twos, .97, "imagesOut/twosOut.png", two_list)

    two_coords = []
    for two in two_list:
        x = math.ceil((two[0]- X_GRID_OFFSET) / CELL_LENGTH)
        y = math.ceil((two[1]- Y_GRID_OFFSET) / CELL_LENGTH)
        two_coords.append([x, y])
    
    for x in two_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "2"


    three_list = []
    threes = cv.imread("images/threes.png", 0)
    resMatchMult(game_sc, threes, .97, "imagesOut/threesOut.png", three_list)

    three_coords = []
    for three in three_list:
        x = math.ceil((three[0]- X_GRID_OFFSET) / CELL_LENGTH)
        y = math.ceil((three[1]- Y_GRID_OFFSET) / CELL_LENGTH)
        three_coords.append([x, y])

    for x in three_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "3"


    four_list = []
    fours = cv.imread("images/fours.png", 0)
    resMatchMult(game_sc, fours, .93, "imagesOut/foursOut.png", four_list)

    four_coords = []
    for four in four_list:
        x = math.ceil((four[0]- X_GRID_OFFSET) / CELL_LENGTH)
        y = math.ceil((four[1]- Y_GRID_OFFSET) / CELL_LENGTH)
        four_coords.append([x, y])
    
    for x in four_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "4"


    five_list = []
    fives = cv.imread("images/fives.png", 0)
    resMatchMult(game_sc, fives, .93, "imagesOut/fivesOut.png", five_list)

    five_coords = []
    for five in five_list:
        x = math.ceil((five[0]- X_GRID_OFFSET) / CELL_LENGTH)
        y = math.ceil((five[1]- Y_GRID_OFFSET) / CELL_LENGTH)
        five_coords.append([x, y])
    
    for x in five_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "5"


    six_list = []
    sixes = cv.imread("images/sixes.png", 0)
    resMatchMult(game_sc, sixes, .93, "imagesOut/sixesOut.png", six_list)

    six_coords = []
    for six in six_list:
        x = math.ceil((six[0]- X_GRID_OFFSET) / CELL_LENGTH)
        y = math.ceil((six[1]- Y_GRID_OFFSET) / CELL_LENGTH)
        six_coords.append([x, y])
    
    for x in six_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "6"

    flag_list = []
    flags = cv.imread("images/flags.png", 0)
    resMatchMult(game_sc, flags, .93, "imagesOut/flagsOut.png", flag_list)

    flag_coords = []
    for flag in flag_list:
        x = math.ceil((flag[0]- X_GRID_OFFSET) / CELL_LENGTH)
        y = math.ceil((flag[1]- Y_GRID_OFFSET) / CELL_LENGTH)
        flag_coords.append([x, y])

    for x in flag_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "f"
    
    zero_list = []
    zeros = cv.imread("images/zero1.png", 0)
    resMatchMult(game_sc, zeros, .93, "imagesOut/zerosOut.png", zero_list)

    zero_coords = []
    for zero in zero_list:
        x = math.ceil((zero[0]- X_GRID_OFFSET) / CELL_LENGTH)
        y = math.ceil((zero[1]- Y_GRID_OFFSET) / CELL_LENGTH)
        zero_coords.append([x, y])

    for x in zero_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1][x[0]-1] = "x"

#-----------------------------------------------------------------------------------------------------------------------

#Processing portion of the Program (Finds the next cell to be clicked and flagged)
#-----------------------------------------------------------------------------------------------------------------------

flag_list = [] #List of flag moves needing to be done
click_list = [] #List of click moves needing to be done
bomb50 = []
greenX = True

def getSurr(x, y, grid): #get surrounding cells
    surrList = []
    if grid.shape[1] >= 29: #If the grid width is greater then 29 (30x16, but using 29 to be safe)
        if x-1 >= 0 and y-1 >= 0:
            surrList.append([grid[y-1, x-1], [x-1, y-1], "top left"]) #top left
        if y-1 >= 0:
            surrList.append([grid[y-1, x], [x, y-1], "top"]) #top
        if x+1 <= 29 and y-1 >= 0:
            surrList.append([grid[y-1, x+1], [x+1, y-1], "top right"]) #top right
        if x-1 >= 0:
            surrList.append([grid[y, x-1], [x-1, y], "left"]) #left
        if x+1 <= 29:
            surrList.append([grid[y, x+1], [x+1, y], "right"]) #right
        if x-1 >= 0 and y+1 <= 15:
            surrList.append([grid[y+1, x-1], [x-1, y+1], "bottom left"]) #bottom left
        if y+1 <= 15:
            surrList.append([grid[y+1, x], [x, y+1], "bottom"]) #bottom
        if x+1 <= 29 and y+1 <= 15:
            surrList.append([grid[y+1, x+1], [x+1, y+1], "bottom right"]) #bottom right
        return surrList
    else: #If the grid width is smaller then 29 (16x16)
        if x-1 >= 0 and y-1 >= 0: 
            surrList.append([grid[y-1, x-1], [x-1, y-1], "top left"]) #top left
        if y-1 >= 0:
            surrList.append([grid[y-1, x], [x, y-1], "top"]) #top
        if x+1 <= 15 and y-1 >= 0:
            surrList.append([grid[y-1, x+1], [x+1, y-1], "top right"]) #top right
        if x-1 >= 0:
            surrList.append([grid[y, x-1], [x-1, y], "left"]) #left
        if x+1 <= 15:
            surrList.append([grid[y, x+1], [x+1, y], "right"]) #right
        if x-1 >= 0 and y+1 <= 15:
            surrList.append([grid[y+1, x-1], [x-1, y+1], "bottom left"]) #bottom left
        if y+1 <= 15:
            surrList.append([grid[y+1, x], [x, y+1], "bottom"]) #bottom
        if x+1 <= 15 and y+1 <= 15:
            surrList.append([grid[y+1, x+1], [x+1, y+1], "bottom right"]) #bottom right
        return surrList

def canReduceOne(x, y, grid, bombCount): #Check if the cell can be reduced to one, for example a 2 with 1 bomb is the same as a 1
    canReduce = False
    if bombCount == 0 and grid[y, x] == "1":
        canReduce = True
    elif bombCount == 1 and grid[y, x] == "2":
        canReduce = True
    elif bombCount == 2 and grid[y, x] == "3":
        canReduce = True
    elif bombCount == 3 and grid[y, x] == "4":
        canReduce = True
    elif bombCount == 4 and grid[y, x] == "5":
        canReduce = True
    elif bombCount == 5 and grid[y, x] == "6":
        canReduce = True
    
    return canReduce

def canReduceTwo(x, y, grid, bombCount): #check if the cell can be reduced to two, for example a 3 with 1 bomb is the same as a 2
    canReduce = False
    if bombCount == 0 and grid[y, x] == "2":
        canReduce = True
    elif bombCount == 1 and grid[y, x] == "3":
        canReduce = True
    elif bombCount == 2 and grid[y, x] == "4":
        canReduce = True
    elif bombCount == 3 and grid[y, x] == "5":
        canReduce = True
    elif bombCount == 4 and grid[y, x] == "6":
        canReduce = True
    return canReduce

def canReduceThree(x, y, grid, bombCount): #check if the cell can be reduced to three, for example a 4 with 1 bomb is the same as a 3
    canReduce = False
    if bombCount == 0 and grid[y, x] == "3":
        canReduce = True
    elif bombCount == 1 and grid[y, x] == "4":
        canReduce = True
    elif bombCount == 2 and grid[y, x] == "5":
        canReduce = True
    elif bombCount == 3 and grid[y, x] == "6":
        canReduce = True
    return canReduce

def canReduceFour(x, y, grid, bombCount): #check if the cell can be reduced to four, for example a 5 with 1 bomb is the same as a 4
    canReduce = False
    if bombCount == 0 and grid[y, x] == "4":
        canReduce = True
    elif bombCount == 1 and grid[y, x] == "5":
        canReduce = True
    elif bombCount == 2 and grid[y, x] == "6":
        canReduce = True
    return canReduce

def B1(x, y, grid): #pattern Basic 1, if a cell is a 1 and has 1 uncovered tile then that tile must be a bomb
    global flag_list
    surrList = getSurr(x, y, grid)
    count = 0
    for surr in surrList:
        if surr[0] == "x" or surr[0] == "f":
            count += 1
    #print("---------")
    #print("count " + str(count))
    #print("value " + grid[y, x])
    #print("coords " + str([x, y]))
    if str(count) == grid[y, x]:
        for surr in surrList:
            if surr[0] == "x":
                flag_list.append(surr[1])

def B2(x, y, grid): #pattern Basic 2, if a cell is a 1 and has 1 flag tile then the rest of the tiles must be safe
    global click_list
    surrList = getSurr(x, y, grid)
    count = 0
    for surr in surrList:
        if surr[0] == "f":
            count += 1
    if str(count) == grid[y, x]:
        for surr in surrList:
            if surr[0] == "x":
                click_list.append(surr[1])

def one1(x, y, grid): #https://minesweeper.online/help/patterns#1-1
    global click_list
    if (grid[y, x] == "1"):
        surrList = getSurr(x, y, grid)
        count = 0
        bomb50temp = []
        for surr in surrList: #first check surroundings for empty space
            if surr[0] == "x":
                count += 1
                bomb50temp.append(surr[1])
            elif surr[0] == "f":
                return
        if count == 2: #if there are 2 empty spaces, then continue
            bomb50.append(bomb50temp)
            for surr in surrList: #check surroundings for 1s
                if str(surr[0]) == "1": #if there is a 1, then continue
                    count1 = 0 
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid) #get the surroundings of the 1
                    for surr1 in surrList1: #for each of the surroundings of the 1
                        if surr1[0] == "x" and surr1[1] in bomb50temp: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                    if count1 == 2:
                        for surr1 in surrList1:
                            if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                click_list.append(surr1[1])

def one2(x, y, grid): #https://minesweeper.online/help/patterns#1-2
    global click_list
    global bomb50
    surrList = getSurr(x, y, grid)
    bombCount = 0
    for surr in surrList:
        if surr[0] == "f":
            bombCount += 1
    canReduce = canReduceOne(x, y, grid, bombCount)
    if canReduce:
        count = 0
        bomb50temp = []
        for surr in surrList: #first check surroundings for empty space
            if surr[0] == "x":
                count += 1
                bomb50temp.append(surr[1])
        if count == 2: #if there are 2 empty spaces, then continue
            bomb50.append(bomb50temp)
            for surr in surrList: #check surroundings for 2s
                if str(surr[0]) == "2": #if there is a 2, then continue
                    count1 = 0 
                    bombCount = 0 
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid) #get the surroundings of the 2
                    for surr1 in surrList1: #for each of the surroundings of the 2
                        if surr1[0] == "x" and surr1[1] in bomb50temp: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                        if surr1[0] == "f":
                            bombCount += 1
                    if count1 == 2:
                        if bombCount == 1:
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    click_list.append(surr1[1])
                        if bombCount == 0:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 1:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
                if str(surr[0]) == "3":
                    count1 = 0 
                    bombCount = 0
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid) #get the surroundings of the 3
                    for surr1 in surrList1: #for each of the surroundings of the 3
                        if surr1[0] == "x" and surr1[1] in bomb50temp: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                        if surr1[0] == "f":
                            bombCount += 1
                    if count1 == 2:
                        if bombCount == 2:
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    click_list.append(surr1[1])
                        if bombCount == 1:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 1:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
                        if bombCount == 0:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 2:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
                if str(surr[0]) == "4":
                    count1 = 0 
                    bombCount = 0
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid)
                    for surr1 in surrList1: #for each of the surroundings of the 4
                        if surr1[0] == "x" and surr1[1] in bomb50temp: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                        if surr1[0] == "f":
                            bombCount += 1
                    if count1 == 2:
                        if bombCount == 3:
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    click_list.append(surr1[1])
                        if bombCount == 2:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 1:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
                        if bombCount == 1:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 2:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
                        if bombCount == 0:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 3:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
                if str(surr[0]) == "5":
                    count1 = 0 
                    bombCount = 0
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid)
                    for surr1 in surrList1: #for each of the surroundings of the 5
                        if surr1[0] == "x" and surr1[1] in bomb50: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                        if surr1[0] == "f":
                            bombCount += 1
                    if count1 == 2:
                        if bombCount == 4:
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    click_list.append(surr1[1])
                        if bombCount == 3:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 1:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
                        if bombCount == 2:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 2:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
                        if bombCount == 1:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 3:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
                        if bombCount == 0:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    Xs += 1
                            if Xs == 4:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                        flag_list.append(surr1[1])
        if count == 3:
            for surr in surrList:
                bombCount1 = 0
                surrList1 = getSurr(surr[1][0], surr[1][1], grid)
                for surr1 in surrList1:
                    if surr1[0] == "f":
                        bombCount1 += 1
                canReduce2 = canReduceTwo(surr[1][0], surr[1][1], grid, bombCount1)
                #canReduce3 = canReduceThree(surr[1][0], surr[1][1], grid, bombCount1)
                #canReduce4 = canReduceFour(surr[1][0], surr[1][1], grid, bombCount1)
                if canReduce2 == True:
                    count1 = 0 
                    bombCount1 = 0 
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid) #get the surroundings of the reducable 2
                    for surr1 in surrList1: #for each of the surroundings of the reducable 2
                        if surr1[0] == "x" and surr1[1] in bomb50temp: #if that surrounding is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                    if count1 == 2:
                        Xs = 0
                        for surr1 in surrList1:
                            if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                Xs += 1
                        if Xs == 1:
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                    flag_list.append(surr1[1])

def one1R(x, y, grid): #https://minesweeper.online/help/patterns#1-1r
    global click_list
    surrList = getSurr(x, y, grid)
    global bomb50
    bombCount = 0
    for surr in surrList:
        if str(surr[0]) == "f":
            bombCount += 1
    canReduce = canReduceOne(x, y, grid, bombCount)

    if canReduce:
        count = 0
        bomb50temp = []
        for surr in surrList: #first check surroundings for empty space
            if surr[0] == "x":
                count += 1
                bomb50temp.append(surr[1])
        if count == 2: #if there are 2 empty spaces, then continue
            bomb50.append(bomb50temp)
            for surr in surrList: #check surroundings for reducable to 1s
                surrList1 = getSurr(surr[1][0], surr[1][1], grid)
                bombCount1 = 0
                for surr1 in surrList1:
                    if str(surr1[0]) == "f":
                        bombCount1 += 1
                canReduce1 = canReduceOne(surr[1][0], surr[1][1], grid, bombCount1)

                if canReduce1: #if there is a 1, then continue
                    count1 = 0 
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid) #get the surroundings of the reducable 1
                    for surr1 in surrList1: #for each of the surroundings of the reducable 1
                        if surr1[0] == "x" and surr1[1] in bomb50temp: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                    if count1 == 2:
                        for surr1 in surrList1:
                            if str(surr1[0]) == "x" and surr1[1] not in bomb50temp:
                                click_list.append(surr1[1])

def one2NonAdj(grid): #performs the same as one2 but does not rely on first finding a 1 then looking for adjacents
    global bomb50
    bomb50 = removeDups(bomb50) # [[[x,y],[x,y]], [[x,y),(x,y]]]
    for bomb in bomb50:
        if grid[bomb[0][1],bomb[0][0]] == "f" or grid[bomb[1][1],bomb[1][0]] == "f":
            bomb50.remove(bomb)  
    for bomb in bomb50: # [[x,y],[x,y]]
        surrList = getSurr(bomb[0][0], bomb[0][1], grid)
        for surr in surrList:
            surrList1 = getSurr(surr[1][0], surr[1][1], grid)
            count1 = 0
            for surr1 in surrList1:
                if str(surr1[0]) == "x" and surr1[1] in bomb:
                    count1 += 1
            if count1 == 2:
                bombCount = 0
                for surr1 in surrList1:
                    if str(surr1[0]) == "f":
                        bombCount += 1
                canReduce = canReduceOne(surr[1][0], surr[1][1], grid, bombCount)
                canReduce2 = canReduceTwo(surr[1][0], surr[1][1], grid, bombCount)
                canReduce3 = canReduceThree(surr[1][0], surr[1][1], grid, bombCount)
                canReduce4 = canReduceFour(surr[1][0], surr[1][1], grid, bombCount)
                if canReduce:
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid)
                    for surr1 in surrList1:
                        if str(surr1[0]) == "x" and surr1[1] not in bomb:
                            click_list.append(surr1[1])
                if canReduce2:
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid)
                    emptyCount = 0
                    for surr1 in surrList1:
                        if str(surr1[0]) == "x" and surr1[1] not in bomb:
                            emptyCount += 1
                    if emptyCount == 1:
                        for surr1 in surrList1:
                            if str(surr1[0]) == "x" and surr1[1] not in bomb:
                                flag_list.append(surr1[1])
                if canReduce3:
                    surrList1 = getSurr(surr[1][0], surr1[1][1], grid)
                    emptyCount = 0
                    for surr1 in surrList1:
                        if str(surr1[0]) == "x" and surr1[1] not in bomb:
                            emptyCount += 1
                    if emptyCount == 2:
                        for surr1 in surrList1:
                            if str(surr1[0]) == "x" and surr1[1] not in bomb:
                                flag_list.append(surr1[1])
                if canReduce4:
                    surrList1 = getSurr(surr[1][0], surr1[1][1], grid)
                    emptyCount = 0
                    for surr1 in surrList1:
                        if str(surr1[0]) == "x" and surr1[1] not in bomb:
                            emptyCount += 1
                    if emptyCount == 3:
                        for surr1 in surrList1:
                            if str(surr1[0]) == "x" and surr1[1] not in bomb:
                                flag_list.append(surr1[1])

                

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Interaction Portion of the Program (Mouse Control)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def doCommands(): #Proccesses the commands in the click_list and flag_list and does them
    global flag_list #global variable flag list which contains commands to flag
    flag_list = removeDups(flag_list) #remove the duplicates from the flag list
    for command in flag_list: #Flag Commands (what tiles need to be flagged)
        print("right click " + str(command)) #Grid coords
        print("wanna right click " + str([(command[0]*CELL_LENGTH)+X_GRID_OFFSET+game_coords[0][0], (command[1]*CELL_LENGTH)+Y_GRID_OFFSET+game_coords[0][1]])) #Multiply by Cell Length then add Grid Offset to return Pixel Coordinates
        print("wanna right click " + str([((command[0]*CELL_LENGTH)+X_GRID_OFFSET+game_coords[0][0]+CELL_LENGTH)*SCALE_FACTOR, ((command[1]*CELL_LENGTH)+Y_GRID_OFFSET+game_coords[0][1]+CELL_LENGTH)*SCALE_FACTOR])) #Scaled coordinates
        pyautogui.rightClick(x=((command[0]*CELL_LENGTH)+X_GRID_OFFSET+game_coords[0][0]+CELL_LENGTH)*SCALE_FACTOR, y=((command[1]*CELL_LENGTH)+Y_GRID_OFFSET+game_coords[0][1]+CELL_LENGTH)*SCALE_FACTOR) #Click the scaled Coordinates
    global click_list #global variable click list which contains commands to click
    click_list = removeDups(click_list) #remove duplicates from the click list
    for command in click_list: #CLick Commands (what tiles need to be clicked)
        print("click " + str(command)) #Grid coords
        print("wanna right click " + str([(command[0]*CELL_LENGTH)+X_GRID_OFFSET+game_coords[0][0], (command[1]*CELL_LENGTH)+Y_GRID_OFFSET+game_coords[0][1]])) #Multiply by Cell Length then add Grid Offset to return Pixel Coordinates
        print("wanna right click " + str([((command[0]*CELL_LENGTH)+X_GRID_OFFSET+game_coords[0][0]+CELL_LENGTH)*SCALE_FACTOR, ((command[1]*CELL_LENGTH)+Y_GRID_OFFSET+game_coords[0][1]+CELL_LENGTH)*SCALE_FACTOR])) #Scaled coordinates
        pyautogui.click(x=((command[0]*CELL_LENGTH)+X_GRID_OFFSET+game_coords[0][0]+CELL_LENGTH)*SCALE_FACTOR, y=((command[1]*CELL_LENGTH)+Y_GRID_OFFSET+game_coords[0][1]+CELL_LENGTH)*SCALE_FACTOR) #Click the scaled Coordinates
    if not flag_list and  not click_list:
        return False
    else:
        return True

def removeDups(list): #simple function that removes duplicates from a list
    newList = []
    for item in list:
        if item not in newList:
            newList.append(item)
    return newList

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
def mainLoop(): #main loop of the program

    global flag_list #global variable flag list which contains commands to flag
    global click_list #global variable click list which contains commands to click
    global bomb50
    global greenX

    

    flag_list = [] #set flag list to empty
    click_list = [] #set click list to empty
    bomb50 = []

    game_sc = pyautogui.screenshot(region=(game_coords[0][0],game_coords[0][1], game_coords[1][0]-game_coords[0][0], game_coords[1][1]-game_coords[0][1])) #take screenshot of playing area
    game_sc1 = cv.cvtColor(np.array(game_sc), cv.COLOR_RGB2BGR) #convert the screenshot to BGR for OpenCV to work with
    cv.imwrite("imagesOut/game_sc.png",game_sc1) #save the screenshot to a file

    print(game_coords[1][0]-game_coords[0][0]) #print the width of the playing area

    if game_coords[1][0]-game_coords[0][0] > CELL_LENGTH * 18: #if the playing area is greater than 18 cells wide (18 for saftey)
        grid = np.full((16,30), "0",  dtype=str) #make the grid 16x30
    elif game_coords[1][0]-game_coords[0][0] < CELL_LENGTH * 18: #if the playeing area is less than 18 cells wide
        grid = np.full((16,16), "0",  dtype=str) #make the grid 16x16

    if greenX: #greenX for first move on No Guessing
        greenXfunc(game_sc)
        doCommands()
        greenX = False
        return
        

    numOCR(game_sc, grid) #run the OCR function on game_sc

    np.set_printoptions(linewidth=240) #set the width of the printout to 240 characters for the 30x30 grid
    print(grid) #printt the grid 

    rows = grid.shape[0] #get rows of the grid
    cols = grid.shape[1] #get columns of the grid

    for x in range(0, cols): 
        for y in range(0, rows): #for every cell in the grid, run the different patterns
            B1(x, y, grid)
            B2(x, y, grid)
            #one1(x, y, grid)
            one1R(x, y, grid)
            one2(x, y, grid)
    finish = doCommands() #run the commands in the click_list and flag_list
    finish1 = True
    if finish == False: #if there are no commands to run, run one2NonAdj
        print("Attempting Last Resort") 
        one2NonAdj(grid) #run the one2NonAdj function, rare pattern so only called when nothing else works
        finish1 = doCommands()
    if finish1 == False: #if no commands are in the click_list and flag_list still, exit the program
        sys.exit("No Other Commands/Finished")




while True: #main loop of the program
    mainLoop()
    time.sleep(.05)





