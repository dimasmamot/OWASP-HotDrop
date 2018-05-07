from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Ganti Masbor, Serius"

@app.route("/test")
def masbor():
    return "Iki yoiso masbor"

@app.route("/test2")
def masbor2():
    return "awawawa"

if __name__ == "__main__":
    app.run()