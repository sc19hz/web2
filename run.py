from app import create
import json
import logging
from flask import Flask,request,jsonify
app=create()

if __name__=="__main__":

    handler = logging.FileHandler('logs/flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter("%(asctime)s flask %(levelname)s %(message)s")
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run(debug=True)