"""
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html

GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

Support me: https://github.com/sponsors/GodsScion

version:    26.01.20.5.08
"""

###################################################### APPLICATION INPUTS ######################################################


# >>>>>>>>>>> Easy Apply Questions & Inputs <<<<<<<<<<<

# Give an relative path of your default resume to be uploaded. If file in not found, will continue using your previously uploaded resume in LinkedIn.
default_resume_path = "all resumes/default/resume.pdf"  # (In Development)

# What do you want to answer for questions that ask about years of experience you have, this is different from current_experience?
years_of_experience = "7"  # A number in quotes Eg: "0","1","2","3","4", etc.

# Do you need visa sponsorship now or in future?
require_visa = "No"  # "Yes" or "No"

# What is the link to your portfolio website, leave it empty as "", if you want to leave this question unanswered
website = "https://github.com/SantGT5"  # "www.example.bio" or "" and so on....

# Please provide the link to your LinkedIn profile.
linkedIn = "https://www.linkedin.com/in/gian-lucas/"  # "https://www.linkedin.com/in/example" or "" and so on...

# What is the status of your citizenship? # If left empty as "", tool will not answer the question. However, note that some companies make it compulsory to be answered
# Valid options are: "U.S. Citizen/Permanent Resident", "Non-citizen allowed to work for any employer", "Non-citizen allowed to work for current employer", "Non-citizen seeking work authorization", "Canadian Citizen/Permanent Resident" or "Other"
us_citizenship = "Other"


## SOME ANNOYING QUESTIONS BY COMPANIES 🫠 ##

# What to enter in your desired salary question (American and European), What is your expected CTC (South Asian and others)?, only enter in numbers as some companies only allow numbers,
desired_salary = (
    120_000  # 80000, 90000, 100000 or 120000 and so on... Do NOT use quotes
)
"""
Note: If question has the word "lakhs" in it (Example: What is your expected CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
And if asked in months, then it will divide by 12 and answer. Examples:
* 2400000 will be answered as "200000"
* 850000 will be answered as "70833"
"""

# What is your current CTC? Some companies make it compulsory to be answered in numbers...
current_ctc = (
    100_000  # 800000, 900000, 1000000 or 1200000 and so on... Do NOT use quotes
)
"""
Note: If question has the word "lakhs" in it (Example: What is your current CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
# And if asked in months, then it will divide by 12 and answer. Examples:
# * 2400000 will be answered as "200000"
# * 850000 will be answered as "70833"
"""

# (In Development) # Currency of salaries you mentioned. Companies that allow string inputs will add this tag to the end of numbers. Eg:
# currency = "INR"                 # "USD", "INR", "EUR", etc.

# What is your expected hourly rate? (e.g. "What is your expected hourly rate?")
hourly_rate = 80  # Any number >= 0 without quotes. Eg: 50, 80, 100, etc.

# What is your notice period in days?
notice_period = 30  # Any number >= 0 without quotes. Eg: 0, 7, 15, 30, 45, etc.
"""
Note: If question has 'month' or 'week' in it (Example: What is your notice period in months), 
then it will divide by 30 or 7 and answer respectively. Examples:
* For notice_period = 66:
  - "66" OR "2" if asked in months OR "9" if asked in weeks
* For notice_period = 15:"
  - "15" OR "0" if asked in months OR "2" if asked in weeks
* For notice_period = 0:
  - "0" OR "0" if asked in months OR "0" if asked in weeks
"""

# Your LinkedIn headline in quotes Eg: "Software Engineer @ Google, Masters in Computer Science", "Recent Grad Student @ MIT, Computer Science"
linkedin_headline = "Software Engineer | Freelancer | TypeScript, Python, Golang | Scalable Systems, Microservices, Docker, Ansible, AI, LLM"  # "Headline" or "" to leave this question unanswered

# Your summary in quotes, use \n to add line breaks if using single quotes "Summary".You can skip \n if using triple quotes """Summary"""
linkedin_summary = """
Software Engineer with 7 years of experience delivering scalable solutions and leading high-performing teams. Proven track record in designing strategic, efficient systems and solving complex technical challenges. Experienced team leader with a strong focus on collaboration, innovation, and driving results that align with business goals.
"""

"""
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
"""

# Your cover letter in quotes, use \n to add line breaks if using single quotes "Cover Letter".You can skip \n if using triple quotes """Cover Letter""" (This question makes sense though)
cover_letter = """
Software Engineer with 7 years of experience delivering scalable solutions and leading high-performing teams. Proven track record in designing strategic, efficient systems and solving complex technical challenges. Experienced team leader with a strong focus on collaboration, innovation, and driving results that align with business goals.
"""
##> ------ Dheeraj Deshwal : dheeraj9811 Email:dheeraj20194@iiitd.ac.in/dheerajdeshwal9811@gmail.com - Feature ------

