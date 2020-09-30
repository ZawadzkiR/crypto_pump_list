import pandas as pd
from tabulate import tabulate
import smtplib 
import time, requests, json
import datetime as dt

COINMARKETCAP_PRO_API_KEY = 'Your_COINMARKETCAP_API_KEY'
mail_adress = 'Your_email_adress'
mail_passw = 'Your_email_password'
SMTP = 'smtp.gmail.com' #for gmail
SMTP_port = 587 #for gmail

def crypto_pump_list(week_change=10, daily_change=10, capitalization=1000000, pairs=5):

  #Connect to API
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=5000'
  headers = {
  'Accept': 'application/json',
  'Accept-Encoding': 'deflate, gzip',
  'X-CMC_PRO_API_KEY': COINMARKETCAP_PRO_API_KEY,
  }
  r = requests.get(url, headers=headers)
  if r.status_code == 200:
    response = json.loads(r.text)
    
  numb_of_coins = response['status']['total_count'] #Number of scaped coins
  table=[]
    #Scrap data about coins
  i = 0
  while i < numb_of_coins:
    name = response['data'][i]['name']
    market_cap = response['data'][i]['quote']['USD']['market_cap']
    price = response['data'][i]['quote']['USD']['price']
    percent_change_1h = response['data'][i]['quote']['USD']['percent_change_1h']
    percent_change_24h = response['data'][i]['quote']['USD']['percent_change_24h']
    percent_change_7d = response['data'][i]['quote']['USD']['percent_change_7d']
    volume_24h = response['data'][i]['quote']['USD']['volume_24h']
    num_market_pairs = response['data'][i]['num_market_pairs']

    table.append([name, price, percent_change_1h, percent_change_24h, percent_change_7d, market_cap, volume_24h, num_market_pairs ])
    i+=1
    
    #create table from list
  df = pd.DataFrame(table, columns=['Name', 'Price', '1H', '24H', '7D', 'MarketCap', 'Volume24H', 'Pairs']).dropna()
  df['1H'] = df['1H'].round(2)
  df['24H'] = df['24H'].round(2)
  df['7D'] = df['7D'].round(2)
  df = df.loc[(df['24H'] >= daily_change) & (df['7D'] >= week_change) & (df['MarketCap'] >= capitalization) & (df['Pairs'] >= pairs) ]
    #wiadomość na maila
  msg = tabulate(df, headers='keys', tablefmt='psql')

    #e-mail sending

  if len(df) >=1:

    s = smtplib.SMTP(SMTP, SMTP_port) 
    s.starttls() 
    s.login(mail_adress, mail_passw) 
    message = msg
    s.sendmail(mail_adress, mail_adress, message) 
    s.quit() 
  print('Last sending: ',dt.datetime.now(), ' Generated: ',len(df),' cryptocurriences')

crypto_pump_list()
