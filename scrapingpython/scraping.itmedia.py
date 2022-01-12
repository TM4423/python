import json
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)

@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")

@app.route("/api/recommend_article")
def api_recommend_article():
    """ITMediaから記事を入手して、ランダムに1件返却します."""
    with urlopen("https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml") as res:
        html = res.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("item")
    shuffle(items)
    item = items[0]
    print(item)
    return json.dumps({
        "content" : item.find("title").string,
        # "link": item.get('href')
        "link": item.get("link")
        # "link": item.find('a').get_text()
    })

if __name__ == "__main__":
    app.run(debug=True, port=5003)
