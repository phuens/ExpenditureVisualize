from flask import Flask, render_template      
import pandas as pd 
import os 
import plotly.express as px
import plotly
import datetime
import json

app = Flask(__name__)

@app.route("/")
def home():
    data = readData()
    category_plot = categoricalDaysExpenditure(data)
    daily_expen = dailyExpenditure(data)
    categorical_expenditure_sum = categoricalExpenditure(data)
    return render_template(
        'home.html',
        plot=category_plot, 
        daily_expenditure = daily_expen, 
        categorical_expenditure_sum = categorical_expenditure_sum)
    

def readData():
    final_csv = []
    entries = os.listdir("./static/data/csv/")
    for i in entries:
        csv_path = os.path.join("./static/data/csv/", i ) #define the path for the csv files
        name, extension = os.path.splitext(csv_path) #check if csv file
        if (extension == ".csv"):
            solo_csv = pd.read_csv(csv_path,index_col=False, header=None, engine='python') # return a panda data frame, engine=python required for unicode issue
            solo_csv[6] = solo_csv[6].str.replace('DR','').str.replace(",", '') #remove the string DR from DEBIT
            solo_csv[7] = solo_csv[7].str.replace('CR','').str.replace(",", '') #remove the string CR from CREDIT
            solo_csv[8] = solo_csv[8].str.replace('CR','').str.replace(",", '') #remove the string CR from BALANCE
            final_csv.append(solo_csv) #append the csv files one after another.
        else:
            print("file {} not a csv ".format(csv_path))
        return createDataFrame(final_csv)
	
def createDataFrame(final_csv): 
	data = pd.concat(final_csv, axis=0, sort=False) 
	data.columns = ["date", "journal", "action", "to", "category", "item", "debit", "credit", "balance"] #set the column headers
	data["debit"] = data.debit.astype('float64')
	data["credit"] = data.credit.astype('float64')
	data["balance"] = data.balance.astype('float64')
	data["date"] = pd.to_datetime(data['date'])
	data['day'] = data['date'].dt.day_name()
	data["date"] = pd.to_datetime(data['date']).dt.date
	data = data.sort_values(by=['date'])
	data.to_csv("./static/data/final/final_data.csv") #write the appended data to a csv file.
	print("----------------------\n" , data.dtypes, "\n----------------------")

	return data

def dailyExpenditure(data):
    start_date , end_date = get_dates()
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    fig = px.scatter(df, x="date", y="debit", labels={'debit':'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def categoricalExpenditure(data):
    start_date , end_date = get_dates()
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    fig = px.bar(df, x="category", y="debit", labels={'debit':'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def categoricalDaysExpenditure(data):
    start_date , end_date = get_dates()
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    df = data.loc[(data['category'] != "FAMILY") & (data['category'] != "SALARY")& (data['category'] != "CREDIT")]
    fig = px.bar(df, x="category", y="debit", barmode="group",facet_col="day",text="debit")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def get_dates(): 
	start_date ='2020-01-01'
	end_date = '2020-12-30'
	start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
	end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
	return start_date , end_date


if __name__ == "__main__":
    app.debug = True
    app.run()