
import streamlit as st
import requests

API_URL = "https://extraalearn-lead-conversion.onrender.com/predict"

st.title("ExtraaLearn Lead Conversion Prediction")
st.write("Enter the lead details to predict whether the lead is likely to convert.")

age = st.number_input("Age", min_value=18, max_value=63, value=40)

current_occupation = st.selectbox(
    "Current Occupation",
    ["Professional", "Unemployed", "Student"]
)

first_interaction = st.selectbox(
    "First Interaction",
    ["Website", "Mobile App"]
)

profile_completed = st.selectbox(
    "Profile Completed",
    ["Low", "Medium", "High"]
)

website_visits = st.number_input(
    "Website Visits",
    min_value=0,
    max_value=30,
    value=3
)

time_spent_on_website = st.number_input(
    "Time Spent on Website",
    min_value=0,
    max_value=2537,
    value=500
)

page_views_per_visit = st.number_input(
    "Page Views per Visit",
    min_value=0.0,
    max_value=18.434,
    value=3.0
)

last_activity = st.selectbox(
    "Last Activity",
    ["Website Activity", "Email Activity", "Phone Activity"]
)

print_media_type1 = st.selectbox(
    "Print Media Type 1",
    ["No", "Yes"]
)

print_media_type2 = st.selectbox(
    "Print Media Type 2",
    ["No", "Yes"]
)

digital_media = st.selectbox(
    "Digital Media",
    ["No", "Yes"]
)

educational_channels = st.selectbox(
    "Educational Channels",
    ["No", "Yes"]
)

referral = st.selectbox(
    "Referral",
    ["No", "Yes"]
)

if st.button("Predict Conversion"):

    lead_data = {
        "age": age,
        "current_occupation": current_occupation,
        "first_interaction": first_interaction,
        "profile_completed": profile_completed,
        "website_visits": website_visits,
        "time_spent_on_website": time_spent_on_website,
        "page_views_per_visit": page_views_per_visit,
        "last_activity": last_activity,
        "print_media_type1": print_media_type1,
        "print_media_type2": print_media_type2,
        "digital_media": digital_media,
        "educational_channels": educational_channels,
        "referral": referral
    }

    response = requests.post(
        API_URL,
        json=lead_data,
        timeout=120
    )

    if response.status_code == 200:

        result = response.json()

        st.write("Prediction:", result["prediction_label"])
        st.write(
            "Conversion Probability:",
            f'{result["conversion_probability"] * 100:.2f}%'
        )

    else:
        st.error("Unable to get prediction from the API.")
