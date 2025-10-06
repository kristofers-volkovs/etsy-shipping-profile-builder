import httpx
from dotenv import load_dotenv
import os


def get_env(key: str) -> str:
    env_variable = os.getenv(key)
    if env_variable is None:
        raise Exception(f"Variable '{key}' not set in .env file")

    return env_variable


load_dotenv()
PUBLIC_KEY = get_env("PUBLIC_KEY")
PRIVATE_KEY = get_env("PRIVATE_KEY")

auth = httpx.BasicAuth(username=PUBLIC_KEY, password=PRIVATE_KEY)
client = httpx.Client(auth=auth)

base_url = "https://api.swotzy.com/public"
rates_path = "/rates"


def main():
    data = {
        "sender_address": {
            "address1": get_env("SENDER_ADDRESS"),
            "address2": "",
            "zip": get_env("SENDER_ZIP"),
            "city": get_env("SENDER_CITY"),
            "country": get_env("SENDER_COUNTRY"),
            "state": get_env("SENDER_STATE"),
            "name": get_env("SENDER_NAME"),
        },
        "shipments": [
            {
                "package": {"length": 16, "width": 16, "height": 7, "weight": 0.2},
                "customs_items": [
                    {
                        "title": "Example product",
                        "quantity": "1",
                        "value": "19.99",
                        "country_of_origin": get_env("SENDER_COUNTRY"),
                        "weight": "0.2",
                        "hs_code": "392690",
                    }
                ],
            }
        ],
        "recipient_address": {
            "address1": get_env("RECEIVER_ADDRESS"),
            "address2": "",
            "zip": get_env("RECEIVER_ZIP"),
            "city": get_env("RECEIVER_CITY"),
            "country": get_env("RECEIVER_COUNTRY"),
            "state": get_env("RECEIVER_STATE"),
            "name": get_env("RECEIVER_NAME"),
        },
    }

    url = base_url + rates_path
    headers = {"Accept": "application/json"}

    res = client.post(url, json=data, headers=headers)

    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        print(res.json())
    else:
        print(res.content)


if __name__ == "__main__":
    main()
