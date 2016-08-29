from Tkinter import *

win = Tk()
win.config(bg="red")
win.geometry("255x355")
win.resizable(width=FALSE, height=FALSE)
win.title("--HORA DE MEDICACION--")

img1 = PhotoImage(file="../img/medicamento_blue.gif")
img2 = PhotoImage(file="../img/medicamento_green.gif")
canvas = Canvas(win)
canvas.pack(fill=BOTH, expand=1)
imgc1 = canvas.create_image(2, 2, image=img1, anchor=NW)

win.after(5000, lambda: canvas.delete(imgc1))
win.after(5000, lambda: canvas.create_image(2, 2, image=img2, anchor=NW))
win.bind('<Escape>', lambda e: win.destroy())
win.after(10000, lambda: win.destroy())

win.mainloop()