import tkinter as tk
import sounddevice as sd
import numpy as np
import math
import pyaudio
from scipy import signal
import threading



class Button():
    def __init__(self, canvas, posx, posy, dimx, dimy, buttonType, currentFreq, chord, mouseDisabled): #Parameters : Canvas that the button will be placed on, x Position, y Position, x Dimension, y Dimension, Button Type, Frequency of The Chord it will play, Chord, Disable Mouse Input 
        self.c = canvas
        self.type = buttonType
        self.mouseDisabled = mouseDisabled
        self.currentFreq = currentFreq
        self.chord = chord
        
        self.dimxperc = 19 / 29 # analogies for the shape of the button 
        self.dimyperc = 0.625   # analogies for the shape of the button
        self.isClicking = False # button is not clicked when created     
        
        #Depending of the button type, the button can be white or black
        if self.type != 5:
            self.fill = "#DDDDDD"
        else:
            self.fill = "#080808"
        
        #Creates a polygon on the piano Canvas, according to the button type
        self.button = self.c.create_polygon(self.cords(posx, posy, dimx, dimy), fill = self.fill, outline = "black") # creation of Piano Key Polygon

        #If the mouse Input is not disabled
        if not self.mouseDisabled:
            self.c.tag_bind(self.button, "<Button-1>", self.clicked)            #binding to left click to the Button Polygon
            self.c.tag_bind(self.button, "<ButtonRelease-1>", self.notclicked)  #binding to left click release to the Button Polygon
        
        
    def clicked(self, event):
        if not self.isClicking:
            self.thread = threading.Thread(target = self.playNote, args = (self.chord,)) #Thread
            #if clicked its changes color to grey until the mouse button is released, and isClicking becomes True
            self.c.itemconfig(self.button, fill = "grey") 
            self.isClicking = True
            self.thread.start() #it initiates a thread, which plays the sound of the Chord(Note)
            

    def notclicked(self, event):
        #when released the button returns to its original color and isClicking becomes False
        if self.isClicking:
            self.c.itemconfig(self.button, fill = self.fill) 
            self.isClicking = False
            

    def playNote(self, chord):
        #plays the Note
        p = pyaudio.PyAudio()
        stream = p.open(format = pyaudio.paFloat32, channels = 1, rate = 22050, output = True)
        stream.write(chord)
        

    def cords(self, x0, y0, width, height): 
        # gets cordinates for polygon according to type of piano key
        self.extrax = self.dimxperc * width
        self.extray = self.dimyperc * height

        if self.type == 1: #cordinates for type 1 Buttons
            return [x0, y0, x0, y0 + height, x0 + width, y0 + height, x0 + width, y0]
        elif self.type == 2: #cordinates for type 2 Buttons
            return [x0, y0, x0, y0 + height, x0 + width, y0 + height, x0 + width, y0 + self.extray, x0 + self.extrax, y0 + self.extray, x0 + self.extrax, y0]
        elif self.type == 3: #cordinates for type 3 Buttons
            return[x0, y0 + self.extray, x0, y0 + height, x0 + width, y0 + height, x0 + width, y0, x0 + width - self.extrax, y0, x0 + width - self.extrax, y0 + self.extray]
        elif self.type == 4: #cordinates for type 4 Buttons
            return [x0, y0 + self.extray, x0, y0 + height,\
                    x0 + width, y0 + height, x0 + width, y0 + self.extray,\
                    x0 + self.extrax, y0 + self.extray, x0 + self.extrax, y0,\
                    x0 + width - self.extrax, y0, x0 + width - self.extrax, y0 + self.extray]
        elif self.type == 5: #cordinates for type 5 Buttons
            return[x0, y0, x0, y0 + height, x0 + width, y0 + height, x0 + width, y0]



class EventHandler(): # event handler is a frame, that has a system to detect keyboard events 
    def __init__(self, root, disableKeyboard):
        print("EventHandler Initiated")
        self.root = root
        self.disableKeybooard = disableKeyboard #When input from the keyboard is disabled, this variable is True 
        self.clicking = False

        self.frame = tk.Frame(self.root, width=100, height=100, bg = "grey")

        self.frame.bind("<KeyPress>", self.keydown) #bound to keyboard keys press
        self.frame.bind("<KeyRelease>", self.keyup) #bound to keyboard keys release
        self.frame.pack(expand = True, fill = "both")

        #If the keyboard Input is not disabled
        if not self.disableKeybooard:
            self.frame.focus_set() #It gets "notified", when there is an event

        self.keyToButton = {} #Dictionary: key character ==> Piano Button
        self.buttonList = [] #List : Includes all the Piano Buttons
        print("EventHandler SetupCompleted")


    def keydown(self, event):
        #Is executed when a key is pressed
        try:
            self.keyToButton[event.char].clicked(event) #Gets the button that is connected to the character pressed on the keyboard, from the self.keyToButton dictionary, and then calls its method .clicked()
            self.keyToButton[event.char].clicking = True #Each time a button is pressed its own clicking variable, which indicates if a button is pressed or not, turns True, so it cannot be pressed continiously
        except:
            pass
            

    def keyup(self, event):
        #Is executd when a key is released
        try:
            self.keyToButton[event.char].notclicked(event) #Gets the button that is connected to the character released on the keyboard, from the self.keyToButton dictionary, and then calls its method .notclicked()
            self.keyToButton[event.char].clicking = False #Each time a button is released its own clicking variable, which indicates if a button is clicked or not, turns False, so it can be pressed again
        except:
            pass



