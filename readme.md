## Eventer

Main purpose: get action sequences from json file and run them one by one. 
<br />
So the user can "program" specific sequences and run them by button click(button auto-generate for each sequense) 
<br />
The project based on: tkinter, pyautogui, pynput 

------------

### Supported commands:
- Mouse click
- Mouse move
- Mouse scroll
- Mouse click at specific image of the screen
- Enter text

------------

### Command specific properties:
- XY position
- Count of the action repeats
- Delay after executed action 
- Enable/Disable

------------

### UpdateFromList:
Additional feature which do some automation:
 1. Parse list of provided web-sites
 2. Open web page on the browser
 3. Perform command sequence (from json file)
 4. Close web page
 5. Repeat 1-4 for each web resource from the list

------------

### Cursor position types:
There are two main cursor position type available: <br />

            absolute:
    0,0                        
    +---------------------------+
    |                        +X |  
    |                           |     
    |                           |
    |                           |     
    |                           |
    | +Y                        |
    +---------------------------+ 


               axis2d:
    0,0
    +---------------------------+
    |             | +Y          | 
    |             |             |    
    | -X          | 0,0      +X |
    |-------------|-------------| 
    |             |             |
    |             |             |
    |             | -Y          |
    +---------------------------+ 

------------

### Note:

The program work in a specific way in a multi-monitor systems:

    -1920,0                        0,0                            1920,0                 3839,0
    +---------------------------+  +---------------------------+  +---------------------------+
    |                           |  |                           |  |                           |  
    |                           |  |                           |  |                           |   
    |       Left screen         |  |        Main screen        |  |        Right Screen       |   
    |                           |  |                           |  |                           |     
    |                           |  |                           |  |                           |   
    |                           |  |                           |  |                           |   
    +---------------------------+  +---------------------------+  +---------------------------+ 
    -1920,1080                     0,1080                          1920,1080          3839,1080

------------

#### Screenshots
There is posibility to take screenshot from the screen with specific width/height
Saved screenshots could be used in the actions at the json file ("image" field)