from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,ValidationError, PasswordField,BooleanField
from wtforms.validators import DataRequired,Email, Length,EqualTo,Required,NumberRange,URL
from jobplus.models import User, db, Company, Message,Job
from flask import flash


class LoginForm(FlaskForm):
    email = StringField('邮箱地址',validators=[Required(),Email(),Length(3,30)])
    password = PasswordField('密码',validators=[Required(),Length(3,30)])
    remember_me = BooleanField('记住帐号')
    submit = SubmitField('提交')
    def validate_email(self,field):
        if field.data and not User.query.filter_by(email=field.data).first():
            print("密码错误")
            return ValidationError('邮箱未注册')
    def validate_password(self,field):
        user = User.query.filter_by(email=self.email.data).first()
 
        if  user and not user.check_password(field.data):
            print("密码错误")
            return ValidationError('密码错误')


class RegisterForm(FlaskForm):
    name = StringField('用户名',validators=[Required(),Length(3,30)])
    email = StringField('邮箱地址',validators=[Required(),Email(),Length(3,30)])
    password = PasswordField('密码', validators=[Required(),Length(3,30)])
    repeat_password = PasswordField('重复密码', validators=[Required(),Length(3,30),EqualTo('password')])
    submit = SubmitField('提交')
    def validate_name(self,field):
        if field.data and User.query.filter_by(name=field.data).first():
            print('帐号已经注册')
            return ValidationError('帐号已经注册')
        print('帐号注册成功')
    def validate_email(self,field):
        if field.data and User.query.filter_by(email=field.data).first():
            print('邮箱已经注册')
            return ValidationError('邮箱已经注册')
        print('邮箱注册成功')
    def create_user(self):

        user = User(name=self.name.data,email=self.email.data,password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user
    def ecreate_user(self):
        user = User(name=self.name.data,email=self.email.data,password=self.password.data,role=20)
        db.session.add(user)
        db.session.commit()
        return user
class EmessageForm(FlaskForm):
    eusername =  StringField('企业名称',validators=[Required(),Length(3,30)])
    email = StringField('邮箱地址',validators=[Required(),Email(),Length(3,30)])
    phone =  StringField('手机号码',validators=[Required(),NumberRange(),Length(3,30)])
    password = PasswordField('密码(不填写保持不变)')
    slug = StringField('Slug',validators=[Required(),Length(3,30)])
    address = StringField('地址',validators=[Required(),Length(3,30)])
    company_url = StringField('公司主页',validators=[Required(),URL(),Length(3,30)])
    logo =  StringField('图标',validators=[Required(),Length(3,150)])
    company_des = StringField('公司一句话描述',validators=[Required(),Length(3,50)])
    company_det = StringField('公司详情',validators=[Required(),Length(3,300)])
    submit = SubmitField('提交')
    def create_emessage(self,session_id):
        com = Company.query.get(int(session_id))
        if com:
            self.populate_obj(com)
            db.session.add(com)
            db.session.commit()
        else:
            user=User.query.get(int(session_id))
            company=Company(company_id=user)
            self.populate_obj(company)
            db.session.add(company)
            db.session.commit()

class MessageForm(FlaskForm):
    username =  StringField('姓名',validators=[Required(),Length(1,30)])
    email = StringField('邮箱地址',validators=[Required(),Email(),Length(3,30)])
    phone =  StringField('手机号码',validators=[Required(),NumberRange(),Length(3,30)])
    password = PasswordField('密码(不填写保持不变)')
    worktime = StringField('工作年限(单位年)',validators=[Required(),Length(1,30)])
    jianli_url = StringField('简历链接',validators=[Required(),URL(),Length(3,150)])
    submit = SubmitField('提交')
    def create_message(self,session_id):
        mes = Message.query.get(int(session_id))
        if mes:
            self.populate_obj(mes)
            db.session.add(mes)
            db.session.commit()
        else:
            user=User.query.get(int(session_id))
            message=Message(message_id=user)
            self.populate_obj(message)
            db.session.add(message)
            db.session.commit()    


class AdduserForm(FlaskForm):
    email = StringField('邮箱地址',validators=[Required(),Email(),Length(3,30)])
    password = PasswordField('密码')
    username =  StringField('姓名',validators=[Required(),Length(1,30)])
    phone =  StringField('手机号码',validators=[Required(),NumberRange(),Length(3,30)])
    submit = SubmitField('提交')
    def create_user(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            return 0
        else:
            users = User()
            self.populate_obj(users)
            message = Message(message_id=users)
            self.populate_obj(message)
            db.session.add(users)
            db.session.add(message)
            db.session.commit()    
            return 1
    def up_user(self):
        user = User.query.filter_by(email=self.email.data).first()
        self.populate_obj(user)
        message = Message.query.get(int(user.id))
        self.populate_obj(message)
        db.session.add(user)
        db.session.add(message)
        db.session.commit()
    
class AddcompanyForm(FlaskForm):
    email = StringField('邮箱地址',validators=[Required(),Email(),Length(3,30)])
    password = PasswordField('密码')
    eusername =  StringField('企业名称',validators=[Required(),Length(1,30)])
    company_url =  StringField('企业网站',validators=[Required(),Length(1,30)])
    company_des =  StringField('一句话简介',validators=[Required(),Length(1,30)])
    submit = SubmitField('提交')
    def create_user(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            return 0
        else:
            users = User(role=20)
            self.populate_obj(users)
            company = Company(company_id=users)
            self.populate_obj(company)
            db.session.add(users)
            db.session.add(company)
            db.session.commit()    
            return 1
    def up_user(self):
        user = User.query.filter_by(email=self.email.data).first()
        self.populate_obj(user)
        company = Company.query.get(int(user.id))
        self.populate_obj(company)
        db.session.add(user)
        db.session.add(company)
        db.session.commit()


class JobForm(FlaskForm):
    __tablename__ = 'job'
    jobname =  StringField('工作名称',validators=[Required(),Length(1,30)])
    wages = StringField('工资范围',validators=[Required(),Length(1,30)])
    worktime = StringField('经验要求',validators=[Required(),Length(1,30)])
    work_address = StringField('邮箱地址',validators=[Required(),Length(1,30)])
    describe = StringField('职位简介',validators=[Required(),Length(1,30)])
    job_des =StringField('职位描述',validators=[Required(),Length(1,100)])
    submit = SubmitField('提交')
    def up_job(self,job_id):
        job = Job.query.filter_by(id=job_id).first()
        print(job)
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
    def create_job(self,company_id):
        company=Company.query.filter_by(id=company_id).first()
        job = Job(Jobid=company)
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
