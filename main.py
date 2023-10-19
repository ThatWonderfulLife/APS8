import pyodbc as db
import json
from flask import Flask,redirect,url_for,render_template,request, jsonify
import pyodbc as db


data=[]
result =[]
server = 'DESKTOP-0LIUFQV'
database = 'python_dataset'

app = Flask(__name__)

def sortData(rows):
    for tuple in rows:
        dict = {'name':tuple[0],
            'platform':tuple[1],
            'yearOfRelease':tuple[2],
            'genre':tuple[3],
            'publisher':tuple[4],
            'NA_Sales':tuple[5],
            'EU_Sales':tuple[6],
            'JP_Sales':tuple[7]
            }
        data.append(dict)
    return dict    

def getData(sqlCommand):
    conn = db.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';')
    call = conn.cursor()
    call.execute(f"{sqlCommand}")
    rows = call.fetchall()
    dict = sortData(rows)
    data.append(dict)
    call.close()
    conn.close()

    return data

def postData(file):
    try:
        conn = db.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';')
        call = conn.cursor()
        data = file
        sqlCommand = "insert into dbo.dataset_import (Name,Platform,YearOfRelease,Genre,Publisher,NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global_Sales,Critic_Score,Critic_Count,User_Score,Developer,Rating) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        call.execute(f"{sqlCommand}",data["Name"],data["Platform"],data["YearOfRelease"],data["Genre"],data["Publisher"],data["NA_Sales"],data["EU_Sales"],data["JP_Sales"],data["Other_Sales"],data["Global_Sales"],data["Critic_Score"],data["Critic_Count"],data["User_Score"],data["Developer"],data["Rating"])
        call.close()
        conn.close()
        return jsonify({"message": "Data added successfully"})
    except Exception as e:
        return jsonify({"Erro": str(e)})
    
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/getAllGames")
def getAllGames():
    return getData("select * from dbo.dataset_import")

@app.route("/getAllGamesByConsole/<console>", methods = ["GET"])
def getAllGamesByConsole(console):
    return getData(f"select * from dbo.dataset_import where Platform = '{console}'")

@app.route("/getAllByYear/<year>",methods = ["GET"])
def getAllByYear(year):
    return getData(f"select * from dbo.dataset_import where YearOfRelease = {year}")

@app.route("/getAllByGenre/<genre>",methods = ["GET"])
def getAllByGenre(genre):
    return getData(f"select * from dbo.dataset_import where Genre = {genre}")

@app.route("/getAllByPublisher/<publisher>",methods = ["GET"])
def getAllByPublisher(publisher):
    return getData(f"select * from dbo.dataset_import where publisher = {publisher}")

@app.route("/getFromUserScore",methods = ["GET"])
def getFromUserScore():
    return getData(f"select * from dbo.dataset_import order by User_Score desc")

@app.route("/getFromCriticScore",methods = ["GET"])
def getFromCriticScore():
    return getData(f"select * from dbo.dataset_import order by Critic_Score desc")

@app.route("/getFromGlobalSales",methods = ["GET"])
def getFromGlobalSales():
    return getData(f"select * from dbo.dataset_import order by Critic_Score desc")

@app.route("/getFromDeveloper/<developer>",methods = ["GET"])
def getFromDeveloper(developer):
    return getData(f"select * from dbo.dataset_import where Developer = '{developer}'")

@app.route("/getBestFromDeveloper/<developer>",methods = ["GET"])
def getBestFromDeveloper(developer):
    return getData(f"select * from dbo.dataset_import where Developer = '{developer}' order by User_Score desc")

@app.route("/postNewGame",methods = ["POST"])
def postNewGame():
    file = request.get_json()
    return postData(file)


if __name__ == "__main__":
    app.run()


