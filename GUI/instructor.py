from tkinter import *
from tkinter import ttk
from database import Database
from tkinter import messagebox
import login
import sessions
import access_control
import registration
from tkcalendar import *
from db.model import User as User
from datetime import datetime

class InstructorControls:
    def __init__(self, root):
        self.root = root

        # local variables
        self.userName = StringVar()
        self.userByName = StringVar()
        self.userPhone = StringVar()
        self.userEmail = StringVar()
        self.userLocation = StringVar()
        self.userDateInit = StringVar()
        self.userDateFinish = StringVar()

        # Call the tkinter frames to the window
        self.instructorControlsFrame()
        self.instructorFrameButtons()
        self.tableOutputFrame()

    """Student Info Entries Frame"""

    def instructorControlsFrame(self):
        # Instructor Control Frame Configurations
        self.entriesFrame = Frame(self.root)
        self.entriesFrame.pack(side=TOP, fill=X)
        self.instructor_frame_title = Label(self.entriesFrame, text="Panel de Control de Registros",
                                            font=("Impact", 35),
                                            fg="black")
        self.instructor_frame_title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

        # User Name
        self.labelUPhone = Label(self.entriesFrame, text="Nombre", font=("Times New Roman", 16, "bold"),
                                fg="black")
        self.labelUPhone.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txtUName = Entry(self.entriesFrame, textvariable=self.userName, font=("Times New Roman", 15), width=30)
        self.txtUName.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # User Phone
        self.labelUPhone = Label(self.entriesFrame, text="Teléfono", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelUPhone.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.txtUPhone = Entry(self.entriesFrame, textvariable=self.userPhone, font=("Times New Roman", 15), width=30)
        self.txtUPhone.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        # User Email
        self.labelEmail = Label(self.entriesFrame, text="Email", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelEmail.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.txtEmail = Entry(self.entriesFrame, textvariable=self.userEmail, font=("Times New Roman", 15), width=30)
        self.txtEmail.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # User Location
        self.labelLocation = Label(self.entriesFrame, text="Locación", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelLocation.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.comboLocation = ttk.Combobox(self.entriesFrame, textvariable=self.userLocation, font=("Times New Roman", 15),
                                        width=28,
                                        state="readonly")
        self.comboLocation['values'] = ("Matriz")
        self.comboLocation.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # User Date init
        self.labelDateInit = Label(self.entriesFrame, text="Fecha inicio", font=("Times New Roman", 16, "bold"),
                              fg="black")
        self.labelDateInit.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entryDateInit = DateEntry(self.entriesFrame, setmode='day', date_pattern='dd/mm/yyyy', textvariable=self.userDateInit,
                                  font=("Times New Roman", 12), width=35, locale='es_ES')
        self.entryDateInit.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # User date finish
        self.labelDateFinish = Label(self.entriesFrame, text="Fecha fin", font=("Times New Roman", 16, "bold"),
                                fg="black")
        self.labelDateFinish.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.entryDateFinish = DateEntry(self.entriesFrame, setmode='day', date_pattern='dd/mm/yyyy', textvariable=self.userDateFinish,
                                  font=("Times New Roman", 12), width=35, locale='es_ES')
        self.entryDateFinish.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # User History
        self.labelHistory = Label(self.entriesFrame, text="Historial de acceso", font=("Times New Roman", 16, "bold"), fg="black")
        self.labelHistory.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.txtUHistory = Text(self.entriesFrame, font=("Times New Roman", 15), width=82, height=3)
        self.txtUHistory.grid(row=4, column=1, padx=10, pady=5, sticky="w", columnspan=4)

        # Search by Name
        self.labelUByName = Label(self.entriesFrame, text="Búsqueda por nombre", font=("Times New Roman", 16, "bold"),
                                fg="black")
        self.labelUByName.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.txtUByName = Entry(self.entriesFrame, textvariable=self.userByName, font=("Times New Roman", 15), width=82)
        self.txtUByName.grid(row=5, column=1, padx=10, pady=5, sticky="w", columnspan=4)

    """Sub Methods to be used in primary CTA methods"""

    # event trigger Method to display the chosen data from the TreeView back in respective fields
    def getData(self, event):
        try:
            self.selectedRow = self.out.focus()
            self.selectedData = self.out.item(self.selectedRow)
            self.chosenRow = self.selectedData["values"]
            self.userName.set(self.chosenRow[1])
            self.userEmail.set(self.chosenRow[2])
            self.userPhone.set(self.chosenRow[3])
            self.userLocation.set(self.chosenRow[4])
            self.userDateInit.set(self.chosenRow[6])
            self.userDateFinish.set(self.chosenRow[7])
            self.txtUHistory.configure(state='normal')
            self.txtUHistory.delete(1.0, END)
            self.txtUHistory.insert(END, self.chosenRow[5])
            self.txtUHistory.configure(state='disabled')
        except IndexError as error:
            pass

    """CTA Methods"""

    # Method to create a new Student
    def regUser(self):
        # if self.txtUName.get() == "" or self.entryDateFinish.get() == "" or self.txtUPhone.get() == "" or self.entryDateInit.get() == "" or self.txtEmail.get() == "" or self.comboLocation.get() == "" or self.txtUHistory.get(
        #         1.0, END) == "":
        #     messagebox.showerror("Error!", "Please fill all the fields!")
        #     return

        # db.insertStudent(self.txtUName.get(), self.txtUPhone.get(), self.txtEmail.get(), self.entryDateInit.get(),
        #                  self.comboLocation.get(),
        #                  self.entryDateFinish.get(), self.txtUHistory.get(1.0, END))
        try:
            # self.tempName = db.selectStudent(self.chosenRow[0])
            self.entriesFrame.destroy()
            self.buttonsFrame.destroy()
            self.tableFrame.destroy()
            # sessions.BookSession(self.root, self.tempName)
            registration.Registration(self.root)
            # messagebox.showinfo("Success!", "Record Successfully Insertered!")
        except AttributeError as error:
            print(error)
            messagebox.showerror("Error!", "Please View and Select a Student to Book a Session!")
        # self.resetForm()
        # self.viewStudents()

    # Method to update selected student details
    def updateStudent(self):
        if self.txtUName.get() == "" or self.entryDateFinish.get() == "" or self.txtUPhone.get() == "" or self.entryDateInit.get() == "" or self.txtEmail.get() == "" or self.comboLocation.get() == "":
            messagebox.showerror("Error!", "Choose a Student to Update Details!")
            return
        user = User.get(self.chosenRow[0])
        user.update(actions=[
                User.FullName.set(self.txtUName.get()),
                User.email.set(self.txtEmail.get()),
                User.phone.set(self.txtUPhone.get()),
                User.location.set(self.comboLocation.get()),
                User.suscription_start.set(self.entryDateInit.get()),
                User.suscription_end.set(self.entryDateFinish.get()),
                # User.access_history.set(self.txtUHistory.get(1.0, END))
            ])
        # from pynamodb.connection import Connection
        # from pynamodb.transactions import TransactWrite
        # connection = Connection()
        # user = User(self.chosenRow[0])
        # with TransactWrite(connection=connection) as transaction:
        #     transaction.update(
        #         user,
        #         actions=[
        #             User.FullName.set(self.txtUName.get()),
        #             User.email.set(self.txtEmail.get()),
        #             User.phone.set(self.txtUPhone.get()),
        #             User.location.set(self.comboLocation.get()),
        #             User.suscription_start.set(self.entryDateInit.get()),
        #             User.suscription_end.set(self.entryDateFinish.get()),
        #             # # User.access_history.set(self.txtUHistory.get(1.0, END))
        #         ]
        #     )
        messagebox.showinfo("Success!", "Record Successfully Updated!")
        self.resetForm()
        self.viewStudents()

    # Method to display all students in the Treeview Frame
    def viewStudents(self):
        self.out.delete(*self.out.get_children())  # emptying the table before reloading
        # for user in User.scan(limit=10):
        #     self.out.insert("", END, values=(user.RekognitionId, user.FullName, user.email, user.phone, user.location, user.access_history, user.suscription_start, user.suscription_end))
        for user in User.FullName_index.scan(User.FullName.contains(self.userByName.get()), limit=10) :
            self.out.insert("", END, values=(user.RekognitionId, user.FullName, user.email, user.phone, user.location, user.access_history, user.suscription_start, user.suscription_end))

    # Method to direct to the next Frame to access control window
    def access_control(self):
        try:
            # self.tempName = db.selectStudent(self.chosenRow[0])
            self.entriesFrame.destroy()
            self.buttonsFrame.destroy()
            self.tableFrame.destroy()
            # sessions.BookSession(self.root, self.tempName)
            access_control.AccessControl(self.root)
        except AttributeError as error:
            print(error)
            messagebox.showerror("Error!", "Please View and Select a Student to Book a Session!")

    # Method to reset all input widgets in the frame
    def resetForm(self):
        self.userName.set("")
        self.userByName.set("")
        self.userPhone.set("")
        self.userLocation.set("")
        self.userDateInit.set("")
        self.userDateFinish.set("")
        self.userEmail.set("")
        self.txtUHistory.configure(state='normal')
        self.txtUHistory.delete(1.0, END)
        self.txtUHistory.configure(state='disabled')

    # Method to redirect to the login frame
    def logOut(self):
        self.entriesFrame.destroy()
        self.buttonsFrame.destroy()
        self.tableFrame.destroy()
        login.Login(self.root)

    # CTA Buttons
    def instructorFrameButtons(self):
        # Button Frame Configurations
        self.buttonsFrame = Frame(self.entriesFrame)
        self.buttonsFrame.grid(row=9, column=1, padx=10, pady=10, sticky="w", columnspan=8)

        # Add a new Record
        self.btnAdd = Button(self.buttonsFrame, command=self.regUser, text="Registrar Cliente", bd=0, cursor="hand2",
                             bg="#ff1909",
                             fg="black", width=15, font=("Impact", 15))
        self.btnAdd.grid(row=0, column=0, padx=0)

        # Update Selected Record
        self.btnUpdate = Button(self.buttonsFrame, command=self.updateStudent, text="Actualizar Cliente", bd=0,
                                cursor="hand2",
                                bg="#ff1909",
                                fg="black", width=15, font=("Impact", 15))
        self.btnUpdate.grid(row=0, column=1, padx=10)

        # Reset Widget Inputs
        self.btnReset = Button(self.buttonsFrame, command=self.resetForm, text="Limpiar", bd=0, cursor="hand2",
                               bg="#ff1909", fg="black", width=10, font=("Impact", 15))
        self.btnReset.grid(row=0, column=2, padx=10)

        # Display List
        self.btnView = Button(self.buttonsFrame, command=self.viewStudents, text="Buscar", bd=0,
                              cursor="hand2",
                              bg="#ff1909",
                              fg="black", width=15, font=("Impact", 15))
        self.btnView.grid(row=0, column=3, padx=210)

        # Book a Session
        self.btnBook = Button(self.entriesFrame, command=self.access_control, text="Control de Acceso", bd=0, cursor="hand2",
                              bg="#ff1909",
                              fg="black", width=15, font=("Impact", 15))
        self.btnBook.grid(row=0, column=4, padx=0)

        # LogOut
        self.btnLogOut = Button(self.entriesFrame, command=self.logOut, text="Salir", bd=0, cursor="hand2",
                                bg="#ff1909",
                                fg="black", width=15, font=("Impact", 15))
        self.btnLogOut.grid(row=0, column=5, padx=50, sticky="e")

    """Table Frame using TreeView"""

    def tableOutputFrame(self):
        # Treeview Frame Configurations
        self.tableFrame = Frame(self.root, bg="#DADDE6")
        self.tableFrame.place(x=0, y=400, width=1400, height=560)
        self.yScroll = Scrollbar(self.tableFrame)
        self.yScroll.pack(side=RIGHT, fill=Y)

        # ttk style object to add configurations
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", font=('Calibri', 12),
                             rowheight=70)
        self.style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky="w")

        # Formatting the output table view
        self.out = ttk.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set, columns=(1, 2, 3, 4, 5, 6, 7, 8),
                                style="mystyle.Treeview")
        self.out.column("0", width=30)
        self.out.column("1", width=50)
        self.out.heading("1", text="Index")
        self.out.heading("2", text="Nombre")
        self.out.column("2", width=250)
        self.out.heading("3", text="Email")
        self.out.column("3", width=250)
        self.out.heading("4", text="Teléfono")
        self.out.column("4", width=100)
        self.out.heading("5", text="Locación")
        self.out.column("5", width=100)
        self.out.heading("6", text="Historial")
        self.out.column("6", width=200)
        self.out.heading("7", text="Fecha inicio")
        self.out.column("7", width=100)
        self.out.heading("8", text="Fecha fin")
        self.out.column("8", width=100)
        self.out['show'] = 'headings'

        # Virtual Events to trigger methods
        self.out.bind("<ButtonRelease-1>", self.getData)

        # TreeView output layout configurations
        self.out.pack(fill=BOTH)
        self.yScroll.config(command=self.out.yview)
