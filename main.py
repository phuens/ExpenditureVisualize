from flask import Flask, render_template, request    
import pandas as pd 
import os 
import plotly.express as px
import plotly.graph_objects as go
import plotly
import datetime
import json

# TODO: need to update the daily sum graph based on the dates from user. 
# export FLASK_APP=main.py | RUN THIS BEFORE FLASK RUN
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    """
    Return all the graphs plotted and handle request from front end. 
    :return: template with all the grpahs.  
    """
    if request.method == 'POST':
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        print("from date: {} and to date: {}".format(from_date, to_date))
        
    else: 
        from_date ='2020-01-01'
        to_date = '2020-12-30'

    data = readData()
    scatter_bar_daily_sum_and_average       = scatterbarDailySumAndAverage(data, from_date, to_date)
    pie_days_expenditure_pie_chart          = pieDaysExpenditurePieChart(data, from_date, to_date)
    bar_day_based_categorical_expenditure   = barDayBasedCategoricalExpenditure(data, from_date, to_date)
    bar_categorical_sum_expenditure         = barCategoricalSumExpenditure(data, from_date, to_date)
    pie_categorical_sum_expenditure         = pieCategoricalSumExpenditure(data, from_date, to_date)
    # scatter_daily_expenditure = scatterDailyExpenditure(data, from_date, to_date)
    return render_template(
            'home.html',
            _scatter_bar_daily_sum_and_average      = scatter_bar_daily_sum_and_average,
            _pie_days_expenditure_pie_chart         = pie_days_expenditure_pie_chart,
            _bar_day_based_categorical_expenditure  = bar_day_based_categorical_expenditure, 
            _bar_categorical_sum_expenditure        = bar_categorical_sum_expenditure,
            _pie_categorical_sum_expenditure        = pie_categorical_sum_expenditure)


def readData():
    """
    Read all the csv's, clean and create a single csv containing all the transactions.
    :return: csv 
    """
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
    """
    Create pandas dataframe. Convert data type for columns and add day of the week column. 
    :return: panadas dataframe 
    :parameter: csv containing all the transaction. 
    """
    data = pd.concat(final_csv, axis=0, sort=False)
    data.columns = ["date", "journal", "action", "to", "category", "item", "debit", "credit", "balance"] #set the column headers
    data["debit"] = data.debit.astype('float64')
    data["credit"] = data.credit.astype('float64')
    data["balance"] = data.balance.astype('float64')
    data["date"] = pd.to_datetime(data['date'])
    data['day'] = data['date'].dt.day_name()
    data["date"] = pd.to_datetime(data['date']).dt.date
    data = data.sort_values(by=['date'])
    data.to_csv("./static/data/final/final_data.csv")
    print("----------------------\n" , data.dtypes, "\n----------------------")
    return data


#1
def scatterbarDailySumAndAverage(data, from_date, to_date):
    """
    Total sum and average of spending on a day.
    :return: bargraph and scatter plot 
    :parameter: data, from_date, to_date
    """
    start_date ,end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    df = data.groupby('date').debit.agg([sum,min,len])
    df['average'] = df['sum']/df['len']
    df['date'] = df.index  #make index to column.
    
    #not display average when average = sum 
    for index, rows in df.iterrows():
        if	rows["average"]==rows["sum"]:
            df.at[index, 'average'] = None
    
    trace1  = go.Scatter(mode='markers', x = df['date'], y = df['average'], name="Average",)
    trace2 = go.Bar(x = df['date'], y = df['sum'], name="Sum", opacity=0.5)
    data = [trace1, trace2]
    
    layout = go.Layout(
        title_text='Sepnding',yaxis=dict(side='left'),
		yaxis2=dict(overlaying='y',anchor='x',),
		annotations=[go.layout.Annotation(text='* No average means average = sum',align='left',showarrow=False,xref='paper',yref='paper',y=1.0291,x=1,width=400,bordercolor='gray',borderwidth=1,opacity=0.5)]
	)
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.025,xanchor="right",x=1))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


#2 
def pieDaysExpenditurePieChart(data, from_date, to_date):
    """
    Total sum of spending based on days of the week.
    :return: piechart 
    :parameter: data, from_date, to_date
    """
    day_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    start_date,end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    # TODO:NEED TO REFACTOR THE BELOW CODE.
    df = df.loc[ (df["category"] != "UNKNOWN") &(df["category"] != "FAMILY") &(df["category"] != "RENT") &(df["category"] != "SALARY") &(df["category"] != "CREDIT") &(df["category"] != "COMPUTER MONITOR") &(df["category"] != "FURNITURE") &(df["category"] !="RETURN") &(df["category"] != "HALF YR.ANNUAL MAINT CHR")&(df["category"] != "INTEREST")]
    df = df.groupby('day').debit.agg([sum, len]).reindex(day_of_the_week) 
    df["day_of_week"] = df.index
    fig = px.pie(df, values='sum', names='day_of_week', labels="day_of_week", title='Total spending by day of week.', hole=.3)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# 3
def barDayBasedCategoricalExpenditure(data, from_date, to_date):
    """
    Spending based on Days of the week by categories.
    :return: bargraph 
    :parameter: data, from_date, to_date
    """
    start_date , end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    df = df.loc[ (df["category"] != "UNKNOWN") &(df["category"] != "FAMILY") &(df["category"] != "RENT") &(df["category"] != "SALARY") &(df["category"] != "CREDIT") &(df["category"] != "COMPUTER MONITOR") &(df["category"] != "FURNITURE") &(df["category"] !="RETURN") &(df["category"] != "HALF YR.ANNUAL MAINT CHR")&(df["category"] != "INTEREST")]
    fig = px.bar(df, x="category", y="debit", barmode="group",facet_col="day",text="debit", title="Spending based on Days of the week by categories")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


#4
def barCategoricalSumExpenditure(data, from_date, to_date):
    """
    Total sum of spending based on Categories.
    :return: bargraph 
    :parameter: data, from_date, to_date
    """
    start_date , end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    fig = px.bar(df, x="category", y="debit", labels={'debit':'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


#5
def pieCategoricalSumExpenditure(data, from_date, to_date):
    """
    Total sum of spending based on categories.
    :return: piechart 
    :parameter: data, from_date, to_date
    """
    start_date , end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    # TODO:NEED TO REFACTOR THE BELOW CODE.
    df = df.loc[ (df["category"] != "UNKNOWN") &(df["category"] != "FAMILY") &(df["category"] != "RENT") &(df["category"] != "SALARY") &(df["category"] != "CREDIT") &(df["category"] != "COMPUTER MONITOR") &(df["category"] != "FURNITURE") &(df["category"] !="RETURN") &(df["category"] != "HALF YR.ANNUAL MAINT CHR")&(df["category"] != "INTEREST")]
    df = df.groupby('category').debit.agg([sum, len])
    df["category_group"] = df.index
    fig = px.pie(df, values='sum', names='category_group', title='Total sum of spending based on Days of the week')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# 6
def scatterDailyExpenditure(data, from_date, to_date):
    """
    Every single spending.
    :return: scatter plot 
    :parameter: data, from_date, to_date
    """
    start_date , end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    fig = px.scatter(df, x="date", y="debit", labels={'debit':'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def get_dates(from_date, to_date):
    """
    Convert string to date type.
    :return: date 
    :parameter: from_date, to_date
    """
    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
    return from_date , to_date


if __name__ == "__main__":
    app.debug = True
    app.run()