from tkinter import *
import login

#main method
def main():
    root = Tk()
    root.title("Xtreme Gym - Sistema de control de acceso | By Christopher Castro")
    root.geometry("1400x930+100+50")
    root.resizable(False, True)
    root.state('zoomed')
    root.config(bg="#f0f0f0")

    photo = PhotoImage(file = "./assets/icon.png")
    root.iconphoto(False, photo)
    #Parsing the root window to the Login class
    #Initiating the System
    login.Login(root)

    root.mainloop()

if __name__ == '__main__':
    main()
