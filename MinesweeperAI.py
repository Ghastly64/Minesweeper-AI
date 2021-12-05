import cv2 as cv
import numpy as np
import pyautogui
import time
import math


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


time.sleep(3)
image = pyautogui.screenshot()
print(pyautogui.position())

scMatch = cv.imread("images/sc-match1.png", 0)
#scMatch = cv.imread("images/grid_tl.png", 0)
top_l = resMatch(image, scMatch, "imagesOut/res1.png")

scMatch2 = cv.imread("images/sc-match2.png", 0)
#scMatch2 = cv.imread("images/grid_br.png", 0)
bot_r = resMatch(image, scMatch2, "imagesOut/res2.png")

game_coords = [top_l[0], bot_r[1]]


def numOCR(game_sc, grid):
    one_list = []
    ones = cv.imread("images/ones.png", 0)
    resMatchMult(game_sc, ones, .93, "imagesOut/onesOut.png", one_list)

    one_coords = []

    for one in one_list:
        x = math.ceil((one[0] - 10) / 48)
        y = math.ceil((one[1] - 137) / 48)
        one_coords.append([x, y])

    for x in one_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1, x[0]-1] = "1"


    two_list = []
    twos = cv.imread("images/twos.png", 0)
    resMatchMult(game_sc, twos, .97, "imagesOut/twosOut.png", two_list)

    two_coords = []
    for two in two_list:
        x = math.ceil((two[0]- 10) / 48)
        y = math.ceil((two[1]- 137) / 48)
        two_coords.append([x, y])
    
    for x in two_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "2"


    three_list = []
    threes = cv.imread("images/threes.png", 0)
    resMatchMult(game_sc, threes, .97, "imagesOut/threesOut.png", three_list)

    three_coords = []
    for three in three_list:
        x = math.ceil((three[0]- 10) / 48)
        y = math.ceil((three[1]- 137) / 48)
        three_coords.append([x, y])

    for x in three_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "3"


    four_list = []
    fours = cv.imread("images/fours.png", 0)
    resMatchMult(game_sc, fours, .93, "imagesOut/foursOut.png", four_list)

    four_coords = []
    for four in four_list:
        x = math.ceil((four[0]- 10) / 48)
        y = math.ceil((four[1]- 137) / 48)
        four_coords.append([x, y])
    
    for x in four_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "4"


    five_list = []
    fives = cv.imread("images/fives.png", 0)
    resMatchMult(game_sc, fives, .93, "imagesOut/fivesOut.png", five_list)

    five_coords = []
    for five in five_list:
        x = math.ceil((five[0]- 10) / 48)
        y = math.ceil((five[1]- 137) / 48)
        five_coords.append([x, y])
    
    for x in five_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "5"


    six_list = []
    sixes = cv.imread("images/sixes.png", 0)
    resMatchMult(game_sc, sixes, .93, "imagesOut/sixesOut.png", six_list)

    six_coords = []
    for six in six_list:
        x = math.ceil((six[0]- 10) / 48)
        y = math.ceil((six[1]- 137) / 48)
        six_coords.append([x, y])
    
    for x in six_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "6"

    flag_list = []
    flags = cv.imread("images/flags.png", 0)
    resMatchMult(game_sc, flags, .93, "imagesOut/flagsOut.png", flag_list)

    flag_coords = []
    for flag in flag_list:
        x = math.ceil((flag[0]- 10) / 48)
        y = math.ceil((flag[1]- 137) / 48)
        flag_coords.append([x, y])

    for x in flag_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1,x[0]-1] = "f"
    
    zero_list = []
    zeros = cv.imread("images/zero1.png", 0)
    resMatchMult(game_sc, zeros, .93, "imagesOut/zerosOut.png", zero_list)

    zero_coords = []
    for zero in zero_list:
        x = math.ceil((zero[0]- 10) / 48)
        y = math.ceil((zero[1]- 137) / 48)
        zero_coords.append([x, y])

    for x in zero_coords:
        if grid[x[1]-1,x[0]-1] == 'x' or grid[x[1]-1,x[0]-1] == '0':
            grid[x[1]-1][x[0]-1] = "x"

def removeDups(list):
    newList = []
    for item in list:
        if item not in newList:
            newList.append(item)
    return newList


flag_list = []
click_list = []

