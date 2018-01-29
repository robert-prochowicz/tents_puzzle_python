'''
Author: Robert Prochowicz, AUG 2017

1. Scanning the image
Scan the image. Use .jpg format.
If you can't scan it take a picture
Make sure the book is flat
In order to avoid distortions of lines make sure the lens is above the center of the image and that your camera is leveled.
2. Preparing the scan
Crop the picture on the external edges of the grid. If the lines are very skewed, retake the picture. During cropping you can crop out a few pixels of the grid if necessary.
Calculate number of columns and rows and multiply it by 40
Resize the image to that values. For example your image is 15 rows and 10 columns. Resize the image to 400 pixels width and 600 pixel height. Do not preserve aspect ratio.
Change to grayscale. In image editor open Levels. In input levels window move the sliders to make white color more white  and black more black. You can place all three sliders in the same spot in the middle of the scale.
3. Numbers
In notepad type the numbers from headers of columns (for example: 5,2,4,3...). In order to avoid typos do it twice and compare both strings. Repeat for rows.
Count Houses in the image. You can also sum numbers from the columns header (or rows, it doesn't matter)
'''
from PIL import Image

w=20 # enter
h=16 # enter
size=30 # enter size of the square you defined by resizing the image
headers = '6,2,5,2,6,2,3,3,3,3,2,5,2,4,2,6,1,3,4,4;9,0,6,2,5,4,4,4,3,6,3,5,4,4,2,7' #enter
basenIm = Image.open('a04621.jpg') #enter picture name
sensitivity = 220 # play with this parameter (140-250) if the script doesn't recognize houses properly
grid=''
sum_col_header=0

for i in headers.split(";")[0].split(","):
    sum_col_header+=int(i)

def get_avg(x1,x2,y1,y2): # get AVG value of Red color in one square
    red_sum=0
    r='.'
    for x in range(x1,x2):
        for y in range(y1,y2):
            red=basenIm.getpixel((x,y))[0]
            red_sum += red
    if red_sum/(size*size)<sensitivity:
        r='X'
    return r #return . or X

for j in range(0,h): #scan all squares and get value of r, append this value to grid
    for i in range(0,w): 
        r=get_avg(i*size,(i+1)*size,j*size,(j+1)*size)
        grid += r
        
riddle = headers + ';' + grid

sum_house_picture = grid.count('X')
print("Number of houses:")
print("- from the columns header:                   ",sum_col_header)
print("- identified by the script from the picture: ",sum_house_picture)
if sum_col_header!=sum_house_picture:
    print("\nERROR! \n The two numbers above should be equal! Check the scanned houses. \n")
print("\nCopy/paste this to the script that solves the puzzle: ")
print(riddle)
