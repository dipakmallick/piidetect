from flask import Flask, g,  session, redirect, render_template, request, jsonify, Response 
from flask import url_for
from models import pii_rep_model 
from models import pii_add_regx_model
import templates
import json
import time


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
      reg_detail=pii_rep_model.piireport()
      r_detail=reg_detail.get_regx(0)
      print(r_detail)
      r_types=reg_detail.get_types()
      print(type(r_types))
      print(r_types)
      return render_template("index.html", r_detail=r_detail, r_types=r_types)

@app.route('/add_regex', methods=['POST'])
def add_regex():
   reg_add=pii_add_regx_model.add_data()
   d=request.get_json()
   r=reg_add.add_regex(d[0]['tid'],d[1]["rvalue"])
   return jsonify()
   
@app.route('/add_r_type', methods=['POST'])
def add_types():
   t_add=pii_add_regx_model.add_data()
   d=request.get_json()
   #print(d)
   r=t_add.add_type(d[0]['rtype'])
   return jsonify()

@app.route('/get_init_stats', methods=['GET'])
def get_init_stats():
   return render_template("regex_reports.html")

if __name__ == '__main__':
   #time.sleep(120)
   app.run(debug=False, host='0.0.0.0',port=5000)
   