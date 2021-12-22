from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from datetime import datetime
from PIL import ImageGrab
import tkinter.font as tkfont
import shutil
import time
import os, sys
import filecmp
import json
import re

savingperiod = ""
sentinel = True
enterNameForBranchSentinel = True
CommandEntryFlags = {
	'searching' : False,
	'branching' : False,
}

Customization = {
	'fontTuple' : ('Calibri', 11, 'normal'),
	'TextBoxHeight' : 720,
	'TextBoxWidth' : 700,
	'Padding': [40,40,40,40], # N E S W
}


BranchingData = [
	{
		'visible_text': 'thisthing',
		'original_branches': ['thisthing', 'thisotherthing'],
		'branches': ['thisthing', 'thisotherthing'],
		'votes': [0, 0],
		'button-configured': True,
	},
]

Defaults = {
	'Customization' : {
		'fontTuple' : ('Calibri', 11, 'normal'),
		'TextBoxHeight' : 720,
		'TextBoxWidth' : 700,
		'Padding': [40,40,40,40], # N E S W
	}
}

BranchingData = []
breakOutOfBranchingSentinel = False
previousSearchEntry = ""
minNewProjectWindowSize = (300, 300)

StatusBarTexts = ["","",""]



def center(toplevel):
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    # PyQt way to find the screen resolution
    #app = QtGui.QApplication([])
    #screen_width = app.desktop().screenGeometry().width()
    #screen_height = app.desktop().screenGeometry().height()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))   



def newProjectWizard():

	def onClosingWizardWindow():
		WizardWindow.destroy()
		root.deiconify()

	def makeProject(projectName):
		try:
			#os.makedirs("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName)
			os.makedirs("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Text/")
			os.makedirs("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/BranchingData/")
			os.makedirs("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/")
			SettingsFile = open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Settings.txt", "w")
			global savingperiod
			savingperiod = savingPeriod.get()
			SettingsFile.write(savingperiod+"\n")
			SettingsFile.close()
			MainFile = open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainText.txt", "w")
			MainFile.close()
			MainBranchingData = open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainBranchingData.txt", "w")
			MainBranchingData.close()
			MainTags = open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainTags.txt", "w")
			MainTags.close()
			WizardWindow.destroy()
			startProject(projectName)
		except Exception as exception1:
			messagebox.showwarning(title="Quit", message="Invalid or previously used name")
			print(exception1)

	root.withdraw()
	WizardWindow = Toplevel(root)
	WizardWindow.geometry("400x400")
	WizardWindow.iconbitmap('C:\Program Files\EssayWritingSystem\icon.ico')
	center(WizardWindow)
	WizardWindow.title("New Project Wizard")
	projectname = StringVar()
	NewProjectNameLabel = Label(WizardWindow, text='Project Name:')
	NewProjectNameLabel.pack(pady=(100,0))
	NewProjectNameField = Entry(WizardWindow, textvariable=projectname)
	NewProjectNameField.pack(pady=(2,10))
	SavingPeriodLabel = Label(WizardWindow, text='Saving Period (sec):')
	SavingPeriodLabel.pack(pady=(10,0))
	global savingperiod
	savingPeriod = StringVar()
	SavingPeriodField = Entry(WizardWindow, textvariable=savingPeriod)
	SavingPeriodField.insert(END, '120')
	SavingPeriodField.pack()
	SubmitButton = Button(WizardWindow, text="Submit", command= lambda: makeProject(projectname.get()))
	SubmitButton.pack(pady=10)
	WizardWindow.protocol("WM_DELETE_WINDOW", onClosingWizardWindow)
	WizardWindow.resizable(False, False)
	WizardWindow.bind('<Return>', lambda event: makeProject(projectname.get()))
	
	


	

