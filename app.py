from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_laws():
    url = "http://www.parlament.gov.rs/akti/doneti-zakoni/doneti-zakoni.1033.html"
    response = requests.get(url)
    html = response.text
    
    # Dodaj ovo da vidiš ceo HTML u logu (oprezno, biće dugačko)
    print("======= HTML content START =======")
    print(html[:1000])  # Samo prvih 1000 karaktera
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
