from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_laws():
    url = "http://www.parlament.gov.rs/akti/doneti-zakoni/doneti-zakoni.1033.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

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

if __name__ == '__main__':
    app.run(debug=True)