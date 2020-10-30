import requests


def update_server_count(key, botID, count):

    data = {"server_count": count}
    url = f"https://top.gg/api/bots/{botID}/stats"
    headers = {
        "Authorization": key,
        "Content-Type": "application/json"
    }
    req = requests.post(url, json=data, headers=headers)

    if req.status_code != 200:
        raise requests.HTTPError(req.content)
