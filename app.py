"""Pathways KE - Grade 10 subject → pathway → career guidance (Flask backend)."""
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="/static")

SUBJECTS = [
    {"name": "Mathematics", "cat": "Core Subjects", "core": True, "desc": "Numbers, patterns and logic: the foundation of almost every career.", "tags": ["STEM", "Social Sciences"]},
    {"name": "English", "cat": "Core Subjects", "core": True, "desc": "Reading, writing and speaking, essential in every pathway.", "tags": ["Social Sciences", "Arts & Sports"]},
    {"name": "Kiswahili", "cat": "Core Subjects", "core": True, "desc": "Kenya's national language and a language of East Africa.", "tags": ["Social Sciences", "Arts & Sports"]},
    {"name": "CSL", "cat": "Core Subjects", "core": True, "desc": "Community Service Learning: a hands-on project where you serve your community and build life skills.", "tags": ["STEM", "Social Sciences", "Arts & Sports"]},
    {"name": "Technical Drawing", "cat": "Technical", "core": False, "desc": "Drawing plans, machine parts and building designs.", "tags": ["STEM"]},
    {"name": "Biology", "cat": "Sciences", "core": False, "desc": "The study of living things, health and the environment.", "tags": ["STEM"]},
    {"name": "Chemistry", "cat": "Sciences", "core": False, "desc": "Matter, reactions and materials.", "tags": ["STEM"]},
    {"name": "Physics", "cat": "Sciences", "core": False, "desc": "Energy, forces and how the physical world works.", "tags": ["STEM"]},
    {"name": "Computer Studies", "cat": "Technical", "core": False, "desc": "Programming, data and digital systems.", "tags": ["STEM"]},
    {"name": "Agriculture", "cat": "Technical", "core": False, "desc": "Crops, livestock and food systems.", "tags": ["STEM"]},
    {"name": "Business Studies", "cat": "Business", "core": False, "desc": "How businesses start, run and grow.", "tags": ["Social Sciences"]},
    {"name": "Geography", "cat": "Humanities", "core": False, "desc": "People, places and the environment.", "tags": ["Social Sciences"]},
    {"name": "History", "cat": "Humanities", "core": False, "desc": "How the past shapes society today.", "tags": ["Social Sciences"]},
    {"name": "CRE", "cat": "Humanities", "core": False, "desc": "Christian Religious Education: ethics and values.", "tags": ["Social Sciences"]},
    {"name": "French", "cat": "Languages", "core": False, "desc": "A global language for diplomacy and trade.", "tags": ["Social Sciences", "Arts & Sports"]},
    {"name": "Music", "cat": "Creative & Sports", "core": False, "desc": "Performance, composition and sound.", "tags": ["Arts & Sports"]},
    {"name": "Fine Art", "cat": "Creative & Sports", "core": False, "desc": "Drawing, design and visual expression.", "tags": ["Arts & Sports"]},
    {"name": "Physical Education", "cat": "Creative & Sports", "core": False, "desc": "Sport science, fitness and coaching.", "tags": ["Arts & Sports"]},
]

TRACKS = {
    "STEM": {"name": "STEM Pathway", "blurb": "Science, Technology, Engineering & Mathematics",
             "subjects": ["Mathematics", "English", "Kiswahili", "Physics", "Chemistry", "Biology", "Computer Studies"],
             "courses": ["BSc Computer Science", "BSc Civil Engineering", "Bachelor of Medicine & Surgery", "BSc Agriculture", "BSc Nursing"]},
    "Social Sciences": {"name": "Social Sciences Pathway", "blurb": "Humanities, languages, business and society",
             "subjects": ["Mathematics", "English", "Kiswahili", "Business Studies", "Geography", "History", "CRE"],
             "courses": ["Bachelor of Laws (LLB)", "Bachelor of Education", "Bachelor of Commerce", "BA Journalism & Media"]},
    "Arts & Sports": {"name": "Arts & Sports Pathway", "blurb": "Creative arts, design, music and sports science",
             "subjects": ["English", "Kiswahili", "Music", "Fine Art", "Physical Education", "Mathematics"],
             "courses": ["BA Design", "Bachelor of Music", "BSc Sports Science", "BA Film & Theatre"]},
}

CAREERS = [
    {"name": "Software Engineer", "track": "STEM", "desc": "Design, build and maintain software for phones, the web and enterprises.",
     "subjects": ["Mathematics", "Computer Studies", "Physics"], "interests": ["Technology & Computers"], "skills": ["Problem solving", "Data & Analysis"], "env": ["Office-based", "Technical / Lab work"], "course": "BSc Computer Science"},
    {"name": "Doctor", "track": "STEM", "desc": "Diagnose and treat illness and promote community health.",
     "subjects": ["Biology", "Chemistry", "Mathematics"], "interests": ["Health & Medicine"], "skills": ["Problem solving", "Communication & Writing"], "env": ["Working directly with people", "Technical / Lab work"], "course": "Bachelor of Medicine & Surgery"},
    {"name": "Civil Engineer", "track": "STEM", "desc": "Plan and oversee roads, bridges, dams and buildings.",
     "subjects": ["Mathematics", "Physics", "Chemistry"], "interests": ["Engineering & Building"], "skills": ["Building & Making Things", "Problem solving", "Leading & Organizing"], "env": ["Outdoor / Field work"], "course": "BSc Civil Engineering"},
    {"name": "Data Scientist", "track": "STEM", "desc": "Turn data into decisions using statistics and code.",
     "subjects": ["Mathematics", "Computer Studies"], "interests": ["Technology & Computers", "Business & Finance"], "skills": ["Data & Analysis", "Problem solving"], "env": ["Office-based"], "course": "BSc Statistics / Data Science"},
    {"name": "Agricultural Scientist", "track": "STEM", "desc": "Improve crop yields, livestock health and food security.",
     "subjects": ["Agriculture", "Biology", "Chemistry"], "interests": ["Agriculture & Environment"], "skills": ["Data & Analysis", "Problem solving"], "env": ["Outdoor / Field work", "Technical / Lab work"], "course": "BSc Agriculture"},
    {"name": "Nurse", "track": "STEM", "desc": "Provide patient care in hospitals and communities.",
     "subjects": ["Biology", "Chemistry", "English"], "interests": ["Health & Medicine"], "skills": ["Communication & Writing", "Leading & Organizing"], "env": ["Working directly with people"], "course": "BSc Nursing"},
    {"name": "Lawyer", "track": "Social Sciences", "desc": "Advise clients, argue cases and uphold justice.",
     "subjects": ["English", "History", "CRE", "Kiswahili"], "interests": ["Law & Justice"], "skills": ["Communication & Writing", "Data & Analysis"], "env": ["Office-based", "Working directly with people"], "course": "Bachelor of Laws (LLB)"},
    {"name": "Business Entrepreneur", "track": "Social Sciences", "desc": "Build products, services and jobs through your own venture.",
     "subjects": ["Business Studies", "Mathematics", "English"], "interests": ["Business & Finance"], "skills": ["Leading & Organizing", "Creativity & Design"], "env": ["A mix of different environments"], "course": "Bachelor of Commerce"},
    {"name": "Teacher", "track": "Social Sciences", "desc": "Guide learners and shape the next generation.",
     "subjects": ["English", "Kiswahili", "Mathematics", "Geography"], "interests": ["Education & Teaching"], "skills": ["Communication & Writing", "Leading & Organizing"], "env": ["Working directly with people"], "course": "Bachelor of Education"},
    {"name": "Journalist", "track": "Social Sciences", "desc": "Investigate and tell stories across print, radio, TV and online.",
     "subjects": ["English", "Kiswahili", "History"], "interests": ["Media & Communication"], "skills": ["Communication & Writing", "Creativity & Design"], "env": ["A mix of different environments"], "course": "BA Journalism & Media"},
    {"name": "Graphic Designer", "track": "Arts & Sports", "desc": "Create brands, posters and digital visuals.",
     "subjects": ["Fine Art", "Computer Studies", "English"], "interests": ["Arts & Design", "Media & Communication"], "skills": ["Creativity & Design"], "env": ["Creative studio work"], "course": "BA Design"},
]


SUBJECTS += [
    {"name": "Home Science", "cat": "Technical", "core": False, "desc": "Nutrition, textiles and managing a home or catering business.", "tags": ["STEM", "Social Sciences"]},
    {"name": "Literature in English", "cat": "Humanities", "core": False, "desc": "Novels, plays and poetry; builds analysis and writing.", "tags": ["Social Sciences", "Arts & Sports"]},
    {"name": "Drama & Theatre", "cat": "Creative & Sports", "core": False, "desc": "Acting, directing and stagecraft.", "tags": ["Arts & Sports"]},
    {"name": "German", "cat": "Languages", "core": False, "desc": "A route to study and work in Germany and Europe.", "tags": ["Social Sciences"]},
    {"name": "Arabic", "cat": "Languages", "core": False, "desc": "Language for trade, tourism and Islamic studies.", "tags": ["Social Sciences"]},
    {"name": "Electricity & Power", "cat": "Technical", "core": False, "desc": "Wiring, circuits and power systems.", "tags": ["STEM"]},
]

