import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#import model
model = joblib.load('forest_model.joblib','r')
df = pd.read_csv("dataset/recruitment_data.csv")
#title
st.title("💼 Hiring Decision Prediction")
st.divider()

gender = ("Female", "Male")
education_level = ("Bachelor's (Type 1)", "Bachelor's (Type 2)","Master's","Ph.D") 
#1 bachelor type 1, 2 bachelor type 2, 3 master, 4 Ph.D

recruitment_strategy = ("aggresive","moderate","conservative") 
#1 aggresive, 2 moderate, 3 conservative

EducationLevel_mapping = {1: "Bachelor's (Type 1)", 2: "Bachelor's (Type 2)", 3: "Master's", 4: "Ph.D"}
df["EducationLevel"] = df["EducationLevel"].replace(EducationLevel_mapping)
RecruitmentStrategy_mapping = {1: "aggresive",2: "moderate", 3: "conservative"}
df["RecruitmentStrategy"] = df["RecruitmentStrategy"].replace(RecruitmentStrategy_mapping)
HiringDecision_mapping = {0: "Not Hired", 1: "Hired"}
df["HiringDecision"] = df["HiringDecision"].replace(HiringDecision_mapping)

def calculate(edu_level, exp_years, prev_company, interview, skill, personality,strategy):
    encoded_edu_level, encoded_strategy = encode(edu_level, strategy)
    x = np.array([[encoded_edu_level,exp_years,prev_company,interview,skill,personality,encoded_strategy]])
    predict = model.predict(x)
    if predict == 1:
        st.success("You are Hired !")
    else:
        st.error("You are not Hired !")

def encode(education_level, recruitment_strategy):
    if education_level == "Bachelor's (Type 1)":
        education_level_encoded = 1
    elif education_level == "Bachelor's (Type 2)":
        education_level_encoded = 2
    elif education_level == "Master's":
        education_level_encoded = 3
    else:
        education_level_encoded = 4
    
    if recruitment_strategy == "aggressive":
        recruitment_strategy_encoded = 1
    elif recruitment_strategy == "moderate":
        recruitment_strategy_encoded = 2
    else:
        recruitment_strategy_encoded = 3
    
    return education_level_encoded, recruitment_strategy_encoded

def show_data(name, age, gender, edu_level, exp_years, prev_company, dist, interview, skill, personality,strategy):
    st.write("Full Name: ", name)
    st.write("Age : ", age)
    st.write("Gender : ", gender)
    st.write("Education Level :", edu_level)
    st.write("Recruitment Strategy :", strategy)
    st.write("Experience Years :", exp_years)
    st.write("Previous Company :", prev_company)
    st.write(f"Distance from Company : {dist} km")
    st.write("Interview Score :", interview)
    st.write("Skill Level :", skill)
    st.write("Personality Score :", personality)
    st.write("Strategy :", strategy)

def barplot(col_name):
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='HiringDecision', hue=col_name, ax=ax, palette="Blues")
    ax.set_title(f"Hiring Decision based on {col_name}")

    # Display the barplot in Streamlit
    st.title(f"{col_name} Barplot")
    st.pyplot(fig)

def histplot(col_name):
    fig, ax = plt.subplots()
    sns.histplot(data=df, x=df[col_name],hue=df["HiringDecision"],palette="Set3")
    ax.set_title(f"Hiring Decision based on {col_name}")
    st.title(f"{col_name} Histogram")
    st.pyplot(fig)
#form
with st.form("Input Form"):
    st.markdown("input form")
    col1, col2= st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="Full Name")
        age = st.number_input("Age :", min_value=0, max_value=200, value=0, step=1,placeholder="Age")
        gender = st.radio("Gender", gender)
    
    with col2:
        education_level = st.selectbox("Education Level",education_level)
        experience_years = st.number_input("Experience Years", min_value=0, max_value=20, value=0, step=1)
        previous_company = st.number_input("Previous Company", min_value=0, max_value=20, value=0, step=1)
        distance_from_company = st.number_input("Distance from Company (km)")


    interviewer_score = st.slider("Interviewer Score", 0,100)
    skill_score = st.slider("Skill Score",0,100)
    personality_score = st.slider("Personality Score",0,100)
    recruitment_strategy = st.radio("Recruitment Strategy",recruitment_strategy)
    submit_button = st.form_submit_button(label="Calculate")

if submit_button:
    st.divider()
    st.header("**Result !**")
    show_data(name, age, gender, education_level, experience_years, previous_company, distance_from_company, interviewer_score, skill_score, personality_score, recruitment_strategy)
    #education_level, experience_years, previous_company, interviewer_score, skill_score, personality_score, recruitment_strategy
    calculate(education_level, experience_years, previous_company, interviewer_score, skill_score, personality_score, recruitment_strategy)
    st.divider()

    #creating tabs
    
    tabs_edu, tabs_exp, tabs_prev, tabs_dist, tabs_interscore, tabs_skillscore, tabs_personalscore, tabs_strats = st.tabs(["Education Level", "Experience Year", "Previous Company", "Distance from Company", "Interviewer Score", "Skill Score", "Personality Score", "Recruitment Strategy"])
    with tabs_edu:
        barplot("EducationLevel")
    
    with tabs_exp:
        histplot("ExperienceYears")
    with tabs_prev:
        histplot("PreviousCompanies")
    with tabs_dist:
        histplot("DistanceFromCompany")
    with tabs_interscore:
        histplot("InterviewScore")
    with tabs_skillscore:
        histplot("SkillScore")
    with tabs_personalscore:
        histplot("PersonalityScore")
    with tabs_strats:
        barplot("RecruitmentStrategy")
