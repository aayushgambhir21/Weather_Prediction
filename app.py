#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, request
import joblib, warnings
warnings.filterwarnings('ignore')


# In[2]:


app = Flask(__name__)


# In[3]:


model = joblib.load('model.pkl')
model


# In[4]:


scaler = joblib.load('scaler.pkl')
scaler


# In[5]:


encoder = joblib.load('label_encoder.pkl')
encoder


# In[6]:


label_mapping = {label:idx for idx, label in enumerate(encoder.classes_)}
label_mapping = {v: k for k, v in label_mapping.items()}
label_mapping


# In[7]:


@app.route("/")
def home():
    return render_template('index.html')


# In[8]:


@app.route("/predict",methods=["GET","POST"])
def predict():
    if request.method == "POST":
        temp = request.form['temperature_C']
        press_kpa = request.form['pressure_kpa']
        rel_hum = request.form['relative_humidity']
        wind_speed = request.form['wind_speed_kmph']
        visibility_km = request.form['visibility_km']
        hour = request.form['hour']
        
        data = [[temp,press_kpa,rel_hum,wind_speed,visibility_km,hour]]
        scaled_data = scaler.transform(data)
        pred = model.predict(scaled_data)[0]
        output = str(label_mapping[pred]).lower()
        return render_template('index.html',prediction_text=f"The current weather is {output}.")


# In[9]:


if __name__ == "__main__":
    app.run(port=8080)

