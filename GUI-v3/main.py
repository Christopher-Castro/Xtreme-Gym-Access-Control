from tkinter import *
# import login
import access_control

#main method
def main():
    root = Tk()
    root.title("Sistema de control de acceso | By Christopher Castro")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    root.resizable(False, True)
    # root.wm_state('zoomed')
    root.config(bg="#f0f0f0")

    photo = PhotoImage(file = "./assets/icon.png")
    root.iconphoto(False, photo)
    #Parsing the root window to the Login class
    #Initiating the System
    access_control.AccessControl(root)

    root.mainloop()

if __name__ == '__main__':
    main()
