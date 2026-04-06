import streamlit as st
import numpy as np
import pickle

# Load model
model = pickle.load(open("model_v2.pkl","rb"))

st.title("AI Campaign ROI Predictor + Strategy Recommender")

st.write("Predict ROI and get best campaign strategy")

# Inputs
budget = st.slider("Marketing Budget", 5000, 200000, 50000)

platform = st.selectbox(
    "Platform",
    ["Instagram","Facebook","Google Ads","LinkedIn","Influencer"]
)

goal = st.selectbox(
    "Campaign Goal",
    ["Sales","Leads","Traffic","Brand Awareness","App Installs"]
)

startup_age = st.slider("Startup Age (years)",1,10,3)

company_size = st.selectbox(
    "Company Size",
    ["Micro (1-10)","Small (11-25)","Medium (26-50)","Large (50+)"]
)

industry = st.selectbox(
    "Industry",
    ["SaaS","E-commerce","FinTech","EdTech","Services","Other"]
)

experience = st.selectbox(
    "Marketing Experience",
    ["Low","Medium","High"]
)

roi_confidence = st.slider("ROI Confidence",1,5,3)

targeting = st.slider("Targeting Score",1,10,7)

content = st.slider("Content Score",1,10,8)

# Mappings
platform_map = {"Instagram":1,"Facebook":2,"Google Ads":3,"LinkedIn":4,"Influencer":5}
goal_map = {"Sales":1,"Leads":2,"Traffic":3,"Brand Awareness":4,"App Installs":5}
company_size_map = {"Micro (1-10)":1,"Small (11-25)":2,"Medium (26-50)":3,"Large (50+)":4}
industry_map = {"SaaS":1,"E-commerce":2,"FinTech":3,"EdTech":4,"Services":5,"Other":6}
experience_map = {"Low":1,"Medium":2,"High":3}


# -------- ROI Prediction --------
if st.button("Predict ROI"):

    input_data = np.array([[
        budget,
        platform_map[platform],
        goal_map[goal],
        startup_age,
        company_size_map[company_size],
        industry_map[industry],
        experience_map[experience],
        roi_confidence,
        targeting,
        content
    ]])

    prediction = model.predict(input_data)

    st.success(f"Predicted ROI: {round(prediction[0],2)} %")


# -------- Recommendation Engine --------
if st.button("Suggest Best Strategy"):

    best_roi = -999
    best_config = None

    for p in platform_map:
        for g in goal_map:
            for t in range(5,11):
                for c in range(5,11):

                    input_data = np.array([[
                        budget,
                        platform_map[p],
                        goal_map[g],
                        startup_age,
                        company_size_map[company_size],
                        industry_map[industry],
                        experience_map[experience],
                        roi_confidence,
                        t,
                        c
                    ]])

                    pred = model.predict(input_data)[0]

                    if pred > best_roi:
                        best_roi = pred
                        best_config = (p, g, t, c, round(pred,2))

    st.subheader("Recommended Strategy")

    st.write(f"Platform: {best_config[0]}")
    st.write(f"Goal: {best_config[1]}")
    st.write(f"Targeting Score: {best_config[2]}")
    st.write(f"Content Score: {best_config[3]}")
    st.success(f"Expected ROI: {best_config[4]} %")