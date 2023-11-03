import mysql.connector
import json
from flask import Flask,render_template,request,jsonify
from functools import wraps

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="mysql"
)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify(message="Authorization required"), 401

        token = auth_header.split("Bearer ")[-1]
        if token != SECRET_TOKEN:
            return jsonify(message="Invalid token"), 401

        return f(*args, **kwargs)
    return decorated

def getData(sqlCommand):
    data = []
    try:
        cursor = mydb.cursor()
        cursor.execute(sqlCommand)

        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        for row in result:
            data.append(dict(zip(columns, row)) if row else None)
    except Exception as e:
        data=[]
    finally:
        cursor.close()
    return json.dumps(data)

def updateData(data,id):
    try:
        cursor = mydb.cursor()

        check_sql = f"SELECT id FROM mysql.Games WHERE id = {id};"
        cursor.execute(check_sql)
        existing_game = cursor.fetchone()

        if not existing_game:
            return jsonify({"error": f"O jogo com o ID: {id} não existe."})

        sqlCommand = f'''
            UPDATE mysql.Games
            SET Name = '{data["Name"]}', Platform = '{data["Platform"]}', Year = {data["YearOfRelease"]},
                Genre = '{data["Genre"]}', Publisher = '{data["Publisher"]}', NA_Sales = {data["NA_Sales"]},
                EU_Sales = {data["EU_Sales"]}, JP_Sales = {data["JP_Sales"]}, Other_Sales = {data["Other_Sales"]},
                Global = {data["Global_Sales"]}, Critical_Score = {data["Critic_Score"]},
                Critical_Count = {data["Critic_Count"]}, User_Score = {data["User_Score"]},
                User_Count = {data["User_Count"]}, Developer = '{data["Developer"]}', Rating = {data["Rating"]}
            WHERE id = {id};
        '''
        cursor.execute(sqlCommand)
        mydb.commit()
        cursor.close()

        return jsonify({"message": "Game updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

def postData(data):
    try:
        cursor = mydb.cursor()
        sqlCommand = f'''
            INSERT INTO  mysql.Games
            (Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global, Critical_Score, Critical_Count, User_Score, User_Count, Developer, Rating) VALUES (
            '{data["Name"]}', '{data["Platform"]}', {data["YearOfRelease"]}, 
            '{data["Genre"]}', '{data["Publisher"]}', {data["NA_Sales"]}, 
            {data["EU_Sales"]}, {data["JP_Sales"]}, {data["Other_Sales"]}, 
            {data["Global_Sales"]}, {data["Critic_Score"]}, {data["Critic_Count"]}, 
            {data["User_Score"]}, {data["User_Count"]}, '{data["Developer"]}', {data["Rating"]});
        '''
        cursor.execute(sqlCommand)
        mydb.commit()

    except Exception as e:
        return jsonify({"Erro": str(e)})
    finally:
        cursor.close()
    return jsonify({"message": "Data added successfully"})

def deleteData(id):
    try:
        cursor = mydb.cursor()

        check_sql = f"SELECT id FROM mysql.Games WHERE id = {id};"
        cursor.execute(check_sql)
        existing_game = cursor.fetchone()

        if not existing_game:
            return jsonify({"error": f"O jogo com o ID: {id} não existe."})

        delete_sql = f"DELETE FROM mysql.Games WHERE id = {id};"
        cursor.execute(delete_sql)
        mydb.commit()
        cursor.close()

        return jsonify({"message": "Game deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

app = Flask(__name__, static_url_path='/static')
SECRET_TOKEN = "CHAVE API"

@app.route("/")
def home():
    return render_template("index.html",api_key="X}u~Pree#wrNj3_0v;&('h+_!")

@app.route("/getAllGames")
@requires_auth
def getAllGames():
    data=json.loads(getData("select * from mysql.Games"))
    return jsonify(data)

@app.route("/getGameID/<id>")
@requires_auth
def getGameID(id):
    data=json.loads(getData(f"select * from mysql.Games where id={id}"))
    return jsonify(data)

@app.route("/getAllGamesByConsole/<console>", methods = ["GET"])
@requires_auth
def getAllGamesByConsole(console):
    data=json.loads(getData(f"select * from mysql.Games where Platform = '{console}'"))
    return jsonify(data)

@app.route("/getAllByYear/<year>",methods = ["GET"])
@requires_auth
def getAllByYear(year):
    data=json.loads(getData(f"select * from mysql.Games where Year = '{year}'"))
    return jsonify(data)

@app.route("/getAllByGenre/<genre>",methods = ["GET"])
@requires_auth
def getAllByGenre(genre):
    data=json.loads(getData(f"select * from mysql.Games where Genre = '{genre}'"))
    return jsonify(data)

@app.route("/getAllByPublisher/<publisher>",methods = ["GET"])
@requires_auth
def getAllByPublisher(publisher):
    data=json.loads(getData(f"select * from mysql.Games where Publisher = '{publisher}'"))
    return jsonify(data)

@app.route("/getFromUserScore",methods = ["GET"])
@requires_auth
def getFromUserScore():
    data=json.loads(getData(f"select * from mysql.Games order by User_Score desc"))
    return jsonify(data)

@app.route("/getFromCriticScore",methods = ["GET"])
@requires_auth
def getFromCriticScore():
    data=json.loads(getData(f"select * from mysql.Games order by Critic_Score desc"))
    return jsonify(data)

@app.route("/getFromGlobalSales",methods = ["GET"])
@requires_auth
def getFromGlobalSales():
    data=json.loads(getData(f"select * from mysql.Games order by Critic_Score desc"))
    return jsonify(data)

@app.route("/getFromDeveloper/<developer>",methods = ["GET"])
@requires_auth
def getFromDeveloper(developer):
    data=json.loads(getData(f"select * from mysql.Games where Developer = '{developer}'"))
    return jsonify(data)

@app.route("/getBestFromDeveloper/<developer>",methods = ["GET"])
@requires_auth
def getBestFromDeveloper(developer):
    data=json.loads(getData(f"select * from mysql.Games where Developer = '{developer}' order by User_Score desc"))
    return jsonify(data)

@app.route("/postNewGame",methods = ["POST"])
@requires_auth
def postNewGame():
    file = request.get_json()
    return postData(file)

@app.route("/updateGame/<int:id>", methods=["PUT"])
@requires_auth
def updateGame(id):
    data = request.get_json()
    return updateData(data,id)

@app.route("/deleteGame/<int:id>", methods=["DELETE"])
@requires_auth
def deleteGame(id):
    return deleteData(id)

if __name__ == "__main__":
    app.run(host='IP',port=5001, debug=True)
    