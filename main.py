from diagonal_movement import DiagonalMovement
from grid import Grid
from a_star import AStarFinder
import xlrd
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import datetime
from stringythings import StringStuffs
import os
import requests
import PIL

IMAGE_EXTENSION = "png" #use jpg to save memory, use png for much clearer text but 10x file size

#try to use colors from colormind.io
colors = [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)] #location, location, start, end, path
resp = requests.post("http://colormind.io/api/", json={"model":"default"})
if resp.status_code == 200:
  colors = resp.json()["result"]
  for i in range(len(colors)):
    colors[i] = tuple(colors[i]) #because imagedraw doesn't like lists for colors

currentTime = str(datetime.datetime.now())[:19] #truncate after seconds
currentTime = currentTime.replace(":", "_") #makes time usable as a file name

#excel file; cells of ones (paths), zeroes (obstacles), and locations (must not contain decimals) representing the school. must be processed first to turn the locations into zeroes (obstacles) before passing into A* algorithm
WORKBOOK_LOCATION = "real small school.xlsx" 
OVERLAY_IMG_LOCATION = "school." + IMAGE_EXTENSION #satellite image of school, use jpg to save memory, use png for clearer text
OVERLAY_IMG_OUT_lOCATION = "output/" + currentTime +"." + IMAGE_EXTENSION #save path image in output folder with unique file name, must have same extension as input img

WARNING = '\033[93m' #yellow terminal text
ENDC = '\033[0m' #end color

workbook = xlrd.open_workbook(WORKBOOK_LOCATION ) #use xlrd to open wkbk in memory

sheet = workbook.sheet_by_index(0) #turn workbook into 2d array

#keys will hold locations ie room numbers and points of interest, values will hold row col location
dictionary = {} 

#make numpy array to which will be passed A* pathfinding algorithm. contains only 1s (paths, incl "1") and 0s (walls, incl "0" and all other cells ie locations)
matrix = np.empty((sheet.nrows,sheet.ncols)) 
for row in range(0, sheet.nrows):
  for col in range(0, sheet.ncols):
    v = str(sheet.cell(row,col).value) #due to excel formatting issues cells may be read in as floats (205 becomes 205.0, not possible for values like e13) or text as is (605 and e13 stays 605 and e13, respectively)
    if "." in v:
      v = v[:v.index(".")] #remove decimals if present
    if not v == "1" and not v == "0": #append to dictionary if location is found
      dictionary[v] = [row, col]
    if v == "1":
      matrix[row][col] = 1 # 1 represents a path
    else:
      matrix[row][col] = 0 # existing obstacles (0s) and locations all become obstacles (0s)

print("Welcome to the RBHS path finder")
print('LIST OF LOCATIONS:')
locations = sorted(dictionary.keys()) #sort alphabetically
locations.sort(key=len, reverse=False) #sort by length
print(StringStuffs.getColString(locations, 5, 5)) #print locations in 5 columns with padding 5 for each entry
closestRoomCoords = () #stores value (starting row/col location of location 'key') of the dictionary key the user entered
destRoomCoords = () #stores value (ending row/col location of location 'key') of the dictionary key the user entered
print("The pathfinder will take a starting location on the RBHS campus and an ending location and display an image showing the shortest path between the two locations. You need to enter the locations so that it matches one of the supported locations listed above.\n")

#user inputs starting loc
while True:
  try:
    closestRoom = raw_input("Which is the closest to your current location? (ex. E13, S1, 401, tennis courts)\n  type here --> ")
    closestRoomCoords = dictionary[closestRoom.lower()]
    break
  except:
    print(WARNING + "Error: not a valid room number" + ENDC)

#user inputs ending loc
while True:
  try:
    destRoom = raw_input("Which is the closest to your destination?\n  type here --> ")
    destRoomCoords = dictionary[destRoom.lower()]
    break
  except:
    print(WARNING + "Error: not a valid room number" + ENDC)

