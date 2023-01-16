import sqlite3 as sql

conn = sql.connect("cinema-info.db")
cursor = conn.cursor()


#tablo oluşturma
table1 = """CREATE TABLE IF NOT EXISTS cities(name,state,zip_code)"""
table2 = """CREATE TABLE IF NOT EXISTS cinemas(name,total_cinema_halls,location,halls)"""
table3 = """CREATE TABLE IF NOT EXISTS cinemahalls(name,total_seats,seats,shows)"""
table4 = """CREATE TABLE IF NOT EXISTS cinemahallseats(hall_seat_id,seat_type)"""
table5 = """CREATE TABLE IF NOT EXISTS shows(show_id,created_on,start_time,end_time,played_at,movie)"""
table6 = """CREATE TABLE IF NOT EXISTS movies(title,description,duration_in_mins,language,release_date,country,genre,movie_added_by,shows)"""
table7 = """CREATE TABLE IF NOT EXISTS bookings(booking_number,number_of_seats,created_on,status,show,seats,payment,owner)"""
table8 = """CREATE TABLE IF NOT EXISTS accounts(id,password,status,name,address,email,phone,account)"""
cursor.execute(table1)
cursor.execute(table2)
cursor.execute(table3)
cursor.execute(table4)
cursor.execute(table5)
cursor.execute(table6)
cursor.execute(table7)
cursor.execute(table8)

#deneme verileri ekleme
#cursor.execute("""INSERT INTO cities VALUES("Istanbul","Turkiye","34000")""") #cities tablosu için
#cursor.execute("""INSERT INTO cinemas VALUES("Kizilay","10","Ankara","none")""")
cursor.execute("""INSERT INTO cinemahalls VALUES("1","50","none","none")""")
cursor.execute("""INSERT INTO cinemahallseats VALUES ("012","orta")""")
cursor.execute("""INSERT INTO shows VALUES ("1234","27.10.2022","17.00","19.00","none","Star-Wars")""")
cursor.execute("""INSERT INTO movies VALUES("Star-Wars","best movie","120","ingilizce","20.10.2006","turkiye","bilim kurgu","none","none")""")
cursor.execute("""INSERT INTO bookings VALUES("1","2","27.12.2022","1","Star-Wars","none","1")""")
cursor.execute("""INSERT INTO accounts VALUES("1","password","status","Cem Yilmaz","address","cemyilmaz@hotmail.com","5054002030","customer")""")


conn.commit()
conn.close()