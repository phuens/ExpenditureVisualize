"""
Different graphs of various expenditure.

:return: graphs of various expen.
"""
from flask import Flask, request
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import plotly
import datetime
import json

# TODO:
#   1. Need to update the daily sum graph based on the dates from user.
#   2. Need to make the graphs responsive.
# export FLASK_APP=main.py | RUN THIS BEFORE FLASK RUN
app = Flask(__name__)


@app.route("/data", methods=['GET', 'POST'])
def home():
    """
    Return all the graphs plotted and handle request from front end.

    :return: template with all the grpahs.
    """
    arg_dates = request.get_json()
    arg_dates = json.loads(arg_dates["body"])
    from_date = arg_dates["fromDate"]
    to_date = arg_dates["toDate"]
    print("from date: {} and to date: {}".format(from_date, to_date))
    # ----------------------------------------------------------------
    data = readData()
    scatter_bar_daily_sum_and_average = scatterbarDailySumAndAverage(
        data, from_date, to_date)
    pie_days_expenditure_pie_chart = pieDaysExpenditurePieChart(
        data, from_date, to_date)
    bar_day_based_categorical_expenditure = barDayBasedCategoricalExpenditure(
        data, from_date, to_date)
    bar_categorical_sum_expenditure = barCategoricalSumExpenditure(
        data, from_date, to_date)
    pie_categorical_sum_expenditure = pieCategoricalSumExpenditure(
        data, from_date, to_date)
    graphs = (scatter_bar_daily_sum_and_average, pie_days_expenditure_pie_chart, bar_day_based_categorical_expenditure, bar_categorical_sum_expenditure, pie_categorical_sum_expenditure)  # noqa
    graphs = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return graphs


@app.route("/summary")
def statSummary():
    """
    Summary of different stats.

    :return: different statistics
    :parameter: data
    """
    data = readData()
    data["date"] = pd.to_datetime(data['date'])  # convert to datetime
    # Stat 1: Total Expenditure
    total_expenditure = data.debit.sum()
    # Stat 2: Total Earning
    total_earning = data.credit.sum()
    # Stat 3: Single Biggest expense
    biggest_expenditure = data.loc[data["debit"] == data.debit.max()]
    biggest_expenditure_amount = biggest_expenditure.debit
    biggest_expenditure_category = biggest_expenditure.category
    biggest_expenditure_item = biggest_expenditure.item
    # Stat 4: most expensive month
    max_month = data.groupby(pd.Grouper(key='date', freq='1M')).sum()
    max_month['month'] = max_month.index
    max_month = max_month.loc[max_month['debit'] == max_month.debit.max()]
    max_month_name = max_month["month"].dt.strftime('%B')
    max_month_amount = max_month.debit
    summary_data = [total_expenditure,
                    total_earning, biggest_expenditure_amount,
                    biggest_expenditure_category, biggest_expenditure_item,
                    max_month_name, max_month_amount]
    summary_data = json.dumps(summary_data, cls=plotly.utils.PlotlyJSONEncoder)
    return (summary_data)


def readData():
    """
    Read clean and create a single csv containing all the transactions.

    :return: csv
    """
    final_csv = []
    entries = os.listdir("../data/csv")
    for i in entries:
        csv_path = os.path.join("../data/csv", i)  # ppath for the csv files
        name, extension = os.path.splitext(csv_path)  # check if csv file
        if (extension == ".csv"):
            # panda data frame, engine=python required for unicode issue
            solo_csv = pd.read_csv(
                csv_path, index_col=False, header=None, engine='python')
            solo_csv[6] = solo_csv[6].str.replace('DR', '') \
                .str.replace(",", '')  # remove the string DR from DEBIT
            solo_csv[7] = solo_csv[7].str.replace('CR', '')\
                .str.replace(",", '')  # remove the string CR from CREDIT
            solo_csv[8] = solo_csv[8].str.replace('CR', '')\
                .str.replace(",", '')   # remove the string CR from BALANCE
            final_csv.append(solo_csv)  # append the csv files.
        else:
            print("file {} not a csv ".format(csv_path))
    return createDataFrame(final_csv)


def createDataFrame(final_csv):
    """
    Create dataframe, convert data type and add day of the week column.

    :return: panadas dataframe
    :parameter: csv containing all the transaction.
    """
    data = pd.concat(final_csv, axis=0, sort=False)
    data.columns = ["date", "journal", "action", "to", "category",
                    "item", "debit", "credit", "balance"]  # set column headers

    data["debit"] = data.debit.astype('float64')
    data["credit"] = data.credit.astype('float64')
    data["balance"] = data.balance.astype('float64')
    data["date"] = pd.to_datetime(data['date'])
    data['day'] = data['date'].dt.day_name()
    data["date"] = pd.to_datetime(data['date']).dt.date
    data = data.sort_values(by=['date'])
    data.to_csv("../data/final/final_data.csv")
    return data