#convert selected locations into paths instead of obstacles in the matrix to be passed to A*
matrix[closestRoomCoords[0]][closestRoomCoords[1]] = 1
matrix[destRoomCoords[0]][destRoomCoords[1]] = 1
#Grid object needed to pass in to A*
grd = Grid(matrix=matrix)
#nodes use X, Y which corresponds to COL, ROW. 
#Node object needed to represent start/ending locations
start = grd.node(closestRoomCoords[1], closestRoomCoords[0]) 
end = grd.node(destRoomCoords[1], destRoomCoords[0])
#make pathfinder object
finder = AStarFinder(diagonal_movement=DiagonalMovement.if_at_most_one_obstacle)
#runs pathfinding algorithm
path, runs = finder.find_path(start, end, grd)
# print('operations:', runs, 'path length:', len(path))
# print(grd.grid_str(path=path, start=start, end=end))
# print(path)

#open satellite img of school 
image = Image.open(OVERLAY_IMG_LOCATION)
#scale pen size to image
WIDTH = float(image.size[0])/sheet.ncols
HEIGHT = float(image.size[1])/sheet.nrows
#create ImageDraw object to draw over satellite img
imgDraw = ImageDraw.Draw(image)

###draw path as ImageDraw lines
##lineCoords = []
##for coords in path:
##  lineCoords.append((int(coords[0] * WIDTH), int(coords[1] * WIDTH)))
##imgDraw.line(lineCoords, fill='red', width=int(WIDTH))
###smooth path a bit
##RADIUS = WIDTH/2
##for coords in lineCoords:
##  imgDraw.ellipse( (coords[0] - RADIUS+2, coords[1] - RADIUS, coords[0] + RADIUS, coords[1] + RADIUS+1), fill='red')

#draw path as scaled up grid, resample is an attempt to preserve anti aliasing and smooth the path
# SPACING = (len(path)/len(colors)) #palette of len(colors) colors distributed evenly along the path with spacing SPACING
# gridImg = Image.new("RGBA", (sheet.ncols, sheet.nrows))
# iDraw = ImageDraw.Draw(gridImg)
# for i in range(len(path)):
#   coords = path[i]
#   iDraw.point((coords[0], coords[1]), fill=colors[4])#colors[int(i/SPACING)])
# gridImg = gridImg.resize(image.size, resample=PIL.Image.NEAREST)
# ##gridImg = gridImg.filter(ImageFilter.BLUR)
# image.paste(gridImg, mask =gridImg)
# gridImg.close()

###draw path as grid of rectangles
for i in range(len(path)):
# print(coords)
 coords = path[i]
 topLeft = (coords[0] * WIDTH, coords[1] * HEIGHT)
 bottomRight = (topLeft[0] + WIDTH, topLeft[1] + HEIGHT)
 imgDraw.rectangle(topLeft + bottomRight, outline='black', fill=colors[4])
### print(WIDTH)

#display location names on satellite map of output img
alternate = False #used to alternate colors for readibility
for key, value in dictionary.items(): #does not use sorted locations
  topLeft = (value[1] * WIDTH, value[0] * HEIGHT)
  background = (topLeft[0] -1 , topLeft[1] -1)
  if alternate:
    imgDraw.text(background, key, fill="#ffffff")
    imgDraw.text(topLeft, key, fill=colors[0])
  else:
    imgDraw.text(background, key, fill="#ffffff")
    imgDraw.text(topLeft, key, fill=colors[1])
  alternate = not alternate

#draw start, end
imgDraw.text((start.x*WIDTH-1, start.y*HEIGHT-1), "start", fill="#ffffff")
imgDraw.text((start.x*WIDTH, start.y*HEIGHT), "start", fill=colors[2])
imgDraw.text((end.x*WIDTH-1, end.y*HEIGHT-1), "end", fill="#ffffff")
imgDraw.text((end.x*WIDTH, end.y*HEIGHT), "end", fill=colors[3])

# image.show() #does nothing

#save img
image.save(OVERLAY_IMG_OUT_lOCATION)
image.close()
print("saved image as " + OVERLAY_IMG_OUT_lOCATION)