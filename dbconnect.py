import mysql.connector

def connection():
	mydb = mysql.connector.connect(
		host="162.241.2.202",
		database="andredev_trabalho_redes2",
		user="andredev_redes2",
		passwd="redes2"
		)

	mycursor = mydb.cursor()
	return mycursor,mydb