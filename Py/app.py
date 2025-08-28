from flask import Flask, request, jsonify
import asyncio
import httpx
from gates import create_cvv_charge

app = Flask(__name__)

@app.route("/api/check", methods=["POST"])
def check():
    data = request.json
    gate = data.get("gate")
    card = data.get("card")

    if gate == "stripe":
        async def run_gate():
            async with httpx.AsyncClient() as client:
                return await create_cvv_charge(card, client)

        result = asyncio.run(run_gate())
    else:
        result = {"status": "error", "response": "Unsupported gate."}

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
