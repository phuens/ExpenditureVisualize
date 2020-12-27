import pandas as pd 
import os 
import plotly.express as px


def main(): 
	final_csv = [] 
	entries = os.listdir("Data/csv/")
	for i in entries: 
		csv_path = os.path.join("Data/csv/", i ) #define the path for the csv files
		name, extension = os.path.splitext(csv_path) #check if csv file

		if (extension == ".csv"): 
			solo_csv = pd.read_csv(csv_path,index_col=False, header=None, engine='python') # return a panda data frame, engine=python required for unicode issue
			solo_csv[6] = solo_csv[6].str.replace('DR','').str.replace(",", '') #remove the string DR from DEBIT
			solo_csv[7] = solo_csv[7].str.replace('CR','').str.replace(",", '') #remove the string CR from CREDIT
			solo_csv[8] = solo_csv[8].str.replace('CR','').str.replace(",", '') #remove the string CR from BALANCE
			final_csv.append(solo_csv) #append the csv files one after another. 
		
		else: 
			print("file {} not a csv ".format(csv_path))

	data = pd.concat(final_csv, axis=0, sort=False) 
	data.columns = ["date", "journal", "action", "to", "category", "item", "debit", "credit", "balance"] #set the column headers
	data.to_csv("Data/final/final_data.csv") #write the appended data to a csv file.

	data["debit"] = data.debit.astype('float64')
	data["credit"] = data.credit.astype('float64')
	data["balance"] = data.balance.astype('float64')

	print("-------------------------------------------------------")
	print("Expenditure: \n{}".format(data["debit"].describe()))
	print("-------------------------------------------------------")
	print("Income: \n{}".format(data["credit"].describe()))
	print("-------------------------------------------------------")

	visualization(data)

def visualization(data): 
	# print(data)
	df = data
	fig = px.scatter(df, x=data.date, y=data.debit)
	fig.show()

if __name__ == '__main__':
	main()
	



# 22/05/2020	202574	CASH DEPOSIT		UNKNOWN	SELF	0	10,000.00CR	10,000.00CR