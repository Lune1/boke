from App.exts import db


# 模型 => 类

class Classify(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(120),unique=True)
    mycount = db.Column(db.Integer,default=0)
    another_name = db.Column(db.String(120),unique=True)
    articles = db.relationship('Article',backref='my_classify',lazy=True)

    def __str__(self):
        return self.name
class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200),unique=True)
    context = db.Column(db.String(5000))
    date = db.Column(db.DateTime,default='2018-10-12 11:12:40')
    tag = db.Column(db.String(50))
    press = db.Column(db.Integer,default=0)
    myclassify = db.Column(db.Integer,db.ForeignKey(Classify.id))
    my_press = db.relationship('Mypress', backref='my_article', lazy=True)

class Mypress(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(1000))
    date = db.Column(db.DateTime,default='2018-10-12 11:12:40')
    articles = db.Column(db.Integer,db.ForeignKey(Article.id))

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),unique=True)
    passwd = db.Column(db.String(50))

