from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Ganti Masbor, Serius"

@app.route("/test")
def hello():
    return "Iki yoiso masbor"

if __name__ == "__main__":
    app.run()