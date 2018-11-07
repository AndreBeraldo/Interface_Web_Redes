from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form
from wtforms import TextField, BooleanField,validators
from wtforms.validators import Required
from dbconnect import connection
import gc

app = Flask(__name__)
app.secret_key = '123'


class ipLinkForm(Form):
	ipLink = TextField('ipLink', validators=[validators.Length(min=4, max=150)])


@app.route('/')
def homepage():
	return render_template("index.html")

@app.route('/sobre/')
def sobre():
	return render_template("sobre.html")


@app.route('/getIpLink/')		
def getIpLink():
	try:
		mycursor2,mydb2 = connection()
		mycursor2.execute('SELECT * FROM linksespecificos')
		data = mycursor2.fetchall()
		mycursor2.close()
		mydb2.close()
		gc.collect()
		return render_template("getIpLink.html", listaIpLinks=data)
	except Exception as e:
		return(str(e))	


@app.route('/getIpLink/<id>', methods=["GET","POST"])	
def deleteIpLink(id):
	try:
		mycursor3,mydb3 = connection()
		consulta = "DELETE FROM linksespecificos WHERE ID= %s"
		mycursor3.execute(consulta,(id,))
		mycursor3.close()
		mydb3.close()
		gc.collect()
		flash("Link deletado!")
		return redirect(url_for('getIpLink'))
	except Exception as e:
		return(str(e))


@app.route('/getIpLink/', methods=["GET","POST"])
def ipLink():
	form = ipLinkForm(request.form)
	try:
		if request.method== 'POST' and form.validate():
			ipLink = form.ipLink.data
			mycursor,mydb = connection()
			mycursor.execute("INSERT INTO linksespecificos(ALVO) VALUES ('"+str(ipLink)+"')")
			mydb.commit()
			flash("LINK/IP inserido com sucesso")
			mycursor.close()
			mydb.close()
			return redirect(url_for("getIpLink"))
			
		else:
			mycursor2,mydb2 = connection()
			mycursor2.execute('SELECT ALVO FROM linksespecificos')
			data = mycursor2.fetchall()
			mycursor2.close()
			mydb2.close()
			return render_template("getIpLink.html", listaIpLinks=data)
	except Exception as e:
		return(str(e))


@app.route('/validarippaises/')	
def getValidarIpPaises():
	try:
		mycursor4,mydb4 = connection()
		mycursor4.execute('SELECT * FROM validarippaises')
		data = mycursor4.fetchall()
		mycursor4.close()
		mydb4.close()
		gc.collect()
		return render_template("validarippaises.html", listaValidarPaises=data)
	except Exception as e:
		return(str(e))


@app.route('/validarippaises/<id>/<tipo>', methods=["GET","POST"])	
def validarPais(id, tipo):
	try:
		mycursor6,mydb6 = connection()
		if tipo == "0":
			atualizacao = "UPDATE validarippaises SET FLAG=1 WHERE ID=%s"
			mycursor6.execute(atualizacao,(id,))
		else:
			atualizacao = "UPDATE validarippaises SET FLAG=0 WHERE ID=%s"
			mycursor6.execute(atualizacao,(id,))		
		mycursor6.close()
		mydb6.close()
		gc.collect()
		return redirect(url_for('getValidarIpPaises'))
	except Exception as e:
		return(str(e))


@app.route('/validarippaises/<tipo>', methods=["GET","POST"])	
def liberarBloquearTodos(tipo):
	try:
		mycursor,mydb = connection()
		if tipo == "0":
			atualizacao = "UPDATE validarippaises SET FLAG=0"
			mycursor.execute(atualizacao)		
		else:
			mycursor,mydb = connection()
			atualizacao = "UPDATE validarippaises SET FLAG=1"
			mycursor.execute(atualizacao)		
		mycursor.close()
		mydb.close()
		gc.collect()
		return redirect(url_for('getValidarIpPaises'))
	except Exception as e:
		return(str(e))


if __name__ == "__main__":
	app.run()