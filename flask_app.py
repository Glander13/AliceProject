import logging

from common.quest import main
from flask import Flask

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/post', methods=['POST'])
def run_app():
    return main()


if __name__ == '__main__':
    app.run()
