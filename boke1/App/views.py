from datetime import datetime

from flask import Blueprint, render_template, request, session, redirect, url_for
from App.models import *

blue = Blueprint('blue', __name__)


# 首页
@blue.route('/')
def index():
    articles = Article.query.all()
    classifies = Classify.query.all()
    return render_template('home/index.html',articles=articles,classifies=classifies)

@blue.route('/share/')
def share():
    return render_template('home/share.html')

@blue.route('/list/')
def list():
    return render_template('home/list.html')

@blue.route('/about/')
def about():
    return render_template('home/about.html')

@blue.route('/gbook/')
def gbook():
    return render_template('home/gbook.html')

@blue.route('/info/')
def info():
    return render_template('home/info.html')

@blue.route('/infopic/')
def infopic():
    return render_template('home/infopic.html')


@blue.route('/classify/<id>/')
def classify(id):
    classify = Classify.query.get(id)
    articles = classify.articles
    classifies = Classify.query.all()
    return render_template('home/index.html',articles=articles,classifies=classifies)

@blue.route('/check_article/<id>/')
def check_article(id):
    article = Article.query.get(id)
    return render_template('home/check_article.html',article=article)

@blue.route('/add_press/<id>/',methods=['POST','GET'])
def add_press(id):
    if request.method == 'POST':
        content = request.form.get('content')
        date = datetime.now().strftime('%Y-%m-%d %X')
        press = Mypress()
        press.content=content
        press.date=date
        press.articles=id
        article = Article.query.get(id)
        article.press +=1
        my_add(press)
        article = Article.query.get(id)
        return render_template('home/check_article.html',article=article)
    return render_template('home/check_article.html')


#后台
@blue.route('/admin/login/',methods=['POST','GET'])
def admin_login():
    if request.method == "POST":
        username = request.form.get('username')
        userwd = request.form.get('userwd')
        user = User.query.filter_by(name=username).first()
        if user:
            if userwd == user.passwd:
                session['username'] = user.name
                return render_template('admin/index.html', username=username)
            else:
                return "密码错误"
        else:
            return "用户不存在"
    return render_template('admin/login.html')

@blue.route('/admin/logout/')
def admin_logout():
    session.pop('username')
    return redirect(url_for('blue.admin_login'))

@blue.route('/admin/index/')
def admin_index():
    username = session.get('username','')
    return render_template('admin/index.html',username=username)

@blue.route('/admin/article/',methods=['POST',"GET"])
def admin_article():
    username = session.get('username','')
    articles = Article.query.all()
    return render_template('admin/article.html',articles=articles,username=username)

@blue.route('/admin/notice/')
def admin_notice():
    username = session.get('username','')
    return render_template('admin/notice.html',username=username)

@blue.route('/admin/comment/')
def admin_comment():
    username = session.get('username','')
    mypress = Mypress.query.all()
    # for i in mypress:
    #     print(i.my_article.id)
    return render_template('admin/comment.html',username=username,mypress=mypress)

@blue.route('/admin/category/')
def admin_category():
    username = session.get('username','')
    classifies = Classify.query.all()
    return render_template('admin/category.html',username=username,classifies=classifies)

@blue.route('/admin/flink/')
def admin_flink():
    username = session.get('username','')
    render_template('admin/flink.html',username=username)

@blue.route('/admin/manage-user/')
def admin_manage_user():
    username = session.get('username','')
    return render_template('admin/manage-user.html',username=username)

@blue.route('/admin/loginlog/')
def admin_loginlog():
    username = session.get('username','')
    return render_template('admin/loginlog.html',username=username)

@blue.route('/admin/setting/')
def admin_setting():
    username = session.get('username','')
    return render_template('admin/setting.html',username=username)

@blue.route('/admin/readset/')
def admin_readset():
    username = session.get('username','')
    return render_template('admin/readset.html',username=username)

@blue.route('/admin/add-notice/')
def admin_add_notice():
    username = session.get('username','0')
    return render_template('admin/add-notice.html',username=username)

