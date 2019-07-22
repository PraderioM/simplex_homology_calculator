import tkinter as tk

from gui import GUI

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Simplex homology calculator')
    GUI(root).pack(fill="both", expand=True)
    root.mainloop()