CAREERS += [
    {"name": "Pharmacist", "track": "STEM", "desc": "Prepare and dispense medicines and advise patients on safe use.",
     "subjects": ["Chemistry", "Biology", "Mathematics"], "interests": ["Health & Medicine"], "skills": ["Data & Analysis", "Communication & Writing"], "env": ["Technical / Lab work", "Working directly with people"], "course": "Bachelor of Pharmacy"},
    {"name": "Electrical Engineer", "track": "STEM", "desc": "Design power networks, electronics and renewable energy systems.",
     "subjects": ["Physics", "Mathematics", "Electricity & Power"], "interests": ["Engineering & Building", "Technology & Computers"], "skills": ["Problem solving", "Building & Making Things"], "env": ["Technical / Lab work", "Outdoor / Field work"], "course": "BSc Electrical Engineering"},
    {"name": "Architect", "track": "STEM", "desc": "Design buildings that are safe, beautiful and affordable.",
     "subjects": ["Mathematics", "Physics", "Fine Art"], "interests": ["Engineering & Building", "Arts & Design"], "skills": ["Creativity & Design", "Building & Making Things"], "env": ["Creative studio work", "Outdoor / Field work"], "course": "Bachelor of Architecture"},
    {"name": "Veterinarian", "track": "STEM", "desc": "Care for livestock, pets and wildlife and protect animal health.",
     "subjects": ["Biology", "Chemistry", "Agriculture"], "interests": ["Health & Medicine", "Agriculture & Environment"], "skills": ["Problem solving", "Data & Analysis"], "env": ["Outdoor / Field work", "Technical / Lab work"], "course": "Bachelor of Veterinary Medicine"},
    {"name": "Cybersecurity Analyst", "track": "STEM", "desc": "Protect banks, telcos and governments from online attacks.",
     "subjects": ["Computer Studies", "Mathematics", "Physics"], "interests": ["Technology & Computers"], "skills": ["Problem solving", "Data & Analysis"], "env": ["Office-based", "Technical / Lab work"], "course": "BSc Computer Security / IT"},
    {"name": "Pilot", "track": "STEM", "desc": "Fly passenger, cargo and charter aircraft.",
     "subjects": ["Mathematics", "Physics", "English"], "interests": ["Engineering & Building"], "skills": ["Leading & Organizing", "Problem solving"], "env": ["A mix of different environments"], "course": "Commercial Pilot Licence (flight school) / BSc Aviation"},
    {"name": "Accountant", "track": "Social Sciences", "desc": "Keep financial records, audit accounts and advise on tax.",
     "subjects": ["Mathematics", "Business Studies", "English"], "interests": ["Business & Finance"], "skills": ["Data & Analysis", "Leading & Organizing"], "env": ["Office-based"], "course": "Bachelor of Commerce (Accounting) + CPA"},
    {"name": "Psychologist", "track": "Social Sciences", "desc": "Help people with mental health, learning and behaviour.",
     "subjects": ["Biology", "English", "CRE"], "interests": ["Health & Medicine", "Education & Teaching"], "skills": ["Communication & Writing", "Data & Analysis"], "env": ["Working directly with people"], "course": "BA / BSc Psychology"},
    {"name": "Hotel & Tourism Manager", "track": "Social Sciences", "desc": "Run hotels, lodges and tour companies, from the coast to the Mara.",
     "subjects": ["Business Studies", "Geography", "English", "Home Science"], "interests": ["Business & Finance"], "skills": ["Leading & Organizing", "Communication & Writing"], "env": ["Working directly with people", "A mix of different environments"], "course": "BSc Hospitality & Tourism Management"},
    {"name": "Environmental Scientist", "track": "STEM", "desc": "Study climate, water and land and protect natural resources.",
     "subjects": ["Geography", "Biology", "Chemistry"], "interests": ["Agriculture & Environment"], "skills": ["Data & Analysis", "Problem solving"], "env": ["Outdoor / Field work", "Technical / Lab work"], "course": "BSc Environmental Science"},
    {"name": "Musician / Sound Producer", "track": "Arts & Sports", "desc": "Perform, compose and produce music for streaming, film and live shows.",
     "subjects": ["Music", "English", "Computer Studies"], "interests": ["Arts & Design", "Media & Communication"], "skills": ["Creativity & Design"], "env": ["Creative studio work"], "course": "Bachelor of Music / Diploma in Sound Engineering"},
    {"name": "Sports Coach", "track": "Arts & Sports", "desc": "Train athletes and teams and manage fitness programmes.",
     "subjects": ["Physical Education", "Biology", "English"], "interests": ["Education & Teaching"], "skills": ["Leading & Organizing", "Communication & Writing"], "env": ["Outdoor / Field work", "Working directly with people"], "course": "BSc Sports Science"},
    {"name": "Film & Theatre Director", "track": "Arts & Sports", "desc": "Direct stories for stage, TV and film.",
     "subjects": ["Drama & Theatre", "Literature in English", "English"], "interests": ["Arts & Design", "Media & Communication"], "skills": ["Creativity & Design", "Leading & Organizing"], "env": ["Creative studio work", "A mix of different environments"], "course": "BA Film & Theatre"},
]

# Indicative details. Pay is an approximate starting-to-mid monthly range in KES; verify with employers.
DETAILS = {
    "Software Engineer": ("60,000 - 250,000", "4 yrs", ["University of Nairobi", "JKUAT", "Strathmore", "Moi University"], "Writes and tests code, fixes bugs and builds features with a team."),
    "Doctor": ("100,000 - 400,000", "6 yrs + internship", ["University of Nairobi", "Moi University", "Kenyatta University", "Maseno University"], "Examines patients, orders tests and plans treatment in hospitals and clinics."),
    "Civil Engineer": ("70,000 - 250,000", "5 yrs", ["University of Nairobi", "JKUAT", "Technical University of Kenya", "Dedan Kimathi University"], "Surveys sites, designs structures and supervises construction."),
    "Data Scientist": ("80,000 - 300,000", "4 yrs", ["University of Nairobi", "Strathmore", "JKUAT", "Kenyatta University"], "Cleans data, builds models and presents findings to decision makers."),
    "Agricultural Scientist": ("50,000 - 180,000", "4 yrs", ["Egerton University", "University of Nairobi", "JKUAT", "Moi University"], "Runs field trials and advises farmers on seeds, soil and pests."),
    "Nurse": ("45,000 - 150,000", "4 yrs", ["University of Nairobi", "Kenyatta University", "Moi University", "KMTC (diploma route)"], "Gives patient care, administers medicine and educates families."),
    "Lawyer": ("60,000 - 350,000", "4 yrs + Kenya School of Law", ["University of Nairobi", "Strathmore", "Moi University", "Kenyatta University"], "Researches the law, drafts documents and represents clients in court."),
    "Business Entrepreneur": ("Varies with the business", "3-4 yrs (optional)", ["Strathmore", "University of Nairobi", "Kenyatta University", "KCA University"], "Spots a need, builds the product, finds customers and manages cash."),
    "Teacher": ("40,000 - 120,000", "4 yrs", ["Kenyatta University", "Moi University", "Maseno University", "Egerton University"], "Plans lessons, teaches and assesses learners and mentors them."),
    "Journalist": ("40,000 - 180,000", "4 yrs", ["University of Nairobi", "Moi University", "Daystar University", "Multimedia University"], "Finds stories, interviews people and publishes across media."),
    "Graphic Designer": ("35,000 - 150,000", "3-4 yrs", ["Multimedia University", "Kenyatta University", "Technical University of Kenya", "Creative Arts colleges"], "Designs logos, posters and social media graphics for clients."),
    "Pharmacist": ("70,000 - 220,000", "5 yrs", ["University of Nairobi", "Kenyatta University", "JKUAT", "Mount Kenya University"], "Dispenses medicine, checks dosages and advises patients."),
    "Electrical Engineer": ("60,000 - 220,000", "5 yrs", ["University of Nairobi", "JKUAT", "Technical University of Kenya", "Moi University"], "Designs circuits and power systems and maintains the electricity grid."),
    "Architect": ("60,000 - 250,000", "5 yrs", ["University of Nairobi", "Jomo Kenyatta University", "Technical University of Kenya", "Strathmore"], "Sketches and models buildings and coordinates with engineers."),
    "Veterinarian": ("60,000 - 200,000", "5 yrs", ["University of Nairobi", "Egerton University", "Jomo Kenyatta University"], "Treats sick animals, vaccinates herds and inspects food safety."),
    "Cybersecurity Analyst": ("70,000 - 250,000", "4 yrs", ["Strathmore", "JKUAT", "University of Nairobi", "Kenyatta University"], "Monitors networks, tests defences and responds to attacks."),
    "Pilot": ("150,000 - 800,000", "1-2 yrs flight school", ["Kenya School of Flying", "East African School of Aviation", "Moi University (aviation)"], "Plans routes, checks aircraft and flies passengers or cargo."),
    "Accountant": ("45,000 - 200,000", "4 yrs + CPA", ["University of Nairobi", "Kenyatta University", "Strathmore", "KCA University"], "Prepares financial statements, audits and files taxes."),
    "Psychologist": ("45,000 - 160,000", "4 yrs + postgraduate", ["University of Nairobi", "Kenyatta University", "Daystar University", "USIU-Africa"], "Counsels clients, assesses needs and runs support programmes."),
    "Hotel & Tourism Manager": ("45,000 - 180,000", "4 yrs", ["Kenyatta University", "Moi University", "Maseno University", "Utalii College (diploma route)"], "Oversees guests, staff, bookings and budgets."),
    "Environmental Scientist": ("50,000 - 180,000", "4 yrs", ["University of Nairobi", "Kenyatta University", "Egerton University", "Maseno University"], "Measures pollution, studies ecosystems and advises on policy."),
    "Musician / Sound Producer": ("Varies with gigs and streams", "3-4 yrs (or training)", ["Kenyatta University", "Daystar University", "Kenya Conservatoire of Music"], "Writes, records and performs music and mixes tracks."),
    "Sports Coach": ("35,000 - 140,000", "4 yrs", ["Kenyatta University", "Moi University", "Maseno University"], "Plans training, studies performance and manages athlete fitness."),
    "Film & Theatre Director": ("Varies with projects", "3-4 yrs", ["Kenyatta University", "Daystar University", "Kenya Film School"], "Leads actors and crew from script to screen or stage."),
}
for c in CAREERS:
    pay, years, unis, daily = DETAILS[c["name"]]
    c.update(pay=pay, years=years, unis=unis, daily=daily)
    if c["course"] not in TRACKS[c["track"]]["courses"]:
        TRACKS[c["track"]]["courses"].append(c["course"])

