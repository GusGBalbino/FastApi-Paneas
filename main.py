from fastapi import FastAPI
import uvicorn
from users.routers import users_router


app = FastAPI(title="APIs de Gerenciamento de Usuários", 
            description="Desafio Técnico de FastAPI - Paneas | Obrigado pela oportunidade!", 
            version="1.0.0")

@app.get("/")
def hello():
    return {"API Paneas"}


app.include_router(users_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port="8000")