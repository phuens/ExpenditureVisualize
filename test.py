from flask import Flask, render_template, request    
import pandas as pd 
import os 
import plotly.express as px
import plotly.graph_objects as go
import plotly
import datetime
import json

def main(): 
	data = readData()
	# dailySum(data)
	dailyExpenditure(data)
	# categoricalExpenditure(data)
	# daysExpenditureBarGraph(data)
	# categoricalExpenditurePieChart(data)
	# daysExpenditurePieChart(data)

def readData():
	final_csv = [] 
	entries = os.listdir("./static/data/csv/")
	
	for i in entries: 
		print("this si the i:", i , "\n=============")
		csv_path = os.path.join("./static/data/csv/", i ) #define the path for the csv files
		name, extension = os.path.splitext(csv_path) #check if csv file

		if (extension == ".csv"): 
			print("csv path: ", csv_path)
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
	data.to_csv("./static/data/final/test_final.csv") #write the appended data to a csv file.
	# print("----------------------\n" , data.dtypes, "\n----------------------")

	return data

def dailySum(data): 
	start_date , end_date = get_dates()
	df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
	df = data.groupby('date').debit.agg([sum,min,len])
	df['average'] = df['sum']/df['len']
	df['date'] = df.index #make the index column which happens to be the grouped date into a column. 
	
	# This is done so that values where average = sum do not  dusplay the average
	for index, rows in df.iterrows(): 
		if	rows["average"]==rows["sum"]: 
			
			df.at[index, 'average'] = None

	trace1  = go.Scatter(
        mode='markers',
        x = df['date'],
        y = df['average'],
        name="Average",
    )
	trace2 = go.Bar(
        x = df['date'],
        y = df['sum'],
        name="Sum",
        # marker_line_width=1.5,
        # marker_line_color='rgb(8,48,107)',
        opacity=0.5
    )
	data = [trace1, trace2]

	layout = go.Layout(
		title_text='Sepnding',
		yaxis=dict(
			side = 'left'
    	),
		yaxis2=dict(
			overlaying='y',
			anchor='x',
		),
		annotations=[
            go.layout.Annotation(
                text='* Values without avergae is because the average and sum are the same',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                y=1.0291,
                x=1,
				width=400,
                bordercolor='gray',
                borderwidth=1,
				opacity=0.5
            )
        ]
	)
	fig = go.Figure(data=data, layout=layout)
	fig.update_layout(legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.025,
		xanchor="right",
		x=1
	))
	fig.show()


	
	
def dailyExpenditure(data):	
	start_date , end_date = get_dates()
	df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
	fig = px.scatter(df, x="date", y="debit", labels={'debit':'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])
	# graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	# print(graphJSON)

def categoricalExpenditure(data): 
	start_date , end_date = get_dates()
	df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
	fig = px.bar(df, x="category", y="debit", labels={'debit':'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])
	fig.show()

def daysExpenditureBarGraph(data):
	start_date , end_date = get_dates()
	df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
	# TODO:NEED TO REFACTOR THE BELOW CODE.
	df = df.loc[ (df["category"] != "UNKNOWN") &(df["category"] != "FAMILY") &(df["category"] != "RENT") &(df["category"] != "SALARY") &(df["category"] != "CREDIT") &(df["category"] != "COMPUTER MONITOR") &(df["category"] != "FURNITURE") &(df["category"] !="RETURN") &(df["category"] != "HALF YR.ANNUAL MAINT CHR")&(df["category"] != "INTEREST")]
	fig = px.bar(df, x="category", y="debit", barmode="group",facet_col="day",text="debit")
	fig.show()
	
def categoricalExpenditurePieChart(data):
	start_date , end_date = get_dates()
	df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
	print(df)
	# TODO:NEED TO REFACTOR THE BELOW CODE.
	df = df.loc[ (df["category"] != "UNKNOWN") &(df["category"] != "FAMILY") &(df["category"] != "RENT") &(df["category"] != "SALARY") &(df["category"] != "CREDIT") &(df["category"] != "COMPUTER MONITOR") &(df["category"] != "FURNITURE") &(df["category"] !="RETURN") &(df["category"] != "HALF YR.ANNUAL MAINT CHR")&(df["category"] != "INTEREST")]
	df = df.groupby('category').debit.agg([sum, len])
	df["category_group"] = df.index
	print(df)
	fig = px.pie(df, values='sum', names='category_group', labels="category_group", title='Total spending by categories', hole=.3)
	fig.show()


def daysExpenditurePieChart(data):
	day_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	start_date,end_date = get_dates()
	df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
	# TODO:NEED TO REFACTOR THE BELOW CODE.
	df = df.loc[ (df["category"] != "UNKNOWN") &(df["category"] != "FAMILY") &(df["category"] != "RENT") &(df["category"] != "SALARY") &(df["category"] != "CREDIT") &(df["category"] != "COMPUTER MONITOR") &(df["category"] != "FURNITURE") &(df["category"] !="RETURN") &(df["category"] != "HALF YR.ANNUAL MAINT CHR")&(df["category"] != "INTEREST")]
	df = df.groupby('day').debit.agg([sum, len]).reindex(day_of_the_week) 
	df["day_of_week"] = df.index
	fig = px.pie(df, values='sum', names='day_of_week', labels="day_of_week", title='Total spending by day of week.', hole=.3)
	fig.show()



def get_dates(): 
	start_date ='2020-01-01'
	end_date = '2020-12-31'
	start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
	end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
	return start_date , end_date

if __name__ == '__main__':
	main()
