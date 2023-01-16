import tkinter as ttk
import sqlite3 as sql
from datetime import date



class RegistirationWindow(ttk.Tk):
    def __init__(self):
        super().__init__()
        self.conn = sql.connect("cinema-info.db")
        self.cursor = self.conn.cursor()
        self.title("Giriş Yap")

        self.nameVar = ttk.StringVar()
        self.passwordVar = ttk.StringVar()
        self.frame = ttk.Frame(self,bg= "lightblue")

        self.nameLabel = ttk.Label(self.frame,text="Kullanıcı adı: ",bg = "lightblue")
        self.nameLabel.grid(row=0,column=0,pady=10,padx=10)
        self.nameEntry = ttk.Entry(self.frame, textvariable=self.nameVar)
        self.nameEntry.grid(row=0,column=1,padx=10,pady=10)

        self.passwordLabel = ttk.Label(self.frame, text="Şifre: ", bg="lightblue")
        self.passwordLabel.grid(row=1, column=0, pady=10, padx=10)
        self.passwordEntry = ttk.Entry(self.frame, textvariable=self.passwordVar)
        self.passwordEntry.grid(row=1, column=1, padx=10, pady=10)

        self.SignInButton = ttk.Button(self.frame, text= "Giriş yap",width=10,height=1,
                                       command=lambda: self.submit(self.nameVar.get(),self.passwordVar.get()))
        self.SignInButton.grid(padx=10,pady=10,row=2,column=0)

        self.SignUpButton = ttk.Button(self.frame, text="Kaydol", width=10, height=1,
                                       command=lambda: self.SignUpScreen())
        self.SignUpButton.grid(padx=10, pady=10, row=2, column=1)

        self.frame.pack()


    def submit(self,name,password):

        self.name = name
        self.password = password
        print("name: " + self.name)
        print("password: "+self.password)
        self.cursor.execute("SELECT name, *FROM accounts")
        self.names = list(self.cursor.fetchall())
        self.cursor.execute("SELECT password, *FROM accounts")
        self.passwords = list(self.cursor.fetchall())

        for i in self.names:
            for j in self.passwords:
                if self.name == i[0] and self.password == j[0]:
                    self.destroy()
                    self.pencere = MainScreen(name)
                    self.pencere.mainloop()
                    break
                else:
                    self.nameLabel1 = ttk.Label(self.frame, text="Hatalı deneme", bg="red")
                    self.nameLabel1.grid(row=4, column=0, pady=10, padx=10)


    def SignUpScreen(self):
        self.pencere = SignUpScreen()
        self.destroy()
        self.pencere.mainloop()

class SignUpScreen(ttk.Tk):
    def __init__(self):
        super().__init__()

        self.conn = sql.connect("cinema-info.db")
        self.cursor = self.conn.cursor()
        self.title("Kaydol")
        self.nameVar = ttk.StringVar(self)
        self.passwordVar = ttk.StringVar(self)
        self.phoneNumberVar = ttk.StringVar(self)
        self.emailVar = ttk.StringVar(self)
        self.addressVar = ttk.StringVar(self)
        self.frame = ttk.Frame(self,bg="lightblue",width=300,height=300)

        self.nameLabel = ttk.Label(self.frame,text= "İsim: ",bg="lightblue")
        self.nameLabel.grid(row=0,column=0,pady=10,padx=10)
        self.nameEntry = ttk.Entry(self.frame,textvariable=self.nameVar)
        self.nameEntry.grid(row=0,column=1,padx=10,pady=10)

        self.passwordLabel = ttk.Label(self.frame, text="Şifre: ", bg="lightblue")
        self.passwordLabel.grid(row=0, column=2, pady=10, padx=10)
        self.passwordEntry = ttk.Entry(self.frame, textvariable=self.passwordVar)
        self.passwordEntry.grid(row=0, column=3, padx=10, pady=10)

        self.phoneNumberLabel = ttk.Label(self.frame, text="Telefon: ", bg="lightblue")
        self.phoneNumberLabel.grid(row=1, column=0, pady=10, padx=10)
        self.phoneNumberEntry = ttk.Entry(self.frame, textvariable=self.phoneNumberVar)
        self.phoneNumberEntry.grid(row=1, column=1, padx=10, pady=10)

        self.emailLabel = ttk.Label(self.frame, text="E-mail: ", bg="lightblue")
        self.emailLabel.grid(row=1, column=2, pady=10, padx=10)
        self.emailEntry = ttk.Entry(self.frame, textvariable=self.emailVar)
        self.emailEntry.grid(row=1, column=3, padx=10, pady=10)

        self.addressLabel = ttk.Label(self.frame, text="Adres: ", bg="lightblue")
        self.addressLabel.grid(row=2, column=0, pady=10, padx=10)
        self.addressEntry = ttk.Entry(self.frame, textvariable=self.addressVar)
        self.addressEntry.grid(row=2, column=1, padx=10, pady=10)

        self.submitButton = ttk.Button(self.frame,text="Onayla",width=10,height=1,command=self.submit)
        self.submitButton.grid(pady=10,padx=10,row=2,column=3)
        self.frame.pack()


    def submit(self):
        print("Signed up new user")
        self.cursor.execute("SELECT id , * FROM accounts")
        self.last_number = self.cursor.fetchall()[-1][0]
        self.data = (str(int(self.last_number)+1), self.passwordVar.get(), "1", self.nameVar.get(), self.addressVar.get(), self.emailVar.get(), self.phoneNumberVar.get(), "Customer")
        print(self.data)
        self.cursor.execute("INSERT INTO accounts VALUES(?,?,?,?,?,?,?,?)",self.data)
        self.conn.commit()
        self.destroy()
        self.pencere = RegistirationWindow()
        self.pencere.mainloop()

