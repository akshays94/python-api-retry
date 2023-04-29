import logging
import uvicorn

from fastapi import FastAPI, HTTPException

app = FastAPI()

users_db: list = [
    {'id': 1, 'name': 'Aaron Apple', 'phone': '99992222'},
    {'id': 2, 'name': 'Bobby Brown', 'phone': '99993333'},
]


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{asctime} {levelprefix} {message}",
        style="{",
        use_colors=True,
        datefmt='%d/%m/%Y %H:%M:%S'
    )
    logger.handlers[0].setFormatter(console_formatter)


@app.get("/")
def base_api():
    return {"Welcome": "to Users Service"}


@app.get('/users/{user_id}')
def get_user(user_id: int):
    raise HTTPException(status_code=502, detail="Service down")
    # import time
    # time.sleep(5)
    for user in users_db:
        if user_id == user['id']:
            return user
    raise HTTPException(status_code=404, detail="User not found")
