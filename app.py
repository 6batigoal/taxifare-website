import streamlit as st
from datetime import datetime, time
import requests

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

# Date and time input
date = st.date_input("Pickup date", value=datetime.today())
time_input = st.time_input("Pickup time")

# Numeric inputs for coordinates
pickup_longitude = st.number_input("Pickup longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff latitude", value=40.748817)

# Passenger count
passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, value=1)

# 2. Combine date and time into full datetime string
pickup_datetime = datetime.combine(date, time_input)
pickup_datetime_str = pickup_datetime.strftime("%Y-%m-%d %H:%M:%S")

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

'''

2. Let's build a dictionary containing the parameters for our API...

'''

# 3. Build dictionary for the API
params = {
    "pickup_datetime": pickup_datetime_str,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": int(passenger_count)
}

# Show the params (for debugging)
st.write("### API parameters:")
st.json(params)

'''

3. Let's call our API using the `requests` package...
4. Let's retrieve the prediction from the **JSON** returned by the API...
5. Finally, we can display the prediction to the user

'''

# Step 3: Call the API
url = 'https://taxifare.lewagon.ai/predict'

if st.button("Get Fare Prediction"):
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            prediction = response.json().get("fare", "No fare in response")
            st.success(f"Predicted fare: ${prediction:.2f}")
        else:
            st.error(f"API returned status code {response.status_code}")
    except Exception as e:
        st.error(f"Error while calling API: {e}")
