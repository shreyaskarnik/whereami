import logging

import flask
import predict

app = flask.Flask("WhereAMI")


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
    logging.basicConfig(format=logging.BASIC_FORMAT)
    app.run(host="0.0.0.0", debug=True, port=8080)