# graph1
def scatterbarDailySumAndAverage(data, from_date, to_date):
    """
    Total sum and average of spending on a day.

    :return: bargraph and scatter plot
    :parameter: data, from_date, to_datea
    """
    start_date, end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    df = df.groupby('date').debit.agg([sum, min, len])
    df['average'] = df['sum']/df['len']
    df['date'] = df.index  # make index to column.
    # not display average when average = sum
    for index, rows in df.iterrows():
        if rows["average"] == rows["sum"]:
            df.at[index, 'average'] = None
    trace1 = go.Scatter(
        mode='markers', x=df['date'], y=df['average'], name="Average")
    trace2 = go.Bar(x=df['date'], y=df['sum'], name="Sum", opacity=0.5)
    data = [trace1, trace2]
    layout = go.Layout(
        margin=go.layout.Margin(
            l=20,  # left margin
            r=20,  # right margin
            b=20,  # bottom margin
            t=50  # top margin
        ),
        title_text='Sum and Average Daily Spending.', yaxis=dict(side='left'),
        yaxis2=dict(overlaying='y', anchor='x',),
        annotations=[go.layout.Annotation(text='* No average = sum', align='left', showarrow=False, xref='paper', yref='paper', y=1.0291, x=1, width=150, bordercolor='gray', borderwidth=1, opacity=0.5)])  # noqa
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(legend=dict(
        orientation="h", yanchor="bottom", y=1.025, xanchor="right", x=1))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# graph2
def pieDaysExpenditurePieChart(data, from_date, to_date):
    """
    Total sum of spending based on days of the week.

    :return: piechart
    :parameter: data, from_date, to_date
    """
    day_of_the_week = ['Monday', 'Tuesday', 'Wednesday',
                       'Thursday', 'Friday', 'Saturday', 'Sunday']
    start_date, end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    # TODO:NEED TO REFACTOR THE BELOW CODE.
    df = df.loc[(df["category"] != "UNKNOWN") & (df["category"] != "FAMILY") & (df["category"] != "RENT") & (df["category"] != "SALARY") & (df["category"] != "CREDIT") & (df["category"] != "COMPUTER MONITOR") & (df["category"] != "FURNITURE") & (df["category"] != "RETURN") & (df["category"] != "HALF YR.ANNUAL MAINT CHR") & (df["category"] != "INTEREST")]  # noqa
    df = df.groupby('day').debit.agg([sum, len]).reindex(day_of_the_week)
    df["day_of_week"] = df.index
    fig = px.pie(df, values='sum', names='day_of_week', labels="day_of_week",
                 title='Total Spending By Day Of The Week.', hole=.3)
    fig.update_layout(
        margin=go.layout.Margin(
            l=20,  # left margin
            r=20,  # right margin
            b=20,  # bottom margin
            t=50  # top margin
        )
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# graph3
def barDayBasedCategoricalExpenditure(data, from_date, to_date):
    """
    Spending based on Days of the week by categories.

    :return: bargraph
    :parameter: data, from_date, to_date
    """
    start_date, end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    df = df.loc[(df["category"] != "UNKNOWN") & (df["category"] != "FAMILY") & (df["category"] != "RENT") & (df["category"] != "SALARY") & (df["category"] != "CREDIT") & (df["category"] != "COMPUTER MONITOR") & (df["category"] != "FURNITURE") & (df["category"] != "RETURN") & (df["category"] != "HALF YR.ANNUAL MAINT CHR") & (df["category"] != "INTEREST")]  # noqa
    fig = px.bar(df, x="category", y="debit", barmode="group", facet_col="day",
                 text="debit", title="Spending Based On Days Of The Week And Categories")  # noqa
    fig.update_layout(
        margin=go.layout.Margin(
            l=20,  # left margin
            r=20,  # right margin
            b=20,  # bottom margin
            t=50  # top margin
        )
    )
    fig.update_xaxes(title_text='')
    # remove the name day = from the title of the graphs
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# graph4
def barCategoricalSumExpenditure(data, from_date, to_date):
    """
    Total sum of spending based on Categories.

    :return: bargraph
    :parameter: data, from_date, to_date
    """
    start_date, end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    fig = px.bar(df, x="category", y="debit", title="Spending Based On Categories", labels={'debit': 'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])  # noqa
    fig.update_layout(
        margin=go.layout.Margin(
            l=20,  # left margin
            r=20,  # right margin
            b=20,  # bottom margin
            t=50  # top margin
        )
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# graph5
def pieCategoricalSumExpenditure(data, from_date, to_date):
    """
    Total sum of spending based on categories.

    :return: piechart
    :parameter: data, from_date, to_date
    """
    start_date, end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    # TODO:NEED TO REFACTOR THE BELOW CODE.
    df = df.loc[(df["category"] != "UNKNOWN") & (df["category"] != "FAMILY") & (df["category"] != "RENT") & (df["category"] != "SALARY") & (df["category"] != "CREDIT") & (df["category"] != "COMPUTER MONITOR") & (df["category"] != "FURNITURE") & (df["category"] != "RETURN") & (df["category"] != "HALF YR.ANNUAL MAINT CHR") & (df["category"] != "INTEREST")]  # noqa
    df = df.groupby('category').debit.agg([sum, len])
    df["category_group"] = df.index
    fig = px.pie(df, values='sum', names='category_group',
                 title='Total Spending Based On Categories')
    # fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    fig.update_layout(
        margin=go.layout.Margin(
            l=20,  # left margin
            r=20,  # right margin
            b=20,  # bottom margin
            t=50  # top margin
        )
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


# graph6
def scatterDailyExpenditure(data, from_date, to_date):
    """
    Every single spending.

    :return: scatter plot
    :parameter: data, from_date, to_date
    """
    start_date, end_date = get_dates(from_date, to_date)
    df = data.loc[(data['date'] > start_date) & (data['date'] <= end_date)]
    fig = px.scatter(df, x="date", y="debit", labels={'debit': 'Expenditure'}, hover_data=['category', 'item', 'date', 'debit', 'balance'])  # noqa
    # fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
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
    return from_date, to_date


if __name__ == "__main__":
    app.debug = True
    app.run()
