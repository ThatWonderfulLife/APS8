import mysql.connector
import json
from flask import Flask,render_template,request,jsonify

mydb = mysql.connector.connect(
  host="",
  user="",
  password="&",
  database=""
)

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

        cursor.close()
        mydb.close()
        return jsonify({"message": "Data added successfully", "Query":[sqlCommand]})
    
    except Exception as e:
        return jsonify({"Erro": str(e), "Query":[sqlCommand]})

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getAllGames")
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
def postNewGame():
    return postData(request.get_json())

if __name__ == "__main__":
    app.run(host='',port=9999, debug=True)