#Functions used to create the Chord
def make_wave(freq, duration, sample_rate = 22050): #makes a sin wave 
    wave = []
    duration = 0.1

    for i in range(0, math.ceil(duration) * sample_rate):
        wave.append(i / ((sample_rate / (2 * np.pi)) / freq))

    wave = np.sin(np.stack(wave))
    return wave


def make_wave2(freq, duration, sample_rate = 22050): #makes sawtooth wave 
    wave = []
    duration = 0.1

    for i in range(0, math.ceil(duration) * sample_rate):
        wave.append(i / ((sample_rate / (2 * np.pi)) / freq))

    wave = signal.sawtooth(np.stack(wave))
    return wave


def chordGenerator(x): #x is the frequency, according to which, the chord is created 
    duration = 0.1
    sample_rate = 22050
    major3_aprox = 1.26
    perfect5_aprox = 1.50

    #With R we represent the rootnotes
    R = make_wave(x, 10)
    R2 = make_wave2(x, 10)
    R2 = 0.002 * R2
    R12 = make_wave(x / 2, 10)
    R12 = 0.7 * R12
    M3 = make_wave(x * major3_aprox, 10)
    M3 = 0.4 * M3
    P5 = make_wave(x * perfect5_aprox, 10)
    P52 = make_wave((x * perfect5_aprox)/2, 10)
    P52 = 0.001 * P52
    P5 = 0.01 * P5

    chord = R + R2 + R12 + M3 + P5 + P52 #all these rootnotes are summed so each chord has a fading and more realistic sound
    chord = chord * 1.5

    for i in range(2000, math.ceil(duration) * sample_rate):
        chord[i] = chord[i] / (i ** (1 / 2))

    for i in range(0, 2000):
        chord[i] = chord[i] / (2001 - (i ** 2))

    chord = np.array(chord)
    chord = (chord).astype(np.float32).tobytes()
    return chord



