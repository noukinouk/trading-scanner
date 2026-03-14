from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
   return {"message": "Trading scanner actif"}

@app.get("/scan")
def scan():

   symbols = [
       "TSLA","NVDA","AAPL","MSFT","META",
       "AMZN","AMD","COIN","PLTR","SOFI"
   ]

   results = []

   for symbol in symbols:
       try:
           ticker = yf.Ticker(symbol)
           data = ticker.history(period="1d")

           if not data.empty:

               price = float(data["Close"].iloc[-1])
               open_price = float(data["Open"].iloc[-1])

               change = ((price-open_price)/open_price)*100

               results.append({
                   "symbol":symbol,
                   "price":round(price,2),
                   "change_percent":round(change,2)
               })

       except:
           pass

   # trier par performance
   results = sorted(results,key=lambda x:x["change_percent"],reverse=True)

   return {"top_movers":results}
