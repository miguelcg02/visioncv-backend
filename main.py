import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from decouple import config
from dotenv import load_dotenv
from api.routes import router


load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=["Agent"], prefix="")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to VisionCV API"}

if __name__ == "__main__":
    port = config("PORT", default=8000, cast=int)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
