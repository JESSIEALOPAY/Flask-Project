from flask import Flask, render_template, templating

app = Flask(__name__)


@app.route("/")
def index():
    poem = """Beni boşver kendini al
Al git uzak dur benden
Seni seven birini bul
Bul unut geçmişi lütfen
Beni sevme sevme nolur
Acın olur üzerim bak
Beni unut bizi unut
Unut geçmişi lütfen"""
    number=42
    header="Welcome to Main Page"
    htmlContent=dict()
    htmlContent["number"]=number
    htmlContent["header"]=header
    htmlContent["poem"]=poem
    return render_template("index.html",htmlContent=htmlContent)


@app.route("/about")
def about():
    return "Would you like to get information about who"

@app.route("/inheritance")
def inheritance():
    return render_template("inheritance.html")


if __name__ == '__main__':
    app.run(debug=True)