class MainScreen(ttk.Tk):
    def __init__(self,accountName):
        super().__init__()
        self.accountName = accountName
        self.conn = sql.connect("cinema-info.db")
        self.columnNamesList = ["BAŞLIK","AÇIKLAMA","SÜRE","DİL","YAYINLAMA TARİHİ",
                                "ÜLKE","TÜR","EKLENME","GÖSTERİMLER"]
        self.columnLabelList = []

        self.cursor = self.conn.cursor()
        self.userState = "Costumer"
        #self.geometry("1150x900")
        self.title("Sinema Rezervasyonu")
        #self.resizable(False,False)

        self.mainFrame = ttk.Frame(self,width=700,height=100,bg="SteelBlue1")
        self.bookingFrame = ttk.Frame(self,width=700,height=200,bg="gray73")
        self.bookingTitleFrame = ttk.Frame(self,bg="gray73")

        for i in range(0,len(self.columnNamesList)):
            self.columnLabelList.append(ttk.Label(self.mainFrame,text=self.columnNamesList[i],width=15,height=2,bg="RoyalBlue3",bd=1,relief="solid"))
            self.columnLabelList[i].grid(row=0,column=i,pady=5)

        if self.userState == "Guest":
            self.GuestScreen()
        elif self.userState == "Costumer":
            self.CostumerScreen()
        self.DatabaseTreeView()
        self.mainFrame.grid(sticky="ew")
        self.bookingTitleFrame.grid(sticky="nsew")
        self.bookingFrame.grid(sticky="ew")


    def GuestScreen(self):
        pass

    def titles(func):
        def wrapper(self):
            self.bookingTitleList = ["ID","KOLTUK SAYISI","OLUŞTURULMA TARİHİ","DURUM","GÖSTERİM","KOLTUKLAR","REZERVASYON SAHİBİ","FİLM","SİNEMA","SALON"]
            self.bookingLabelList = []
            for i in range(0, len(self.bookingTitleList)):
                self.bookingLabelList.append(
                    ttk.Label(self.bookingFrame, text=self.bookingTitleList[i], width=16, height=2, bg="lightsteelblue",borderwidth=2,relief="solid"))
                self.bookingLabelList[i].grid(row=1, column=i, pady=5)
            func(self)
        return wrapper

    @titles
    def CostumerScreen(self):
        self.bookingTitle = ttk.Label(self.bookingTitleFrame, text="Aktif Rezervasyonlar",
                                      bg="gray73", font="Times 20 italic")
        self.bookingTitle.grid(row=0, column=5, padx=10, pady=10,sticky="ew")

        self.cursor.execute("SELECT * FROM bookings WHERE owner = (?)",(self.accountName,))
        self.items = self.cursor.fetchall()
        self.bookList = []
        self.rowList = []

        for i in self.items:
            self.bookList.append(list(i))
        for i in range(0,len(self.bookList)):
            self.list0 = []
            for j in range(0,len(self.bookList[i])):
                self.list0.append(ttk.Label(self.bookingFrame,text=self.bookList[i][j],width=15,height=2,bg="gray73"))
            self.rowList.append(self.list0)
        for i in range(0,len(self.rowList)):
            for j in range(1,len(self.rowList[i])):
                self.rowList[i][j-1].grid(row=i+2, column=j-1, pady=5)



    def AdminScreen(self):
        pass
    def FrontDeskOfficerScreen(self):
        pass

    def DatabaseTreeView(self):
        self.cursor.execute("SELECT * FROM movies")
        self.items = self.cursor.fetchall()
        self.movieList = []
        self.rowList = []


        for i in self.items:
            self.movieList.append(list(i))
        for i in range(0,len(self.movieList)):
            self.list0 = []
            for j in range(0,len(self.movieList[i])):
                self.list0.append(ttk.Label(self.mainFrame,text=self.movieList[i][j],width=15,height=2,bg="SteelBlue1",bd=1,relief="solid"))
            self.list0.append(ttk.Button(self.mainFrame,text="Rezervasyon",width=20,height=1,command=lambda: self.BookingScreen(self.movieList[i][0]),bg= "lightcyan2"))
            self.rowList.append(self.list0)
        for i in range(0,len(self.rowList)):
            for j in range(1,len(self.rowList[i])):
                self.rowList[i][j-1].grid(row=i+1, column=j-1,)
            self.rowList[i][9].configure(command=lambda i=i: self.BookingScreen(i))
            self.rowList[i][9].grid(row=i+1,column=9)

    def BookingScreen(self,buttonValue):
        self.destroy()
        self.pencere = BookingScreen(self.accountName,self.movieList[buttonValue][0])
        self.pencere.mainloop()


