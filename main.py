from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
   return {"message": "Trading scanner actif"}

@app.get("/scan")
def scan():
   symbols = ["TSLA", "NVDA", "AAPL", "MSFT", "BTC-USD"]

   results = {}

   for symbol in symbols:
       ticker = yf.Ticker(symbol)
       data = ticker.history(period="1d")

       if not data.empty:
           price = float(data["Close"].iloc[-1])
           open_price = float(data["Open"].iloc[-1])
           change = round(((price - open_price) / open_price) * 100, 2)

           results[symbol] = {
               "price": price,
               "change_percent": change
           }

   return results
