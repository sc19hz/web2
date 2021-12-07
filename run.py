from app import create
import json
import logging
from flask import Flask,request,jsonify
app=create()

if __name__=="__main__":


    app.run(debug=True)