CORE = ["English", "Kiswahili", "Mathematics", "CSL"]   # compulsory: 4 subjects
ELECTIVES = {   # learners choose 3 more, making 7 subjects in total
    "STEM": ["Physics", "Chemistry", "Biology", "Computer Studies", "Agriculture", "Electricity & Power", "Home Science", "Technical Drawing"],
    "Social Sciences": ["Business Studies", "Home Science", "Geography", "History", "CRE", "Literature in English", "French", "German", "Arabic"],
    "Arts & Sports": ["Music", "Fine Art", "Physical Education", "Drama & Theatre", "Literature in English"],
}
for _k, _v in ELECTIVES.items():
    TRACKS[_k]["electives"] = _v


# Each career lists the 3 electives that go with the 4 core subjects (7 in total).
# Every elective must belong to the career's own pathway.
CAREER_ELECTIVES = {
    "Software Engineer": ["Computer Studies", "Physics", "Electricity & Power"],
    "Doctor": ["Biology", "Chemistry", "Physics"],
    "Civil Engineer": ["Physics", "Chemistry", "Technical Drawing"],
    "Data Scientist": ["Computer Studies", "Physics", "Chemistry"],
    "Agricultural Scientist": ["Agriculture", "Biology", "Chemistry"],
    "Nurse": ["Biology", "Chemistry", "Home Science"],
    "Lawyer": ["History", "CRE", "Literature in English"],
    "Business Entrepreneur": ["Business Studies", "Geography", "French"],
    "Teacher": ["Literature in English", "Geography", "History"],
    "Journalist": ["Literature in English", "History", "Geography"],
    "Graphic Designer": ["Fine Art", "Literature in English", "Drama & Theatre"],
    "Pharmacist": ["Chemistry", "Biology", "Computer Studies"],
    "Electrical Engineer": ["Physics", "Electricity & Power", "Computer Studies"],
    "Architect": ["Physics", "Technical Drawing", "Computer Studies"],
    "Veterinarian": ["Biology", "Chemistry", "Agriculture"],
    "Cybersecurity Analyst": ["Computer Studies", "Physics", "Electricity & Power"],
    "Pilot": ["Physics", "Computer Studies", "Electricity & Power"],
    "Accountant": ["Business Studies", "Geography", "History"],
    "Psychologist": ["CRE", "History", "Literature in English"],
    "Hotel & Tourism Manager": ["Business Studies", "Geography", "Home Science"],
    "Environmental Scientist": ["Biology", "Agriculture", "Physics"],
    "Musician / Sound Producer": ["Music", "Literature in English", "Drama & Theatre"],
    "Sports Coach": ["Physical Education", "Drama & Theatre", "Literature in English"],
    "Film & Theatre Director": ["Drama & Theatre", "Literature in English", "Music"],
}
_names = {s["name"] for s in SUBJECTS}
for c in CAREERS:
    els = CAREER_ELECTIVES[c["name"]]
    assert len(els) == 3 and all(e in TRACKS[c["track"]]["electives"] and e in _names for e in els), c["name"]
    c["subjects"] = els


# More careers: (name, track, description, 3 electives, interests, skills, work environments, course, pay KES/month, study time, where to study, a typical day)
_MORE = [
    ("Mechanical Engineer", "STEM", "Design and maintain engines, machines and factory equipment.", ["Physics", "Technical Drawing", "Chemistry"], ["Engineering & Building"], ["Problem solving", "Building & Making Things"], ["Technical / Lab work", "Outdoor / Field work"], "BSc Mechanical Engineering", "65,000 - 230,000", "5 yrs", ["University of Nairobi", "JKUAT", "Technical University of Kenya", "Moi University"], "Designs parts, tests machines and supervises repairs and production."),
    ("Land Surveyor", "STEM", "Measure and map land for building, farming and property ownership.", ["Physics", "Technical Drawing", "Computer Studies"], ["Engineering & Building"], ["Data & Analysis", "Building & Making Things"], ["Outdoor / Field work"], "BSc Geospatial / Land Surveying", "55,000 - 200,000", "5 yrs", ["University of Nairobi", "JKUAT", "Technical University of Kenya", "Kenya Institute of Surveying and Mapping"], "Measures plots with GPS and total stations and prepares survey plans."),
    ("Renewable Energy Technician", "STEM", "Install and maintain solar, wind and geothermal power systems.", ["Electricity & Power", "Physics", "Technical Drawing"], ["Engineering & Building", "Agriculture & Environment"], ["Building & Making Things", "Problem solving"], ["Outdoor / Field work", "Technical / Lab work"], "BSc Renewable Energy / TVET Diploma in Electrical Engineering", "40,000 - 150,000", "2-4 yrs", ["Dedan Kimathi University", "JKUAT", "Technical University of Mombasa", "TVET colleges"], "Installs panels and inverters and checks that systems run safely."),
    ("Medical Laboratory Technologist", "STEM", "Run tests on blood and tissue that help doctors diagnose disease.", ["Biology", "Chemistry", "Physics"], ["Health & Medicine"], ["Data & Analysis", "Problem solving"], ["Technical / Lab work"], "BSc Medical Laboratory Science", "45,000 - 150,000", "4 yrs", ["KMTC", "University of Nairobi", "Kenyatta University", "Moi University"], "Prepares samples, runs lab tests and reports accurate results."),
    ("Nutritionist & Dietitian", "STEM", "Plan healthy diets for patients, schools and communities.", ["Chemistry", "Biology", "Home Science"], ["Health & Medicine"], ["Communication & Writing", "Data & Analysis"], ["Working directly with people", "A mix of different environments"], "BSc Nutrition & Dietetics", "40,000 - 140,000", "4 yrs", ["Kenyatta University", "JKUAT", "Egerton University", "Maseno University"], "Assesses nutrition needs, designs meal plans and teaches families."),
    ("Dentist", "STEM", "Care for teeth and gums and treat mouth disease.", ["Biology", "Chemistry", "Physics"], ["Health & Medicine"], ["Problem solving", "Building & Making Things"], ["Working directly with people", "Technical / Lab work"], "Bachelor of Dental Surgery", "100,000 - 350,000", "5 yrs + internship", ["University of Nairobi", "Moi University"], "Examines patients, fills and extracts teeth and fits dental appliances."),
    ("Diplomat", "Social Sciences", "Represent Kenya abroad and negotiate with other countries.", ["History", "Geography", "French"], ["Law & Justice", "Media & Communication"], ["Communication & Writing", "Leading & Organizing"], ["Office-based", "A mix of different environments"], "BA International Relations", "80,000 - 300,000", "4 yrs", ["University of Nairobi", "USIU-Africa", "Kenyatta University", "Foreign Service Institute (training)"], "Writes reports, attends talks and builds ties with other governments."),
    ("Economist", "Social Sciences", "Study how money, trade and policy shape the economy.", ["Business Studies", "Geography", "History"], ["Business & Finance"], ["Data & Analysis", "Problem solving"], ["Office-based"], "BA / BSc Economics", "60,000 - 250,000", "4 yrs", ["University of Nairobi", "Kenyatta University", "Strathmore", "Moi University"], "Analyses data, models trends and advises governments and companies."),
    ("Social Worker", "Social Sciences", "Support families and communities facing hardship.", ["CRE", "History", "Home Science"], ["Education & Teaching", "Health & Medicine"], ["Communication & Writing", "Leading & Organizing"], ["Working directly with people"], "BA Social Work", "35,000 - 120,000", "4 yrs", ["University of Nairobi", "Kenyatta University", "Moi University", "Maseno University"], "Visits families, assesses needs and links people to services."),
    ("Human Resource Manager", "Social Sciences", "Recruit, train and look after the people in an organisation.", ["Business Studies", "CRE", "Literature in English"], ["Business & Finance"], ["Communication & Writing", "Leading & Organizing"], ["Office-based", "Working directly with people"], "BCom Human Resource Management", "60,000 - 250,000", "4 yrs", ["Kenyatta University", "JKUAT", "University of Nairobi", "Mount Kenya University"], "Hires staff, handles payroll and settles workplace issues."),
    ("Translator & Interpreter", "Social Sciences", "Turn speech and writing from one language into another.", ["French", "German", "Literature in English"], ["Media & Communication"], ["Communication & Writing"], ["Office-based", "A mix of different environments"], "BA Linguistics / Translation", "40,000 - 180,000", "4 yrs", ["Kenyatta University", "University of Nairobi", "Moi University", "Alliance Fran\u00e7aise (language training)"], "Translates documents and interprets at meetings and courts."),
    ("Marketing Manager", "Social Sciences", "Plan campaigns that help a brand reach and keep customers.", ["Business Studies", "Literature in English", "Geography"], ["Business & Finance", "Media & Communication"], ["Creativity & Design", "Communication & Writing"], ["Office-based", "A mix of different environments"], "BCom Marketing", "60,000 - 250,000", "4 yrs", ["Strathmore", "University of Nairobi", "Kenyatta University", "USIU-Africa"], "Studies customers, plans adverts and tracks sales results."),
    ("Fashion Designer", "Arts & Sports", "Design clothing and accessories, from sketch to finished garment.", ["Fine Art", "Literature in English", "Drama & Theatre"], ["Arts & Design"], ["Creativity & Design", "Building & Making Things"], ["Creative studio work"], "BA Fashion Design / Diploma in Fashion", "30,000 - 150,000", "2-4 yrs", ["Technical University of Kenya", "Kenyatta University", "Creative arts colleges"], "Sketches designs, picks fabric and oversees sewing."),
    ("Professional Athlete", "Arts & Sports", "Compete in sport at club, national or international level.", ["Physical Education", "Literature in English", "Music"], ["Education & Teaching"], ["Leading & Organizing"], ["Outdoor / Field work"], "BSc Sports Science (alongside training)", "Varies with contracts and prizes", "Training from school age", ["Kenyatta University", "Moi University", "Sports academies and clubs"], "Trains daily, recovers, studies tactics and competes."),
    ("TV & Radio Presenter", "Arts & Sports", "Host shows and bring news and entertainment to audiences.", ["Drama & Theatre", "Literature in English", "Music"], ["Media & Communication", "Arts & Design"], ["Communication & Writing", "Creativity & Design"], ["Creative studio work", "A mix of different environments"], "BA Journalism & Media / Diploma in Broadcasting", "35,000 - 200,000", "3-4 yrs", ["Kenyatta University", "Daystar University", "Multimedia University", "Moi University"], "Prepares scripts, interviews guests and presents live."),
]
for (_n, _t, _d, _sub, _int, _sk, _env, _course, _pay, _yrs, _unis, _daily) in _MORE:
    assert len(_sub) == 3 and all(e in TRACKS[_t]["electives"] for e in _sub), _n
    CAREERS.append({"name": _n, "track": _t, "desc": _d, "subjects": _sub, "interests": _int, "skills": _sk, "env": _env,
                    "course": _course, "pay": _pay, "years": _yrs, "unis": _unis, "daily": _daily})
    if _course not in TRACKS[_t]["courses"]:
        TRACKS[_t]["courses"].append(_course)


