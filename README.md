# Next Shift
 
Next Shift is a handoff tool for home health nurses. You leave report for the next nurse and it gets sorted so the most urgent data shows up first.
 
## Why I made it
 
I'm an LPN working in home health. My patient has a different nurse at night and we don't usually see each other, so report tends to get passed through the family. This could mean inaccurate or even missed clinical information. I wanted a way to leave and read report that is more accurate and efficient.
 
## What it does
 
You log in and the app finds your shift for the day and takes you to your patient. You can only see and give report for the patients you're assigned to.
 
Report covers things that you want the next shift to know quickly without having to sift through pages of nursing notes. It includes things like vent and tube feed tolerance, PRN medications given, medication refills needed, nutrition, elimination, out-of-range vitals, skin issues, DME problems, new orders, things to pass on to the doctor, ADLs, and incidents. Items are color-coded by urgency so you can scan it quickly and prioritize tasks. If there isn't a shift report from the previous shift, you'll see an alert that one wasn't done for that shift and be able to view the last report that was left with the date and time. You can add to already submitted reports before logging out, but the report locks after session logout to protect data integrity.
 
## Built with
 
- Python
- Django
- Bootstrap
- SQLite

## Setup

1. Clone the repo and open project folder
```
   git clone https://github.com/Jeanie-Walker/SDEV_220_Final_Project_Jeanie_Walker.git
   cd SDEV_220_Final_Project_Jeanie_Walker
```
2. Create and activate virtual environment
```
   python3 -m venv .venv
   source .venv/bin/activate
```
3. Install the requirements
```
   pip install -r requirements.txt
```
4. Set up the database and load demo data
```
   python manage.py migrate
   python manage.py seed_demo
```
5. Run server and open locally
```
   python manage.py runserver
```

## Using demo

- Select a nurse and a day. The day stands in for today's date. 
- Not every nurse works every day, so if a nurse is off, the no shift page is displayed. 
- Each patient starts with a report from Sunday night. 
- Reload the seed data at any time to reset the demo data
```
  python manage.py seed_demo
```

## Demo schedule

| Patient | Mon day | Mon night | Tue day | Tue night | Wed day | Wed night |
|---|---|---|---|---|---|---|
| Linda Williams | Francis Smith | Gail Robinson | Francis Smith | Alex Walls | Francis Smith | Alex Walls |
| Sherry Banks | Pilar Flores | Samantha Couch | Pilar Flores | Amanda Richards | Samantha Couch | Amanda Richards |
| Bethany Carter | Whitni Tailor | Ayesha Johnson | Whitni Tailor | Gail Robinson | Ayesha Johnson | Gail Robinson |

**Days off:** Mon: Alex Walls, Amanda Richards · Tue: Samantha Couch, Ayesha Johnson · Wed: Pilar Flores, Whitni Tailor

To test a handoff, log in as Francis Smith on Mon and save a report for Linda Williams. Log out, then log in as Gail Robinson on Mon to see it. If you log in as Gail first, you'll see the missed report alert instead.