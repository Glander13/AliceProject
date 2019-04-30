from flask import Flask
import quest
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/quest', methods=['POST'])
def run_quest():
    return quest.main()


if __name__ == '__main__':
    app.run()