# Your user_information_all letter in quotes, use \n to add line breaks if using single quotes "user_information_all".You can skip \n if using triple quotes """user_information_all""" (This question makes sense though)
# We use this to pass to AI to generate answer from information , Assuing Information contians eg: resume  all the information like name, experience, skills, Country, any illness etc.
# This profile is also used by the Claude AI relevance filter to score how well each job matches you.
user_information_all = """
Name: Gian de Abreu
Title: Senior Software Engineer (AI & Backend Systems)
Location: Netherlands (EU work authorization). Phone: +31 6 42118304. GitHub: SantGT5.
Experience: 7+ years building scalable backend systems, AI-powered applications, microservices, and cloud-native solutions, with a track record of leading technical initiatives and delivering high-impact products in fintech and SaaS.

Core languages & frameworks: Python, Golang, Node.js, TypeScript, JavaScript, React, React Native, Vue.
Backend & APIs: REST APIs, GraphQL, API design, microservices architecture, event-driven architecture, distributed systems, system design.
Databases & data: MongoDB, PostgreSQL, InfluxDB, data pipelines, Redis.
DevOps & tooling: Docker, Ansible, CI/CD, GitHub Actions, Grafana, monitoring.
Messaging & IoT: RabbitMQ, MQTT.
AI & emerging tech: Large Language Models (LLMs), vLLM, OpenAI API, prompt engineering, AI agents, generative AI, AI automation.
Methodologies: Agile, Scrum, Kanban. Leadership: mentoring, team & technical leadership, cross-functional collaboration.

Work history:
- Bluem (Software Engineer, Nov 2024-present): led AI/LLM-powered solutions; built the WealthCheck SDK for financial document analysis; designed scalable backend services and APIs in Python, Golang, and TypeScript; high-volume document processing with RabbitMQ/Redis; deployed cloud-native apps with Docker, Ansible, CI/CD, and vLLM.
- WonderBit B.V. (Full Stack Engineer, Jul 2023-Nov 2024): full-stack delivery with Node.js, Python, React, Vue; Docker containerization; scalable REST APIs; CI/CD with Ansible.
- Billetero (Freelance Software Engineer, Jan 2024-Apr 2024): AI-powered LLM document processing; backend in Python and Golang; containerized deployments with Docker and Ansible.
- Plauti Data Management (Full Stack Engineer, May 2022-Jun 2023): SaaS data quality platform; Node.js backend microservices; REST APIs; unit/integration testing with Vitest.
- BBVA Bank (Software Developer, Feb 2019-Apr 2022): internal banking apps with React, Node.js, MongoDB; transaction monitoring dashboard.

Preferences: Remote work; contract or temporary engagements; backend, full-stack, Python, Golang, Node.js, or TypeScript roles at mid-senior/senior level. Strong fit for AI/LLM, fintech, and SaaS. Not a fit for primarily C#/.NET, C/C++, PHP, Ruby, embedded.
"""
##<
"""
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
"""

# Name of your most recent employer
recent_employer = "Bluem payment & identity"  # "", "Lala Company", "Google", "Snowflake", "Databricks"

# Example question: "On a scale of 1-10 how much experience do you have building web or mobile applications? 1 being very little or only in school, 10 being that you have built and launched applications to real users"
confidence_level = (
    "8"  # Any number between "1" to "10" including 1 and 10, put it in quotes ""
)
##


# >>>>>>>>>>> RELATED SETTINGS <<<<<<<<<<<

## Allow Manual Inputs
# Should the tool pause before every submit application during easy apply to let you check the information?
pause_before_submit = False  # True or False, Note: True or False are case-sensitive
"""
Note: Will be treated as False if `run_in_background = True`
"""

# Should the tool pause if it needs help in answering questions during easy apply?
# Note: If set as False will answer randomly...
pause_at_failed_question = True  # True or False, Note: True or False are case-sensitive
"""
Note: Will be treated as False if `run_in_background = True`
"""
##

# Do you want to overwrite previous answers?
overwrite_previous_answers = (
    False  # True or False, Note: True or False are case-sensitive
)


############################################################################################################
"""
THANK YOU for using my tool 😊! Wishing you the best in your job hunt 🙌🏻!

Sharing is caring! If you found this tool helpful, please share it with your peers 🥺. Your support keeps this project alive.

Support my work on <PATREON_LINK>. Together, we can help more job seekers.

As an independent developer, I pour my heart and soul into creating tools like this, driven by the genuine desire to make a positive impact.

Your support, whether through donations big or small or simply spreading the word, means the world to me and helps keep this project alive and thriving.

Gratefully yours 🙏🏻,
Sai Vignesh Golla
"""
############################################################################################################
