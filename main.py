import requests
from datetime import date, timedelta
import smtplib

STOCK_API_KEY = "V7C0P84K525LPMKP"
NEWS_API_KEY = "9c3e35f65b67480dbb787bbb21eeeb2d"
EMAIL = "thinh.mc08514@sinhvien.hoasen.edu.vn"
PASSWORD = "**************"

url = f'https://www.alphavantage.co/query'
stock_params = {
     "function": "TIME_SERIES_DAILY",
     "symbol": "TSLA",
     "apikey": STOCK_API_KEY
}
r = requests.get(url, params= stock_params)
r.raise_for_status()
data = r.json()["Time Series (Daily)"]
data = [value for (key,value) in data.items()]

yesterday_data = data[0]
previous_day_data = data[1]

up_down = ""
diff = float(yesterday_data["4. close"]) - float(previous_day_data["4. close"])
if diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Because the changing percent is too small, it rarely be 5% or 10%, so i set to 0.14% to test
diff_percentage = round((abs(diff)/float(previous_day_data["4. close"])) * 100, 2)
if diff_percentage > 0.14:
    YESTERDAY = date.today() - timedelta(days=1)
    YESTERDAY = YESTERDAY.strftime("%y-%m-%d")
    news_params = {
        "q": "Tesla",
        "apiKey": NEWS_API_KEY,
        "from": YESTERDAY,
        "to": YESTERDAY
    }
    url = f"https://newsapi.org/v2/everything"
    r = requests.get(url, params= news_params)
    articles = r.json()["articles"][:3] # Only take 3 main articles
    #Sent email
    with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user= EMAIL, password = PASSWORD)
            content = ""
            content += f"TSLA {up_down} {diff_percentage} \n\n"
            for article in articles:
                  content += f"Title: {article['title']} \n Description: {article['description']} \n\n"
            message = f"Subject: TESLA news!!\n\n{content}".encode("utf-8")
            connection.sendmail(
                from_addr= EMAIL,
                to_addrs= "macthinh22@gmail.com",
                msg= message
            )