_MORE2 = [
    ("Geologist", "STEM", "Study rocks, minerals and the earth to find water, oil and metals.", ["Physics", "Chemistry", "Technical Drawing"], ["Agriculture & Environment", "Engineering & Building"], ["Data & Analysis", "Problem solving"], ["Outdoor / Field work", "Technical / Lab work"], "BSc Geology", "55,000 - 200,000", "4 yrs", ["University of Nairobi", "Kenyatta University", "Taita Taveta University", "Moi University"], "Collects rock samples in the field and analyses them in the lab."),
    ("Meteorologist", "STEM", "Forecast weather and climate to protect farmers, pilots and cities.", ["Physics", "Computer Studies", "Technical Drawing"], ["Agriculture & Environment", "Technology & Computers"], ["Data & Analysis", "Problem solving"], ["Office-based", "Technical / Lab work"], "BSc Meteorology", "50,000 - 180,000", "4 yrs", ["University of Nairobi", "Kenya Meteorological Training Institute"], "Reads satellite and radar data and issues forecasts and warnings."),
    ("Marine Biologist", "STEM", "Study ocean life and help protect fisheries and coral reefs.", ["Biology", "Chemistry", "Agriculture"], ["Agriculture & Environment"], ["Data & Analysis", "Problem solving"], ["Outdoor / Field work", "Technical / Lab work"], "BSc Marine Science / Fisheries", "45,000 - 160,000", "4 yrs", ["Pwani University", "Technical University of Mombasa", "University of Nairobi", "Maseno University"], "Dives and samples water, counts species and writes research reports."),
    ("Biotechnologist", "STEM", "Use living cells to make medicines, better crops and clean fuels.", ["Biology", "Chemistry", "Computer Studies"], ["Health & Medicine", "Agriculture & Environment"], ["Data & Analysis", "Problem solving"], ["Technical / Lab work"], "BSc Biotechnology", "55,000 - 220,000", "4 yrs", ["JKUAT", "Kenyatta University", "University of Nairobi", "Egerton University"], "Runs lab experiments on DNA, enzymes and microbes."),
    ("Chemist", "STEM", "Test and develop materials, medicines and food products.", ["Chemistry", "Physics", "Biology"], ["Health & Medicine", "Engineering & Building"], ["Data & Analysis", "Problem solving"], ["Technical / Lab work"], "BSc Chemistry / Industrial Chemistry", "50,000 - 180,000", "4 yrs", ["University of Nairobi", "JKUAT", "Kenyatta University", "Egerton University"], "Mixes and analyses compounds and checks product quality."),
    ("Physicist", "STEM", "Explore energy, matter and forces, from electronics to space.", ["Physics", "Computer Studies", "Electricity & Power"], ["Technology & Computers", "Engineering & Building"], ["Problem solving", "Data & Analysis"], ["Technical / Lab work", "Office-based"], "BSc Physics", "50,000 - 200,000", "4 yrs", ["University of Nairobi", "Kenyatta University", "Egerton University", "Maseno University"], "Builds models, runs experiments and analyses measurements."),
    ("Wildlife Conservationist", "STEM", "Protect animals and habitats in parks and conservancies.", ["Biology", "Agriculture", "Chemistry"], ["Agriculture & Environment"], ["Leading & Organizing", "Data & Analysis"], ["Outdoor / Field work"], "BSc Wildlife Management", "40,000 - 150,000", "4 yrs", ["Moi University", "Egerton University", "University of Nairobi", "KWS Training Institute (Naivasha)"], "Tracks animals, patrols parks and works with local communities."),
    ("Forensic Scientist", "STEM", "Analyse evidence from crime scenes to help courts decide cases.", ["Chemistry", "Biology", "Physics"], ["Law & Justice", "Health & Medicine"], ["Data & Analysis", "Problem solving"], ["Technical / Lab work"], "BSc Forensic Science", "50,000 - 180,000", "4 yrs", ["Kenyatta University", "University of Nairobi", "Mount Kenya University"], "Examines DNA, fingerprints and chemicals and writes court reports."),
    ("Biomedical Engineer", "STEM", "Design medical devices such as scanners, prosthetics and monitors.", ["Physics", "Biology", "Electricity & Power"], ["Health & Medicine", "Engineering & Building"], ["Problem solving", "Building & Making Things"], ["Technical / Lab work"], "BSc Biomedical Engineering", "60,000 - 220,000", "5 yrs", ["JKUAT", "University of Nairobi", "Kenyatta University"], "Designs, tests and repairs equipment used in hospitals."),
    ("Robotics Engineer", "STEM", "Build robots and automated machines for farms, factories and homes.", ["Computer Studies", "Physics", "Electricity & Power"], ["Technology & Computers", "Engineering & Building"], ["Problem solving", "Building & Making Things"], ["Technical / Lab work"], "BSc Mechatronics / Robotics Engineering", "70,000 - 250,000", "5 yrs", ["JKUAT", "Dedan Kimathi University", "University of Nairobi", "Strathmore"], "Programs controllers, wires sensors and tests robot movements."),
    ("Aerospace Engineer", "STEM", "Design and maintain aircraft, drones and satellites.", ["Physics", "Technical Drawing", "Computer Studies"], ["Engineering & Building", "Technology & Computers"], ["Problem solving", "Building & Making Things"], ["Technical / Lab work"], "BSc Aerospace / Aeronautical Engineering", "80,000 - 300,000", "5 yrs", ["University of Nairobi", "Moi University", "JKUAT", "Study abroad options"], "Models airflow, designs parts and tests flight systems."),
    ("Mining Engineer", "STEM", "Plan safe ways to extract minerals, from quarries to deep mines.", ["Physics", "Chemistry", "Technical Drawing"], ["Engineering & Building"], ["Problem solving", "Leading & Organizing"], ["Outdoor / Field work"], "BSc Mining & Mineral Processing Engineering", "70,000 - 250,000", "5 yrs", ["Taita Taveta University", "Technical University of Kenya", "University of Nairobi"], "Plans excavation, checks safety and manages mine crews."),
    ("Air Traffic Controller", "STEM", "Guide aircraft safely through the sky and on the ground.", ["Physics", "Computer Studies", "Electricity & Power"], ["Technology & Computers"], ["Problem solving", "Leading & Organizing"], ["Office-based", "Technical / Lab work"], "Diploma / Certificate in Air Traffic Services", "90,000 - 300,000", "2-3 yrs", ["East African School of Aviation", "Kenya Civil Aviation Authority training"], "Tracks flights on radar and gives pilots clear instructions."),
    ("Physiotherapist", "STEM", "Help patients recover movement after injury, illness or surgery.", ["Biology", "Chemistry", "Physics"], ["Health & Medicine"], ["Communication & Writing", "Problem solving"], ["Working directly with people"], "BSc Physiotherapy", "50,000 - 180,000", "4 yrs", ["University of Nairobi", "Kenyatta University", "Moi University", "KMTC"], "Assesses patients and guides exercises and treatments."),
    ("Food Technologist", "STEM", "Develop and test safe, long-lasting foods and drinks.", ["Chemistry", "Biology", "Home Science"], ["Agriculture & Environment", "Health & Medicine"], ["Data & Analysis", "Creativity & Design"], ["Technical / Lab work"], "BSc Food Science & Technology", "45,000 - 170,000", "4 yrs", ["JKUAT", "University of Nairobi", "Egerton University", "Maseno University"], "Tests recipes, checks hygiene and improves packaging."),
    ("Archaeologist", "Social Sciences", "Dig up and study the remains of past societies.", ["History", "Geography", "CRE"], ["Education & Teaching"], ["Data & Analysis", "Communication & Writing"], ["Outdoor / Field work"], "BA Archaeology / Heritage Studies", "40,000 - 140,000", "4 yrs", ["University of Nairobi", "Kenyatta University", "Moi University", "National Museums of Kenya (training)"], "Excavates sites, records finds and writes reports."),
    ("Urban Planner", "Social Sciences", "Plan how towns grow: housing, roads, parks and services.", ["Geography", "Business Studies", "History"], ["Engineering & Building", "Agriculture & Environment"], ["Data & Analysis", "Leading & Organizing"], ["Office-based", "Outdoor / Field work"], "BA / BSc Urban & Regional Planning", "55,000 - 200,000", "4-5 yrs", ["University of Nairobi", "Technical University of Kenya", "Maseno University", "JKUAT"], "Studies land use, drafts plans and consults communities."),
    ("Public Administrator", "Social Sciences", "Run government offices and carry out public policy.", ["History", "Geography", "Business Studies"], ["Law & Justice", "Business & Finance"], ["Leading & Organizing", "Communication & Writing"], ["Office-based"], "BA Public Administration", "50,000 - 200,000", "4 yrs", ["University of Nairobi", "Kenyatta University", "Moi University", "Kenya School of Government (training)"], "Implements policy, manages budgets and serves citizens."),
    ("Librarian & Archivist", "Social Sciences", "Organise books, records and digital archives so people can find them.", ["Literature in English", "History", "CRE"], ["Education & Teaching", "Media & Communication"], ["Data & Analysis", "Communication & Writing"], ["Office-based"], "BSc Information Science / Library Studies", "35,000 - 120,000", "4 yrs", ["Kenyatta University", "Moi University", "University of Nairobi", "Technical University of Kenya"], "Catalogues collections, helps researchers and preserves records."),
    ("Animator", "Arts & Sports", "Bring characters and stories to life in cartoons, games and adverts.", ["Fine Art", "Drama & Theatre", "Music"], ["Arts & Design", "Technology & Computers"], ["Creativity & Design"], ["Creative studio work"], "BSc / Diploma in Animation & Multimedia", "35,000 - 160,000", "2-4 yrs", ["Multimedia University", "Kenyatta University", "Technical University of Kenya"], "Draws frames, rigs characters and edits movement and sound."),
    ("Cinematographer", "Arts & Sports", "Shoot the images for films, series and music videos.", ["Drama & Theatre", "Fine Art", "Music"], ["Arts & Design", "Media & Communication"], ["Creativity & Design", "Building & Making Things"], ["Creative studio work", "A mix of different environments"], "BA Film & Television Production", "35,000 - 180,000", "3-4 yrs", ["Kenya Film School", "Multimedia University", "Kenyatta University", "Daystar University"], "Plans shots, sets lights and operates cameras on location."),
    ("Choreographer", "Arts & Sports", "Create and teach dance for stage, film and events.", ["Music", "Drama & Theatre", "Physical Education"], ["Arts & Design"], ["Creativity & Design", "Leading & Organizing"], ["Creative studio work"], "BA Dance / Performing Arts", "30,000 - 130,000", "3-4 yrs", ["Kenyatta University", "Daystar University", "Kenya Conservatoire of Music"], "Designs routines, rehearses dancers and stages performances."),
    ("Photographer", "Arts & Sports", "Capture images for news, weddings, brands and art.", ["Fine Art", "Literature in English", "Drama & Theatre"], ["Arts & Design", "Media & Communication"], ["Creativity & Design"], ["Creative studio work", "A mix of different environments"], "Diploma / BA in Photography & Media", "25,000 - 150,000", "2-4 yrs", ["Multimedia University", "Kenyatta University", "Technical University of Kenya"], "Shoots on location or in a studio and edits the final images."),
]
for (_n, _t, _d, _sub, _int, _sk, _env, _course, _pay, _yrs, _unis, _daily) in _MORE2:
    assert len(_sub) == 3 and all(e in TRACKS[_t]["electives"] for e in _sub), _n
    assert _n not in {c["name"] for c in CAREERS}, _n
    CAREERS.append({"name": _n, "track": _t, "desc": _d, "subjects": _sub, "interests": _int, "skills": _sk, "env": _env,
                    "course": _course, "pay": _pay, "years": _yrs, "unis": _unis, "daily": _daily})
    if _course not in TRACKS[_t]["courses"]:
        TRACKS[_t]["courses"].append(_course)


