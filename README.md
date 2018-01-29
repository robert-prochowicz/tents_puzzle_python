# tents_puzzle_python
A Python program that solves Tents puzzle (other names: Tents and Trees, Camping puzzle, Architect puzzle, Zeltlager). The first program transforms an image of the puzzle into a numeric form. The second part applies a set of scenarios that finally leads to a solution of the puzzle. I have managed to solve the most difficult puzzles with this program. I know, it is too big and the code is to dirty. And the program should not run all the scenarios, but use some kind of decision tree to solve it. However, this approach with scenarios also has some advantages: you can see which scenarios are working, and wich aren't when you solve it just with a pencil in your hand.
I really, really plan to clean the code and make it easier to understand. But you know how it is with free time...

#### 1) pil_script.py + a04621.jpg (example scan of a puzzle - medium difficulty) ####
This program transforms an image of the puzzle into a numeric form so you can use it in the second program

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

### 2)basenyPyCharm5.py + examples.py ###
This is the actual solver of the puzzle.
examples.py - this file contains examples of puzzles: easy and pretty difficult. It also contains snapshots - half-solved puzzles which I struggled with until I found a working solving scenario. Just pick an example and use it's name in basenyPyCharm5.py file.

basenyPyCharm5.py - actual solver . Run the program and select the option from menu. Choose a scenario you want to apply. Statistics will show if you are making any progress. Try different scenarios in loops until you solve the puzzle.

In my program House means Tent, Tank means Tree. Just so you know.
