import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import cv2
import os
import shutil
import mainframe
from PIL import Image, ImageTk
import presetBuilder
import webbrowser
aRow = 0
aColumn = 0
fileContent = []
deletedPresetList = []

def myportfolio():
    webbrowser.open_new('https://kishlaykumar.me')

def openprojectrecord():
    webbrowser.open_new('#')

def filename(fp):
    fn = fp.split('/')
    return fn[len(fn)-1]

def deletetemp():
    global root
    try:
        shutil.rmtree(".temp")
    except:
        print("Couldn't delete directory temp")
    root.destroy()

def deletePreset(lineIndex,presetFrame,presetName):
    global rootCanvas
    global fileContent
    global deletedPresetList

    confirm = messagebox.askyesno("Confrim","Are you sure you want to delete \""+str(presetName)+"\" preset ?")

    if confirm:
        fileContent[lineIndex] = ""

        with open('.presets','w+') as f:
            for line in range(len(fileContent)):
                f.write(fileContent[line])

        #Deleted Log
        print("Deleted Preset " + str(presetName))

        #Destroying That Frame
        presetFrame.destroy()
        root.update() 

def createNewPreset():
    global root

    messagebox.showinfo("For Making New Preset", "To make a new preset please open a blank omr sheet.")

    #Reading The File
    ftype = [('JPEG','*.jpg'),('PNG','*.png')]
    dlg = filedialog.Open(filetypes = ftype)
    fp = dlg.show()     #Gives path of the open file
    fn = filename(fp)   #Returns File Name
    
    #Creating temp Folder For opencv access
    try:
        os.mkdir(".temp")
    except OSError:
        print("Failed to make temp folder")

    #Copying Image to the temp folder
    destination = os.getcwd() + "/.temp/" + fn
    try:
        dest = shutil.copyfile(fp,destination)
        #Final File Path
        image_path = ".temp/"+str(fn)

        # Load an color image
        img = cv2.imread(image_path)

        root.destroy()
        presetBuilder.main(img)
    except Exception as e:
        print("failed to copy file into temp : " + str(e))

def buildNewPresetButton():
    global aRow,aColumn,rootCanvas
    aRow = 0
    aColumn = 0

    newPresetFrame = tk.LabelFrame(rootCanvas,text="New Preset",width=100,height=100,padx=10,pady=5)
    newPresetFrame.grid(row=aRow,column=aColumn,sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=5)
    
    #New Preset Button
    newPresetButton = tk.Button(newPresetFrame,text="+",command=createNewPreset,width=15,height=5)
    newPresetButton.pack(fill=tk.BOTH,expand=True)

    #Increments
    aColumn += 1

def usePreset(presetIndex):
    global root
    methodWindow = tk.Tk()
    methodWindow.title("Choose Method")
    methodWindow.geometry("300x100")
    methodWindow.focus_force()

    methodWindow.grid_rowconfigure(0,weight=1)
    methodWindow.grid_rowconfigure(1,weight=1)

    methodWindow.grid_columnconfigure(0,weight=1)
    methodWindow.grid_columnconfigure(1,weight=1)

    def selectMethod(scanningMethod):
        print("Preset In Use : " + str(fileContent[presetIndex]))
        root.destroy()
        methodWindow.destroy()
        mainframe.presetProcessor(fileContent[presetIndex],scanningMethod)

    chooseMethodLabel = tk.Label(methodWindow,text="Choose Scanning Method")
    chooseMethodLabel.grid(row=0,column=0,columnspan=2)

    simpleMethodButton = tk.Button(methodWindow,text="Simple Method",command= lambda : selectMethod(0))
    simpleMethodButton.grid(row=1,column=0,sticky="nwes",padx=5,pady=5)

    aiMethodButton = tk.Button(methodWindow,text="AI Method (very unstable)",command= lambda : selectMethod(1))
    aiMethodButton.grid(row=1,column=1,sticky="nwes",padx=5,pady=5)

    methodWindow.mainloop()

def buildPresetButton(presetName,presetDescription,presetIndex):
    global aRow,aColumn,rootCanvas
    print(aRow,aColumn)

    if (aColumn >= 5):
        aRow += 1
        aColumn = 0

    #Building Preset Frame
    presetFrame = tk.LabelFrame(rootCanvas,text=presetName,width=100,height=100,padx=10,pady=5)
    presetFrame.grid(row=aRow,column=aColumn,sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=5)

    #Preset Description
    presetDescriptionLabel = tk.Label(presetFrame,text="Description : "+str(presetDescription),wraplength=150)
    presetDescriptionLabel.pack()
    #Preset Functionality
    presetOpen = tk.Button(presetFrame,text="Use",command=lambda:usePreset(presetIndex))
    presetDelete = tk.Button(presetFrame,text="Delete", command = lambda : deletePreset(presetIndex,presetFrame,presetName))
    presetDelete.pack(side=tk.BOTTOM,fill=tk.X)
    presetOpen.pack(side=tk.BOTTOM,fill=tk.X)

    #Increments
    aColumn += 1

def buildAll():
    global fileContent
    fileContent = []
    #Reading Saved Presets
    try:
        with open('.presets','r') as f:
            lineIndex = 0
            for line in f:
                fileContent.append(line)
                arguments = line.split("$")
                presetName = arguments[0]
                presetDescription = arguments[1]
                buildPresetButton(presetName,presetDescription,lineIndex)
                lineIndex += 1

    except Exception as e:
        print("Couldn't Read File Bcoz : "+str(e))

def main():
    global root,rootCanvas
    root = tk.Tk()
    root.title("OMR Evaluator by Kishlay and Ashish under Prof. Ashutosh Parida")
    root.geometry("900x500+100+100")
    root.focus_force()

    '''-------------------- Menu bars --------------------'''
    menubar = tk.Menu(root)
    #file menu
    filemenu = tk.Menu(menubar,tearoff=0)
    filemenu.add_command(label="My Portfolio",command=myportfolio)
    filemenu.add_command(label="Open Project Record",command=openprojectrecord)
    menubar.add_cascade(label="Click here to explore Documentation",menu=filemenu)
    root.config(menu=menubar)
    
    rootCanvas = tk.Canvas(root)
    rootCanvas.pack(fill=tk.BOTH,expand=True)

    #New Preset Button
    buildNewPresetButton()

    #Building Other Preset Buttons
    buildAll()

    root.protocol('WM_DELETE_WINDOW', deletetemp)
    root.mainloop()

if __name__ == "__main__":
    main()