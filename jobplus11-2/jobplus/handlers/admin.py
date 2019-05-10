from flask import Blueprint,render_template, redirect, url_for, flash,session,request,current_app
from flask_login import login_user,logout_user,login_required
from jobplus.models import User,Company,Message,Job
from jobplus.forms import EmessageForm,MessageForm,AdduserForm,AddcompanyForm
from jobplus.decorators import euser_requeired,user_requeired,admin_requeired,login_timeat

admin = Blueprint('admin', __name__,url_prefix='/admin')


@admin.route('/emessage',methods=['GET','POST'])
@euser_requeired
@login_timeat
def emessage():
    company=Company.query.get(int(session.get('user_id')))
    form = EmessageForm(obj=company)
    if form.validate_on_submit():
        if form.password.data is "":
            pass
        else:
            user=User.query.get(int(session.get('user_id')))
            user.up_password(form.password.data)
            flash('密码修改成功')
        form.create_emessage(session.get('user_id'))
        flash('企业信息设置成功')
        return redirect(url_for('front.index'))
    else:
        flash('企业信息设置失败')
    return render_template('admin/emessage.html',form=form,usersname='编辑企业信息')

@admin.route('/message',methods=['GET','POST'])
@user_requeired
@login_timeat
def message():
    message=Message.query.get(int(session.get('user_id')))
    form = MessageForm(obj=message)
    if form.validate_on_submit():
        if form.password.data is "":
            pass
        else:
            user=User.query.get(int(session.get('user_id')))
            user.up_password(form.password.data)
            flash('密码修改成功')
        form.create_message(session.get('user_id'))
        flash('个人信息设置成功')
        return redirect(url_for('front.index'))
    else:
        flash('个人信息设置失败')
    return render_template('admin/emessage.html',form=form,usersname='编辑求职者信息')

@admin.route('/')
@admin_requeired
@login_timeat
def index():
    print('aaaaaaaaaaa')
    return render_template('admin/admin_base.html',**locals())

@admin.route('/users')
@admin_requeired
@login_timeat
def users():
    page = request.args.get('page',default=1,type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    print(pagination.items)
    return render_template('admin/users.html',pagination=pagination)


@admin.route('/users/adduser',methods=['GET','POST'])
@admin_requeired
@login_timeat
def adduser():
    form = AdduserForm()
    if form.validate_on_submit():
        form_user=form.create_user()
        if form_user == 1:
            flash('帐号创建成功')
            return redirect(url_for('admin.users'))
        elif form_user == 0:
            flash('邮箱帐号已经存在')

    return render_template('admin/adduser.html',**locals())


@admin.route('/users/addcompany',methods=['GET','POST'])
@admin_requeired
@login_timeat
def addcompany():
    form = AddcompanyForm()
    if form.validate_on_submit():
        form_user=form.create_user()
        if form_user == 1:
            flash('帐号创建成功')
       #     return redirect(url_for('admin.users'))
        elif form_user == 0:
            flash('邮箱帐号已经存在')

    return render_template('admin/addcompany.html',**locals())

@admin.route('/users/state')
@admin_requeired
@login_timeat
def state():
    page = request.args.get('page',default=1,type=int)
    email = request.args.get('email')
    state = request.args.get('state')
    print(state)
    print(type(state))
    if state == "启用":
        state = "禁用"
    else:
        state = "启用"
    users = User.query.filter_by(email=email).first()
    users.upstates(state)

    return redirect(url_for('admin.users',page=page))


@admin.route('/users/edituser',methods=['GET','POST'])
@admin_requeired
@login_timeat
def edituser():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    form = AdduserForm(obj=user)
    if form.validate_on_submit():
        form.up_user()
        flash("修改成功")
        return redirect(url_for('admin.users'))
    else:
        form.username.data=user.messages[0].username
        form.phone.data=user.messages[0].phone
  
        return render_template('admin/edituser.html',form=form)

@admin.route('/users/editcompany',methods=['GET','POST'])
@admin_requeired
@login_timeat
def editcompany():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    form = AddcompanyForm(obj=user)
    if form.validate_on_submit():
        form.up_user()
        flash("修改成功")
        return redirect(url_for('admin.users'))
    else:

        form.eusername.data=user.companys[0].eusername
        form.company_url.data=user.companys[0].company_url
        form.company_des.data=user.companys[0].company_des
        return render_template('admin/editcompany.html',form=form)



@admin.route('/users/jobs')
@admin_requeired
@login_timeat
def jobs():
    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    print(pagination.items)
    return render_template('admin/jobs.html',pagination=pagination)


@admin.route('/job/<int:job_id>/enable')
@admin_requeired
@login_timeat
def jobs_state(job_id):
    page = request.args.get('page',default=1,type=int)
    state = request.args.get('state')
    print(state)
    print(type(state))
    if state == "上线":
        state = "下线"
    else:
        state = "上线"
    job = Job.query.filter_by(id=job_id).first()
    job.upstates(state)

    return redirect(url_for('admin.jobs',page=page))



@admin.route('/job/<int:job_id>/disable')
@euser_requeired
@login_timeat
def jobs_states(job_id):
    page = request.args.get('page',default=1,type=int)
    state = request.args.get('state')
    print(state)
    print(type(state))
    if state == "上线":
        state = "下线"
    else:
        state = "上线"
    job = Job.query.filter_by(id=job_id).first()
    job.upstates(state)

    return redirect(url_for('job.euseradmin',page=page))