def getSurr(x, y, grid):
    surrList = []
    if grid.shape[1] >= 29:
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
    else:
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

def canReduceOne(x, y, grid, bombCount):
    canReduce = False
    if bombCount == 0 and grid[y][x] == "1":
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

def canReduceTwo(x, y, grid, bombCount):
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

def canReduceThree(x, y, grid, bombCount):
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

def canReduceFour(x, y, grid, bombCount):
    canReduce = False
    if bombCount == 0 and grid[y, x] == "4":
        canReduce = True
    elif bombCount == 1 and grid[y, x] == "5":
        canReduce = True
    elif bombCount == 2 and grid[y, x] == "6":
        canReduce = True
    return canReduce

def doCommands():
    global flag_list
    flag_list = removeDups(flag_list)
    for command in flag_list:
        print("right click " + str(command))
        print("wanna right click " + str([(command[0]*48)+10+game_coords[0][0], (command[1]*48)+137+game_coords[0][1]]))
        print("wanna right click " + str([((command[0]*48)+10+game_coords[0][0]+50)*0.5, ((command[1]*48)+137+game_coords[0][1]+50)*0.5]))
        #mouse.move(((command[0]*48)+10+game_coords[0][0]+24)*0.5625, ((command[1]*48)+137+game_coords[0][1]+24)*0.5625, absolute=True, duration=0.1)
        #mouse.right_click()
        pyautogui.rightClick(x=((command[0]*48)+10+game_coords[0][0]+50)*0.5, y=((command[1]*48)+137+game_coords[0][1]+50)*0.5)
    global click_list
    click_list = removeDups(click_list)
    for command in click_list:
        print("click " + str(command))
        print("wanna click " + str([(command[0]*48)+10+game_coords[0][0], (command[1]*48)+137+game_coords[0][1]]))
        print("wanna click " + str([((command[0]*48)+10+game_coords[0][0]+24)*0.5, ((command[1]*48)+137+game_coords[0][1]+24)*0.5]))
        #mouse.move(((command[0]*48)+10+game_coords[0][0]+24)*0.5625, ((command[1]*48)+137+game_coords[0][1]+24)*0.5625, absolute=True, duration=0.1)
        #mouse.right_click()
        pyautogui.click(x=((command[0]*48)+10+game_coords[0][0]+50)*0.5, y=((command[1]*48)+137+game_coords[0][1]+50)*0.5)

def B1(x, y, grid):
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

def B2(x, y, grid):
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

def one1(x, y, grid):
    global click_list
    if (grid[y, x] == "1"):
        surrList = getSurr(x, y, grid)
        count = 0
        bomb50 = []
        for surr in surrList: #first check surroundings for empty space
            if surr[0] == "x":
                count += 1
                bomb50.append(surr[1])
            elif surr[0] == "f":
                return
        if count == 2: #if there are 2 empty spaces, then continue
            for surr in surrList: #check surroundings for 1s
                if str(surr[0]) == "1": #if there is a 1, then continue
                    count1 = 0 
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid) #get the surroundings of the 1
                    for surr1 in surrList1: #for each of the surroundings of the 1
                        if surr1[0] == "x" and surr1[1] in bomb50: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                    if count1 == 2:
                        for surr1 in surrList1:
                            if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                click_list.append(surr1[1])

