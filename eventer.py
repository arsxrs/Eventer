from pynput.keyboard import Key, Listener as KeyListener, Controller as KeyboardController
from pynput.mouse import Button as MouseButton, Listener as MouseListener, Controller as MouseController
from time import sleep
import pyautogui
import webbrowser
import json
import re
import tkinter as tk
from PIL import Image, ImageTk


# Global data
root = tk.Tk()
screen_size = pyautogui.size()
keyboard_ctrl = KeyboardController()
# mouse_ctrl = MouseController()
mouse_position = tk.StringVar()
program_running = False


def start_process():
    global program_running
    program_running = True


def stop_process():
    global program_running
    program_running = False


def is_process_running():
    return program_running


class Eventer:

    def __init__(self):
        self.text_widget = None
        self.resources = []
        self.program_running = False

        # Read json file
        with open('map.json',  'r', encoding='utf-8') as json_file:
            # Reading from json file
            json_data = json.load(json_file)

        # Retrieve available resources
        for item in json_data['resources']:
            self.resources.append(item)

        keyboard_listener = KeyListener(on_press=self.on_press, on_release=None)
        keyboard_listener.start()
        mouse_listener = MouseListener(on_move=self.on_move, on_click=None, on_scroll=None)
        mouse_listener.start()

        self.init_gui()

    def init_gui(self):

        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        root.title("Eventer")
        root.attributes('-topmost', True)

        root.update()
        frame1 = tk.ttk.Frame(root)
        frame2 = tk.ttk.Frame(root)
        frame3 = tk.ttk.Frame(root)

        frame1.grid(row=0, column=0, sticky=tk.N+tk.W, pady=(2, 0), padx=(0, 15))
        frame2.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W, pady=(29, 0))
        frame3.grid(row=1, column=0, sticky=tk.S+tk.W)

         # Create special button for get resources from the list
        btn = tk.ttk.Button(frame1, text="Get from list")
        btn.bind("<ButtonRelease>", lambda event, text="UpdateFromList": self.button_event_handler(text))
        btn.pack(side=tk.LEFT, fill="both")

        # Create action buttons for available resources
        for item in self.resources:
            btn = tk.ttk.Button(frame1, text=item['name'])
            btn.bind("<ButtonRelease>", lambda event, text=item['name']: self.button_event_handler(text))
            btn.pack(side=tk.LEFT, fill="both")

        # Create text box for list of resources
        scrollbar = tk.ttk.Scrollbar(frame2)
        self.text_widget = tk.Text(frame2, height=2, width=30, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.pack(side="left",  fill="both", expand=True,)

        btn = tk.ttk.Button(frame3, text="SC", width=4, command= lambda : self.Screnshot())
        btn.pack(side=tk.LEFT, fill="both", padx=2)

        # Mouse Position label
        label = tk.ttk.Label(frame3, textvariable=mouse_position)
        label.pack(side=tk.LEFT, fill="both")

        root.mainloop()

    class Screnshot:

        def __init__(self):
            self.file_name = "screenshot.png"
            self.window = tk.Toplevel(root)
            self.window.attributes('-topmost', True)
            self.window.title("Screenshot")

            self.X = tk.StringVar(self.window)
            self.Y = tk.StringVar(self.window)
            self.W = tk.StringVar(self.window)
            self.H = tk.StringVar(self.window)

            tk.ttk.Label(self.window, text="X:").grid(row=0, column=0, padx=5, sticky="w")
            tk.ttk.Label(self.window, text="Y:").grid(row=1, column=0, padx=5, sticky="w")
            tk.ttk.Label(self.window, text="W:").grid(row=0, column=2, padx=5, sticky="w")
            tk.ttk.Label(self.window, text="H:").grid(row=1, column=2, padx=5, sticky="w")

            tk.ttk.Spinbox(self.window, width=6, from_= 0, to = screen_size[0], textvariable=self.X).grid(row=0, column=1, padx=0, sticky="w")
            tk.ttk.Spinbox(self.window, width=6, from_= 0, to = screen_size[0], textvariable=self.Y).grid(row=1, column=1, padx=0, sticky="w")
            tk.ttk.Spinbox(self.window, width=6, from_= 0, to = screen_size[0], textvariable=self.W).grid(row=0, column=3, padx=0, sticky="w")
            tk.ttk.Spinbox(self.window, width=6, from_= 0, to = screen_size[0], textvariable=self.H).grid(row=1, column=3, padx=0, sticky="w")

            self.X.set(0)
            self.Y.set(0)
            self.W.set(32)
            self.H.set(32)

            btn = tk.ttk.Button(self.window, text="Take", command=self.take_screenshot)
            btn.grid(row=0, column=4, rowspan=2, sticky="ns")

        def render_image(self):
            self.load = Image.open(self.file_name)
            self.render = ImageTk.PhotoImage(self.load)
            self.img = tk.Label(self.window, image=self.render)
            self.img.image = self.render
            self.img.grid(row=2, column=0, columnspan=5, sticky="ewns")

        def take_screenshot(self):
            x = int(self.X.get()) - (int(self.W.get()) / 2)
            y = int(self.Y.get()) - (int(self.H.get()) / 2)
            w = int(self.W.get())
            h = int(self.H.get())
            pyautogui.screenshot(self.file_name, region=(x, y, w, h))
            self.render_image()

    def button_event_handler(self, button_name):
        start_process()
        if button_name == "UpdateFromList":
            self.process_resource_list()
        else:
            self.process_resource(button_name)
        stop_process()

    def process_resource_list(self):
        while len(self.text_widget.get("1.0", 'end-1c')) and is_process_running():
            text_line = self.text_widget.get("1.0", "1.0 lineend")

            url = self.get_url(text_line)
            matched_resource = self.is_resource_in_json(url)

            if matched_resource:
                if matched_resource['postfix']:
                    url += matched_resource['postfix']

                print("Process url: ",  url)
                webbrowser.open_new_tab(url)
                sleep(5)
                self.process_resource(matched_resource['name'])
                # print("before ctrl w")
                pyautogui.hotkey('ctrl', 'w')  # close tab
                # print("after ctrl w")
            else:
                print("Skip resource as no map for it: ",  url)
            
            if is_process_running():
                self.text_widget.delete("1.0", "2.0")
            root.update()

    def process_resource(self, source):
        resource = None
        repeat = 1
        for item in self.resources:
            if item['name'] == source:
                resource = item
                break
        print(resource['name'])
        if resource:
            if 'repeat' in resource:
                repeat = int(resource['repeat'])
            while repeat:
                repeat -= 1
                for act in resource['actions']:
                    print(act)
                    if is_process_running():
                        if self.Action(act).process():
                            break

    @staticmethod
    def get_url(text_with_url):
        text_with_url = re.sub(r'^.*?https', 'https', text_with_url)
        text_with_url = text_with_url.split(" ", 1)[0]
        return text_with_url

    def is_resource_in_json(self, url):
        resource = None
        for item in self.resources:
            if re.search(item['name'], url, re.IGNORECASE):
                resource = item
        print("Is resource known: ", self.is_resource_in_json)
        return resource

    @staticmethod
    def on_press(key):
        if key == Key.esc:
            stop_process()
            print("Running stopped by user")

    @staticmethod
    def on_move(x, y):

        axis_x = int(x - screen_size[0]/2)
        axis_y = int(screen_size[1]/2 - y)

        absolute_position = str(x) + "," + str(y)
        axis2d_position = str(axis_x) + "," + str(axis_y)
        positions = absolute_position + "  " + axis2d_position
        mouse_position.set(positions)

    class Action:

        def __init__(self, action):
            self.active = False
            self.command = ''
            self.action = None
            self.x, self.y = pyautogui.position()
            self.coordinate_type = "absolute"
            self.delay = 0
            self.repeat = 1
            self.scroll = 0
            self.text = ""
            self.images = []

            if "active" in action and action['active']:
                self.active = True

                if "x" in action:
                    self.x = action['x']

                if "y" in action:
                    self.y = action['y']

                if 'coordinate_type' in action:
                    coordinate_type = action['coordinate_type']
                    self.convert_pos(self.x, self.y, coordinate_type)

                if 'delay' in action:
                    self.delay = action['delay']

                if 'repeat' in action and action['repeat'] > 0:
                    self.repeat = action['repeat']

                if 'command' in action:
                    self.command = action['command']
                    self.get_command()

                if 'scroll' in action:
                    self.scroll = action['scroll']

                if 'text' in action:
                    self.text = action['text']

                if 'image' in action:
                    for img in action['image']:
                        self.images.append(img)

        def get_command(self):
            if self.command == 'click':
                self.action = self.click
            elif self.command == 'click2':
                self.action = self.click2
            elif self.command == 'set_pos':
                self.action = self.set_pos
            elif self.command == 'move':
                self.action = self.move
            elif self.command == 'scroll':
                self.action = self.scroll
            elif self.command == 'click_pos':
                self.action = self.click_pos
            elif self.command == 'click2_pos':
                self.action = self.click2_pos
            elif self.command == 'click_move':
                self.action = self.click_move
            elif self.command == 'move_click':
                self.action = self.move_click
            elif self.command == 'click_scroll':
                self.action = self.click_scroll
            elif self.command == 'click_image':
                self.action = self.click_image
            elif self.command == 'enter_text':
                self.action = self.enter_text

        def process(self):
            result = 0

            if self.active and self.action:
                for i in range(self.repeat):
                    if is_process_running():
                        result = self.action()

                        # Delay after command
                        if self.delay:
                            sleep(self.delay)
            else:
                print("Skip command")

            return result

        def convert_pos(self, in_x, in_y, pos_type):
            pos = (0, 0)
            if pos_type == "absolute":
                pos = (in_x, in_y)
            elif pos_type == "axis2d":
                pos = (int(in_x + screen_size[0] / 2),
                       int(screen_size[1] - (in_y + screen_size[1] / 2)))
            elif pos_type == "percent":
                pos = (int(in_x * screen_size[0] / 100.0),
                       int(in_y * screen_size[1] / 100.0))
            # print(self.name, pos)
            self.x = pos[0]
            self.y = pos[1]

        def click(self):
            pyautogui.click()
            return 0

        def click2(self):
            pyautogui.doubleClick()
            return 0

        def set_pos(self):
            pyautogui.moveTo(x=self.x, y=self.y)
            return 0

        def move(self):
            pyautogui.move(self.x, self.y)
            return 0

        def scroll(self):
            pyautogui.scroll(self.scroll)
            return 0

        def click_pos(self):
            pyautogui.click(x=self.x, y=self.y)
            return 0

        def click2_pos(self):
            pyautogui.doubleClick(x=self.x, y=self.y)
            return 0

        def click_move(self):
            pyautogui.click()
            pyautogui.move(self.x, self.y)
            return 0

        def move_click(self):
            print("move_click:", self.x, self.y)
            pyautogui.move(self.x, self.y)
            pyautogui.click()
            return 0

        def click_scroll(self):
            pyautogui.click(x=self.x, y=self.y)
            pyautogui.scroll(self.scroll)
            return 0

        def click_image(self):
            for img in self.images:
                if is_process_running():
                    print("mouse_click_image:", img)
                    pos = pyautogui.locateCenterOnScreen(img, confidence=0.95)
                    if pos:
                        print("mouse_click_image pos:", pos)
                        pyautogui.click(x=pos.x + self.x, y=pos.y + self.y)
                        return 0
                    else:
                        print("Could not find the image")

            return -1

        def enter_text(self):
            keyboard_ctrl.type(self.text)
            return 0


# Run
Eventer()
