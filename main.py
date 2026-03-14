from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
   return {"message": "Trading scanner actif"}

@app.get("/scan")
def scan():

   symbols = [
       "TSLA","NVDA","AMD","PLTR","SOFI","COIN","AAPL","META","AMZN",
       "MARA","RIOT","LCID","NIO","RIVN"
   ]

   movers = []

   for symbol in symbols:

       try:
           ticker = yf.Ticker(symbol)
           data = ticker.history(period="1d")

           if data.empty:
               continue

           open_price = float(data["Open"].iloc[-1])
           price = float(data["Close"].iloc[-1])

           change = ((price-open_price)/open_price)*100

           if change > 1:   # filtrer les actions qui montent
               movers.append({
                   "symbol":symbol,
                   "price":round(price,2),
                   "change_percent":round(change,2)
               })

       except:
           pass

   movers = sorted(movers,key=lambda x:x["change_percent"],reverse=True)

   return {"top_momentum":movers}
