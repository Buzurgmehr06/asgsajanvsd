pip install streamlit
pip install sqlite3
pip install pathlib
pip install pickle
pip install io
import streamlit as st
import sqlite3
from pathlib import Path
import streamlit_authenticator as stauth
import pickle
from io import BytesIO

names = ["Negmatov Buzurgmehr", "Rebecca Miller"]
usernames = ["Negmatov B", "rmiller"]
passwords = ["XXX", "XXX"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                    "sales_dashboard", "abcdef", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "main")
if authentication_status == False:
    st.error("Username/password is incorrect")
if authentication_status == None:
    st.warning("Please enter your username and password")
if authentication_status:
    st.sidebar.info('Анализ пользователей контент_сервиса Буквомешалка')
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
# Connect to the SQLite database
    conn = sqlite3.connect('new_quiz_database.db')
    cursor = conn.cursor()
# SQL queries
    total_subscribers_query = "SELECT COUNT() FROM Users"
    active_users_query = "SELECT count() subscriptionStatus FROM Users WHERE subscriptionStatus = 1"
    inactive_users_query = "SELECT count() subscriptionStatus FROM Users WHERE subscriptionStatus = 0"
#total_answers_query = "SELECT COUNT() FROM DailyQuestions"
#average_answers_per_user_query = "SELECT COUNT() / (SELECT COUNT(DISTINCT user_id) FROM answers) FROM answers"
    total_answered_query = "SELECT count() responsestatus FROM UserResponses"
    correct_answers_query = "SELECT COUNT() FROM UserResponses WHERE responsestatus='не правильно'"
    incorrect_answers_query = "SELECT COUNT() FROM UserResponses WHERE responsestatus='правильно'"
#additional_questions_query = "SELECT COUNT() FROM additional_questions"
#quarterly_wins_query = "SELECT COUNT() FROM wins WHERE type = 'quarterly'"
#annual_wins_query = "SELECT COUNT() FROM wins WHERE type = 'annual'"
#prizes_query = "SELECT COUNT(*) FROM prizes"
    top_users_query = "SELECT phoneNumber, SUM(currentScore) FROM Users GROUP BY phoneNumber ORDER BY SUM(currentScore)"
# Execute the SQL queries
    total_subscribers = cursor.execute(total_subscribers_query).fetchone()[0]
    active_users = cursor.execute(active_users_query).fetchone()[0]
    inactive_users = cursor.execute(inactive_users_query).fetchone()[0]
#total_answers = cursor.execute(total_answers_query).fetchone()[0]
#average_answers_per_user = cursor.execute(average_answers_per_user_query).fetchone()[0]
    total_answered = cursor.execute(total_answered_query).fetchone()[0]
    correct_answers = cursor.execute(correct_answers_query).fetchone()[0]
    incorrect_answers = cursor.execute(incorrect_answers_query).fetchone()[0]
#additional_questions = cursor.execute(additional_questions_query).fetchone()[0]
#quarterly_wins = cursor.execute(quarterly_wins_query).fetchone()[0]
#annual_wins = cursor.execute(annual_wins_query).fetchone()[0]
#prizes = cursor.execute(prizes_query).fetchone()[0]
    top_users = cursor.execute(top_users_query).fetchall()
# Display the results
    st.write("Total Subscribers:", total_subscribers)
    st.write("Active Users:", active_users)
    st.write("Inactive Users:", inactive_users)
#st.write("Total Answers:", total_answers)
#st.write("Average Answers per User:", average_answers_per_user)
    st.write("How Many Answered:", total_answered)
    st.write("Correct Answers:", correct_answers)
    st.write("Incorrect Answers:", incorrect_answers)
    percentage_correct = (correct_answers / total_answered) * 100
# Display the percentage of correct answers
    st.write("Percentage of Correct Answers:", int(percentage_correct),'%')

#st.write("Additional Questions:", additional_questions)
#st.write("Quarterly Wins:", quarterly_wins)
#st.write("Annual Wins:", annual_wins)
#st.write("Prizes:", prizes)
    top_3_users = sorted(top_users, key=lambda x: x[1], reverse=True)[:3]
    st.write("Top 3 Users:")
    for index, user in enumerate(top_3_users, start=1):
        phoneNumber, currentScore = user
        st.write(f"     User #{index}:  phoneNumber: {phoneNumber},  Points: {currentScore}")



# Close the database connection
    conn.close()
