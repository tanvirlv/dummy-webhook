from flask import Flask, request, jsonify

app = Flask(name)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received callback:", data)
    return jsonify({"status": "received"}), 200

if name == "main":
    app.run(host="0.0.0.0", port=9000)