import re
EL = {"Ph": "Physics", "Ch": "Chemistry", "Bi": "Biology", "Cs": "Computer Studies", "Ag": "Agriculture", "Ep": "Electricity & Power",
      "Hs": "Home Science", "Td": "Technical Drawing", "Bs": "Business Studies", "Gg": "Geography", "Hi": "History", "Cr": "CRE",
      "Li": "Literature in English", "Fr": "French", "Mu": "Music", "Fa": "Fine Art", "Pe": "Physical Education", "Dr": "Drama & Theatre"}
INT = {"T": "Technology & Computers", "H": "Health & Medicine", "E": "Engineering & Building", "B": "Business & Finance", "L": "Law & Justice",
       "M": "Media & Communication", "A": "Agriculture & Environment", "D": "Education & Teaching", "Z": "Arts & Design"}
TRK = {"S": "STEM", "O": "Social Sciences", "A": "Arts & Sports"}
BASE = {"T": (["Problem solving", "Data & Analysis"], ["Office-based"]),
        "H": (["Problem solving", "Communication & Writing"], ["Working directly with people", "Technical / Lab work"]),
        "E": (["Building & Making Things", "Problem solving"], ["Outdoor / Field work", "Technical / Lab work"]),
        "B": (["Leading & Organizing", "Data & Analysis"], ["Office-based"]),
        "L": (["Communication & Writing", "Data & Analysis"], ["Office-based", "Working directly with people"]),
        "M": (["Communication & Writing", "Creativity & Design"], ["Creative studio work", "A mix of different environments"]),
        "A": (["Data & Analysis", "Problem solving"], ["Outdoor / Field work"]),
        "D": (["Communication & Writing", "Leading & Organizing"], ["Working directly with people"]),
        "Z": (["Creativity & Design"], ["Creative studio work"])}
