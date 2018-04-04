import tkinter as tk

def helloWorld():
  #root creates the root widget, aka the window that pops up
  root = tk.Tk()

  # creates the label widget, attaches it to root, gives it text
  w = tk.Label(root, text="Hello Tkinter!")
  #tells Tk to fit size of window to given text
  w.pack()
  #window won't appear until we enter the Tkinter event loop
  root.mainloop()

def images():
  root = tk.Tk()
  logo = tk.PhotoImage(file="test.gif")

  explanation = """At present, only GIF and PPM/PGM
  formats are supported, but an interface 
  exists to allow additional image file
  formats to be added easily."""

  # tk.Label(root,
    # justify=tk.CENTER,
    # padx=10,
    # text=explanation).pack(side="right")
  # tk.Label(root, image=logo).pack(side="left")

  tk.Label(
    root,
    justify = tk.LEFT,
    compound = tk.LEFT,
    padx = 10,
    text = explanation,
    image = logo
  ).pack(side="right")

  root.mainloop()

def labels():
  import tkinter as tk

  root = tk.Tk()
  tk.Label(root,
          text="Red Text in Times Font",
          fg="red",
          padx=20,
          font="Times").pack()
  tk.Label(root,
          text="Green Text in Helvetica Font",
          fg="light green",
          bg="dark green",
          font="Helvetica 32 bold italic").pack()
  tk.Label(root,
          text="Blue Text in Verdana bold",
          fg="blue",
          bg="yellow",
          font="Verdana 10 bold").pack()

  root.mainloop()

# counter = 0 
# def counter_label(label):
#   def count():
#     global counter
#     counter += 1
#     label.config(text=str(counter))
#     label.after(1000, count)
#   count()


# root = tk.Tk()
# root.title("Counting Seconds")
# label = tk.Label(root, fg="green")
# label.pack()
# counter_label(label)
# button = tk.Button(root, text='Stop', width=25, command=root.destroy)
# button.pack()
# root.mainloop()

def messageWidget():
  master = tk.Tk()
  whatever_you_do = "Whatever you do will be insignificant, but it is very important that you do it.\n(Mahatma Gandhi)"
  msg = tk.Message(master, text=whatever_you_do)
  msg.config(bg='lightgreen', font=('times', 24, 'italic'))
  msg.pack()
  tk.mainloop()

def buttons():
  def write_slogan():
    print("Tkinter is easy to use!")

  root = tk.Tk()
  frame = tk.Frame(root)
  frame.pack()

  button = tk.Button(frame,
                    text="QUIT",
                    fg="red",
                    command=quit)
  button.pack(side=tk.LEFT)
  slogan = tk.Button(frame,
                    text="Hello",
                    command=write_slogan)
  slogan.pack(side=tk.LEFT)

  root.mainloop()

def entryWidget():
  master = tk.Tk()
  tk.Label(master, text="First Name").grid(row=0)
  tk.Label(master, text="Last Name").grid(row=1)

  e1 = tk.Entry(master)
  e2 = tk.Entry(master)

  e1.grid(row=0, column=1)
  e2.grid(row=1, column=1)

  master.mainloop()

entryWidget()