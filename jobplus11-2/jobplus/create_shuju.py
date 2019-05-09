import os
import json
from random import randint
from faker import Faker
from jobplus.models import db,User,Company,Job

fake = Faker()

def iter_users():
    for i in range(100):
        print(i)
        yield User(
            name=fake.user_name(),
            email=fake.safe_email(),
            password=fake.password(),
            role=20
        )



def iter_Company():
    users = User.query
    for user in users:
        print(user)
        if user.role == 30 or user.role == 10:
            continue
        company=Company.query.filter_by(id=user.id).first()
        if company:
            continue
        yield Company(
            eusername=fake.company(),
            email=fake.safe_email(),
            phone = fake.phone_number(),
            address = fake.address(),
            company_url = "https://www.shiyanlou.com/faq/",
            company_des = fake.word(),
            company_det = fake.word(),
            company_id=user
        )

def iter_Job():
    companys = Company.query
    for company in companys:
        print(company)

        yield Job(
            jobname = fake.job(),
            wages = str(fake.random_digit_not_null())+str(fake.random_digit_not_null())+str(fake.random_digit_not_null())+str(fake.random_digit_not_null()),
            worktime = fake.random_digit_not_null(),
            work_address = fake.street_address(),
            Jobid=company
        )


def run():
    for user in iter_users():
        db.session.add(user)

    for company in iter_Company():
        db.session.add(company)


    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def runjob():

    
    for job in iter_Job():
        db.session.add(job)


    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def runstate():
    jobs=Job.query.all()
    
    for job in jobs:
        if job.job_state == "上线":
            pass
        else:
            print(job)
            job.job_state = "上线"
            db.session.add(job)
            db.session.commit()
