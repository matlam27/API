from fastapi import FastAPI

import database
from routes import router as routes_router

app = FastAPI()

database.database_connection()

app.include_router(routes_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