def startProject(projectName, fullText = "", Tags = []):
	global Customization
	global Defaults
	# Cut Text
	def cut_text(e):
		global selected
		# Check to see if keyboard shortcut used
		if e:
			selected = root.clipboard_get()
		else:
			if MainText.selection_get():
				# Grab selected text from text box
				selected = MainText.selection_get()
				# Delete Selected Text from text box
				MainText.delete("sel.first", "sel.last")
				# Clear the clipboard then append
				root.clipboard_clear()
				root.clipboard_append(selected)

	# Copy Text
	def copy_text(e):
		global selected
		# check to see if we used keyboard shortcuts
		if e:
			selected = root.clipboard_get()

		if MainText.selection_get():
			# Grab selected text from text box
			selected = MainText.selection_get()
			# Clear the clipboard then append
			root.clipboard_clear()
			root.clipboard_append(selected)

	# Paste Text
	def paste_text(e):
		global selected
		#Check to see if keyboard shortcut used
		if e:
			selected = root.clipboard_get()
		else:
			if selected:
				position = MainText.index(INSERT)
				MainText.insert(position, selected)

	# Bold Text
	def bold_it(e):
		# Create our font
		bold_font = font.Font(MainText, MainText.cget("font"))
		bold_font.configure(weight="bold")

		# Configure a tag
		MainText.tag_configure("bold", font=bold_font)

		# Define Current tags
		current_tags = MainText.tag_names("sel.first")

		# If statment to see if tag has been set
		if "bold" in current_tags:
			MainText.tag_remove("bold", "sel.first", "sel.last")
		else:
			MainText.tag_add("bold", "sel.first", "sel.last")

	# Italics Text
	def italics_it():
		# Create our font
		italics_font = font.Font(MainText, MainText.cget("font"))
		italics_font.configure(slant="italic")

		# Configure a tag
		MainText.tag_configure("italic", font=italics_font)

		# Define Current tags
		current_tags = MainText.tag_names("sel.first")

		# If statment to see if tag has been set
		if "italic" in current_tags:
			MainText.tag_remove("italic", "sel.first", "sel.last")
		else:
			MainText.tag_add("italic", "sel.first", "sel.last")

	# Change Selected Text Color
	def text_color():
		# Pick a color
		my_color = colorchooser.askcolor()[1]
		if my_color:
			# Create our font
			color_font = font.Font(MainText, MainText.cget("font"))

			# Configure a tag
			MainText.tag_configure("colored", font=color_font, foreground=my_color)

			# Define Current tags
			current_tags = MainText.tag_names("sel.first")

			# If statment to see if tag has been set
			if "colored" in current_tags:
				MainText.tag_remove("colored", "sel.first", "sel.last")
			else:
				MainText.tag_add("colored", "sel.first", "sel.last")

	# Change bg color
	def bg_color():
		my_color = colorchooser.askcolor()[1]
		if my_color:
			MainText.config(bg=my_color)

	# Select all Text
	def select_all(e):
		# Add sel tag to select all text
		MainText.tag_add('sel', '1.0', 'end')

	# Clear All Text
	def clear_all():
		MainText.delete(1.0, END)

	def logPos(e):
		print(MainText.index(INSERT))

	def switchFullScreen(menu, screen):
		FullscreenLabel = menu.entrycget(1, "label")
		if(FullscreenLabel == "Fullscreen"):
			menu.entryconfigure(1, label="Exit Fullscreen")
			screen.attributes('-fullscreen',True)
			Customization["TextBoxHeight"] = 710
			MainFrame.configure(height=Customization["TextBoxHeight"])
		elif (FullscreenLabel == "Exit Fullscreen"):
			menu.entryconfigure(1, label="Fullscreen")
			screen.attributes('-fullscreen',False)
			Customization["TextBoxHeight"] = 630
			MainFrame.configure(height=Customization["TextBoxHeight"])
		
	def exitFullScreen(menu, screen):
		menu.entryconfigure(1, label="Fullscreen")
		screen.attributes('-fullscreen',False)
		Customization["TextBoxHeight"] = Defaults["Customization"]['TextBoxHeight']
		MainFrame.configure(height=Customization["TextBoxHeight"])

	def changeTextBoxDims():
		def defaultTextBoxDims(e=0):
			Customization["TextBoxWidth"] = Defaults["Customization"]["TextBoxWidth"]
			Customization["TextBoxHeight"] = Defaults["Customization"]["TextBoxHeight"]
			MainFrame.configure(width=Customization["TextBoxWidth"])
			MainFrame.configure(height=Customization["TextBoxHeight"])
			mainframexpadding = round(0.5*(NewProjectWindow.winfo_width()-Customization["TextBoxWidth"]))
			mainframexpadding = (mainframexpadding + abs(mainframexpadding))/2
			MainFrame.pack(padx=(mainframexpadding, 0), side=LEFT)

		TextBoxDimsChangeWindow = Toplevel(NewProjectWindow)
		TextBoxDimsChangeWindow.iconbitmap('C:/Program Files/EssayWritingSystem/icon.ico')
		TextBoxDimsChangeWindow.geometry("300x200")
		TextBoxDimsChangeWindow.resizable(False, False)
		center(TextBoxDimsChangeWindow)
		TextBoxDimsChangeWindow.title("Modify Textbox Dimensions")
		widthChangeScale = ttk.Scale(TextBoxDimsChangeWindow, orient=HORIZONTAL, length=200, from_=0, to=(NewProjectWindow.winfo_width() - 300), command=defaultTextBoxDims)
		widthChangeScale.set(Customization["TextBoxWidth"])
		heightChangeScale = ttk.Scale(TextBoxDimsChangeWindow, orient=HORIZONTAL, length=200, from_=0, to=(NewProjectWindow.winfo_height() - 50), command=defaultTextBoxDims)
		heightChangeScale.set(Customization["TextBoxHeight"])
		
		def makeChanges(e):
			Customization["TextBoxWidth"] = int(widthChangeScale.get())
			Customization["TextBoxHeight"] = int(heightChangeScale.get())
			MainFrame.configure(width=Customization["TextBoxWidth"])
			MainFrame.configure(height=Customization["TextBoxHeight"])
			mainframexpadding = round(0.5*(NewProjectWindow.winfo_width()-Customization["TextBoxWidth"]))
			mainframexpadding = (mainframexpadding + abs(mainframexpadding))/2
			MainFrame.pack(padx=(mainframexpadding, 0), side=LEFT)

		
		widthChangeScale = ttk.Scale(TextBoxDimsChangeWindow, orient=HORIZONTAL, length=200, from_=0, to=(NewProjectWindow.winfo_width() - 300), command=makeChanges)
		widthChangeScale.set(Customization["TextBoxWidth"])
		heightChangeScale = ttk.Scale(TextBoxDimsChangeWindow, orient=HORIZONTAL, length=200, from_=0, to=(NewProjectWindow.winfo_height() - 50), command=makeChanges)
		heightChangeScale.set(Customization["TextBoxHeight"])
		resetToDefaultsButton = Button(TextBoxDimsChangeWindow, width=10, text="Defaults", command=lambda: defaultTextBoxDims())
		widthChangeScale.pack(padx = 20, pady = 20)
		heightChangeScale.pack(padx = 20, pady = 20)
		resetToDefaultsButton.pack(pady=(20,0))
		
		


	def changeFontType():
		global Customization
		Customization["fontTuple"][1] = 15
		MainText.configure(font=(Customization["fontTuple"][0], Customization["fontTuple"][1]))

	def onClosingNewProjectWindow(currentText):
		global BranchingData
		if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
			MainFile = open(file="C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainText.txt", mode="wb")
			MainFile.write(MainText.get("1.0",END).encode("utf8"))
			MainFile.close()
			BranchingData2 = BranchingData.copy()
			for branch in BranchingData2:
				branch['button-configured'] = False
			with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainBranchingData.txt", "w") as f:
				f.write(json.dumps(BranchingData2))
			MainTags = MainText.dump("1.0", "end", tag=True)
			
			for index in range(len(MainTags)-1, -1, -1):
				if(MainTags[index][1] == 'sel'):
					MainTags.pop(index)
			

			with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainTags.txt", "w") as f:
				f.write(json.dumps(MainTags))
			DateToday = date.today().strftime("%m.%d.%y")
			TimeNow = datetime.now().strftime("%H.%M.%S")
			try:
				os.makedirs("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Text/" + DateToday)
				os.makedirs("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/BranchingData/" + DateToday)
				os.makedirs("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/" + DateToday)
			except:
				pass
			
			# checking if last archived copy is same as current
			try:
				if (not filecmp.cmp("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainText.txt", "C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Text/" + DateToday + "/" + sorted(os.listdir("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Text/" + DateToday))[-1])) or (not filecmp.cmp("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainTags.txt", "C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/" + DateToday + "/" + sorted(os.listdir("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/" + DateToday))[-1])):
					NextArchive = open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Text/" + DateToday + "/" + TimeNow + ".txt", "wb")
					NextArchive.write(MainText.get("1.0",END).encode('utf8'))
					NextArchive.close()
					with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/BranchingData/" + DateToday + "/" + TimeNow + ".txt", "w") as f:
						f.write(json.dumps(BranchingData2))
					MainTags = MainText.dump("1.0", "end", tag=True)
					for index in range(len(MainTags)-1, -1, -1):
						if(MainTags[index][1] == 'sel'):
							MainTags.pop(index)
					with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/" + DateToday + "/" + TimeNow + ".txt", "w") as f:
						f.write(json.dumps(MainTags))
					
					
			except:
				NextArchive = open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Text/" + DateToday + "/" + TimeNow + ".txt", "wb")
				NextArchive.write(MainText.get("1.0",END).encode('utf8'))
				NextArchive.close()
				with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/BranchingData/" + DateToday + "/" + TimeNow + ".txt", "w") as f:
					f.write(json.dumps(BranchingData2))
				MainTags = MainText.dump("1.0", "end", tag=True)
				for index in range(len(MainTags)-1, -1, -1):
					if(MainTags[index][1] == 'sel'):
						MainTags.pop(index)
				with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/" + DateToday + "/" + TimeNow + ".txt", "w") as f:
					f.write(json.dumps(MainTags))
			global sentinel
			sentinel = False
			BranchingData = []
			global savingperiod, enterNameForBranchSentinel, CommandEntryFlags, Customization, breakOutOfBranchingSentinel, previousSearchEntry, minNewProjectWindowSize, StatusBarTexts
			savingperiod = ""
			enterNameForBranchSentinel = True
			CommandEntryFlags = {
				'searching' : False,
				'branching' : False,
			}

			Customization = {
				'fontTuple' : ('Calibri', 11, 'normal'),
				'TextBoxHeight' : 630,
				'TextBoxWidth' : 700,
				'Padding': [40,40,40,40], # N E S W
			}
			breakOutOfBranchingSentinel = False
			previousSearchEntry = ""
			minNewProjectWindowSize = (300, 300)

			StatusBarTexts = ["","",""]
			NewProjectWindow.destroy()
			root.deiconify()

	def closeCommandBox():
		global CommandEntryFlags
		global previousSearchEntry
		if(CommandEntryFlags["searching"]):
			previousSearchEntry = CommandEntry.get()
		CommandEntryFlags["searching"] = False
		CommandEntryFlags["changeFont"] = False
		CommandEntry.delete(0, END)
		global breakOutOfBranchingSentinel
		global enterNameForBranchSentinel
		breakOutOfBranchingSentinel = True
		enterNameForBranchSentinel = False
		MainText.tag_remove("found", "1.0", "end")
		MainText.tag_remove("stem" + str(len(BranchingData)), "1.0", "end")
		

	def togglesearching(e):
		global CommandEntryFlags
		if(not CommandEntryFlags['branching']):
			global previousSearchEntry
			CommandEntryFlags["searching"] = not CommandEntryFlags["searching"]
			if(not CommandEntryFlags["searching"]):
				MainText.tag_remove("found", "1.0", "end")
			if(CommandEntry.get() != ""):
				CommandEntry.delete('1.0', END)
				CommandEntry.set(previousSearchEntry)

	def openBranchingWindow(stemIndex):
		global BranchingData
		BranchingWindow = Toplevel(NewProjectWindow)
		BranchingWindow.iconbitmap('C:/Program Files/EssayWritingSystem/icon.ico')
		BranchingWindow.geometry("350x350")
		center(BranchingWindow)
		BranchingWindow.title("Branch Config: " + BranchingData[stemIndex]['visible_text'])
		def downwars_shift(event):
			tv = event.widget
			select = [tv.index(s) for s in tv.selection()]
			select.append(tv.index(tv.identify_row(event.y)))
			select.sort()
			for i in range(select[0],select[-1]+1,1):
				tv.selection_add(tv.get_children()[i])

		def move_down(event):
			tv = event.widget
			if tv.identify_row(event.y) not in tv.selection():
				tv.selection_set(tv.identify_row(event.y))    

		def move_up(event):
			tv = event.widget
			if tv.identify_row(event.y) in tv.selection():
				tv.selection_set(tv.identify_row(event.y))    

		def upward_shift(event):
			pass

		def add_branch():
			branchName = ""
			global getOutOfBranchNamingSentinel
			getOutOfBranchNamingSentinel = False
			def getOutOfBranchNaming():
				try:
					BranchingData[stemIndex]['branches'].index(branchName)
					messagebox.showwarning('Duplicate Branch', 'Cannot create a branch with the same content: \'' + branchName + '\'')
				except:
					BranchingData[stemIndex]['branches'].append(branchName)
					BranchingData[stemIndex]['original_branches'].append(branchName)
					BranchingData[stemIndex]['votes'].append(0)
				
				global getOutOfBranchNamingSentinel
				getOutOfBranchNamingSentinel = True
			def breakOutOfBranchNaming():
				global getOutOfBranchNamingSentinel
				getOutOfBranchNamingSentinel = True

			AddBranchButton.pack_forget()
			AddBranchNameEntry = Entry(BranchButtonsFrame, width=12)
			AddBranchNameEntry.pack(side=LEFT, padx = 4, pady = 4)
			
			AddBranchNameEntry.bind("<Return>", lambda event: getOutOfBranchNaming())
			AddBranchNameEntry.bind("<Escape>", lambda event: breakOutOfBranchNaming())

			while (not getOutOfBranchNamingSentinel):
				BranchingWindow.update_idletasks()
				BranchingWindow.update()
				branchName = AddBranchNameEntry.get()
			
			AddBranchNameEntry.pack_forget()
			AddBranchButton.pack(side=LEFT, padx = 4, pady= 4)
			AddBranchNameEntry.unbind("<Return>")
			AddBranchNameEntry.unbind("<Escape>")
			tv.delete(*tv.get_children())
			for index in range(0,len(BranchingData[stemIndex]['branches'])):
				tv.insert(parent='', index=index, iid=index, text='', values=(BranchingData[stemIndex]['branches'][index],BranchingData[stemIndex]['votes'][index]))
		
		def delete_branch():
			for row in tv.selection():
				BranchingData[stemIndex]['branches'].pop(int(row))
			if(len(BranchingData[stemIndex]['branches']) == 0):
				deleteBranch(stemIndex, False)
				BranchingWindow.destroy()
			else:
				tv.delete(*tv.get_children())
				for index in range(0,len(BranchingData[stemIndex]['branches'])):
					tv.insert(parent='', index=index, iid=index, text='', values=(BranchingData[stemIndex]['branches'][index],BranchingData[stemIndex]['votes'][index]))
				stem = BranchingData[stemIndex]
				stem['visible_text'] = stem['branches'][0]
				stem['visible_text'].replace('\n', ' ↵ ')
				if len(stem['visible_text']) > 25:
					stem['visible_text'] = stem['visible_text'][0:22] + '...'
				branchingbuttons[BranchingData.index(stem)].configure(text=stem['visible_text'])
				textToChange = MainText.tag_nextrange('stem'+str(BranchingData.index(stem)), '1.0')
				MainText.delete(textToChange[0], textToChange[1])
				MainText.insert(textToChange[0], stem['visible_text'])
				MainText.tag_add('stem'+str(BranchingData.index(stem)), textToChange[0], textToChange[0]+'+'+str(len(stem['visible_text']))+'c')


		def Movement(event):
			tv = event.widget
			moveto = tv.index(tv.identify_row(event.y))
			#print(tv.identify_row(event.y))
			global BranchingData
			my_temp_index = 0	
			for s in tv.selection():
				my_temp_index = my_temp_index + 1
				if(my_temp_index > 1):
					print("what?")
				tv.move(s, '', moveto)
				
				startIndex = BranchingData[stemIndex]['branches'].index(BranchingData[stemIndex]['original_branches'][int(s)])
				endIndex = int(moveto)
				if(startIndex > endIndex):
					BranchingData[stemIndex]['branches'] = (BranchingData[stemIndex]['branches'][0:endIndex]+ [BranchingData[stemIndex]['branches'][startIndex]]+ BranchingData[stemIndex]['branches'][endIndex:startIndex]+BranchingData[stemIndex]['branches'][startIndex+1:])
				elif(startIndex < endIndex):
					BranchingData[stemIndex]['branches'] = (BranchingData[stemIndex]['branches'][0:startIndex]+ BranchingData[stemIndex]['branches'][startIndex+1:endIndex+1]+ [BranchingData[stemIndex]['branches'][startIndex]]+BranchingData[stemIndex]['branches'][endIndex+1:])
				#temp = BranchingData[stemIndex]['branches'][int(moveto)]
				#BranchingData[stemIndex]['branches'][int(moveto)] = BranchingData[stemIndex]['branches'][int(s)]
				#BranchingData[stemIndex]['branches'][int(s)] = temp

			
			stem = BranchingData[stemIndex]
			stem['visible_text'] = stem['branches'][0]
			stem['visible_text'].replace('\n', ' ↵ ')
			if len(stem['visible_text']) > 25:
				stem['visible_text'] = stem['visible_text'][0:22] + '...'
			branchingbuttons[BranchingData.index(stem)].configure(text=stem['visible_text'])
			textToChange = MainText.tag_nextrange('stem'+str(BranchingData.index(stem)), '1.0')
			MainText.delete(textToChange[0], textToChange[1])
			MainText.insert(textToChange[0], stem['visible_text'])
			MainText.tag_add('stem'+str(BranchingData.index(stem)), textToChange[0], textToChange[0]+'+'+str(len(stem['visible_text']))+'c')

			for child in tv.get_children():
				print(tv.item(child)["values"][0], end=" ")
			print("\n", end="")
			for branch in BranchingData[stemIndex]['branches']:
				print(branch, end=" ")
			print("\n\n")
			
			#tv.delete(*tv.get_children())
			#for index in range(0,len(BranchingData[stemIndex]['branches'])):
			#	tv.insert(parent='', index=index, iid=index, text='', values=(BranchingData[stemIndex]['branches'][index],BranchingData[stemIndex]['votes'][index]))
		
			

	
		tv = ttk.Treeview(BranchingWindow)
		BranchButtonsFrame = Frame(BranchingWindow)
		BranchButtonsFrame.pack(side=BOTTOM)
		AddBranchButton = Button(BranchButtonsFrame, width=12, text="+", command=add_branch)
		AddBranchButton.pack(side=LEFT, padx = 4, pady= 4)
		DeleteBranchButton = Button(BranchButtonsFrame, width=12, text="-", command=delete_branch)
		DeleteBranchButton.pack(side=RIGHT, padx = 4, pady = 4)
		tv['columns']=('Text', 'Votes')
		tv.column('#0', width=0, stretch=NO)
		tv.column('Text', anchor=CENTER, width=160)
		tv.column('Votes', anchor=CENTER, width=50)
		
		tv.heading('#0', text='', anchor=CENTER)
		tv.heading('Text', text='Text', anchor=CENTER)
		tv.heading('Votes', text='Votes', anchor=CENTER)

		
		for index in range(0,len(BranchingData[stemIndex]['branches'])):
			tv.insert(parent='', index=index, iid=index, text='', values=(BranchingData[stemIndex]['branches'][index],BranchingData[stemIndex]['votes'][index]))
		tv.pack(pady=20)

		#tv.bind("<ButtonPress-1>",move_down)
		#tv.bind("<ButtonRelease-1>",move_up, add='+')
		tv.bind("<B1-Motion>", Movement, add='+')
		#tv.bind("<Shift-ButtonPress-1>",downwars_shift, add='+')
		#tv.bind("<Shift-ButtonRelease-1>",upward_shift, add='+')


		#style = ttk.Style()
		#style.theme_use("default")
		#style.map("Treeview")

	def deleteBranch(stemIndex, popup=True):
		global BranchingData
		if popup:
			if messagebox.askokcancel("Branch " + BranchingData[stemIndex]['visible_text'] + " Deletion", "Are you sure you want to delete this branch?"):
				BranchingData.pop(stemIndex)
				branchingbuttons[stemIndex].pack_forget()
				branchdeletebuttons[stemIndex].pack_forget()
				branchingbuttons.pop(stemIndex)
				branchdeletebuttons.pop(stemIndex)
				MainText.tag_remove('stem'+str(stemIndex),"1.0", END)
		else:
			BranchingData.pop(stemIndex)
			branchingbuttons[stemIndex].pack_forget()
			branchdeletebuttons[stemIndex].pack_forget()
			branchingbuttons.pop(stemIndex)
			branchdeletebuttons.pop(stemIndex)
			MainText.tag_remove('stem'+str(stemIndex),"1.0", END)


	NewProjectWindow = Toplevel(root)
	NewProjectWindow.iconbitmap('C:/Program Files/EssayWritingSystem/icon.ico')
	center(NewProjectWindow)
	NewProjectWindow.title("Essay Writing System: " + projectName)
	NewProjectWindow.state('zoomed')
	NewProjectWindow.minsize(300, 300)

	ToolbarFrame = Frame(NewProjectWindow)
	ToolbarFrame.pack(fill=X)




	# Status Bar

	StatusFrame = Frame(NewProjectWindow, height=20, width=NewProjectWindow.winfo_width())
	StatusFrame.pack(side = BOTTOM)
	StatusFrame.pack_propagate(False)

	global StatusBarTexts
	StatusBar1 = Label(StatusFrame, text=StatusBarTexts[1], bd=1, relief=SUNKEN, anchor=SW, width = 30, height = 2)
	StatusBar1.pack(side=RIGHT)

	StatusBar2 = Label(StatusFrame, text=StatusBarTexts[2], bd=1, relief=SUNKEN, anchor=SW, width = 30, height = 2)
	StatusBar2.pack(side=RIGHT)

	CommandEntry = Entry(StatusFrame, width = 20, font=Customization["fontTuple"])
	



	# Main Frame

	
	#MainText = Text(MainFrame, width=80, height=31, font=(Customization["fontTuple"][0], Customization["fontTuple"][1]), selectbackground="#bad2ff", selectforeground="black", undo=True, yscrollcommand=TextScroll.set, wrap=WORD, pady=30, padx=30)
	mainframexpadding = round(0.5*(NewProjectWindow.winfo_width()-Customization["TextBoxWidth"]))
	mainframexpadding = (mainframexpadding + abs(mainframexpadding))/2
	OuterMainFrame = Frame(NewProjectWindow)
	OuterMainFrame.pack()
	MainFrame = Frame(OuterMainFrame, height=Customization["TextBoxHeight"], width=Customization["TextBoxWidth"], bd = 2)
	MainFrame.pack(side=LEFT)
	#MainFrame.pack(pady=5, padx=(200, 0), side=LEFT)
	MainFrame.pack_propagate(False)

	# Create our Scrollbar For the Text Box
	TextScroll = Scrollbar(MainFrame)
	TextScroll.pack(side=RIGHT, fill=Y)

	

	def enterNameForBranch(textForBranch, alternateTextForBranch):
		global enterNameForBranchSentinel
		if(textForBranch != alternateTextForBranch):
			enterNameForBranchSentinel = False
		else:
			messagebox.showwarning('Duplicate Branch', 'Cannot create a branch with the same contents: \'' + textForBranch + '\'')

	def toEditingView(e=1):
		BranchingFrameOuter.pack_forget()
		NewProjectWindow.minsize(300, 300)
	
	def toBranchingView(e=1):
		if(len(BranchingData) != 0):
			BranchingFrameOuter.pack(anchor=NW)
			NewProjectWindow.minsize(500, 300)

	def toVotingView(e=1):
		print("not yet implemented")

	def makeAlt(e):
		global BranchingData
		global enterNameForBranchSentinel
		global CommandEntryFlags
		CommandEntryFlags['branching'] = True
		enterNameForBranchSentinel = True
		NewProjectWindow.bind('<Return>', lambda event: enterNameForBranch(textForBranch, alternateTextForBranch))
		# Configure a tag
		MainText.tag_add("stem" + str(len(BranchingData)), "sel.first", "sel.last")
		NewProjectWindow.update()
		MainText.tag_configure("stem" + str(len(BranchingData)))
		textForBranch = MainText.selection_get()
		global Customization
		my_font = tkfont.Font(family=Customization["fontTuple"][0], size=Customization["fontTuple"][1], weight="normal")
		m_len = my_font.measure("0")
		CommandEntry.pack(padx=(round((NewProjectWindow.winfo_width()-21*m_len)/2),0), side=LEFT)
		#CommandEntry.pack(padx=(0,0), side=LEFT)
		CommandEntry.focus_set()
		while (enterNameForBranchSentinel):
			NewProjectWindow.update_idletasks()
			NewProjectWindow.update()
			alternateTextForBranch = CommandEntry.get()

		CommandEntry.delete(0,END)
		CommandEntry.pack_forget()
		global breakOutOfBranchingSentinel
		if (breakOutOfBranchingSentinel):
			breakOutOfBranchingSentinel = False
			return
		
		textForBranch2 = textForBranch.replace('\n', ' ↵ ')
		if (len(textForBranch) > 25):
			textForBranch2 = textForBranch2[0:22] + "..."
		BranchingData.append({
		'visible_text': textForBranch2,
		'original_branches': [textForBranch, alternateTextForBranch],
		'branches': [textForBranch, alternateTextForBranch],
		'votes': [0, 0],
		'button-configured': False,
		})
		my_color = "#0080c0"
		MainText.tag_configure("stem" + str(len(BranchingData)-1), foreground=my_color)
		CommandEntryFlags['branching'] = False
		NewProjectWindow.unbind('<Return>')


	# Horizontal Scrollbar
	#hor_scroll = Scrollbar(MainFrame, orient='horizontal')
	#hor_scroll.pack(side=BOTTOM, fill=X)

	# Create Text Box
	#MainText = Text(MainFrame, width=80, height=31, font=(Customization["fontTuple"][0], Customization["fontTuple"][1]), selectbackground="#bad2ff", selectforeground="black", undo=True, yscrollcommand=TextScroll.set, wrap=WORD, pady=30, padx=30)
	#MainText = Text(MainFrame, width=round(700/m_len), height=round(240/m_len), font=(Customization["fontTuple"][0], Customization["fontTuple"][1]), selectbackground="#bad2ff", selectforeground="black", undo=True, yscrollcommand=TextScroll.set, wrap=WORD, pady=30, padx=30)
	SubMainFrame = Frame(MainFrame, bg="white", bd = 1, relief="groove", padx=40, pady=40)
	SubMainFrame.pack(side=LEFT, fill=BOTH, expand=True)
	MainText = Text(SubMainFrame, font=(Customization["fontTuple"][0], Customization["fontTuple"][1]), selectbackground="#bad2ff", selectforeground="black", undo=True, yscrollcommand=TextScroll.set, wrap=WORD, bd = 0)
	
	MainText.insert('end', fullText)
	MainText.pack(side=LEFT, fill=BOTH, expand=True)
	MainText.tag_config('found', background='#d9ead3')
	TagsData = []
	for tag in Tags:
		if(tag[0] == 'tagon'):
			TagsData.append([tag[1], tag[2], ''])
		elif(tag[0] == 'tagoff'):
			for tagdata in TagsData:
				if(tagdata[0] == tag[1]):
					tagdata[2] = tag[2]

	for tagData in TagsData:
		MainText.tag_add(tagData[0], tagData[1], tagData[2])
		my_color = "#0080c0"
		MainText.tag_configure(tagData[0], foreground=my_color)
	# Configure our Scrollbar
	TextScroll.config(command=MainText.yview)

	# Branching Window
	branchingbuttons = []
	branchdeletebuttons = []
	BranchingFrameOuter = Frame(OuterMainFrame)
	BranchingFrame = Frame(BranchingFrameOuter)
	BranchingFrame.pack(side=LEFT)
	BranchDeleteFrame = Frame(BranchingFrameOuter)
	BranchDeleteFrame.pack(side=RIGHT)
	

	# Create Menu
	MainMenu = Menu(NewProjectWindow)
	NewProjectWindow.config(menu=MainMenu)

	# Add File Menu
	ControlsMenu = Menu(MainMenu, tearoff=False)
	MainMenu.add_cascade(label="Controls", menu=ControlsMenu)
	#ControlsMenu.add_command(label="New", command=new_file)
	#ControlsMenu.add_command(label="Open", command=open_file)
	#ControlsMenu.add_command(label="Save", command=save_file)
	#ControlsMenu.add_command(label="Save As...", command=save_as_file)
	#ControlsMenu.add_command(label="Print File", command=print_file)
	ControlsMenu.add_command(label="Fullscreen", command= lambda: switchFullScreen(ControlsMenu, NewProjectWindow))
	ControlsMenu.add_command(label="Change Textbox Dimensions", command= changeTextBoxDims)
	#ControlsMenu.add_command(label="Change Font", command=changeFontType)
	ControlsMenu.add_command(label="Exit", command=lambda: onClosingNewProjectWindow(MainText.get("1.0",END)))

	# Add Edit Menu
	EditMenu = Menu(MainMenu, tearoff=False)
	MainMenu.add_cascade(label="Edit", menu=EditMenu)
	EditMenu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
	EditMenu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
	EditMenu.add_command(label="Paste             ", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
	EditMenu.add_separator()
	EditMenu.add_command(label="Undo", command=MainText.edit_undo, accelerator="(Ctrl+z)")
	EditMenu.add_command(label="Redo", command=MainText.edit_redo, accelerator="(Ctrl+y)")
	EditMenu.add_separator()
	EditMenu.add_command(label="Select All", command=lambda: select_all(True), accelerator="(Ctrl+a)")
	EditMenu.add_command(label="Clear", command=clear_all)

	ModesMenu = Menu(MainMenu, tearoff=False)
	MainMenu.add_cascade(label="Modes", menu=ModesMenu)
	ModesMenu.add_command(label = "Editing", command=toEditingView)
	ModesMenu.add_command(label = "Branching", command=toBranchingView)
	ModesMenu.add_command(label = "Voting", command=toVotingView)
	
	'''
	ViewsMenu = Menu(MainMenu, tearoff=False)
	MainMenu.add_cascade(label="Views", menu=ViewsMenu)
	ViewsMenu.add_command(label = "Dark", command=)
	ViewsMenu.add_command(label = "Inverted", command=)
	'''
	# Edit Bindings
	NewProjectWindow.bind('<Control-Key-x>', cut_text)
	NewProjectWindow.bind('<Control-Key-c>', copy_text)
	NewProjectWindow.bind('<Control-Key-v>', paste_text)
	NewProjectWindow.bind('<Control-Key-b>', bold_it)
	NewProjectWindow.bind('<Control-Key-i>', italics_it)
	NewProjectWindow.bind('<Control-A>', select_all)
	NewProjectWindow.bind('<Control-a>', select_all)
	NewProjectWindow.bind('<Control-Key-l>', logPos)
	NewProjectWindow.bind('<Escape>', lambda event: [closeCommandBox(), exitFullScreen(ControlsMenu, NewProjectWindow)])
	NewProjectWindow.bind('<Control-Key-s>', makeAlt)
	NewProjectWindow.bind('<Control-Key-f>', togglesearching)


	NewProjectWindow.protocol("WM_DELETE_WINDOW", lambda: onClosingNewProjectWindow(MainText.get("1.0",END)))
	

	start = time.time()
	global sentinel
	global savingperiod
	global CommandEntryFlags
	global BranchingData
	my_font = tkfont.Font(family=Customization["fontTuple"][0], size=Customization["fontTuple"][1], weight="normal")
	m_len = my_font.measure("0")
	previousWindowWidth = NewProjectWindow.winfo_width()
	previousWindowHeight = NewProjectWindow.winfo_height()




	while 1==1:
		NewProjectWindow.update_idletasks()
		NewProjectWindow.update()

		
		StatusBarTexts[1] = savingperiod

		if(sentinel == False):
			with open('Log.txt', 'w') as f:
				f.write("sentinel")
				sentinel = True
			break

		# 'Find' Functionality
		if(CommandEntryFlags["searching"]):
			CommandEntry.pack(padx=(round((NewProjectWindow.winfo_width()-20*m_len)/2),0), side=LEFT)
			CommandEntry.focus_set()
			str2find = CommandEntry.get()
			MainText.tag_remove('found', "1.0", END)
			if(str2find != ''):
				idx = "1.0"
				while 1==1:
					idx = MainText.search(pattern=str2find, index=idx, nocase=True, stopindex=END)
					if not idx: break
						
					#last index sum of current index and
					#length of text
					lastidx = '%s+%dc' % (idx, len(str2find))
						
					#overwrite 'Found' at idx
					MainText.tag_add('found', idx, lastidx)
					idx = lastidx
				
				#mark located string as red
				
    		#CommandEntry.focus_set()
		else:
			CommandEntry.delete(0,END)
			CommandEntry.pack_forget()



		
		# Making branching buttons for new branches
		m_len = my_font.measure("m")
		for stemIndex1 in range(0, len(BranchingData)):
			stem = BranchingData[stemIndex1]
			if(not stem['button-configured']):
				branchingbuttons.append(Button(BranchingFrame, text=stem['visible_text'], width=30, command=lambda stemIndex2=stemIndex1:openBranchingWindow(stemIndex2)))
				branchingbuttons[len(branchingbuttons)-1].pack( side=TOP, anchor=NW, padx=(10,0))
				branchdeletebuttons.append(Button(BranchDeleteFrame, text='x', width=2, command=lambda stemIndex2=stemIndex1:deleteBranch(stemIndex2)))
				branchdeletebuttons[len(branchdeletebuttons)-1].pack( side=TOP, anchor=NW)
				stem['button-configured'] = True
				toBranchingView()

		# Deleting branches if stem has been deleted
		for stemIndex1 in range(0, len(BranchingData)):
			if(len(MainText.tag_nextrange('stem'+str(stemIndex1), '1.0')) == 0):
				#if messagebox.askokcancel("Branch " + BranchingData[stemIndex1]['visible_text'] + " Deletion", "Are you sure you want to delete this branch?"):
				deleteBranch(stemIndex1, popup=False)
		if(len(BranchingData) == 0):
			toEditingView()
		

		# Adjusting TextBox Size
		if(NewProjectWindow.winfo_width() != previousWindowWidth):
			mainframexpadding = round(0.5*(NewProjectWindow.winfo_width()-Customization["TextBoxWidth"]))
			mainframexpadding = (mainframexpadding + abs(mainframexpadding))/2
			MainFrame.pack_configure(padx=(mainframexpadding, 0))
			if(NewProjectWindow.winfo_width() < Customization["TextBoxWidth"]+30):
				if(NewProjectWindow.winfo_height() != previousWindowHeight and NewProjectWindow.winfo_height() < Defaults["Customization"]["TextBoxHeight"]+30):
					Customization["TextBoxWidth"]
				else:
					MainFrame.pack_configure(fill = X)
		elif ((NewProjectWindow.winfo_height() != previousWindowHeight and NewProjectWindow.winfo_height() < Defaults["Customization"]["TextBoxHeight"]+30)):
			MainFrame.pack_configure(fill = Y)
		previousWindowHeight = NewProjectWindow.winfo_height()
		previousWindowWidth = NewProjectWindow.winfo_width()
		#print(previousWindowWidth)


		# Word Count
		wordCount = 0
		text = MainText.get("1.0",END).strip()
		for ch in text:
			if(ch != ' '):
				wordCount = 1
				break
		#wordCount = wordCount + len(re.findall("\S\s.*\S", text))
		onSpaceFlag = False
		for ch in text:
			if(onSpaceFlag):
				if(ch != ' '):
					wordCount += 1
					onSpaceFlag = False
			elif(ch == ' '):
				onSpaceFlag = True
		StatusBarTexts[2] = wordCount
		StatusBar1.config(text=StatusBarTexts[2])


		# File Saving
		if float(time.time() - start) > float(savingperiod):
			start = time.time()
			# main file write
			MainFile = open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainText.txt", "wb")
			MainFile.write(MainText.get("1.0",END).encode('utf8'))
			MainFile.close()
			
			# main branching data file write
			BranchingData2 = BranchingData.copy()
			for branch in BranchingData2:
				branch['button-configured'] = False
			with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainBranchingData.txt", "w") as f:
				f.write(json.dumps(BranchingData2))
			
			# tags data file write
			MainTags = MainText.dump("1.0", "end", tag=True)
			for index in range(len(MainTags)-1, -1, -1):
				if(MainTags[index][1] == 'sel'):
					MainTags.pop(index)
			with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainTags.txt", "w") as f:
				f.write(json.dumps(MainTags))
			DateToday = date.today().strftime("%m.%d.%y")
			TimeNow = datetime.now().strftime("%H.%M.%S")
			try:
				os.makedirs("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/" + DateToday)
			except:
				pass
			
			# checking if last archived copy is same as current
			try:
				if (not filecmp.cmp("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainText.txt", "C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/" + DateToday + "/" + sorted(os.listdir("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/" + DateToday))[-1] + "/Text.txt")) or (not filecmp.cmp("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/MainTags.txt", "C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/" + DateToday + "/" + sorted(os.listdir("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/" + DateToday))[-1])):
					NextArchive = open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Text/" + DateToday + "/" + TimeNow + ".txt", "wb")
					NextArchive.write(MainText.get("1.0",END).encode('utf8'))
					NextArchive.close()
					with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/BranchingData/" + DateToday + "/" + TimeNow + ".txt", "w") as f:
						f.write(json.dumps(BranchingData2))
					MainTags = MainText.dump("1.0", "end", tag=True)
					for index in range(len(MainTags)-1, -1, -1):
						if(MainTags[index][1] == 'sel'):
							MainTags.pop(index)
					with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/" + DateToday + "/" + TimeNow + ".txt", "w") as f:
						f.write(json.dumps(MainTags))
				
			except:
				NextArchive = open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Text/" + DateToday + "/" + TimeNow + ".txt", "wb")
				NextArchive.write(MainText.get("1.0",END).encode('utf8'))
				NextArchive.close()
				with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/BranchingData/" + DateToday + "/" + TimeNow + ".txt", "w") as f:
					f.write(json.dumps(BranchingData2))
				MainTags = MainText.dump("1.0", "end", tag=True)
				for index in range(len(MainTags)-1, -1, -1):
					if(MainTags[index][1] == 'sel'):
						MainTags.pop(index)
				with open("C:/Users/vedha/Documents/Essays - Essay Writing System/" + projectName + "/Archive/Tags/" + DateToday + "/" + TimeNow + ".txt", "w") as f:
					f.write(json.dumps(MainTags))
			



def openProject():
	# Grab Filename
	sentinel = TRUE
	try:
		dir = filedialog.askdirectory(initialdir="C:/Users/vedha/Documents/Essays - Essay Writing System", title="Open Existing Project")
		os.chdir(dir)
	except:
		sentinel = FALSE
	
	if(sentinel):
		dirpath = os.path.basename(os.getcwd())
		try:
			with open('Settings.txt') as f:
				global savingperiod
				savingperiod = f.readline()
				StatusBarTexts[1] = savingperiod
				fullText = ""
			with open('MainText.txt', mode="rb") as f:
				fullText = f.read().decode('utf8')
			with open('MainBranchingData.txt', 'r') as f:
				global BranchingData
				BranchingData = json.loads(f.read())
			with open('MainTags.txt', 'r') as f:
				Tags = json.loads(f.read())

			
			
		except Exception as exception1:
			messagebox.showerror(title="Exit", message="This project has been corrupted and cannot be opened at this time. Please consult the documentation to try to revive it.")
			print(exception1)
		root.withdraw()
		startProject(dirpath, fullText, Tags)

				
	





root = Tk()
root.geometry("400x400")
center(root)
root.title('Essay Writing System')
root.iconbitmap('C:/Program Files/EssayWritingSystem/icon.ico')
NewProjectBtn = Button(root, text="Create New Project", command=newProjectWizard)
OpenProjectBtn = Button(root, text="Open Existing Project", command=openProject)
QuitButton = Button(root, text="Quit", command=root.destroy)
NewProjectBtn.pack(pady=(70,10))
OpenProjectBtn.pack(pady=10)
QuitButton.pack(pady=10)
root.resizable(False, False)
root.mainloop()
