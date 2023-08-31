import requests


def fetch_data(isbn):
    """
    Fetches the book cover via the ISBN
    """
    params = {
        "apikey": __IMDB_API_KEY__,
        "i": imdb_id
    }

    __URL__ = "https://www.omdbapi.com/"
    data = requests.get(__URL__, params=params)
    content = data.json()
    return content
