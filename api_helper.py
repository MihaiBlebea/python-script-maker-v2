#!/usr/bin/env python3

API_TEMPLATE = """
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
	return jsonify({"status": "OK"})

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("HTTP_PORT", 5000)))
"""

def main():
    write_file("server.py", API_TEMPLATE.strip())


def write_file(file_path: str, content: str):
    f = open(file_path, "w")
    f.write(content)
    f.close()


if __name__ == "__main__":
    main()