@blue.route('/admin/update-article/<id>/',methods=['POST',"GET"])
def admin_update_article(id):
    username = session.get('username','')
    if request.method == 'POST':
        title = request.form.get('title')
        context = request.form.get('context')
        tag = request.form.get('tag')
        classify = request.form.get('classify')
        date = datetime.now().strftime('%Y-%m-%d %X')
        article = Article.query.get(id)
        article.context = context
        article.title = title
        article.tag = tag
        article.date = date
        print(classify)
        classify = Classify.query.filter_by(name=classify).first()
        if article.myclassify != classify.id:
            article.myclassify = classify.id
            # print(classify.mycount)
            classify.mycount += int(1)
                # print(classify.mycount)
                # print(Classify.query.get(article.myclassify).mycount)
            Classify.query.get(article.myclassify).mycount -= int(1)
                # print(Classify.query.get(article.myclassify).mycount)
            my_update()
            return redirect(url_for('blue.admin_article', values='修改成功'))
        else:
            my_update()
            return redirect(url_for('blue.admin_article', values='修改成功'))
    article = Article.query.get(id)
    classifies = Classify.query.all()
    if classifies:
    	return render_template('admin/modify_article.html', article=article, classifies=classifies, username=username)
    else:
    	return redirect(url_for('blue.admin_category'))
@blue.route('/admin/update-category/<id>/',methods=['POST',"GET"])
def admin_update_category(id):
    username = session.get('username','')
    if request.method=="POST":
        name = request.form.get('name')
        another_name = request.form.get('another_name')
        classify = Classify.query.get(id)
        classify.name=name
        classify.another_name=another_name
        my_update()
        return redirect(url_for('blue.admin_category',username=username))
    classify = Classify.query.get(id)
    return render_template('admin/update-category.html',username=username,classify=classify)


@blue.route('/admin/update-flink')
def admin_update_flink():
    username = session.get('username','0')
    return render_template('admin/update-flink.html',username=username)

@blue.route('/admin/add-flink/')
def admin_add_flink():
    username = session.get('username','0')
    return render_template('admin/add-flink.html',username=username)


@blue.route('/delete_classify/<id>/')
def delete_classify(id):
    classify=Classify.query.filter_by(id=id).first()
    my_delete(classify)
    return redirect(url_for('blue.admin_category'))

@blue.route('/delete_article/<id>/')
def delete_article(id):
    article=Article.query.filter_by(id=id).first()
    if article.myclassify:
        classify = Classify.query.get(article.myclassify)
        classify.mycount -= int(1)
    my_delete(article)
    return redirect(url_for('blue.admin_article'))

@blue.route('/delete_press/<id>/',methods=['POST','GET'])
def admin_delete_press(id):
    username = session.get('username','')
    print('ok:',id)
    press=Mypress.query.filter_by(id=id).first()
    my_delete(press)
    mypress = Mypress.query.all()
    return redirect(url_for('blue.admin_comment',mypress=mypress,username=username))

@blue.route('/add_category/',methods=['POST','GET'])
def add_category():
    username = session.get('username', '')
    if request.method == 'POST':
        name = request.form.get('name')
        another_name = request.form.get('another_name')
        classify = Classify()
        classify.name=name
        classify.another_name=another_name
        my_add(classify)
        return redirect(url_for('blue.admin_category'))
    classifies = Classify.query.all()
    return render_template('admin/category.html', username=username, classifies=classifies)


@blue.route('/admin/add-article/',methods=['POST','GET'])
def admin_add_article():
    username = session.get('username','')
    if request.method == 'POST':
        context = request.form.get('context')
        title = request.form.get('title')
        tag = request.form.get('tag')
        classify = request.form.get('classify')
        if classify:
            classify = Classify.query.filter_by(name=classify).first()
            # print(context,tag,title,category)
            # classify = Classify.query.filter_by(id=category).first()
            classify.mycount += int(1)
        date = datetime.now().strftime('%Y-%m-%d %X')
        article = Article(title=title,context=context,date=date,myclassify=classify.id,tag=tag)
        my_add(article)
        return redirect(url_for('blue.admin_article'))
    else:
        classifies = Classify.query.all()
        return render_template('admin/add-article.html',username=username,classifies=classifies)
@blue.route('/check_press/<id>/',methods=['POST','GET'])
def admin_check_press(id):
    username = session.get('username', '')
    if username:
        acticle = Article.query.get(id)
        mypress = acticle.my_press
        print(mypress)
        return render_template('admin/mypress.html',mypress=mypress)
    else:
        return render_template('admin/login.html')

def my_update():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()

def my_add(r):
    try:
        db.session.add(r)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()

def my_delete(r):
    try:
        db.session.delete(r)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
