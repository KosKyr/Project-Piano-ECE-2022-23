import tkinter as tk
from PIL import ImageTk,Image
import project as PianoFile


class MenuHandler():
    def __init__(self, myParent):
        self.mainMenu(myParent)


    def mainMenu(self, myParent): #Main Menu 
        self.root = myParent
        self.root.resizable(False, False)
        self.playButtonClicked = False
        self.infoButtonClicked = False
        self.settingsButtonClicked = False
        self.mouseDisabled = False
        self.keyboardDisabled = False

        img_bg = tk.PhotoImage(file = "images\mlsb.png") #Background Image
        labelbg= tk.Label(self.root, image = img_bg)
        labelbg.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        img0= tk.PhotoImage(file= "images\PIANO.TEXT.png")  #Title Image
        img0_l = tk.Label(self.root, image = img0, borderwidth = 0)
        img0_l.pack()

        #Main Menu Buttons
        img1=tk.PhotoImage(file= "images\PLAYPIANO.png") 
        img2=tk.PhotoImage(file= "images\SETTINGS.png") 
        img3=tk.PhotoImage(file= "images\INFO.png")
        img1_l=tk.Label(image = img1)
        img2_l=tk.Label(image = img2)
        img3_l=tk.Label(image = img3)
        pianoButton= tk.Button(self.root, image = img1, borderwidth = 0, command = self.openPiano) #Play Button
        settingsButton=tk.Button(self.root, image = img2 ,borderwidth = 0, command = self.openSettings) #Settings Button
        infoButton=tk.Button(self.root, image = img3, borderwidth = 0, command = self.openInfo) #Info Button
        pianoButton.pack()
        settingsButton.pack()
        infoButton.pack()

        self.root.mainloop()


    def openPiano(self): 
        if not self.playButtonClicked:
            self.playButtonClicked = True

            #Initialize Piano Window 
            print("Piano Opened")
            self.pianoTopLevel = tk.Toplevel(self.root)
            self.pianoTopLevel.geometry("690x300")
            self.pianoTopLevel.resizable(False, False)
            e = PianoFile.EventHandler(self.pianoTopLevel, self.keyboardDisabled) #Event handler, for the keyboard input is initiated
            piano = PianoFile.Piano(e.frame, e, self.mouseDisabled) #A piano instance is created
            piano.piano() #The piano is created
            piano.piano_modules() #The piano modules are created

            #When closing the window
            def on_closing():
                self.playButtonClicked = False
                self.pianoTopLevel.destroy()
            self.pianoTopLevel.protocol("WM_DELETE_WINDOW", on_closing)

            self.pianoTopLevel.mainloop()


    def openInfo(self):
        if not self.infoButtonClicked:
            self.infoButtonClicked = True

            #Initialize the Info window
            print("Info Opened")
            self.infoTopLevel = tk.Toplevel(self.root)
            self.infoTopLevel.geometry("700x700")
            self.infoTopLevel.resizable(False, False)
            imginfo=tk.PhotoImage(file = "images\INFO.DEF.png") #Info Image
            labelinfo = tk.Label(self.infoTopLevel, image = imginfo)
            labelinfo.place(x = 0, y = 0, relwidth = 1, relheight = 1)

            #When closing the window
            def on_closing():
                self.infoButtonClicked = False
                self.infoTopLevel.destroy()
            self.infoTopLevel.protocol("WM_DELETE_WINDOW", on_closing)

            self.infoTopLevel.mainloop()


    def openSettings(self):
        if not self.settingsButtonClicked:
            self.settingsButtonClicked = True

            #Initialize the Settings window
            print("Settings Opened")
            self.settingsTopLevel = tk.Toplevel(self.root)
            self.settingsTopLevel.geometry("400x200")
            self.settingsTopLevel.resizable(False, False)
            
            imgset = tk.PhotoImage(file = "images\defsettings.png")  #Settings Title Image
            imgset_l = tk.Label(self.settingsTopLevel, image = imgset, borderwidth = 0)
            imgset_l.pack()

            #Variables for the CheckButtons' values
            var1=tk.IntVar(value = self.mouseDisabled)
            var2=tk.IntVar(value = self.keyboardDisabled)


            c1 = tk.Checkbutton(self.settingsTopLevel, text = 'Disable Mouse Input', variable = var1, font = 'Arial 15') #Disable Mouse Input Checkbutton
            c1.pack()
            c2 = tk.Checkbutton(self.settingsTopLevel, text = 'Disable Keyboard Input',variable = var2, font = 'Arial 15') #Disable Keyboard Input Checkbutton
            c2.pack()

            #When closing the window with the save button
            imgsave = tk.PhotoImage(file = "images\save.png") #Save Image
            imgsave_l = tk.Label(image = imgsave)
            def saveAndExit():
                self.settingsButtonClicked = False
                self.settingsTopLevel.destroy()
                #If the save button is pressed, the value of the Checkboxes is stored
                self.mouseDisabled = bool(var1.get()) 
                self.keyboardDisabled = bool(var2.get())
                print(self.mouseDisabled, self.keyboardDisabled)
            btnsave= tk.Button(self.settingsTopLevel, image = imgsave, borderwidth = 0, command = saveAndExit) #Save Button
            btnsave.pack()

            #When closing the window without saving
            def on_closing():
                self.settingsButtonClicked = False
                self.settingsTopLevel.destroy()
            self.settingsTopLevel.protocol("WM_DELETE_WINDOW", on_closing)
            self.settingsTopLevel.mainloop()



#Runs when the app is executed
if __name__ == "__main__":
    root = tk.Tk() #Main Window
    root.title('ece.piano')
    root.geometry('500x400')

    m = MenuHandler(root) #Initialize MenuHandler

    root.mainloop()
