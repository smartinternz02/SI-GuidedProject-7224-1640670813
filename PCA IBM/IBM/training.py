from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import pickle
import requests
import json

model=pickle.load(open('PCASSS_model.pkl','rb'))
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('demo.html')

@app.route('/predict',methods=["POST"])
def predict1():
   API_KEY = "G3dbtlgP0_6fCsH_w1VDRT0h5lpTdiWi1REAiR8zssIH"
   token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
   mltoken = token_response.json()["access_token"]

   header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
   payload_scoring = {"input_data": [{"field": [["Global_reactive_power","Global_intensity","Sub_metering_1","Sub_metering_2","Sub_metering_3"]], "values": [[0.48,8,0,1,17]]}]}

   response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/8ad97539-6c91-46f2-8a35-4252457ab228/predictions?version=2021-10-23&version=2021-10-23', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
   print("Scoring response")
   predictions= response_scoring.json()
   print(predictions)
   return render_template('result.html',predictions=predictions)
if __name__ == "__main__" :
        app.run(debug=False)