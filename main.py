import mysql.connector
import json
from flask import Flask,render_template,request,jsonify
from functools import wraps

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
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
    
def postData(data):
    try:
        cursor = mydb.cursor()
        sqlCommand = f'''insert into mysql.Games (Name,Platform,Year,Genre,Publisher,NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global,Critical_Score,Critical_Count,User_Score,User_Count,Developer,Rating) VALUES ('{data["Name"]}','{data["Platform"]}',{data["YearOfRelease"]},'{data["Genre"]}','{data["Publisher"]}',{data["NA_Sales"]},{data["EU_Sales"]},{data["JP_Sales"]},{data["Other_Sales"]},{data["Global_Sales"]},{data["Critic_Score"]},{data["Critic_Count"]},{data["User_Score"]},{data["User_Count"]},'{data["Developer"]}',{data["Rating"]});'''
        cursor.execute(sqlCommand)
        mydb.commit()

    except Exception as e:
        return jsonify({"Erro": str(e)})
    finally:
        cursor.close()
    return jsonify({"message": "Data added successfully"})

app = Flask(__name__)
SECRET_TOKEN = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getAllGames")
@requires_auth
def getAllGames():
    data=json.loads(getData("select * from mysql.Games"))
    return jsonify(data)

@app.route("/getAllGamesByConsole/<console>", methods = ["GET"])
def getAllGamesByConsole(console):
    data=json.loads(getData(f"select * from mysql.Games where Platform = '{console}'"))
    return jsonify(data)

@app.route("/getAllByYear/<year>",methods = ["GET"])
def getAllByYear(year):
    data=json.loads(getData(f"select * from mysql.Games where Year = '{year}'"))
    return jsonify(data)

@app.route("/getAllByGenre/<genre>",methods = ["GET"])
def getAllByGenre(genre):
    data=json.loads(getData(f"select * from mysql.Games where Genre = '{genre}'"))
    return jsonify(data)

@app.route("/getAllByPublisher/<publisher>",methods = ["GET"])
def getAllByPublisher(publisher):
    data=json.loads(getData(f"select * from mysql.Games where Publisher = '{publisher}'"))
    return jsonify(data)

@app.route("/getFromUserScore",methods = ["GET"])
def getFromUserScore():
    data=json.loads(getData(f"select * from mysql.Games order by User_Score desc"))
    return jsonify(data)

@app.route("/getFromCriticScore",methods = ["GET"])
def getFromCriticScore():
    data=json.loads(getData(f"select * from mysql.Games order by Critic_Score desc"))
    return jsonify(data)

@app.route("/getFromGlobalSales",methods = ["GET"])
def getFromGlobalSales():
    data=json.loads(getData(f"select * from mysql.Games order by Critic_Score desc"))
    return jsonify(data)

@app.route("/getFromDeveloper/<developer>",methods = ["GET"])
def getFromDeveloper(developer):
    data=json.loads(getData(f"select * from mysql.Games where Developer = '{developer}'"))
    return jsonify(data)

@app.route("/getBestFromDeveloper/<developer>",methods = ["GET"])
def getBestFromDeveloper(developer):
    data=json.loads(getData(f"select * from mysql.Games where Developer = '{developer}' order by User_Score desc"))
    return jsonify(data)

@app.route("/postNewGame",methods = ["POST"])
@requires_auth
def postNewGame():
    file = request.get_json()
    return postData(file)

if __name__ == "__main__":
    app.run(host='',port=9999, debug=True)