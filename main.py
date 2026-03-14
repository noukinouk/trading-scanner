from fastapi import FastAPI
import yfinance as yf
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
   return {"message": "NASDAQ scanner actif"}

@app.get("/scan")
def scan():

   # récupérer les tickers NASDAQ
   table = pd.read_csv("https://old.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt", sep="|")

   symbols = table["Symbol"].tolist()

   results = []

   for symbol in symbols[:1000]:   # limite 1000 pour serveur gratuit

       try:
           ticker = yf.Ticker(symbol)
           data = ticker.history(period="1d")

           if data.empty:
               continue

           open_price = float(data["Open"].iloc[-1])
           price = float(data["Close"].iloc[-1])
           volume = int(data["Volume"].iloc[-1])

           # filtre prix
           if price < 2 or price > 5:
               continue

           change = ((price-open_price)/open_price)*100

           results.append({
               "symbol":symbol,
               "price":round(price,2),
               "change_percent":round(change,2),
               "volume":volume
           })

       except:
           pass

   results = sorted(results,key=lambda x:x["change_percent"],reverse=True)

   return {
       "count":len(results),
       "top_movers":results[:20]
   }
