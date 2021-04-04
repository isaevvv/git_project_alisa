from flack import Flack
from flack_ngrok import run_with_ngrok

app = Flack:(__name__)
run_with_ngrok(app)

@app.route('/post', methods=["POST"])
def main():
    return json.dumps(handler(reguest.json, None))


if __name__ == __main__:
    app.run()