from flask import Flask, request, json

app = Flask(__name__)


@app.route("/")
def hello():
    return "Webhooks with Python"


@app.route("/test/", methods=["POST", "GET"])
def githubIssue():
    if request.method == "GET":
        return "OK"
    data = request.json
    print("\n" * 5)
    print(data)
    return data


if __name__ == "__main__":
    app.run(debug=True)