# Name|track|3 electives|interest|course|study time|description  (pay and institutions: check official sources)
_COMPACT = """
Network Engineer|S|Cs,Ph,Ep|T|BSc Computer Networks / IT|4 yrs|Sets up and maintains computer networks for companies and campuses.
Web Developer|S|Cs,Ph,Ep|T|BSc Information Technology|4 yrs|Builds and updates websites and web apps.
Mobile App Developer|S|Cs,Ph,Ep|T|BSc Computer Science|4 yrs|Creates apps for Android and iPhone, including mobile money tools.
Game Developer|S|Cs,Ph,Ep|T|BSc Computer Science / Game Design|4 yrs|Programs and designs video games.
AI Engineer|S|Cs,Ph,Ch|T|BSc Computer Science / Data Science|4 yrs|Trains models that recognise images, speech and patterns.
Database Administrator|S|Cs,Ph,Ep|T|BSc Information Technology|4 yrs|Keeps company data organised, secure and backed up.
IT Support Specialist|S|Cs,Ph,Ep|T|Diploma in Information Technology|2-3 yrs|Fixes computers, networks and software problems for users.
Cloud Engineer|S|Cs,Ph,Ep|T|BSc Computer Science + cloud certification|4 yrs|Runs company systems on cloud platforms.
Telecommunications Engineer|S|Ep,Ph,Cs|E|BSc Telecommunications Engineering|5 yrs|Designs and maintains mobile, fibre and radio networks.
Electronics Technician|S|Ep,Ph,Td|E|Diploma in Electrical & Electronic Engineering|2-3 yrs|Repairs and tests electronic equipment.
Electrician|S|Ep,Ph,Td|E|TVET Certificate in Electrical Installation|1-2 yrs|Wires buildings and fixes electrical faults.
Welder & Fabricator|S|Td,Ph,Ep|E|TVET Certificate in Welding & Fabrication|1-2 yrs|Joins and shapes metal for buildings, vehicles and machines.
Motor Vehicle Mechanic|S|Ph,Ep,Td|E|TVET Diploma in Motor Vehicle Technology|2-3 yrs|Diagnoses and repairs cars, trucks and motorbikes.
Automotive Engineer|S|Ph,Td,Ep|E|BSc Mechanical / Automotive Engineering|5 yrs|Designs and tests vehicles and engines.
Chemical Engineer|S|Ch,Ph,Td|E|BSc Chemical Engineering|5 yrs|Designs plants that make fuels, foods, fertilisers and medicines.
Petroleum Engineer|S|Ph,Ch,Td|E|BSc Petroleum Engineering|5 yrs|Plans how to find and produce oil and gas safely.
Water Engineer|S|Ph,Ch,Td|E|BSc Water & Environmental Engineering|5 yrs|Designs systems that supply clean water and treat waste.
Structural Engineer|S|Ph,Td,Cs|E|BSc Civil Engineering|5 yrs|Calculates loads so bridges and buildings stay standing.
Quantity Surveyor|S|Ph,Td,Cs|E|BSc Quantity Surveying|4 yrs|Estimates and controls the cost of building projects.
Construction Manager|S|Ph,Td,Cs|E|BSc Construction Management|4 yrs|Runs building sites, crews, budgets and schedules.
Agronomist|S|Ag,Bi,Ch|A|BSc Agronomy / Crop Science|4 yrs|Advises on seeds, soil and methods to raise crop yields.
Horticulturist|S|Ag,Bi,Hs|A|BSc Horticulture|4 yrs|Grows fruit, vegetables and flowers, including for export.
Animal Scientist|S|Ag,Bi,Ch|A|BSc Animal Science|4 yrs|Improves feeding and breeding of livestock.
Soil Scientist|S|Ag,Ch,Bi|A|BSc Soil Science|4 yrs|Tests soil and recommends fertilisers and land care.
Agricultural Engineer|S|Ag,Ph,Td|E|BSc Agricultural Engineering|5 yrs|Designs irrigation, machines and storage for farms.
Forester|S|Ag,Bi,Ch|A|BSc Forestry|4 yrs|Manages forests and tree planting and fights illegal logging.
Fisheries Officer|S|Bi,Ag,Ch|A|BSc Fisheries & Aquaculture|4 yrs|Supports fish farming and protects lakes and ocean stocks.
Public Health Officer|S|Bi,Ch,Hs|H|BSc Environmental Health / Public Health|4 yrs|Prevents disease through sanitation, vaccination and education.
Clinical Officer|S|Bi,Ch,Ph|H|Diploma / BSc Clinical Medicine|3-4 yrs|Diagnoses and treats common illnesses in clinics and hospitals.
Radiographer|S|Ph,Bi,Ch|H|BSc Medical Imaging|4 yrs|Takes X-ray, CT and ultrasound images for diagnosis.
Optometrist|S|Ph,Bi,Ch|H|BSc Optometry|4 yrs|Tests eyesight and prescribes glasses and eye care.
Midwife|S|Bi,Ch,Hs|H|BSc Nursing (Midwifery)|4 yrs|Cares for mothers and babies before, during and after birth.
Occupational Therapist|S|Bi,Ch,Hs|H|BSc Occupational Therapy|4 yrs|Helps people regain daily skills after injury or illness.
Epidemiologist|S|Bi,Ch,Cs|H|BSc Public Health + MSc Epidemiology|4 yrs + masters|Tracks how diseases spread and how to stop them.
Microbiologist|S|Bi,Ch,Ag|H|BSc Microbiology|4 yrs|Studies bacteria, viruses and fungi in labs.
Geneticist|S|Bi,Ch,Cs|H|BSc Genetics / Biotechnology|4 yrs|Studies genes to understand inheritance and disease.
Astronomer|S|Ph,Cs,Ep|T|BSc Physics / Astronomy|4 yrs + masters|Studies stars, planets and space data.
Statistician|S|Cs,Ph,Ch|T|BSc Statistics|4 yrs|Collects and analyses data to guide decisions.
Pharmacy Technologist|S|Ch,Bi,Cs|H|Diploma in Pharmaceutical Technology|3 yrs|Prepares and dispenses medicines under a pharmacist.
Animal Health Technician|S|Bi,Ag,Ch|A|Diploma in Animal Health|2-3 yrs|Vaccinates and treats farm animals.
Judge / Magistrate|O|Hi,Cr,Li|L|Bachelor of Laws (LLB) + years of practice|4 yrs + practice|Hears cases and gives fair rulings.
Human Rights Officer|O|Hi,Cr,Gg|L|BA Human Rights / LLB|4 yrs|Documents abuses and defends people's rights.
Police Officer|O|Hi,Gg,Cr|L|National Police Service recruit training|1-2 yrs|Keeps order, prevents crime and investigates cases.
Customs Officer|O|Bs,Gg,Hi|L|Degree in Commerce or Customs (KRA training)|4 yrs|Checks goods at borders and collects duties.
Banker|O|Bs,Gg,Hi|B|BCom Finance / Banking|4 yrs|Serves customers and manages loans and savings.
Financial Analyst|O|Bs,Gg,Hi|B|BCom Finance + CFA|4 yrs|Studies markets and companies to guide investment.
Auditor|O|Bs,Gg,Hi|B|BCom Accounting + CPA|4 yrs|Checks that accounts are accurate and honest.
Actuary|O|Bs,Gg,Hi|B|BSc Actuarial Science|4 yrs|Uses maths to price insurance and pension risk.
Procurement Officer|O|Bs,Gg,Hi|B|BCom Procurement & Logistics|4 yrs|Buys goods and services and manages suppliers.
Supply Chain Manager|O|Bs,Gg,Hi|B|BCom Supply Chain Management|4 yrs|Plans how goods move from factory to customer.
Real Estate Agent|O|Bs,Gg,Hi|B|Diploma / BA Real Estate|2-4 yrs|Sells and rents property and advises on land.
Event Planner|O|Bs,Hs,Li|B|Diploma / BA Events Management|2-4 yrs|Plans weddings, conferences and festivals.
Chef|O|Hs,Bs,Gg|B|Diploma in Culinary Arts|2-3 yrs|Creates menus and runs a professional kitchen.
Tour Guide|O|Gg,Hi,Fr|B|Diploma in Tourism & Travel|2-3 yrs|Leads visitors through parks, towns and cultural sites.
Cabin Crew|O|Gg,Fr,Hs|B|Certificate / Diploma in Aviation Cabin Crew|1-2 yrs|Looks after passenger safety and comfort on flights.
Public Relations Officer|O|Li,Bs,Hi|M|BA Public Relations / Communication|4 yrs|Manages an organisation's image and media relations.
Copywriter|O|Li,Bs,Hi|M|BA Communication / Journalism|3-4 yrs|Writes adverts, slogans and web content.
Editor & Publisher|O|Li,Hi,Cr|M|BA Literature / Publishing|4 yrs|Prepares books, magazines and news for publication.
University Lecturer|O|Li,Hi,Gg|D|Bachelor's, Master's and PhD|8+ yrs|Teaches and researches at a university.
Education Counsellor|O|Cr,Hi,Li|D|BEd Guidance & Counselling|4 yrs|Guides students on learning, wellbeing and careers.
Early Childhood Educator|O|Hs,Cr,Li|D|Diploma / BEd Early Childhood Education|2-4 yrs|Teaches and cares for young children.
Special Needs Teacher|O|Cr,Hs,Li|D|BEd Special Needs Education|4 yrs|Teaches learners with disabilities and learning needs.
Community Development Officer|O|Gg,Cr,Hi|D|BA Community Development|4 yrs|Helps communities plan and run local projects.
NGO Programme Manager|O|Gg,Bs,Cr|B|BA Development Studies / Project Management|4 yrs|Runs aid and development projects.
Clergy / Pastor|O|Cr,Hi,Li|D|Theology degree or diploma|3-4 yrs|Leads worship and guides and counsels a congregation.
Sociologist|O|Hi,Gg,Cr|D|BA Sociology|4 yrs|Studies how groups and societies work.
Political Scientist|O|Hi,Gg,Li|L|BA Political Science|4 yrs|Studies government, elections and policy.
Historian|O|Hi,Gg,Li|D|BA History|4 yrs|Researches and explains the past.
Interior Designer|A|Fa,Li,Dr|Z|BA Interior Design|4 yrs|Plans colour, furniture and layout for homes and offices.
Illustrator|A|Fa,Li,Dr|Z|BA Fine Art / Design|3-4 yrs|Draws images for books, magazines and brands.
Fine Artist|A|Fa,Li,Mu|Z|BA Fine Art|4 yrs|Creates paintings and sculptures for galleries and clients.
Actor|A|Dr,Li,Mu|Z|BA Theatre & Film / Acting|3-4 yrs|Performs on stage, TV and film.
Scriptwriter|A|Li,Dr,Fa|M|BA Film / Creative Writing|3-4 yrs|Writes scripts for TV, film and radio.
Author|A|Li,Dr,Mu|M|BA Literature / Creative Writing|3-4 yrs|Writes novels, poems and non-fiction.
Singer|A|Mu,Dr,Li|Z|Diploma / BA Music|2-4 yrs|Performs and records songs.
DJ & Music Producer|A|Mu,Dr,Li|Z|Diploma in Music Production|1-3 yrs|Mixes, produces and plays music for events and radio.
Dancer|A|Pe,Mu,Dr|Z|Diploma / BA Dance|2-4 yrs|Performs dance on stage, TV and at events.
Fitness Trainer|A|Pe,Li,Mu|D|Certificate / Diploma in Fitness & Sports Science|1-3 yrs|Designs workouts and coaches clients.
Sports Journalist|A|Li,Pe,Dr|M|BA Journalism|4 yrs|Reports on matches and athletes.
Sports Agent|A|Pe,Li,Dr|B|BA / BCom Sports Management|3-4 yrs|Negotiates contracts and manages athletes' careers.
Video Editor|A|Fa,Dr,Mu|M|Diploma / BA Film & Television|2-4 yrs|Cuts footage into films, adverts and shows.
Makeup Artist|A|Fa,Dr,Li|Z|Certificate / Diploma in Cosmetology|1-2 yrs|Does makeup for weddings, film and fashion.
"""
_names = {c["name"] for c in CAREERS}
for _line in _COMPACT.strip().splitlines():
    n, t, e, i, course, yrs, desc = _line.split("|")
    t, subs = TRK[t], [EL[x] for x in e.split(",")]
    assert n not in _names and len(subs) == 3 and all(s in TRACKS[t]["electives"] for s in subs), n
    _names.add(n)
    sk, env = BASE[i]
    CAREERS.append({"name": n, "track": t, "desc": desc, "subjects": subs, "interests": [INT[i]], "skills": sk, "env": env,
                    "course": course, "pay": "Varies. Check with employers", "years": yrs,
                    "unis": ["Search this course on KUCCPS (kuccps.net) or CUE (cue.or.ke)"], "daily": desc})
    if course not in TRACKS[t]["courses"]:
        TRACKS[t]["courses"].append(course)
for c in CAREERS:
    nums = [int(x) for x in re.findall(r"\d+", c["years"])]
    if nums:
        c["ymin"], c["ymax"] = min(nums), max(nums)

