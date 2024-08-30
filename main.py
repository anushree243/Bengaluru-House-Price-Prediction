#flask, scikit-learn, pandas, pickle-mixin,flask-cors
import pandas as pd
from flask import Flask, render_template,request
import pickle
# from sklearn.linear_model import Ridge
import numpy as np

app= Flask(__name__ ,static_url_path='/static')
data=pd.read_csv('Cleaned_data.csv')
pipe = pickle.load(open('RidgeModel.pkl', 'rb'))

@app.route('/')
def index():
    locations = sorted(data['location'].unique())
    bhks = sorted(data['bhk'].unique())
    baths = sorted(data['bath'].unique())
    total_sqfts = sorted(data['total_sqft'].unique())
    return render_template('index.html',locations=locations,bhks=bhks,baths=baths,total_sqfts=total_sqfts)


@app.route('/predict',methods=['POST'])
def predict():
    locations= request.form.get('location')
    bhk = float(request.form.get('bhk'))
    bath=float(request.form.get('bath'))
    sqft = request.form.get('total_sqft')

    print(locations, bhk, bath, sqft)
    input_data = pd.DataFrame( [[locations, sqft, bath, bhk]], columns=['location', 'total_sqft', 'bath', 'bhk'])

    prediction=pipe.predict(input_data)[0] * 1e5
    print(prediction)
    return str(np.round(prediction,2))

if __name__=="__main__":
    app.run(debug=True, port=5502)