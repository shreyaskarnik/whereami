import logging

import flask
import predict

app = flask.Flask("WhereAMI")
logging.basicConfig(level=logging.INFO)

appLogger = logging.StreamHandler()
appLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
app.logger.addHandler(appLogger)
app.logger.setLevel(logging.INFO)


@app.route("/ping")
def ping():
    logging.info("hit ping handler")
    return "pong"


@app.route("/invocations", methods=["POST"])
def invoke():
    logging.info("hit invoke handler")
    data = flask.request.get_json(force=True)
    try:
        result = predict.download_and_predict(
            data['url'],
            int(data.get('max_predictions', 3))
        )
        return flask.jsonify(result)
    except Exception as e:
        return "Error Occured", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8080)
