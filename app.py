import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load('forest_model.joblib')

# Define options for select boxes and radio buttons
gender_options = ("Female", "Male")
education_level_options = ("Bachelor's (Type 1)", "Bachelor's (Type 2)", "Master's", "Ph.D")
recruitment_strategy_options = ("aggressive", "moderate", "conservative")

# Function to calculate hiring decision
def calculate(edu_level, exp_years, prev_company, interview, skill, personality, strategy):
    encoded_edu_level, encoded_strategy = encode(edu_level, strategy)
    x = np.array([[encoded_edu_level, exp_years, prev_company, interview, skill, personality, encoded_strategy]])
    predict = model.predict(x)
    if predict == 1:
        return "You are Hired !"
    else:
        return "You are not Hired !"

# Function to encode education level and recruitment strategy
def encode(education_level, recruitment_strategy):
    education_level_encoded = education_level_options.index(education_level) + 1
    recruitment_strategy_encoded = recruitment_strategy_options.index(recruitment_strategy) + 1
    return education_level_encoded, recruitment_strategy_encoded

# Function to display user input data
def show_data(name, age, gender, edu_level, exp_years, prev_company, dist, interview, skill, personality, strategy):
    st.write("**Personal Information**")
    st.write(f"Full Name: {name}")
    st.write(f"Age: {age}")
    st.write(f"Gender: {gender}")
    st.write(f"Education Level: {edu_level}")
    st.write(f"Recruitment Strategy: {strategy}")
    st.write(f"Experience Years: {exp_years}")
    st.write(f"Previous Company: {prev_company}")
    st.write(f"Distance from Company: {dist} km")
    st.write("**Scores**")
    st.write(f"Interview Score: {interview}")
    st.write(f"Skill Level: {skill}")
    st.write(f"Personality Score: {personality}")

# Streamlit app
st.title("💼 Hiring Decision Prediction")

# Sidebar styling and layout
st.sidebar.header("Input Form")
name = st.sidebar.text_input("Full Name")
age = st.sidebar.number_input("Age", min_value=0, max_value=200, value=0, step=1)
gender = st.sidebar.radio("Gender", gender_options)
edu_level = st.sidebar.selectbox("Education Level", education_level_options)
exp_years = st.sidebar.number_input("Experience Years", min_value=0, max_value=20, value=0, step=1)
prev_company = st.sidebar.number_input("Previous Company", min_value=0, max_value=20, value=0, step=1)
dist = st.sidebar.number_input("Distance from Company (km)")
interview = st.sidebar.slider("Interview Score", 0, 100)
skill = st.sidebar.slider("Skill Score", 0, 100)
personality = st.sidebar.slider("Personality Score", 0, 100)
strategy = st.sidebar.radio("Recruitment Strategy", recruitment_strategy_options)
submit_button = st.sidebar.button("Calculate")

# Display results upon submission
if submit_button:
    st.header("Result")
    show_data(name, age, gender, edu_level, exp_years, prev_company, dist, interview, skill, personality, strategy)
    result = calculate(edu_level, exp_years, prev_company, interview, skill, personality, strategy)
    st.success(result)
