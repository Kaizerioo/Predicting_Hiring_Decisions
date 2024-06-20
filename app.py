import streamlit as st
import joblib
import numpy as np
model = joblib.load('forest_model.joblib','r')
st.title('Machine Learning Project')

st.write("""Recruitment data""")
gender = (
    "Female",
    "Male"
)

education_level = ("Bachelor's (Type 1)", "Bachelor's (Type 2)","Master's","Ph.D") #1 bachelor type 1, 2 bachelor type 2, 3 master, 4 Ph.D
recruitment_strategy = ("aggresive","moderate","conservative") #1 aggresive, 2 moderate, 3 conservative

age = st.number_input("Age :", min_value=0, max_value=200, value=0, step=1)
gender = st.selectbox("Gender :",gender)
education_level = st.selectbox("education level :",education_level)
experience_years = st.number_input("Experience Years :", min_value=0, max_value=20, value=0, step=1)
previous_company = st.number_input("Previous Company :", min_value=0, max_value=20, value=0, step=1)
distance_from_company = st.number_input("Distance from Company (km)")
interviewer_score = st.slider("Interviewer Score :", 0,100)
skill_score = st.slider("Skill Score :",0,100)
personality_score = st.slider("Personality Score :",0,100)
recruitment_strategy = st.selectbox("Recruitment Strategy :",recruitment_strategy)
ok = st.button("Calculate")
if ok:
    if education_level == "Bachelor's (Type 1)":
        education_level = 1
    elif education_level == "Bachelor's (Type 2)":
        education_level = 2
    elif education_level == "Master's":
        education_level = 3
    else:
        education_level = 4
    
    if recruitment_strategy == "aggresive":
        recruitment_strategy = 1
    elif recruitment_strategy == "moderate":
        recruitment_strategy = 2
    else:
        recruitment_strategy = 3
    
    x = np.array([[education_level,experience_years,previous_company,interviewer_score,skill_score,personality_score,recruitment_strategy]])
    x = x/255
    predict = model.predict(x)
    if predict == 1:
        st.header("You are Hired !")
    else:
        st.header("You are not Hired !")
    
    st.markdown("Prediction with 96% Accuracy model")
