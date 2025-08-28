from tkinter import *
root = Tk()
root.title("Test Window")
root.geometry("1000x800")
root.geometry("1000x800+480+270")

lbl1 = Label(root, text = "와! 샌즈! 아시는구나!", width=30, height=4, font=("Helvetica", 24), bg="lightblue")
lbl1.location(0, -100)

sans = PhotoImage(file="sans.gif")
lbl2 = Label(root, image=sans)
lbl2.location(0, -200)

def Wa():
    lbl1.pack()
    lbl2.pack()

btn = Button(root, text="와!", command=Wa, width=3, height=5)
btn.location(0, -50)
btn.pack()

root.mainloop()
