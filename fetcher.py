from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# build embed URLs from IDs
def build_url(tmdb=None, imdb=None):
    if imdb:
        return f"https://ythd.org/embed/{imdb}"
    if tmdb:
        return f"https://vsembed.ru/embed/movie/{tmdb}"
    return None


@app.route("/fetch")
def fetch():
    tmdb = request.args.get("tmdb")
    imdb = request.args.get("imdb")

    url = build_url(tmdb=tmdb, imdb=imdb)

    if not url:
        return jsonify({"error": "missing tmdb or imdb"}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        resp = requests.get(url, headers=headers, timeout=10)
        html = resp.text

        soup = BeautifulSoup(html, "html.parser")

        # extract iframe sources
        iframes = []
        for iframe in soup.find_all("iframe"):
            src = iframe.get("src")
            if src:
                iframes.append(src)

        return jsonify({
            "input": {"tmdb": tmdb, "imdb": imdb},
            "embed_url": url,
            "iframe_count": len(iframes),
            "iframes": iframes
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4343, debug=True)
