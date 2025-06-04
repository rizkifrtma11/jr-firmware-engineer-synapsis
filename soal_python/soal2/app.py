from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/rizki", methods=["POST"])
def processGrade():
    data = request.get_json()

    if not data or "nilai" not in data or "nama" not in data:
        return jsonify({"error": "Invalid input"}), 400

    nama = data["nama"]
    nilai = data["nilai"]

    if not isinstance(nilai, int) or nilai < 0 or nilai > 100:
        result = "Invalid"
        status = "tidak lulus"
    else:
        if nilai >= 80:
            result = "A"
        elif nilai >= 65:
            result = "B"
        elif nilai >= 50:
            result = "C"
        elif nilai >= 35:
            result = "D"
        else:
            result = "E"

        if result in ["A", "B", "C"]:
            status = "lulus"
        else:
            status = "tidak lulus"

    return jsonify({"nama": nama, "nilai": result, "status": status})


if __name__ == "__main__":
    app.run(port=8080)
