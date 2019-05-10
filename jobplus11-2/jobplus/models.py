from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

class User(Base,UserMixin):
    __tablename__ = 'user'
    logindated_at = db.Column(db.DateTime, default=datetime.utcnow)
    ADMIN_ROLE = '30'
    USER_ROLE = '10'
    EUSER_ROLE = '20'
    USER_STATE = '启用'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True,index=True)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    _password =	db.Column(db.String(255),nullable=False)
    state = db.Column(db.String(32), default=USER_STATE)
    role = db.Column(db.SmallInteger, default=USER_ROLE)
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, row_password):
        self._password = generate_password_hash(row_password)



    def check_password(self, row_password):
        result = check_password_hash(self._password,row_password)
        return result
    def upstates(self,state):
        self.state=state
        db.session.add(self)
        db.session.commit()
    def up_password(self,password):
        self._password = generate_password_hash(password)
        db.session.add(self)
        db.session.commit()

    def login_datetime(self):
        self.logindated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    def look_datetime(self):
        seconds_time=(datetime.utcnow()-self.logindated_at).seconds
        if seconds_time <= 60:
            return '已登录'+str(seconds_time)+'秒'
        elif seconds_time <= 3600:
            return '已登录'+str(int(seconds_time/60))+'分钟'
        elif seconds_time <= 86400:
            return '已登录'+str(int(seconds_time/3600))+'小时'
class Company(Base):
    __tablename__ = 'company'
    id = db.Column(db.Integer,db.ForeignKey("user.id"),primary_key=True)
    eusername = db.Column(db.String(32))
    email = db.Column(db.String(32))
    phone =  db.Column(db.String(32))
    slug = db.Column(db.String(32))
    address = db.Column(db.String(32))
    company_url = db.Column(db.String(128))
    logo = db.Column(db.String(150))
    company_des = db.Column(db.String(50))
    company_det = db.Column(db.String(30))
    company_id = db.relationship('User',uselist=False,backref='companys')
    def job_len(self):
        if self.jobs:
            return len(self.jobs)
        else:
            return 0


class Message(Base):
    __tablename__ = 'message'
    id = db.Column(db.Integer,db.ForeignKey("user.id"),primary_key=True)
    username =  db.Column(db.String(32))
    email = db.Column(db.String(32))
    phone =  db.Column(db.String(32))
    worktime = db.Column(db.String(32))
    jianli_url = db.Column(db.String(128))
    message_id = db.relationship('User',uselist=False,backref='messages')
    def Sending_resume(self,job_id):
        jobz=Job.query.filter_by(id=job_id).first()
        print(jobz)
        if jobz in self.Jobm:
            return "你已经投递过了"
        else:
            self.Jobm.append(jobz)
            minjob=Minjob(message_id=self.id,job_id=job_id)
            db.session.add(self)
            db.session.add(minjob)
            db.session.commit()
            return "投递成功"
    def create_time(self,job_id):
        minjob=Minjob.query.filter_by(message_id=self.id,job_id=int(job_id)).first()
        if minjob:
            return minjob.created_at
    def statess(self,job_id):
        minjob=Minjob.query.filter_by(message_id=self.id,job_id=int(job_id)).first()
        if minjob:
            return minjob.state


Rela = db.Table('rela',
        db.Column('message_id',db.Integer,db.ForeignKey('message.id')),
        db.Column('job_id',db.Integer,db.ForeignKey('job.id'))
)
class Job(Base):
    __tablename__ = 'job'
    id = db.Column(db.Integer,primary_key=True)
    jobname =  db.Column(db.String(32))
    wages = db.Column(db.String(32))
    worktime = db.Column(db.String(32))
    work_address = db.Column(db.String(128))
    job_company = db.Column(db.Integer,db.ForeignKey("company.id"))
    describe = db.Column(db.String(128))
    job_des = db.Column(db.String(128))
    job_state = db.Column(db.String(32), default="上线")
    job_state2 = db.Column(db.String(32), default="启用")
    Jobid = db.relationship('Company',uselist=False,backref='jobs')
    message = db.relationship('Message', secondary=Rela, backref='Jobm')
    def upstates(self,state):
        self.job_state=state
        db.session.add(self)
        db.session.commit()
    def upstates2(self):
        self.job_state2='待删除'
        db.session.add(self)
        db.session.commit()



class Minjob(Base):
    __tablename__ = 'minjob'
    id = db.Column(db.Integer,primary_key=True)
    message_id =  db.Column(db.String(32))
    job_id = db.Column(db.String(32))
    state = db.Column(db.String(32), default="未面试")
    def up_state(self,state):
        self.state=state
        db.session.add(self)
        db.session.commit()
