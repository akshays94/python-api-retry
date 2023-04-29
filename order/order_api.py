import requests

from fastapi import FastAPI, HTTPException
from requests.adapters import HTTPAdapter, Retry

app = FastAPI()

orders_db = [
    {'id': 1, 'user': 1, 'product': 'Apple IPhone'},
    {'id': 2, 'user': 2, 'product': 'Macbook'},
    {'id': 3, 'user': 1, 'product': 'Wireless Charger'},
    {'id': 4, 'user': 2, 'product': 'Book 1'},
    {'id': 5, 'user': 2, 'product': 'Book 2'},
    {'id': 6, 'user': 2, 'product': 'Book 3'},
    {'id': 6, 'user': 3, 'product': 'Book 3'},
]


class RetryManager:

    def __init__(self, num_retries: int = 3) -> None:
        self.num_retries = num_retries

    def get_session(self):
        session = requests.Session()

        BACKOFF_FACTOR = 1  # if 1 then 1s, 2s, 4s, 8s, 16s
        STATUS_CODES_TO_RETRY_ON = [404, 502, 503, 504]
        METHODS_TO_RETRY_ON = ['GET', 'POST', 'OPTIONS']

        retries = Retry(
            total=self.num_retries,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=STATUS_CODES_TO_RETRY_ON,
            method_whitelist=frozenset(METHODS_TO_RETRY_ON)
        )

        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session


class UserNotFound(HTTPException):
    status_code = 404

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail=detail)


@app.get("/")
def base_api():
    return {"Welcome": "to Orders Service"}


def call_api_without_retry(url: str, api_timeout_in_secs: int = 10):
    return requests.get(url=url, timeout=api_timeout_in_secs)


def call_api_with_retry(url: str, api_timeout_in_secs: int = 10):
    retry_session = RetryManager(
        num_retries=5
    ).get_session()
    return retry_session.get(url=url, timeout=api_timeout_in_secs)


def get_user_data(user_id: int) -> dict:
    try:
        # response = call_api_without_retry(
        #     url=f'http://user_api_1:8200/users/{user_id}?fromService=order',
        #     api_timeout_in_secs=3
        # )
        response = call_api_with_retry(
            url=f'http://user_api_1:8200/users/{user_id}?fromService=order',
            api_timeout_in_secs=10
        )
    except requests.exceptions.ReadTimeout:
        raise UserNotFound('User not found: User API timed out')
    except requests.exceptions.RetryError:
        raise UserNotFound('User not found: User service may be down')

    if response.status_code == 200:
        return response.json()

    if response.status_code == 404:
        return {'id': user_id}

    raise UserNotFound('User not found: User API failed')


@app.get("/orders/")
def get_orders(user_id: int):
    orders = list(filter(lambda item: item['user'] == user_id, orders_db))
    if not orders:
        raise HTTPException(
            status_code=404, detail="No orders found for this user ID")
    # raise UserNotFound('sdasdasd')
    return {
        'user': get_user_data(user_id=user_id),
        'orders': orders,
    }
