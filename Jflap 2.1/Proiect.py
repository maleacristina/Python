from Tkinter import *
from tkFileDialog import *
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stateId = -1


class TransitionDialog(object):
    def __init__(self, parent):
        self.toplevel = Toplevel(parent, bg="gray")
        self.toplevel.overrideredirect(1)
        self.toplevel.bind("<Return>", self.enter_pressed)
        self.var = StringVar()
        label = Label(self.toplevel, text="Values:", bg="gray")
        entry = Entry(self.toplevel, width=40, textvariable=self.var)
        entry.focus_set()
        button = Button(self.toplevel, text="OK", command=self.set_value, bg="white")

        label.pack()
        entry.pack()
        button.pack()
        self.toplevel.grab_set()
        x = (parent.winfo_x() + parent.winfo_width()) / 2 - 35
        y = (parent.winfo_y() + parent.winfo_height()) / 2 - 33
        self.toplevel.geometry("+%d+%d" % (x, y))
        self.toplevel.wait_window()

    def set_value(self):
        global stateValue
        stateValue = self.var.get()
        self.toplevel.destroy()

    def enter_pressed(self, event):
        self.set_value()


class SaveDialog(object):
    def __init__(self, parent):
        self.toplevel = Toplevel(parent, bg="gray")
        self.toplevel.overrideredirect(1)
        self.toplevel.bind("<Return>", self.enter_pressed)
        self.var = StringVar()
        label = Label(self.toplevel, text="Do you want to save your project?", bg="gray")
        entry = Entry(self.toplevel, width=40, textvariable=self.var)
        entry.focus_set()
        buttonOk = Button(self.toplevel, text="Ok", command=self.set_value, bg="white")
        buttonCancel = Button(self.toplevel, text="Cancel", command=self.cancel_value, bg="white")

        label.pack()
        entry.pack()
        buttonOk.pack()
        buttonCancel.pack()
        self.toplevel.grab_set()
        x = (parent.winfo_x() + parent.winfo_width()) / 2 - 35
        y = (parent.winfo_y() + parent.winfo_height()) / 2 - 33
        self.toplevel.geometry("+%d+%d" % (x, y))
        self.toplevel.wait_window()

    def set_value(self):
        global saveFileName
        saveFileName = self.var.get()
        self.toplevel.destroy()

    def cancel_value(self):
        global saveFileName
        saveFileName = "no name for the file"
        self.toplevel.destroy()

    def enter_pressed(self, event):
        self.set_value()


