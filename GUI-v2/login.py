from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import admin
import instructor
from database import Database

# creating a database object
db = Database("mainDatabase.db")


class Login:
    def __init__(self, root):
        self.root = root

        self.username = StringVar()
        self.password = StringVar()

        # Background Color
        # self.root.config(bg="#ffffff")
        # self.frame = Frame(self.root, width=600, height=400)
        # self.frame.pack()
        # self.frame.place(anchor='center', relx=0.5, rely=0.5)

        # Call the tkinter frame to the window
        self.loginControlFrame()

    """CTA Methods"""

    # login method to redirect to the next frames
    def loginFunc(self):
        if self.txtUsername.get() == 'admin' and self.txtPassword.get() == 'admin':
            self.loginFrame.destroy()
            self.rightFrame.destroy()
            admin.AdminControls(self.root)
        # elif db.instructorLogin(self.txtUsername.get(), self.txtPassword.get()):
        elif self.txtUsername.get() == 'user' and self.txtPassword.get() == 'user':
            self.loginFrame.destroy()
            self.rightFrame.destroy()
            instructor.InstructorControls(self.root)
        else:
            messagebox.showerror("Error!", "Check your credentials or Please Contact System Admin!")
            self.username.set("")
            self.password.set("")

    """Login Frame"""

    def loginControlFrame(self):
        # Login Frame Configurations
        self.loginFrame = Frame(self.root)
        self.loginFrame.pack(side=LEFT, fill=X, padx=100)
        self.login_frame_title = Label(self.loginFrame, text="Iniciar Sesión", font=("Impact", 35), fg="black")
        self.login_frame_title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

        # Username
        self.labelUsername = Label(self.loginFrame, text="Usuario", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelUsername.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txtUsername = Entry(self.loginFrame, textvariable=self.username, font=("Times New Roman", 15), width=30,
                                 bd=5)
        self.txtUsername.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Password
        self.labelPassword = Label(self.loginFrame, text="Contraseña", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelPassword.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.txtPassword = Entry(self.loginFrame, textvariable=self.password, font=("Times New Roman", 15), width=30,
                                 bd=5, show="*")
        self.txtPassword.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Login Button
        self.btnLogin = Button(self.loginFrame, command=self.loginFunc, text="Login", bd=0, cursor="hand2",
                               fg="black", bg="#ff1909", width=10, font=("Impact", 15))
        self.btnLogin.grid(row=3, column=1, padx=10, sticky="e")

        # empty label for spacing in grid
        self.emptyLabel = Label(self.loginFrame, font=("Times New Roman", 16, "bold"))
        self.emptyLabel.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Right Side Frame as Welcome Message
        self.rightFrame = Frame(self.root)
        self.rightFrame.pack(side=RIGHT, padx=100)

        self.img = ImageTk.PhotoImage(Image.open("./assets/icon.png").resize((450, 350)))
        self.labelCompanyLogo = Label(self.rightFrame, image = self.img)
        self.labelCompanyLogo.grid(row=0, column=2, columnspan=2, padx=10)
        self.labelCompanyName = Label(self.rightFrame, text="Xtreme Gym", font=("Goudy Old Style", 55),
                                      fg="black")
        self.labelCompanyName.grid(row=1, column=2, columnspan=2, padx=10)
        self.labelDesc = Label(self.rightFrame, text="Xtreme Group", font=("Times New Roman", 25, "italic"),
                               fg="black")
        self.labelDesc.grid(row=2, column=2, columnspan=2, padx=10, pady=6)