STUDY = ["Up to 2 years (certificate or diploma)", "3 to 4 years (a degree)", "5 years or more (long professional degree)", "Not sure yet"]
VALUES = {
    "Helping people": {"interests": ["Health & Medicine", "Education & Teaching", "Law & Justice"], "skills": ["Communication & Writing"]},
    "Earning a high income": {"interests": ["Business & Finance", "Technology & Computers", "Engineering & Building", "Health & Medicine"], "skills": []},
    "Being creative": {"interests": ["Arts & Design", "Media & Communication"], "skills": ["Creativity & Design"]},
    "Job security": {"interests": ["Health & Medicine", "Education & Teaching", "Engineering & Building"], "skills": []},
    "Adventure and travel": {"interests": ["Agriculture & Environment", "Media & Communication"], "skills": []},
    "Leading others": {"interests": [], "skills": ["Leading & Organizing"]},
    "Making discoveries": {"interests": ["Technology & Computers", "Agriculture & Environment"], "skills": ["Data & Analysis", "Problem solving"]},
    "Protecting nature": {"interests": ["Agriculture & Environment"], "skills": []},
}
STYLES = {
    "On my own": {"env": ["Office-based", "Creative studio work", "Technical / Lab work"], "skills": ["Data & Analysis"]},
    "In a small team": {"env": ["A mix of different environments", "Technical / Lab work"], "skills": ["Problem solving"]},
    "Leading a big team": {"env": ["A mix of different environments"], "skills": ["Leading & Organizing"]},
    "With the public": {"env": ["Working directly with people"], "skills": ["Communication & Writing"]},
}
PROBLEMS = {
    "Improve health and wellbeing": ["Health & Medicine"],
    "Feed people and protect the environment": ["Agriculture & Environment"],
    "Build roads, homes and energy systems": ["Engineering & Building"],
    "Make technology useful for everyone": ["Technology & Computers"],
    "Create fairness and justice": ["Law & Justice"],
    "Grow businesses and create jobs": ["Business & Finance"],
    "Tell stories and inspire people": ["Media & Communication", "Arts & Design"],
    "Teach and guide young people": ["Education & Teaching"],
}


# ---- Official CBC senior school subjects (KICD Grade 10 curriculum design). Each subject belongs to ONE pathway. ----
_OFFICIAL = [
 ("Compulsory (everyone)", "core", [
  ("English", "Reading, writing, speaking and listening in English."),
  ("Kiswahili / Kenya Sign Language (KSL)", "Kenya's national language, or Kenya Sign Language."),
  ("Community Service Learning (CSL)", "A practical project that serves your community.")]),
 ("Mathematics (by pathway)", "maths", [
  ("Core Mathematics", "Compulsory for STEM learners. Abstract, analytical mathematics: algebra, geometry, calculus-related ideas and modelling. Prepares for medicine, engineering, architecture, computer science and actuarial science."),
  ("Essential Mathematics", "Compulsory for Social Sciences, Arts & Sports Science and other non-STEM learners. Practical numeracy, financial literacy, data and statistics, and applied geometry for business, law, journalism, social work and the arts.")]),
 ("STEM", "STEM", [
  ("Advanced Mathematics", "Deeper algebra, calculus and statistics."),
  ("Biology", "Living things, health and the environment."),
  ("Chemistry", "Matter, reactions and materials."),
  ("Physics", "Energy, forces and how the physical world works."),
  ("Computer Studies", "Programming, data and digital systems."),
  ("Agriculture", "Crops, livestock and food systems."),
  ("Home Science", "Food, nutrition, textiles and home management."),
  ("Drawing and Design", "Technical drawing and design of objects and buildings."),
  ("Aviation Technology", "Aircraft, flight and airport systems."),
  ("Building and Construction", "Building methods, materials and site work."),
  ("Electrical Technology", "Wiring, circuits and electrical systems."),
  ("Metal Technology", "Working and joining metal."),
  ("Power Mechanics", "Engines, vehicles and machines."),
  ("Wood Technology", "Carpentry, joinery and furniture."),
  ("Marine and Fisheries Technology", "Fishing, boats and aquatic resources.")]),
 ("Social Sciences", "Social Sciences", [
  ("Business Studies", "How businesses start, run and grow."),
  ("History and Citizenship", "How the past shapes society and your role as a citizen."),
  ("Geography", "People, places and the environment."),
  ("Religious Education (CRE / IRE / HRE)", "Christian, Islamic or Hindu religious education."),
  ("Advanced English", "A deeper course in language and writing."),
  ("Literature in English", "Novels, plays and poetry."),
  ("Indigenous Language", "Study of a Kenyan mother tongue."),
  ("Kiswahili Kipevu", "An advanced course in Kiswahili."),
  ("Fasihi ya Kiswahili", "Kiswahili literature."),
  ("Arabic", "Arabic language and culture."),
  ("French", "French language for trade and diplomacy."),
  ("German", "German language for study and work in Europe."),
  ("Mandarin Chinese", "Chinese language for trade and travel."),
  ("Sign Language", "Communication through sign language.")]),
 ("Arts & Sports Science", "Arts & Sports", [
  ("Music and Dance", "Performance, composition and movement."),
  ("Theatre and Film", "Acting, directing and film making."),
  ("Fine Arts", "Drawing, painting and visual design."),
  ("Sports and Recreation", "Sport science, coaching and recreation."),
  ("Physical Education", "Sport, fitness and the science of movement.")]),
]
SUPPORT = ["Physical Education / Physical Health", "ICT Skills", "Pastoral Programme of Instruction (or Religious Instruction)"]
SUBJECTS = [{"name": n, "cat": cat, "core": tag == "core", "desc": d, "tags": [] if tag in ("core", "maths") else [tag]}
            for cat, tag, items in _OFFICIAL for n, d in items]
CORE = [s["name"] for s in SUBJECTS if s["core"]]
MATHS = ["Core Mathematics", "Essential Mathematics"]
for _k in TRACKS:
    TRACKS[_k]["electives"] = [s["name"] for s in SUBJECTS if _k in s["tags"]]
    TRACKS[_k]["subjects"] = TRACKS[_k]["electives"]

_OLD2NEW = {"Technical Drawing": "Drawing and Design", "Electricity & Power": "Electrical Technology", "Music": "Music and Dance",
            "Drama & Theatre": "Theatre and Film", "Fine Art": "Fine Arts",
            "CRE": "Religious Education (CRE / IRE / HRE)", "History": "History and Citizenship"}
_MATHY = {"Accountant", "Economist", "Actuary", "Banker", "Financial Analyst", "Auditor", "Procurement Officer", "Supply Chain Manager"}
_valid = {s["name"] for s in SUBJECTS}
for c in CAREERS:
    subs = []
    for s in (_OLD2NEW.get(x, x) for x in c["subjects"]):
        if s not in subs:
            subs.append(s)
    own = set(TRACKS[c["track"]]["electives"])
    assert len(subs) == 3 and len(set(subs)) == 3 and all(s in _valid for s in subs), (c["name"], subs)
    assert sum(s in own for s in subs) >= 2, (c["name"], subs)   # at least 2 of the 3 electives from the career's own pathway
    c["subjects"] = subs


# Well-known people in each field (examples only; written from general knowledge, so verify before publishing widely).
_P = {
    "Professional Athlete": [("Eliud Kipchoge", "Olympic marathon champion"), ("David Rudisha", "Olympic 800 m champion"), ("Faith Kipyegon", "Olympic 1500 m champion"), ("Catherine Ndereba", "marathon world champion")],
    "Sports Coach": [("Patrick Sang", "coach of Eliud Kipchoge")],
    "Environmental Scientist": [("Wangari Maathai", "Nobel Peace Prize winner, Green Belt Movement")],
    "Wildlife Conservationist": [("Richard Leakey", "conservationist, former head of KWS"), ("Paula Kahumbu", "CEO of WildlifeDirect")],
    "Archaeologist": [("Louis Leakey", "archaeologist and palaeontologist"), ("Richard Leakey", "palaeoanthropologist")],
    "Actor": [("Lupita Nyong'o", "Oscar-winning actress")],
    "Film & Theatre Director": [("Wanuri Kahiu", "filmmaker, director of Rafiki")],
    "Author": [("Ng\u0169g\u0129 wa Thiong'o", "novelist and professor"), ("Binyavanga Wainaina", "writer, Caine Prize winner")],
    "Software Engineer": [("Juliana Rotich", "co-founder of Ushahidi and BRCK")],
    "Business Entrepreneur": [("Tabitha Karanja", "founder of Keroche Breweries"), ("James Mwangi", "CEO of Equity Group"), ("Juliana Rotich", "tech entrepreneur")],
    "Pilot": [("Irene Koki Mutungi", "first African woman to captain a Boeing 787")],
    "Banker": [("James Mwangi", "CEO of Equity Group")],
    "Agricultural Scientist": [("Calestous Juma", "Harvard professor of international development")],
    "Biotechnologist": [("Florence Wambugu", "plant pathologist and biotechnology advocate")],
    "Nutritionist & Dietitian": [("Ruth Oniang'o", "professor and nutrition and food-security leader")],
    "Public Health Officer": [("Miriam Were", "public health expert")],
    "Economist": [("Njuguna Ndung'u", "economist, former Central Bank governor"), ("David Ndii", "economist and public commentator")],
    "Diplomat": [("Amina Mohamed", "diplomat and former Cabinet Secretary"), ("Macharia Kamau", "diplomat, former ambassador to the UN")],
    "Judge / Magistrate": [("David Maraga", "former Chief Justice"), ("Willy Mutunga", "former Chief Justice")],
    "Lawyer": [("Martha Karua", "lawyer and politician"), ("Willy Mutunga", "lawyer, former Chief Justice")],
    "Human Rights Officer": [("Maina Kiai", "lawyer and human rights activist")],
    "Journalist": [("Larry Madowo", "international correspondent"), ("Julie Gichuru", "journalist and TV presenter")],
    "TV & Radio Presenter": [("Jeff Koinange", "TV journalist and host"), ("Julie Gichuru", "journalist and TV presenter"), ("Maina Kageni", "radio presenter")],
    "Musician / Sound Producer": [("Sauti Sol", "Kenyan band"), ("Eric Wainaina", "singer-songwriter")],
    "Singer": [("Sauti Sol", "Kenyan band"), ("Eric Wainaina", "singer-songwriter")],
    "Fine Artist": [("Wangechi Mutu", "artist known for collage and sculpture")],
}
_have = {c["name"] for c in CAREERS}
for _n, _l in _P.items():
    assert _n in _have, _n
