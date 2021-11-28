import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


api_key = "your stock key"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": api_key
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()

data = response.json()
daily_data = data["Time Series (Daily)"]
closing_stock_price = [value["4. close"] for(key, value) in daily_data.items()]
y_price = float(closing_stock_price[0])
dby_price = float(closing_stock_price[1])
d = None
#decreases
if y_price - dby_price < 0:
    d = "🔻"
    price_difference = abs(y_price - dby_price)
    difference = price_difference/dby_price*100
#increase
else:
    d = "🔺"
    difference = (y_price - dby_price)/y_price*100

## When stock price increase/decreases by 5% between yesterday and the day before yesterday then send 3 articles.

api_key_news ="your news key"
if difference > 5:
    news_parameters = {
        "apiKey": api_key_news,
        "qinTitle": COMPANY_NAME
    }
    response_news = requests.get(NEWS_ENDPOINT, params=news_parameters)
    response_news.raise_for_status()
   # print(response_news.status_code)
    data_news = response_news.json()

    articles = data_news["articles"][:3]
    articles_description = [f"TSLA: {d}{round(difference)}%\nHeadline:{item['title']}\nBrief:{item['description']}" for item in articles]
    print(articles_description)

    # send each article(item) as a separate massage via Twilio

    account_sid = "your account sid"
    auth_token = "your token"
    client = Client(account_sid, auth_token)
    for item in articles_description:
        message = client.messages \
            .create(
            body= item,
            from_='your Twilio number',
            to='your mobile number'
        )

    print(message.sid)