def one2(x, y, grid):
    global click_list
    surrList = getSurr(x, y, grid)
    bombCount = 0
    for surr in surrList:
        if surr[0] == "f":
            bombCount += 1
    canReduce = canReduceOne(x, y, grid, bombCount)
    if canReduce:
        count = 0
        bomb50 = []
        for surr in surrList: #first check surroundings for empty space
            if surr[0] == "x":
                count += 1
                bomb50.append(surr[1])
        if count == 2: #if there are 2 empty spaces, then continue
            for surr in surrList: #check surroundings for 2s
                if str(surr[0]) == "2": #if there is a 2, then continue
                    count1 = 0 
                    bombCount = 0 
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid) #get the surroundings of the 2
                    for surr1 in surrList1: #for each of the surroundings of the 2
                        if surr1[0] == "x" and surr1[1] in bomb50: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                        if surr1[0] == "f":
                            bombCount += 1
                    if count1 == 2:
                        if bombCount == 1:
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    click_list.append(surr1[1])
                        if bombCount == 0:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    Xs += 1
                            if Xs == 1:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                        flag_list.append(surr1[1])
                if str(surr[0]) == "3":
                    count1 = 0 
                    bombCount = 0
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid) #get the surroundings of the 3
                    for surr1 in surrList1: #for each of the surroundings of the 3
                        if surr1[0] == "x" and surr1[1] in bomb50: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                        if surr1[0] == "f":
                            bombCount += 1
                    if count1 == 2:
                        if bombCount == 2:
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    click_list.append(surr1[1])
                        if bombCount == 1:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    Xs += 1
                            if Xs == 1:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                        flag_list.append(surr1[1])
                        if bombCount == 0:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    Xs += 1
                            if Xs == 2:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                        flag_list.append(surr1[1])
                if str(surr[0]) == "4":
                    count1 = 0 
                    bombCount = 0
                    surrList1 = getSurr(surr[1][0], surr[1][1], grid)
                    for surr1 in surrList1: #for each of the surroundings of the 4
                        if surr1[0] == "x" and surr1[1] in bomb50: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                        if surr1[0] == "f":
                            bombCount += 1
                    if count1 == 2:
                        if bombCount == 3:
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    click_list.append(surr1[1])
                        if bombCount == 2:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    Xs += 1
                            if Xs == 1:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                        flag_list.append(surr1[1])
                        if bombCount == 1:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    Xs += 1
                            if Xs == 2:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                        flag_list.append(surr1[1])
                        if bombCount == 0:
                            Xs = 0
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    Xs += 1
                            if Xs == 3:
                                for surr1 in surrList1:
                                    if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                        flag_list.append(surr1[1])
        """ if count == 3:
            for surr in surrList:
                bombCount1 = 0
                for surr1 in surrList:
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
                        if surr1[0] == "x" and surr1[1] in bomb50: #if that surrounding is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                    if count1 == 2:
                        Xs = 0
                        for surr1 in surrList1:
                            if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                Xs += 1
                        if Xs == 1:
                            for surr1 in surrList1:
                                if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                    flag_list.append(surr1[1]) """
                                 
def one1R(x, y, grid): 
    global click_list
    surrList = getSurr(x, y, grid)
    bombCount = 0
    for surr in surrList:
        if str(surr[0]) == "f":
            bombCount += 1
    canReduce = canReduceOne(x, y, grid, bombCount)

    if canReduce:
        count = 0
        bomb50 = []
        for surr in surrList: #first check surroundings for empty space
            if surr[0] == "x":
                count += 1
                bomb50.append(surr[1])
        if count == 2: #if there are 2 empty spaces, then continue
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
                        if surr1[0] == "x" and surr1[1] in bomb50: #if that surrounfing is an empty space and is in the bomb50 list
                            count1 += 1 #add to counter
                    if count1 == 2:
                        for surr1 in surrList1:
                            if str(surr1[0]) == "x" and surr1[1] not in bomb50:
                                click_list.append(surr1[1])




        
def mainLoop():

    global flag_list
    global click_list

    flag_list = []
    click_list = []

    game_sc = pyautogui.screenshot(region=(game_coords[0][0],game_coords[0][1], game_coords[1][0]-game_coords[0][0], game_coords[1][1]-game_coords[0][1]))
    game_sc1 = cv.cvtColor(np.array(game_sc), cv.COLOR_RGB2BGR)
    cv.imwrite("imagesOut/game_sc.png",game_sc1)

    print(game_coords[1][0]-game_coords[0][0])

    if game_coords[1][0]-game_coords[0][0] > 900:
        grid = np.full((16,30), "0",  dtype=str)
    elif game_coords[1][0]-game_coords[0][0] < 900:
        grid = np.full((16,16), "0",  dtype=str)

    print(game_coords[0][0])
    print(game_coords[0][1])

    numOCR(game_sc, grid);

    np.set_printoptions(linewidth=240)
    print(grid)

    rows = grid.shape[0]
    cols = grid.shape[1]

    for x in range(0, cols):
        for y in range(0, rows):
            #print(grid[x,y])
            B1(x, y, grid)
            B2(x, y, grid)
            #one1(x, y, grid)
            one1R(x, y, grid)
            one2(x, y, grid)
            
    doCommands()
    
for i in range(0, 10):
    mainLoop()
    time.sleep(.1)





