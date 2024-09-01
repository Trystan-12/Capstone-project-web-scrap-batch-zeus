from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,'html.parser')

#find your right key here
table = soup.find('table',attrs={'class':'history-rates-data'})
row = table.find_all('span', attrs={'class':'w'})

row_length = len(row)

temp = [] #initiating a list 

for i in range(0, row_length):
#insert the scrapping process here
	period = table.find_all('a', attrs={'class':'w'})[i].text
	kurs_dolar = table.find_all('span', attrs={'class':'w'})[i].text
	temp.append((period,kurs_dolar)) 

temp = temp[::-1]

#change into dataframe
not_clean_data = pd.DataFrame(temp,columns=('Period','USD to IDR'))

#insert data wrangling here
not_clean_data
not_clean_data['Period'] = not_clean_data['Period'].astype('datetime64[ns]')
not_clean_data['USD to IDR']=not_clean_data['USD to IDR'].str.replace('1 USD =','')
not_clean_data['USD to IDR'] = not_clean_data['USD to IDR'].str.replace(' IDR','')
not_clean_data['USD to IDR'] = not_clean_data['USD to IDR'].str.replace(',','')
not_clean_data['USD to IDR'] = not_clean_data['USD to IDR'].astype('int64')
not_clean_data
df= not_clean_data.set_index('Period')


#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{not_clean_data["USD to IDR"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)