from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
   return {"message": "Trading scanner en ligne"}

@app.get("/scan")
def scan():
   return {
       "status": "ok",
       "scanner": "actif",
       "message": "Le scanner fonctionne"
   }
