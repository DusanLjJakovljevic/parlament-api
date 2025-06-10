from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_laws():
    url = "http://www.parlament.gov.rs/akti/doneti-zakoni/doneti-zakoni.1033.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    html = response.text

    print("======= HTML content START =======")
    print(html[:1000])
    print("======= HTML content END =======")

    soup = BeautifulSoup(html, 'html.parser')
    laws = []

    for link in soup.select("div#content a[href*='.doc'], a[href*='.pdf']"):
        laws.append({
            "title": link.text.strip(),
            "url": link['href']
        })

    return laws

@app.route('/laws', methods=['GET'])
def get_laws():
    return jsonify(scrape_laws())

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
