from flask import Blueprint,render_template, redirect, url_for, flash
from flask_login import login_user,logout_user,login_required
from jobplus.models import User,Job,Company
from jobplus.forms import LoginForm,RegisterForm
from jobplus.decorators import euser_requeired,user_requeired,admin_requeired,login_timeat
front = Blueprint('front', __name__)


@front.route('/')
@login_timeat
def index():
    page = 1
    jobs = Job.query.order_by(-Job.id).paginate(
        page=page,
        per_page=8,
        error_out=False
    )
    companys = Company.query.order_by(-Company.id).paginate(
        page=page,
        per_page=8,
        error_out=False
    )
    flash('欢迎光临七天招聘网','success')
    return render_template('index.html',**locals())

@front.route('/login',methods=['GET','POST'])
@login_timeat
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            if user.state == '禁用':
                flash('Sorry,用户被封号，请联系管理员')
                return redirect(url_for('front.login'))
            else:
                login_user(user,form.remember_me.data)
                return redirect(url_for('front.index'))
        else:
            flash('Sorry,用户名或者密码错误')

    return render_template('front/login.html',form=form)
    
@front.route('/userregister',methods=['GET','POST'])
@login_timeat
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not User.query.filter_by(email=form.email.data).first() and not User.query.filter_by(email=form.name.data).first():
            form.create_user()
            flash('注册成功','success')
            return redirect(url_for('front.login'))
        else:
            flash('注册失败','success')
    return render_template('front/register.html',form=form,usersname="求职者注册")

@front.route('/companyregister',methods=['GET','POST'])
@login_timeat
def eregister():
    form = RegisterForm()
    if form.validate_on_submit():
        if not User.query.filter_by(email=form.email.data).first() and not User.query.filter_by(email=form.name.data).first():
            form.ecreate_user()
            flash('注册成功','success')
            return redirect(url_for('front.login'))
        else:
            flash('注册失败','success')
    return render_template('front/register.html',form=form,usersname="企业注册")



@front.route('/logout')
@login_required
@login_timeat
def logout():
    logout_user()
    flash('退出登录，欢迎你的下次光临')
    return redirect(url_for('front.index'))