for c in CAREERS:
    c["people"] = [{"name": a, "note": b} for a, b in _P.get(c["name"], [])]


# International universities (example options by field; check each one's entry rules, fees and visa requirements).
def _u(*pairs):
    return [{"name": n, "country": c} for n, c in pairs]
_INTL_FIELD = {
    "Technology & Computers": _u(("Carnegie Mellon University Africa", "Rwanda"), ("University of Cape Town", "South Africa"), ("ETH Zurich", "Switzerland"), ("Imperial College London", "UK"), ("Massachusetts Institute of Technology (MIT)", "USA")),
    "Engineering & Building": _u(("University of Cape Town", "South Africa"), ("University of the Witwatersrand", "South Africa"), ("ETH Zurich", "Switzerland"), ("Imperial College London", "UK"), ("Technical University of Munich", "Germany")),
    "Health & Medicine": _u(("Makerere University", "Uganda"), ("University of Cape Town", "South Africa"), ("University of Oxford", "UK"), ("Johns Hopkins University", "USA"), ("Karolinska Institutet", "Sweden")),
    "Business & Finance": _u(("University of Cape Town", "South Africa"), ("University of the Witwatersrand", "South Africa"), ("London School of Economics", "UK"), ("University of Pennsylvania (Wharton)", "USA"), ("Erasmus University Rotterdam", "Netherlands")),
    "Law & Justice": _u(("University of Cape Town", "South Africa"), ("University of the Witwatersrand", "South Africa"), ("University of Oxford", "UK"), ("University of Cambridge", "UK"), ("Harvard Law School (postgraduate)", "USA")),
    "Media & Communication": _u(("Rhodes University", "South Africa"), ("University of the Witwatersrand", "South Africa"), ("University of the Arts London", "UK"), ("University of Westminster", "UK"), ("New York University", "USA")),
    "Agriculture & Environment": _u(("Wageningen University", "Netherlands"), ("Makerere University", "Uganda"), ("Stellenbosch University", "South Africa"), ("University of California, Davis", "USA"), ("ETH Zurich", "Switzerland")),
    "Education & Teaching": _u(("University of Cape Town", "South Africa"), ("Makerere University", "Uganda"), ("University College London", "UK"), ("University of Edinburgh", "UK"), ("University of Melbourne", "Australia")),
    "Arts & Design": _u(("University of the Arts London", "UK"), ("Royal College of Art", "UK"), ("Parsons School of Design", "USA"), ("University of Cape Town (Michaelis School of Fine Art)", "South Africa")),
}
_AVIATION = _u(("Embry-Riddle Aeronautical University", "USA"), ("Cranfield University", "UK"), ("Delft University of Technology", "Netherlands"), ("University of the Witwatersrand", "South Africa"))
_HOSPITALITY = _u(("\u00c9cole h\u00f4teli\u00e8re de Lausanne", "Switzerland"), ("Glion Institute of Higher Education", "Switzerland"), ("Hong Kong Polytechnic University", "Hong Kong"))
_SPORT = _u(("Loughborough University", "UK"), ("Deakin University", "Australia"), ("University of Cape Town", "South Africa"), ("Stellenbosch University", "South Africa"))
_MINING = _u(("Colorado School of Mines", "USA"), ("University of the Witwatersrand", "South Africa"), ("Heriot-Watt University", "UK"), ("Imperial College London", "UK"))
_MUSIC = _u(("Berklee College of Music", "USA"), ("Royal Academy of Music", "UK"), ("University of Cape Town (South African College of Music)", "South Africa"))
_FILM = _u(("National Film and Television School", "UK"), ("NYU Tisch School of the Arts", "USA"), ("AFDA", "South Africa"))
_ARCH = _u(("The Bartlett, University College London", "UK"), ("ETH Zurich", "Switzerland"), ("University of Cape Town", "South Africa"), ("Delft University of Technology", "Netherlands"))
_MARINE = _u(("James Cook University", "Australia"), ("University of Cape Town", "South Africa"), ("Wageningen University", "Netherlands"))
_POLICY = _u(("Sciences Po", "France"), ("Georgetown University", "USA"), ("London School of Economics", "UK"), ("University of Cape Town", "South Africa"))
_VET = _u(("Royal Veterinary College", "UK"), ("University of Pretoria", "South Africa"), ("Utrecht University", "Netherlands"))
_FASHION = _u(("Central Saint Martins", "UK"), ("Parsons School of Design", "USA"), ("University of the Arts London", "UK"))
_OVR = {}
for _names, _lst in [
    (["Pilot", "Aerospace Engineer", "Air Traffic Controller"], _AVIATION),
    (["Hotel & Tourism Manager", "Chef", "Event Planner", "Tour Guide", "Cabin Crew"], _HOSPITALITY),
    (["Sports Coach", "Professional Athlete", "Fitness Trainer", "Sports Agent"], _SPORT),
    (["Mining Engineer", "Geologist", "Petroleum Engineer"], _MINING),
    (["Musician / Sound Producer", "Singer", "DJ & Music Producer"], _MUSIC),
    (["Film & Theatre Director", "Cinematographer", "Actor", "Scriptwriter", "Video Editor", "Animator"], _FILM),
    (["Architect", "Urban Planner"], _ARCH),
    (["Marine Biologist", "Fisheries Officer"], _MARINE),
    (["Diplomat", "Political Scientist", "Public Administrator"], _POLICY),
    (["Veterinarian", "Animal Health Technician"], _VET),
    (["Fashion Designer"], _FASHION),
]:
    for _n in _names:
        _OVR[_n] = _lst
_have = {c["name"] for c in CAREERS}
assert all(n in _have for n in _OVR)
for c in CAREERS:
    c["intl"] = _OVR.get(c["name"]) or _INTL_FIELD[c["interests"][0]]

INTERESTS = ["Technology & Computers", "Health & Medicine", "Engineering & Building", "Business & Finance",
             "Law & Justice", "Media & Communication", "Agriculture & Environment", "Education & Teaching", "Arts & Design"]
SKILLS = ["Problem solving", "Communication & Writing", "Creativity & Design", "Data & Analysis",
          "Building & Making Things", "Leading & Organizing"]
ENVS = ["Office-based", "Outdoor / Field work", "Creative studio work", "Technical / Lab work",
        "Working directly with people", "A mix of different environments"]


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/data")
def data():
    return jsonify(support=SUPPORT, maths=MATHS, study=STUDY, values=VALUES, styles=STYLES, problems=PROBLEMS, core=CORE, subjects=SUBJECTS, careers=CAREERS, tracks=TRACKS,
                   interests=INTERESTS, skills=SKILLS, envs=ENVS)


@app.post("/api/assess")
def assess():
    a = request.get_json(force=True) or {}
    enjoy, strong = set(a.get("enjoy", [])), set(a.get("strong", []))
    interests, skills = set(a.get("interests", [])), set(a.get("skills", []))
    considering, env = set(a.get("careers", [])), a.get("env", "")

    ranked = []
    for c in CAREERS:
        s = sum(1 for x in c["subjects"] if x in enjoy) + sum(2 for x in c["subjects"] if x in strong)
        s += 3 * sum(1 for x in c["interests"] if x in interests)
        s += sum(1 for x in c["skills"] if x in skills)
        s += 4 if c["name"] in considering else 0
        s += 2 if env in c["env"] else 0
        ci, cs, ce = set(c["interests"]), set(c["skills"]), set(c["env"])
        vs = sum(1 for v in a.get("values", []) if v in VALUES and (ci & set(VALUES[v]["interests"]) or cs & set(VALUES[v]["skills"])))
        s += min(2, vs)
        st = STYLES.get(a.get("style", ""))
        if st and (ce & set(st["env"]) or cs & set(st["skills"])):
            s += 1
        pm = {i for pr in a.get("problems", []) for i in PROBLEMS.get(pr, [])}
        if ci & pm:
            s += 3
        sd = a.get("study", "")
        if c.get("ymin") is not None:
            if sd.startswith("Up to 2") and c["ymin"] <= 2: s += 2
            elif sd.startswith("3 to 4") and c["ymin"] <= 4 and c["ymax"] >= 3: s += 2
            elif sd.startswith("5 years") and c["ymax"] >= 5: s += 2
        best = 3 * len(c["subjects"]) + 3 * len(c["interests"]) + len(c["skills"]) + 6 + 8
        ranked.append({**c, "score": min(100, round(s / best * 100 * 1.6))})
    ranked.sort(key=lambda c: c["score"], reverse=True)

    track_scores = {}
    for c in ranked:
        track_scores[c["track"]] = track_scores.get(c["track"], 0) + c["score"]
    top_track = max(track_scores, key=track_scores.get)

    liked = enjoy | strong
    # Electives are chosen to serve the learner's best-matching careers in the winning pathway.
    weight = {}
    for c in [c for c in ranked if c["track"] == top_track][:3]:
        for e in c["subjects"]:
            if e not in MATHS:
                weight[e] = weight.get(e, 0) + c["score"] + (5 if e in strong else 0) + (2 if e in enjoy else 0)
    electives = sorted(weight, key=lambda e: -weight[e])[:3]
    for e in TRACKS[top_track]["electives"]:
        if len(electives) < 3 and e not in electives:
            electives.append(e)
    maths = "Core Mathematics" if top_track == "STEM" else "Essential Mathematics"
    subjects = [CORE[0], CORE[1], maths, CORE[2]] + electives
    return jsonify(track=top_track, track_info=TRACKS[top_track], careers=ranked[:5],
                   subjects=subjects, liked=sorted(liked))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