class Piano():
    def __init__(self, myParent, eventHandler, mouseDisabled):
        self.myParent = myParent
        self.eventHandler = eventHandler
        self.mouseDisabled = mouseDisabled #This var indicated whether the mouse input is disabled or not
        
        startingFreqList = [261.63, 523.25, 1046.5, 2093] #These are the starting frequencies that the user can change between
        self.freqIndex = 0 
        self.currentFreq = startingFreqList[self.freqIndex]
        

    def piano(self):
        #Lists of the keyboard keys that will be used
        buttonKeys1 = ["q", "w", "e", "r", "t", "y", "u", "z", "x", "c", "v", "b", "n", "m", ","]
        buttonKeys2 = ["2", "3"]
        buttonKeys3 = ["5", "6", "7"]
        buttonKeys4 = ["s", "d"]
        buttonKeys5 = ["g", "h", "j"]

        #Dimensions of the Buttons
        dimxWhite = 46
        dimyWhite = 200
        dimxBlack = 30
        dimyBlack = 125

        startingFreq = 261.63 #Starting Frequency 

        c = tk.Canvas(self.myParent, bg = "white")  #Canvas for piano (is picked within the event handler frame)
        c.pack(expand=True, fill="both")

        #At first the frequency of the current note is calculated, and then according to the buttonType, a button is created 
        for i in range(0,15):
            if i < 3: 
                currentFreq = startingFreq * 2 ** ((i * 2) / 12)
            elif i < 8:
                currentFreq = startingFreq * 2 ** ((i * 2 - 1) / 12)
            elif i < 11:
                currentFreq = startingFreq * 2 ** ((i * 2 - 2) / 12)
            elif i < 14:
                currentFreq = startingFreq * 2 ** ((i * 2 - 3) / 12)
            else:
                currentFreq = startingFreq * 2 ** ((i * 2 - 4) / 12)

            chord = chordGenerator(currentFreq) #The chord is generated according to the current Button's chord frequency 

            #In this for loop, the white Buttons are created
            if i == 0 or i==3 or i==7 or i==10 :
                b = Button(c, 46 * i, 0, dimxWhite, dimyWhite, 2, currentFreq, chord, self.mouseDisabled)
            elif i ==1 or i== 4 or i==5 or i==8 or i==11 or i ==12:
                b = Button(c, 46 * i, 0, dimxWhite, dimyWhite, 4, currentFreq,chord, self.mouseDisabled)
            elif i ==2 or i== 6 or i==9 or i==13:
                b = Button(c, 46 * i, 0, dimxWhite, dimyWhite, 3, currentFreq, chord, self.mouseDisabled)
            else :
                b = Button(c, 46 * i, 0, dimxWhite, dimyWhite, 1, currentFreq, chord, self.mouseDisabled)
            
            self.eventHandler.keyToButton[buttonKeys1[i]] = b #Each time a button is created it is stored in a dictionary (keyToButton), with the key being the character "bound" to this Button
            self.eventHandler.buttonList.append(b) #Each button instance is stored in a list so later on, the chord it plays can be changed more easily

        #These for loops create the black Buttons
        for i in range(2): 
            currentFreq = startingFreq * 2 ** ((2 * i + 1) / 12)
            chord = chordGenerator(currentFreq)
            b = Button(c, (i*46)+31.1, 0, dimxBlack, dimyBlack, 5, currentFreq, chord, self.mouseDisabled)
            self.eventHandler.keyToButton[buttonKeys2[i]] = b
            self.eventHandler.buttonList.append(b)

        for i in range(3):
            currentFreq = startingFreq * 2 ** ((2 * i +  6) / 12)
            chord = chordGenerator(currentFreq)
            b = Button(c, (i * 46) + 169, 0, dimxBlack, dimyBlack, 5, currentFreq, chord, self.mouseDisabled)
            self.eventHandler.keyToButton[buttonKeys3[i]] = b
            self.eventHandler.buttonList.append(b)

        for i in range(2):
            currentFreq = startingFreq * 2 ** ((2 * i + 13) / 12)
            chord = chordGenerator(currentFreq)
            b = Button(c, (i*46)+353, 0, dimxBlack, dimyBlack, 5, currentFreq, chord, self.mouseDisabled)
            self.eventHandler.keyToButton[buttonKeys4[i]] = b
            self.eventHandler.buttonList.append(b)

        for i in range(3):
            currentFreq = startingFreq * 2 ** ((2 * i + 18) / 12)
            chord = chordGenerator(currentFreq)
            b = Button(c, (i * 46) + 491, 0, dimxBlack, dimyBlack, 5, currentFreq, chord, self.mouseDisabled)
            self.eventHandler.keyToButton[buttonKeys5[i]] = b
            self.eventHandler.buttonList.append(b)


    def piano_modules(self):
        #Plus and Minus Widgets to change octave
        self.plus_sign = tk.PhotoImage(file = "images\plus_sign.png")
        self.minus_sign = tk.PhotoImage(file = "images\minus_sign.png")
        self.plus_button = tk.Button(self.myParent,image = self.plus_sign, command = self.increaseStartingFreq, borderwidth = 0, bg = "white")
        self.minus_button = tk.Button(self.myParent, image = self.minus_sign, command = self.lowerStartingFreq, borderwidth = 0, bg = "white")
        self.plus_button.place(x = 650,y = 220)
        self.minus_button.place(x = 650,y = 265)


    def lowerStartingFreq(self): #This method is used to lower the Octave of the Piano
        if self.freqIndex > 0: #Checks if this is possible (the user doesn't already use the lowest Octave)
            print(f"{self.freqIndex} => {self.freqIndex - 1}")
            self.freqIndex -= 1
            for button in self.eventHandler.buttonList: #for each Button in buttonList
                button.currentFreq /= 2 #it divides its current Frequency in half
                button.chord = chordGenerator(button.currentFreq) #according to its new current Frequency, each button is assigned a new chord


    def increaseStartingFreq(self): #This method is used to lower the Octave of the Piano
        if self.freqIndex < 3: #Checks if this is possible (the user doesn't already use the highest Octave)
            print(f"{self.freqIndex} => {self.freqIndex + 1}")            
            self.freqIndex += 1
            for button in self.eventHandler.buttonList: #for each Button in buttonList
                button.currentFreq *= 2 #it doubles its current Frequency 
                button.chord = chordGenerator(button.currentFreq) #according to its new current Frequency, each button is assigned a new chord

        

        
#This part is executed only if project.py is executed directly
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("690x300")

    #At the beginning of the piano, both mouse and keyboard input is enabled
    disableKeyboard = False
    disableMouse = False

    e = EventHandler(root, disableKeyboard) #Event Handler for keyboard input is initiated
    piano = Piano(e.frame, e, disableMouse) 
    
    piano.piano() #Piano is created
    piano.piano_modules() #Piano modules are created
    root.mainloop()
