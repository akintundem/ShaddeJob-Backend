# import ollama
# import time

# def extract_resume_info(resume_text):
#     prompt = f"""
#     I have provided the following resume text. Please extract the following information and format it as a JSON object with the following keys: "skills", "education", "volunteering", "experience", and "certifications". Each key should contain an array of relevant entries.

#     Resume:
#     {resume_text}

#     JSON Output:
#     {{
#       "skills": [],
#       "education": [],
#       "volunteering": [],
#       "experience": [],
#       "certifications": []
#     }}
#     """

#     # Send the prompt to LLaMA
#     response = ollama.chat(model='llama3.1', messages=[
#         {
#             'role': 'user',
#             'content': prompt,
#         },
#     ])

#     return response

# # Replace with your actual resume text
# resume_text = """
# Mayokun Moses Akintunde
# (204)-869-1025 | akintundemayokun@gmail.com | Linkedin | GitHub
# PROFILE
# Computer Engineering graduate passionate about technology, innovation, complex systems and solving
# complex business challenges. Proficient in cloud computing, embedded systems, digital signals and
# systems, computer vision, databases, and parallel processing. Possess strong communication and
# problem-solving skills, with experience in designing, writing, debugging and testing code effectively.
# TECHNICAL SKILLS
# Technologies: Java, Python, C/C++, SQL, MATLAB, Amazon AWS (EC2, ECS, RDS, S3, Cognito),
# Linux/Unix, CUDA, Docker, Open MPI, TensorFlow, OpenCV, Flask, Agile, Android Studio,
# Git/GitHub/Gitlab, JIRA.
# Relevant Course: Web Developer Bootcamp Udemy, AWS Cloud Practitioner Udemy, Docker &
# Kubernetes Udemy, Software Engineering 1, Parallel Processing, Operating System, and Introduction to
# Database.
# WORK EXPERIENCE
# Database Engineering Intern (Engineering Aide II)
# Manitoba Hydro
# May 2023 - December 2023.
# Winnipeg, Manitoba.
# • Designed and developed a specialized database with Microsoft SQL Server to manage extensive
# power generation study data from PSS\E software for the Integrated Resource Planning Division.
# • Developed a web server with Flask and designed a user-friendly interface using HTML and CSS
# to enable engineers store, access, and download automated reports and files (PSS\E softwarecompatible
# formats).
# • Implemented an authentication system and session-based authorization to enhance the security
# and access/resource control of the web server.
# • Regularly submitted progress reports to supervisors and maintained an up-to-date documentation
# for the database design and web server.
# Engineering Aide I
# Greif Inc
# May 2022 - September 2022.
# Winnipeg, Manitoba.
# • Troubleshot and configured devices to develop a local network architecture, incorporating
# Android tablets, MOXA, and a Server Panel to improve production documentation in the factory.
# Student Experience Ambassador
# International College of Manitoba
# Feb 2021 - June 2024.
# Winnipeg, Manitoba.
# • Dispatch student status letters and transcripts via email or courier services.
# • Deliver lessons, tutorials, and workshops on pre-arrival success strategies to >120 students per
# semester.
# EDUCATION
# Bachelor of Science in Computer Engineering
# Price of Faculty of Engineering
# University of Manitoba
# June 2024.
# Winnipeg, Manitoba.
# Mayokun Moses Akintunde
# (204)-869-1025 | akintundemayokun@gmail.com | Linkedin | GitHub
# PROJECT EXPERIENCE
# Full Stack Engineer
# E-commerce App (Amazon Replica)
# April 2024 - Present.
# • Implemented AWS Cognito for user authentication and server authorization of client requests.
# • Developed a containerized Flask server on AWS EC2 and an AWS RDS database for an ecommerce
# app, featuring product recommendations, shopping cart management, and payment
# processing, along with a user-friendly Android app.
# Computer Vision Engineer
# Monitoring room occupancy
# September 2023 – April 2024.
# • Collaborated with peers and industry partner Antec Controls on a room occupancy system
# capstone project. Contributed to integrating ultrasonic, RGB and IR sensors to a Raspberry Pibased
# system for real-time occupancy monitoring to optimize HVAC systems in critical spaces.
# • Designed a door monitoring algorithm using YOLO V8 tracking feature to determine individuals
# entering or exiting a door using sequences of 2D images.
# Full Stack Engineer & Scrum Leader
# Airline Reservation System
# January 2024 – April 2024.
# • Managed a team as a Scrum Master while developing a comprehensive Android airline
# reservations app, incorporating features such as booking, user authentication, flight search, seat
# selection, user profile management, payment system, and online check-in.
# • Performed rigorous testing, including unit tests with stubs and mocks, integration tests, and
# system tests with Espresso to ensure compliance with client’s requirements.
# Computer Vision Engineer
# Image Processing
# October 2023 - December 2023.
# • Utilized load balancing techniques using Open MPI for parallel image processing (spatial
# filtering) with C++.
# • Implemented CUDA Kernels and cuBLAS library for parallel image processing (spatial filtering)
# and conducted a comparative analysis of the distributed versus GPU methodologies using C++.
# Embedded System Engineer
# Communication Device for Hard of Hearing Curlers
# January 2023 - April 2023.
# • Collaborated in a team to develop Skip and Sweeper devices to aid communication for deaf
# curlers. Led software development and integrated components such as buttons and potentiometers
# to the ESP32 microcontrollers.
# • Designed one-way Wi-Fi communication (ESP-NOW) to transmit instructions from the skip to
# sweepers, displaying commands via LEDs devices on the sweeper’s brooms.
# AWARDS
# • IEEE Ted Glass Award for Best Design Project – Capstone, 2024.
# • Appeared on the Dean’s Honor List (2019, 2020, 2021, 2023, and 2024).
# • Susan Deane Memorial Scholarship Award at The International College of Manitoba."""

# # # Extract information
# # extracted_info = 

# # Print the extracted information
# # if extracted_info:
# noRun = 10
# total = 0
# for i in range(0,noRun):
#     start = time.time()
#     # val  = extracted_info['message']['content']
#     extract_resume_info(resume_text)
#     end = time.time()
#     # print(val)
#     elapsed = end - start
#     total += elapsed
#     print("Time taken:",elapsed)
# print("AVERAGE:",{total/noRun})


import requests

def generate_response(prompt):
    url = "http://localhost:11434/api/generate"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3",
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=data
        )
        
        # Check if the response status code indicates an error
        response.raise_for_status()
        
        # Parse and return the JSON response
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

# Example usage
prompt = "What color is the sky at different times of the day? Respond using JSON"
response = generate_response(prompt)
print(response)
