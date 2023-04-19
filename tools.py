import requests

SITE_URL = 'https://sat-guess.glitch.me'


def get_question(complexity='', country=''):
    url = SITE_URL + '/api/question'
    params = {'key': 'GFz%ZlClgA9MikNrCZ', 'complexity': complexity, 'country': country}
    response = requests.get(url, params=params).json()
    return response