class Transition:

    def __init__(self, canvasFrame):
        self.canvas = canvasFrame
        self.state1Id = self.state2Id = -1

    def create_line(self, x, y, width, height):
        self.line = self.canvas.create_line(x, y, width, height, arrow="last")

    def create_second_line(self, x, y, width, height):
        self.line2 = self.canvas.create_line(x, y, width, height)

    def create_text(self, value):
        self.value = value
        coords = self.canvas.coords(self.line)
        if self.state1Id != self.state2Id:
            if self.state1Id < self.state2Id:
                self.text = self.canvas.create_text((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2 - 10, text=value, fill="blue")
            else:
                self.text = self.canvas.create_text((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2 + 10, text=value, fill="blue")
        else:
            self.text = self.canvas.create_text(coords[0], coords[1] - 10, text=value, fill="blue")
        self.canvas.tag_bind(self.text, "<ButtonPress-1>", self.remove_item)

    def remove_item(self, event):
        global removeItem, lines
        if removeItem:
            self.canvas.delete(self.line)
            self.canvas.delete(self.text)
            if self.state1Id == self.state2Id:
                self.canvas.delete(self.line2)
            lines.remove(self)

    def move_text(self):
        coords = self.canvas.coords(self.line)
        if self.state1Id != self.state2Id:
            if self.state1Id < self.state2Id:
                self.canvas.coords(self.text, (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2 - 10)
            else:
                self.canvas.coords(self.text, (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2 + 10)
        else:
            self.canvas.coords(self.text, coords[0], coords[1] - 10)


class State:

    def __init__(self, canvasFrame, id):
        self.canvas = canvasFrame
        self.id = id
        self.status = "normal"

    def create_circle(self, x, y, width, height):
        self.circle = self.canvas.create_oval(x, y, width, height, fill="gray")
        self.canvas.tag_bind(self.circle, "<B1-Motion>", self.move_box)
        self.canvas.tag_bind(self.circle, "<ButtonPress-1>", self.start_move)
        self.canvas.tag_bind(self.circle, "<ButtonPress-3>", self.pop_up_menu)
        self.text = self.canvas.create_text((x + width) / 2, (y + height) / 2, text="q" + str(self.id), fill="black")
        self.canvas.tag_bind(self.text, "<B1-Motion>", self.move_box)
        self.canvas.tag_bind(self.text, "<ButtonPress-1>", self.start_move)
        self.canvas.tag_bind(self.text, "<ButtonPress-3>", self.pop_up_menu)

    def pop_up_menu(self, event):
        global window, addState, addTransition, removeItem

        if not addState and not addTransition and not removeItem:
            menu = Menu(window)
            if self.status == "both":
                menu.add_command(label="Remove Initial State", command=self.remove_initial_state)
                menu.add_command(label="Remove Final State", command=self.remove_final_state)
            elif self.status == "initial":
                menu.add_command(label="Remove Initial State", command=self.remove_initial_state)
                menu.add_command(label="Set Final State", command=self.set_final_state)
            elif self.status == "final":
                menu.add_command(label="Set Initial State", command=self.set_initial_state)
                menu.add_command(label="Remove Final State", command=self.remove_final_state)
            else:
                menu.add_command(label="Set Initial State", command=self.set_initial_state)
                menu.add_command(label="Set Final State", command=self.set_final_state)
            menu.post(event.x_root, event.y_root)

    def set_initial_state(self):
        global states
        for state in states:
            if state.id != self.id:
                if state.status == "initial" or state.status == "both":
                    state.remove_initial_state()
        if self.status == "final":
            self.status = "both"
            self.canvas.itemconfig(self.circle, fill="#006600")
        else:
            self.status = "initial"
            self.canvas.itemconfig(self.circle, fill="#0099FF")

    def remove_initial_state(self):
        if self.status == "both":
            self.status = "final"
            self.canvas.itemconfig(self.circle, fill="#FF9900")
        else:
            self.status = "normal"
            self.canvas.itemconfig(self.circle, fill="gray")

    def set_final_state(self):
        if self.status == "initial":
            self.status = "both"
            self.canvas.itemconfig(self.circle, fill="#006600")
        else:
            self.status = "final"
            self.canvas.itemconfig(self.circle, fill="#FF9900")

    def remove_final_state(self):
        if self.status == "both":
            self.status = "initial"
            self.canvas.itemconfig(self.circle, fill="#0099FF")
        else:
            self.status = "normal"
            self.canvas.itemconfig(self.circle, fill="gray")

    def move_box(self, event):
        global addState, addTransition, removeItem, lines, canvas, states

        if not addState and not addTransition and not removeItem:
            deltax = event.x - self.x
            deltay = event.y - self.y
            self.canvas.move(self.circle, deltax, deltay)
            self.canvas.move(self.text, deltax, deltay)
            self.x = event.x
            self.y = event.y
            firstStateCoords = self.canvas.coords(self.circle)

            newX1 = (firstStateCoords[0] + firstStateCoords[2]) / 2
            newY1 = (firstStateCoords[1] + firstStateCoords[3]) / 2

            for line in lines:
                redraw = False
                lineCoords = line.canvas.coords(line.line)
                if line.state1Id != line.state2Id:
                    if self.id == line.state1Id:
                        lineCoords[0] = newX1
                        lineCoords[1] = newY1
                        for state in states:
                            if state.id == line.state2Id:
                                secondStateCoords = state.canvas.coords(state.circle)
                                lineCoords[2] = (secondStateCoords[0] + secondStateCoords[2]) / 2
                                lineCoords[3] = (secondStateCoords[1] + secondStateCoords[3]) / 2
                                break

                        redraw = True
                    elif self.id == line.state2Id:
                        lineCoords[2] = newX1
                        lineCoords[3] = newY1

                        for state in states:
                            if state.id == line.state1Id:
                                secondStateCoords = state.canvas.coords(state.circle)
                                lineCoords[0] = (secondStateCoords[0] + secondStateCoords[2]) / 2
                                lineCoords[1] = (secondStateCoords[1] + secondStateCoords[3]) / 2
                                break
                        redraw = True

                    if redraw:
                        line.canvas.coords(line.line, lineCoords[0], lineCoords[1], lineCoords[2], lineCoords[3])
                        while True:
                                circleCoords = self.canvas.coords(self.circle)
                                lineCoords = line.canvas.coords(line.line)

                                if math.sqrt(((lineCoords[0] - lineCoords[2]) ** 2) + ((lineCoords[1] - lineCoords[3]) ** 2)) < 0.1:
                                    break
                                x = (circleCoords[0] + circleCoords[2]) / 2
                                y = (circleCoords[1] + circleCoords[3]) / 2
                                square_dist = (x - lineCoords[0]) ** 2 + (y - lineCoords[1]) ** 2
                                if square_dist <= 25 ** 2:
                                    line.canvas.scale(line.line, (lineCoords[0] + lineCoords[2]) / 2, (lineCoords[1] + lineCoords[3]) / 2, 0.99, 0.99)
                                    line.move_text()
                                else:
                                    square_dist = (x - lineCoords[2]) ** 2 + (y - lineCoords[3]) ** 2
                                    if square_dist <= 25 ** 2:
                                        line.canvas.scale(line.line, (lineCoords[0] + lineCoords[2]) / 2, (lineCoords[1] + lineCoords[3]) / 2, 0.99, 0.99)
                                        line.move_text()
                                    else:
                                        break
                else:
                    if self.id == line.state1Id:
                        coords = self.canvas.coords(self.circle)
                        x = (coords[0] + coords[2]) / 2
                        y = (coords[1] + coords[3]) / 2
                        line.canvas.coords(line.line2, x - 20, y - 16, x, y - 60)
                        line.canvas.coords(line.line, x, y - 60, x + 20, y - 16)
                        line.move_text()

    def start_move(self, event):
        global addState, addTransition, removeItem, lines, states, statesNumber

        if not addState and not addTransition and not removeItem:
            self.x = event.x
            self.y = event.y
        elif removeItem:
            i = 0
            while i < len(lines):
                if self.id == lines[i].state1Id or self.id == lines[i].state2Id:
                    lines[i].canvas.delete(lines[i].line)
                    lines[i].canvas.delete(lines[i].text)
                    if lines[i].state1Id == lines[i].state2Id:
                        lines[i].canvas.delete(lines[i].line2)
                    lines.remove(lines[i])
                else:
                    i += 1
            self.canvas.delete(self.text)
            self.canvas.delete(self.circle)
            for line in lines:
                if line.state1Id > self.id:
                    line.state1Id -= 1
                if line.state2Id > self.id:
                    line.state2Id -= 1
            for state in states:
                if state.id > self.id:
                    state.id -= 1
                    state.canvas.itemconfig(state.text, text="q" + str(state.id))
            statesNumber -= 1
            states.remove(self)


def add_state_function():

    global addState, addTransition, removeItem

    if addState:
        addState = False
        addStateButton.configure(bg="grey")
    else:
        addState = True
        addTransition = False
        removeItem = False
        addStateButton.configure(bg="white")
        addTransitionButton.configure(bg="grey")
        removeItemButton.configure(bg="grey")
        transitionPoints[:] = []


def add_transition_function():

    global addState, addTransition, removeItem

    if addTransition:
        addTransition = False
        addTransitionButton.configure(bg="grey")
        transitionPoints[:] = []
    else:
        addTransition = True
        addState = False
        removeItem = False
        addTransitionButton.configure(bg="white")
        addStateButton.configure(bg="grey")
        removeItemButton.configure(bg="grey")


def remove_item_function():

    global addState, addTransition, removeItem

    if removeItem:
        removeItem = False
        removeItemButton.configure(bg="grey")
    else:
        removeItem = True
        addState = False
        addTransition = False
        removeItemButton.configure(bg="white")
        addStateButton.configure(bg="grey")
        addTransitionButton.configure(bg="grey")
        transitionPoints[:] = []


def check_canvas_operations(event):
    global addState, addTransition, removeItem, states, stateSize, statesNumber, transitionPoints, lines, window

    if addState:
        state = State(canvas, statesNumber)
        state.create_circle(event.x - stateSize, event.y - stateSize, event.x + stateSize, event.y + stateSize)
        states.append(state)
        statesNumber += 1
    elif addTransition:
        for state in states:
            coords = state.canvas.coords(state.circle)
            x = (coords[0] + coords[2]) / 2
            y = (coords[1] + coords[3]) / 2
            square_dist = (x - event.x) ** 2 + (y - event.y) ** 2
            if square_dist <= 25 ** 2:
                point = Point(x, y)
                point.stateId = state.id
                transitionPoints.append(point)
                break

        if len(transitionPoints) == 2:
            transitionExist = False
            for line in lines:
                if line.state1Id == transitionPoints[0].stateId and line.state2Id == transitionPoints[1].stateId:
                    transitionExist = True
                    break

            if not transitionExist:
                transition = Transition(canvas)
                transition.state1Id = transitionPoints[0].stateId
                transition.state2Id = transitionPoints[1].stateId
                if transitionPoints[0].stateId == transitionPoints[1].stateId:
                    transition.create_second_line(transitionPoints[0].x - 20, transitionPoints[0].y - 16, transitionPoints[0].x, transitionPoints[0].y - 60)
                    transition.create_line(transitionPoints[0].x, transitionPoints[0].y - 60, transitionPoints[0].x + 20, transitionPoints[1].y - 16)
                else:
                    transition.create_line(transitionPoints[0].x, transitionPoints[0].y, transitionPoints[1].x, transitionPoints[1].y)
                    for state in states:
                        if state.id == transition.state1Id:
                            while True:
                                circleCoords = state.canvas.coords(state.circle)
                                lineCoords = transition.canvas.coords(transition.line)
                                if math.sqrt(((lineCoords[0] - lineCoords[2]) ** 2) + ((lineCoords[1] - lineCoords[3]) ** 2)) < 0.1:
                                    break
                                x = (circleCoords[0] + circleCoords[2]) / 2
                                y = (circleCoords[1] + circleCoords[3]) / 2
                                square_dist = (x - lineCoords[0]) ** 2 + (y - lineCoords[1]) ** 2
                                if square_dist <= 25 ** 2:
                                    transition.canvas.scale(transition.line, (lineCoords[0] + lineCoords[2]) / 2, (lineCoords[1] + lineCoords[3]) / 2, 0.99, 0.99)
                                else:
                                    break

                TransitionDialog(window)
                transition.create_text(stateValue)
                lines.append(transition)
            transitionPoints[:] = []


def save_project():
    global lines, states, window, saveFileName
    if len(states) > 0:
        SaveDialog(window)
        if saveFileName != "no name for the file":
            file = open(saveFileName + ".txt", "w")

            file.write("states\n")

            for state in states:
                file.write(str(state.id) + ";")
                file.write(state.status + ";")
                coords = state.canvas.coords(state.circle)
                file.write(str(coords[0]) + ";")
                file.write(str(coords[1]) + ";")
                file.write(str(coords[2]) + ";")
                file.write(str(coords[3]) + "\n")

            file.write("transitions\n")
            for line in lines:
                file.write(str(line.state1Id) + ";")
                file.write(str(line.state2Id) + ";")
                file.write(line.value + ";")
                coords = line.canvas.coords(line.line)
                file.write(str(coords[0]) + ";")
                file.write(str(coords[1]) + ";")
                file.write(str(coords[2]) + ";")
                file.write(str(coords[3]) + "\n")

            file.close()


def clear_project():
    global lines, states, statesNumber, inputDataList, outputDataList
    canvas.delete(ALL)
    lines[:] = []
    states[:] = []
    transitionPoints[:] = []
    #for i in range(0, 8):
     #   inputDataList[i].set("")
     #   outputDataList[i].set("")
    statesNumber = 0


def load_project():
    global states, lines, statesNumber
    fileName = askopenfilename()
    if fileName != "":
        clear_project()
        file = open(fileName, "r")
        readStates = True
        for line in file:
            line = line[:-1]
            if line == "states":
                readStates = True
            elif line == "transitions":
                readStates = False
            elif readStates:
                info = line.split(";")
                state = State(canvas, int(info[0]))
                state.status = info[1]
                state.create_circle(float(info[2]), float(info[3]), float(info[4]), float(info[5]))
                if state.status == "both":
                    state.canvas.itemconfig(state.circle, fill="#006600")
                elif state.status == "initial":
                    state.canvas.itemconfig(state.circle, fill="#0099FF")
                elif state.status == "final":
                    state.canvas.itemconfig(state.circle, fill="#FF9900")
                else:
                    state.canvas.itemconfig(state.circle, fill="gray")
                states.append(state)
                statesNumber += 1
                print line.split(";")
            else:
                info = line.split(";")
                transition = Transition(canvas)
                transition.state1Id = int(info[0])
                transition.state2Id = int(info[1])
                transition.create_line(float(info[3]), float(info[4]), float(info[5]), float(info[6]))
                if transition.state1Id == transition.state2Id:
                    transition.create_second_line(float(info[5]) - 40, float(info[6]), float(info[3]), float(info[4]))
                transition.create_text(info[2])
                lines.append(transition)
                print line.split(";")

        file.close()


def new_project():
    global states
    save_project()
    clear_project()


def close_project():
    global window
    save_project()
    window.destroy()

stateSize = 25
statesNumber = 0
transitionPoints = []
stateValue = ""
saveFileName = ""

window = Tk()
window.wm_title("JFLAP")
window.protocol('WM_DELETE_WINDOW', close_project)
menu = Menu(window)
window.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New Project", command=new_project)
subMenu.add_command(label="Save Project", command=save_project)
subMenu.add_command(label="Load Project", command=load_project)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=window.destroy)

topFrame = Frame(window)
topFrame.pack(side=TOP)
#bottomFrame = Frame(window)
#bottomFrame.pack(side=BOTTOM)
middleFrame = Frame(window)
middleFrame.pack(side=BOTTOM)


addStateButton = Button(topFrame, text="Add State", bg="grey", command=add_state_function)
addStateButton.pack(side=LEFT)
addState = False

addTransitionButton = Button(topFrame, text="Add Transition", bg="grey", command=add_transition_function)
addTransitionButton.pack(side=LEFT)
addTransition = False

removeItemButton = Button(topFrame, text="Remove Item", bg="grey", command=remove_item_function)
removeItemButton.pack(side=LEFT)
removeItem = False

canvas = Canvas(middleFrame, width=700, height=500, bg="white", borderwidth=5, highlightbackground="black")
canvas.pack()
canvas.bind("<ButtonPress-1>", check_canvas_operations)

#inputDataList = []
#outputDataList = []
#column1 = Label(bottomFrame, text="Inputs")
#column2 = Label(bottomFrame, text="Results")
#column1.grid(row=0, column=0)
#column2.grid(row=0, column=1)

#for i in range(1, 9):
    #inputData = StringVar()
    #inputDataList.append(inputData)
    #Entry(bottomFrame, borderwidth=2, textvariable=inputDataList[i - 1]).grid(row=i, column=0)
    #outputData = StringVar()
   # outputDataList.append(outputData)
    #Entry(bottomFrame, borderwidth=2, state=DISABLED, textvariable=outputDataList[i - 1]).grid(row=i, column=1)
#inputDataList[5].set("ceva")

lines = []
states = []

window.mainloop()
