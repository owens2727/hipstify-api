import os
from flask import Flask, request, jsonify
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def is_merch_url(url):
    url = "https://chadwickstokes.bandcamp.com/merch"
    response = requests.get(url)
    return "merch" in response.url


def get_artist_link(artist):
    search_url = f"https://bandcamp.com/search"
    search_response = requests.get(search_url, params={"q": artist})
    search_soup = BeautifulSoup(search_response.text, 'html.parser')
    search_results = search_soup.find_all("div", attrs={"class": "itemtype"})

    if not search_results:
        return

    artist_results = [
        result
        for result in search_results
        if "ARTIST" in result.text
    ]

    first_result = artist_results[0]

    merch_url = first_result.parent.find_all("a")[0]["href"].split("?")[0] + "/merch"
    merch_response = requests.get(merch_url)

    if "merch" in merch_response.url:
      return merch_url
    else:
      return None


@app.route('/merch-url')
def hipstify():
    artist = request.args.get('artist')
    response = jsonify({"url": get_artist_link(artist)})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

port = int(os.environ.get('PORT', 8000))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