class BookingScreen(ttk.Tk):
    def __init__(self,owner,movieID):
        super().__init__()

        self.owner = owner
        self.movieID = movieID

        self.frame = ttk.Frame(self,width= 300,height=300,bg= "lightblue")
        self.title("Rezervasyon Yap")
        self.conn = sql.connect("cinema-info.db")
        self.cursor = self.conn.cursor()

        self.cities = []
        self.cinemas = []
        self.halls = []
        self.seats = []
        self.shows = []

        self.cityVar = ttk.StringVar(self)
        self.cinemaVar = ttk.StringVar(self)
        self.hallVar = ttk.StringVar(self)
        self.seatVar = ttk.StringVar(self)
        self.showVar = ttk.StringVar(self)

        self.cursor.execute("SELECT name, * FROM cities")
        for i in self.cursor.fetchall():
            self.cities.append(i[0])
        print(self.cities)

        self.cursor.execute("SELECT name, * FROM cinemas")
        for i in self.cursor.fetchall():
            self.cinemas.append(i[0])
        print(self.cinemas)

        self.cursor.execute("SELECT name, * FROM cinemahalls")
        for i in self.cursor.fetchall():
            self.halls.append(i[0])
        print(self.halls)

        self.cursor.execute("SELECT hall_seat_id, * FROM cinemahallseats")
        for i in self.cursor.fetchall():
            self.seats.append(i[0])
        print(self.seats)

        self.cursor.execute("SELECT start_time, * FROM shows")
        for i in self.cursor.fetchall():
            self.shows.append(i[0])
        print(self.shows)

        self.cityVar.set(self.cities[0])
        self.cinemaVar.set(self.cinemas[0])
        self.hallVar.set(self.halls[0])
        self.seatVar.set(self.seats[0])
        self.showVar.set(self.shows[0])


        self.label1 = ttk.Label(self.frame,text= "Şehir Seçimi",width=15,height=2,bg="lightblue")
        self.label2 = ttk.Label(self.frame, text= "Sinema Seçimi", width=15, height=2,bg="lightblue")
        self.label3 = ttk.Label(self.frame, text="Salon Seçimi", width=15, height=2,bg="lightblue")
        self.label4 = ttk.Label(self.frame, text="Koltuk Numarası", width=15, height=2,bg="lightblue")
        self.label5 = ttk.Label(self.frame, text="Saat", width=15, height=2, bg="lightblue")

        self.label1.grid(row=0, column=0, pady=5, padx=5)
        self.label2.grid(row=1, column=0, pady=5, padx=5)
        self.label3.grid(row=2, column=0, pady=5, padx=5)
        self.label4.grid(row=3, column=0, pady=5, padx=5)
        self.label5.grid(row=4, column=0, pady=5, padx=5)

        self.optionMenu1 = ttk.OptionMenu(self.frame,self.cityVar, *self.cities,)
        self.optionMenu2 = ttk.OptionMenu(self.frame, self.cinemaVar, *self.cinemas)
        self.optionMenu3 = ttk.OptionMenu(self.frame, self.hallVar, *self.halls)
        self.optionMenu4 = ttk.OptionMenu(self.frame, self.seatVar, *self.seats)
        self.optionMenu5 = ttk.OptionMenu(self.frame, self.showVar, *self.shows)

        self.optionMenu1.grid(row=0, column=1, pady=5,padx=5, sticky="ew")
        self.optionMenu2.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        self.optionMenu3.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        self.optionMenu4.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        self.optionMenu5.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        self.placeBookButton = ttk.Button(self.frame,text="Onayla",width=10,height=1,command=lambda: self.PlaceBook())
        self.placeBookButton.grid(row=5, column=0, padx=5, pady=5)

        self.frame.pack()
        self.conn.commit()





    def PlaceBook(self):
        print("book placed")
        self.cursor.execute("SELECT booking_number , * FROM bookings")
        self.last_number = self.cursor.fetchall()[-1][0]
        self.data = (str(int(self.last_number)+1), "1", str(date.today()), "1", self.showVar.get(), self.seatVar.get(),"1", self.owner, str(self.movieID), self.cinemaVar.get(), self.hallVar.get())
        self.cursor.execute("INSERT INTO bookings VALUES(?,?,?,?,?,?,?,?,?,?,?)",self.data)
        self.conn.commit()
        self.destroy()
        self.pencere = MainScreen(self.owner)
        self.pencere.mainloop()



def main():
    conn = sql.connect("cinema-info.db")
    pencere1 = RegistirationWindow()
    pencere1.mainloop()
    conn.close()


if __name__ == '__main__':
    main()


