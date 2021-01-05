import pandas as pd 
import os 
import plotly.express as px
import plotly.graph_objects as go
import datetime

def main(): 
	data = readData()
	dailySum(data)
	# dailyExpenditure(data)
	# categoricalExpenditure(data)
	# categoricalDaysExpenditure(data)

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
	df = data.groupby('date').debit.agg([sum,min,len],)
	df['average'] = df['sum']/df['len']
	df['date'] = df.index #make the index column which happens to be the grouped date into a column. 
	
	
	# fig = px.bar(df, x="date", y="sum",  mode='bar')

	trace1  = go.Scatter(
        mode='markers',
        x = df['date'],
        y = df['average'],
        name="Average"
    )

	trace2 = go.Bar(
        x = df['date'],
        y = df['sum'],
        name="Sum",
        yaxis='y2',
        marker_line_width=1.5,
        marker_line_color='rgb(8,48,107)',
        opacity=0.5
    )
	data = [trace1, trace2]

	layout = go.Layout(
		title_text='Sepnding',
		yaxis=dict(
			side = 'right'
    	),
		yaxis2=dict(
			overlaying='y',
			anchor='y',
		)
	)
	fig = go.Figure(data=data, layout=layout)
	fig.show()
	print("----------------------\n" , df.dtypes, "\n----------------------")
	
	# fig.show()

	
	
def dailyExpenditure(data):	
	start_date , end_date = get_dates()
	df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
	fig = px.scatter(df, x="date", y="debit", labels={'debit':'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])
	fig.show()

def categoricalExpenditure(data): 
	start_date , end_date = get_dates()
	df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
	fig = px.bar(df, x="category", y="debit", labels={'debit':'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])
	fig.show()

def categoricalDaysExpenditure(data):
	start_date , end_date = get_dates()
	df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
	df = data.loc[(data['category'] != "FAMILY") & (data['category'] != "SALARY")& (data['category'] != "CREDIT")]
	fig = px.bar(df, x="category", y="debit", barmode="group",facet_col="day",text="debit")
	# fig.update_layout(yaxis=dict(range=[0,1100]))
	fig.show()

def get_dates(): 
	start_date ='2020-05-05'
	end_date = '2020-07-05'
	start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
	end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
	return start_date , end_date

if __name__ == '__main__':
	main()
