from flask import Blueprint,render_template, redirect, url_for, flash,session,request,current_app
from flask_login import login_user,logout_user,login_required,current_user
from jobplus.models import User,Company,Message,Job,Minjob
from jobplus.forms import EmessageForm,MessageForm,AdduserForm,AddcompanyForm,JobForm
from jobplus.decorators import euser_requeired,user_requeired,admin_requeired,user_requeired2,login_timeat

job = Blueprint('job', __name__,url_prefix='/job')


@job.route('/')
@login_timeat
def index():
    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.order_by(-Job.id).paginate(
        page=page,
        per_page=current_app.config['COMPANY_PER_PAGE'],
        error_out=False
    )
    print(pagination.items)
    return render_template('job/job.html',pagination=pagination)


@job.route('/<int:job_id>')
@login_timeat
def job_des(job_id):
    jobs=Job.query.filter_by(id=job_id).first()

    return render_template('job/job_des.html',jobs=jobs)

@job.route('/<int:job_id>/apply')
@user_requeired2
@login_timeat
def resume(job_id):
    print(current_user.messages[0])
    message=current_user.messages[0].Sending_resume(job_id)
    flash(message)
    jobs=Job.query.filter_by(id=job_id).first()

    return  render_template('job/job_des.html',jobs=jobs)



@job.route('/admin')
@euser_requeired
@login_timeat
def euseradmin():
    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.filter_by(job_company=current_user.id).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    print(pagination.items)
    return  render_template('job/admin.html',pagination=pagination)



@job.route('/<int:job_id>/edit',methods=['GET','POST'])
@euser_requeired
@login_timeat
def editjob(job_id):
    job = Job.query.filter_by(id=job_id).first()
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.up_job(job_id)
        flash("修改成功")
        return redirect(url_for('job.euseradmin'))
    else:

        return render_template('job/editjob.html',form=form,job_id=job_id)


@job.route('/<int:job_id>/delete',methods=['GET','POST'])
@euser_requeired
@login_timeat
def delete(job_id):
    job = Job.query.filter_by(id=job_id).first()
    job.upstates2()
    flash("删除成功")
    return redirect(url_for('job.euseradmin'))





@job.route('/new',methods=['GET','POST'])
@euser_requeired
@login_timeat
def newjob():
    form = JobForm()
    if form.validate_on_submit():
        form.create_job(current_user.id)
        flash("修改成功")
        return redirect(url_for('job.euseradmin'))
    else:
        flash("请开始添加")
        print("请开始添加")
    return render_template('job/new_job.html',form=form)

@job.route('/apply/todolist',methods=['GET','POST'])
@euser_requeired
@login_timeat
def todolist():
    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.filter_by(job_company=current_user.id).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    print(pagination.items)

    return  render_template('job/job_todolist.html',pagination=pagination)


@job.route('/apply/reject',methods=['GET','POST'])
@euser_requeired
@login_timeat
def reject():
    job_id = request.args.get('job_id')
    message_id = request.args.get('message_id')
    minjob=Minjob.query.filter_by(message_id=int(message_id),job_id=int(job_id)).first()
    minjob.up_state("不合适")
    flash("不合适成功")
    return redirect(url_for('job.todolist'))

@job.route('/apply/interview',methods=['GET','POST'])
@euser_requeired
@login_timeat
def interview():
    job_id = request.args.get('job_id')
    message_id = request.args.get('message_id')
    minjob=Minjob.query.filter_by(message_id=int(message_id),job_id=int(job_id)).first()
    minjob.up_state("面试")
    flash("面试成功")
    return redirect(url_for('job.todolist'))


@job.route('/apply/interviewlist',methods=['GET','POST'])
@euser_requeired
@login_timeat
def interviewlist():
    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.filter_by(job_company=current_user.id).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    print(pagination.items)

    return  render_template('job/job_interviewlist.html',pagination=pagination)


@job.route('/apply/rejectlist',methods=['GET','POST'])
@euser_requeired
@login_timeat
def rejectlist():
    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.filter_by(job_company=current_user.id).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    print(pagination.items)

    return  render_template('job/job_rejectlist.html',pagination=pagination)



@job.route('/userjobs',methods=['GET','POST'])
@user_requeired
@login_timeat
def userjobs():
    message = Message.query.filter_by(id=current_user.id).first()
    print(message.Jobm)
    return  render_template('job/userjobs.html',message=message)
