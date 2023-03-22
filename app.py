import pickle
import flask
from flask  import Flask,request,app,jsonify,render_template
from flask import Response
from flask_cors import CORS
import numpy as np
import pandas as pd

app=Flask(__name__)

model=pickle.load(open('rfr_model_airfoil.pkl','rb'))


@app.route("/")
def home():
    return render_template('home.html')

#predict for form input
@app.route('/predict',methods=['POST'])
def predict():
    '''
    for direct api calls through request

    '''
    ## single inputs

    # data=request.form.values()
    data=[float(x) for x in request.form.values()]
    final_features=[np.array(data)]
    #request helps to capture the json data coming from postman
    print(data)

    output=model.predict(final_features)[0]
    # return jsonify(output[0])
    return render_template('home.html',prediction_text=f"Air foil pressure is {output}")

'''
## POSTMAN data

{
    "data":{
        "Frequency":9,
        "Angle of Attack":8,
        "Chord Length":10,
        "Free-stream Velocity":1,
        "Suction side":7
    }
}
## conda env 
-> ml_model_flask
'''



@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    for direct api calls through request

    '''
    ## single inputs
    data=request.json['data']
    #request helps to capture the json data coming from postman
    print(data)
    new_data=[list(data.values())]
    output=model.predict(new_data)[0]
    return jsonify(output)

@app.route('/predict_api_batch',methods=['POST'])
def predict_api_batch():
    batch_data=request.json['batch_data']
    batch_data_list=[ list(i.values()) for i in batch_data ]
    output=model.predict(batch_data_list)
    return jsonify(output.tolist())



if __name__=="__main__":
    app.run(debug=True)

