from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import messagebox
from datetime import date
from datetime import datetime
import shutil
import time
import os, sys
import win32print
import win32api
import filecmp

sentinel = True
#StatusBarTexts = ["","","Ready"]
	
def newProjectWizard():
	def onClosingWizardWindow():
		WizardWindow.destroy()
		root.deiconify()

	def makeProject(projectName):
		try:
			os.mkdir("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get())
			os.mkdir("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive")
			SettingsFile = open("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Settings.txt", "w")
			SettingsFile.close()
			MainFile = open("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Main.txt", "w")
			MainFile.close()
			WizardWindow.destroy()
			newProject(projectName)
		except:
			messagebox.showwarning(title="Quit", message="Invalid or previously used name")
		

	root.withdraw()
	WizardWindow = Toplevel(root)
	WizardWindow.geometry("400x400")
	WizardWindow.title("New Project Wizard")
	projectname = StringVar()
	NewProjectNameLabel = Label(WizardWindow, text='Project Name:')
	NewProjectNameLabel.pack(pady=(100,0))
	NewProjectNameField = Entry(WizardWindow, textvariable=projectname)
	NewProjectNameField.pack(pady=(2,10))
	SavingPeriodLabel = Label(WizardWindow, text='Saving Period (sec):')
	SavingPeriodLabel.pack(pady=(10,0))
	global savingperiod
	savingperiod = StringVar()
	SavingPeriodField = Entry(WizardWindow, textvariable=savingperiod)
	SavingPeriodField.insert(END, '120')
	SavingPeriodField.pack()
	SubmitButton = Button(WizardWindow, text="Submit", command= lambda: makeProject(projectname))
	SubmitButton.pack(pady=10)
	WizardWindow.protocol("WM_DELETE_WINDOW", onClosingWizardWindow)
	WizardWindow.resizable(False, False) 
	
	


	

def newProject(projectName):
	# Cut Text
	def cut_text(e):
		global selected
		# Check to see if keyboard shortcut used
		if e:
			selected = root.clipboard_get()
		else:
			if my_text.selection_get():
				# Grab selected text from text box
				selected = my_text.selection_get()
				# Delete Selected Text from text box
				my_text.delete("sel.first", "sel.last")
				# Clear the clipboard then append
				root.clipboard_clear()
				root.clipboard_append(selected)

	# Copy Text
	def copy_text(e):
		global selected
		# check to see if we used keyboard shortcuts
		if e:
			selected = root.clipboard_get()

		if my_text.selection_get():
			# Grab selected text from text box
			selected = my_text.selection_get()
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
				position = my_text.index(INSERT)
				my_text.insert(position, selected)

	# Bold Text
	def bold_it():
		# Create our font
		bold_font = font.Font(my_text, my_text.cget("font"))
		bold_font.configure(weight="bold")

		# Configure a tag
		my_text.tag_configure("bold", font=bold_font)

		# Define Current tags
		current_tags = my_text.tag_names("sel.first")

		# If statment to see if tag has been set
		if "bold" in current_tags:
			my_text.tag_remove("bold", "sel.first", "sel.last")
		else:
			my_text.tag_add("bold", "sel.first", "sel.last")

	# Italics Text
	def italics_it():
		# Create our font
		italics_font = font.Font(my_text, my_text.cget("font"))
		italics_font.configure(slant="italic")

		# Configure a tag
		my_text.tag_configure("italic", font=italics_font)

		# Define Current tags
		current_tags = my_text.tag_names("sel.first")

		# If statment to see if tag has been set
		if "italic" in current_tags:
			my_text.tag_remove("italic", "sel.first", "sel.last")
		else:
			my_text.tag_add("italic", "sel.first", "sel.last")

	# Change Selected Text Color
	def text_color():
		# Pick a color
		my_color = colorchooser.askcolor()[1]
		if my_color:
			# Create our font
			color_font = font.Font(my_text, my_text.cget("font"))

			# Configure a tag
			my_text.tag_configure("colored", font=color_font, foreground=my_color)

			# Define Current tags
			current_tags = my_text.tag_names("sel.first")

			# If statment to see if tag has been set
			if "colored" in current_tags:
				my_text.tag_remove("colored", "sel.first", "sel.last")
			else:
				my_text.tag_add("colored", "sel.first", "sel.last")

	# Change bg color
	def bg_color():
		my_color = colorchooser.askcolor()[1]
		if my_color:
			my_text.config(bg=my_color)

	# Print File Function
	def print_file():
		#printer_name = win32print.GetDefaultPrinter()
		#status_bar.config(text=printer_name)
		
		# Grab Filename
		file_to_print = filedialog.askopenfilename(initialdir="C:/gui/", title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

		# Check to see if we grabbed a filename
		if file_to_print:
			# Print the file
			win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)

	# Select all Text
	def select_all(e):
		# Add sel tag to select all text
		my_text.tag_add('sel', '1.0', 'end')

	# Clear All Text
	def clear_all():
		my_text.delete(1.0, END)

	def logPos(e):
		print(my_text.index(INSERT))

	def switchFullScreen(menu, screen):
		FullscreenLabel = menu.entrycget(1, "label")
		if(FullscreenLabel == "Fullscreen"):
			menu.entryconfigure(1, label="Exit Fullscreen")
			screen.attributes('-fullscreen',True)
		elif (FullscreenLabel == "Exit Fullscreen"):
			menu.entryconfigure(1, label="Fullscreen")
			screen.attributes('-fullscreen',False)
		
	def exitFullScreen(menu, screen):
		menu.entryconfigure(1, label="Fullscreen")
		screen.attributes('-fullscreen',False)

	def onClosingNewProjectWindow(currentText):
		if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
			MainFile = open("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Main.txt", "w")
			MainFile.write(my_text.get("1.0",END))
			MainFile.close()
			DateToday = date.today().strftime("%m.%d.%y")
			TimeNow = datetime.now().strftime("%H.%M.%S")
			try:
				os.mkdir("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday)
			except:
				pass
			
			# checking if last archived copy is same as current
			try:
				if not filecmp.cmp("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Main.txt", "C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday + "/" + sorted(os.listdir("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday))[-1]):
					NextArchive = open("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday + "/" + TimeNow + ".txt", "w")
					NextArchive.write(my_text.get("1.0",END))
					NextArchive.close()	
			except:
				NextArchive = open("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday + "/" + TimeNow + ".txt", "w")
				NextArchive.write(my_text.get("1.0",END))
				NextArchive.close()
			global sentinel
			sentinel = False
			NewProjectWindow.destroy()
			root.deiconify()

	def makeAlt(e):
		# Create our font
		my_color = "#0080c0"
		color_font = font.Font(my_text, my_text.cget("font"))

		# Configure a tag
		my_text.tag_configure("colored", font=color_font, foreground=my_color)

		# Define Current tags
		current_tags = my_text.tag_names("sel.first")

		# If statment to see if tag has been set
		if "colored" in current_tags:
			my_text.tag_remove("colored", "sel.first", "sel.last")
		else:
			my_text.tag_add("colored", "sel.first", "sel.last")

		
	
	NewProjectWindow = Toplevel(root)
	NewProjectWindow.title("Essay Writing System: " + projectName.get())
	NewProjectWindow.state('zoomed')

	ToolbarFrame = Frame(NewProjectWindow)
	ToolbarFrame.pack(fill=X)

	# Create Main Frame
	MainFrame = Frame(NewProjectWindow)
	MainFrame.pack(pady=5)

	# Create our Scrollbar For the Text Box
	TextScroll = Scrollbar(MainFrame)
	TextScroll.pack(side=RIGHT, fill=Y)

	# Horizontal Scrollbar
	#hor_scroll = Scrollbar(MainFrame, orient='horizontal')
	#hor_scroll.pack(side=BOTTOM, fill=X)

	# Create Text Box
	my_text = Text(MainFrame, width=80, height=31, font=("Calibri", 12), selectbackground="blue", selectforeground="black", undo=True, yscrollcommand=TextScroll.set, wrap=WORD, pady=30, padx=30)
	my_text.pack()
	# Configure our Scrollbar
	TextScroll.config(command=my_text.yview)

	# Create Menu
	MainMenu = Menu(NewProjectWindow)
	NewProjectWindow.config(menu=MainMenu)

	# Add File Menu
	FileMenu = Menu(MainMenu, tearoff=False)
	MainMenu.add_cascade(label="Controls", menu=FileMenu)
	#FileMenu.add_command(label="New", command=new_file)
	#FileMenu.add_command(label="Open", command=open_file)
	#FileMenu.add_command(label="Save", command=save_file)
	#FileMenu.add_command(label="Save As...", command=save_as_file)
	FileMenu.add_command(label="Print File", command=print_file)
	FileMenu.add_command(label="Fullscreen", command= lambda: switchFullScreen(FileMenu, NewProjectWindow))
	FileMenu.add_command(label="Exit", command=lambda: onClosingNewProjectWindow(my_text.get("1.0",END)))

	# Add Edit Menu
	EditMenu = Menu(MainMenu, tearoff=False)
	MainMenu.add_cascade(label="Edit", menu=EditMenu)
	EditMenu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
	EditMenu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
	EditMenu.add_command(label="Paste             ", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
	EditMenu.add_separator()
	EditMenu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")
	EditMenu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")
	EditMenu.add_separator()
	EditMenu.add_command(label="Select All", command=lambda: select_all(True), accelerator="(Ctrl+a)")
	EditMenu.add_command(label="Clear", command=clear_all)


	# Edit Bindings
	NewProjectWindow.bind('<Control-Key-x>', cut_text)
	NewProjectWindow.bind('<Control-Key-c>', copy_text)
	NewProjectWindow.bind('<Control-Key-v>', paste_text)
	NewProjectWindow.bind('<Control-Key-b>', bold_it)
	NewProjectWindow.bind('<Control-Key-i>', italics_it)
	NewProjectWindow.bind('<Control-A>', select_all)
	NewProjectWindow.bind('<Control-a>', select_all)
	NewProjectWindow.bind('<Control-Key-l>', logPos)
	NewProjectWindow.bind('<Escape>', lambda: [exitFullScreen(FileMenu, NewProjectWindow)])
	NewProjectWindow.bind('<Control-Key-s>', makeAlt)

	global StatusBar
	StatusBar = Label(NewProjectWindow, text="Ready", bd=1, relief=SUNKEN, anchor=E)
	StatusBar.pack(side=BOTTOM, fill=X)

	NewProjectWindow.protocol("WM_DELETE_WINDOW", lambda: onClosingNewProjectWindow(my_text.get("1.0",END)))
	

	start = time.time()
	while 1==1:
		NewProjectWindow.update_idletasks()
		NewProjectWindow.update()
		global sentinel
		if(sentinel == False):
			break
		global savingperiod
		if float(time.time() - start) > float(savingperiod.get()):
			start = time.time()
			MainFile = open("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Main.txt", "w")
			MainFile.write(my_text.get("1.0",END))#
			MainFile.close()
			DateToday = date.today().strftime("%m.%d.%y")
			TimeNow = datetime.now().strftime("%H.%M.%S")
			try:
				os.mkdir("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday)
			except:
				pass
			
			# checking if last archived copy is same as current
			try:
				if not filecmp.cmp("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Main.txt", "C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday + "/" + sorted(os.listdir("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday))[-1]):
					NextArchive = open("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday + "/" + TimeNow + ".txt", "w")
					NextArchive.write(my_text.get("1.0",END))
					NextArchive.close()
				
			except:
				NextArchive = open("C:/Users/750010316/Documents/Essays - Essay Writing System/" + projectName.get() + "/Archive/" + DateToday + "/" + TimeNow + ".txt", "w")
				NextArchive.write(my_text.get("1.0",END))
				NextArchive.close()
			

	

def openProject():
	# Grab Filename
	dir = filedialog.askdirectory(initialdir="C:/", title="Open File")
	os.chdir(dir)
	dirpath = os.path.basename(os.getcwd())
	print(dirpath)




root = Tk()
root.geometry("400x400")
root.title('Essay Writing System')
root.iconbitmap('C:\Program Files\EssayWritingTool\icon.ico')
NewProjectBtn = Button(root, text="Create New Project", command=newProjectWizard)
OpenProjectBtn = Button(root, text="Open Existing Project", command=openProject)
QuitButton = Button(root, text="Quit", command=root.destroy)
NewProjectBtn.pack(pady=(70,10))
OpenProjectBtn.pack(pady=10)
QuitButton.pack(pady=10)
root.resizable(False, False) 
root.mainloop()
