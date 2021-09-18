import argparse

from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, engine_options={'echo': True})


class Student(db.Model):
    sid = db.Column(db.String(10), primary_key=True)
    sname = db.Column(db.String(10))
    sage = db.Column(db.DateTime())
    ssex = db.Column(db.String(10))

    scores = db.relationship('Score', backref='student', lazy=True)

    def __repr__(self):
        return '<Student - Sid: %s, Sname: %s>' % (self.sid, self.sname)


class Course(db.Model):
    cid = db.Column(db.String(10), primary_key=True)
    cname = db.Column(db.String(10))
    tid = db.Column(db.String(10), db.ForeignKey('teacher.tid'))

    scores = db.relationship('Score', backref='course', lazy=True)

    def __repr__(self):
        return '<Course %s>' % self.cname


class Teacher(db.Model):
    tid = db.Column(db.String(10), primary_key=True)
    tname = db.Column(db.String(10))

    courses = db.relationship('Course', backref='teacher', lazy=True)

    def __repr__(self):
        return '<Teacher %s>' % self.tname


class Score(db.Model):
    sid = db.Column(db.String(10), db.ForeignKey('student.sid'), primary_key=True)
    cid = db.Column(db.String(10), db.ForeignKey('course.cid'), primary_key=True)
    score = db.Column(db.Integer)

    def __repr__(self) -> str:
        return '<Score - Student: %s, Course: %s, Score: %s>' % (self.sid, self.cid, self.score)


def init_database():
    db.create_all()
    students = [
        Student(sid='01', sname='赵雷', sage=datetime.strptime(
            '1990-01-01', '%Y-%m-%d'), ssex='男'),
        Student(sid='02', sname='钱电', sage=datetime.strptime(
            '1990-12-21', '%Y-%m-%d'), ssex='男'),
        Student(sid='03', sname='孙风', sage=datetime.strptime(
            '1990-05-20', '%Y-%m-%d'), ssex='男'),
        Student(sid='04', sname='李云', sage=datetime.strptime(
            '1990-08-06', '%Y-%m-%d'), ssex='男'),
        Student(sid='05', sname='周梅', sage=datetime.strptime(
            '1991-12-01', '%Y-%m-%d'), ssex='女'),
        Student(sid='06', sname='吴兰', sage=datetime.strptime(
            '1992-03-01', '%Y-%m-%d'), ssex='女'),
        Student(sid='07', sname='郑竹', sage=datetime.strptime(
            '1989-07-01', '%Y-%m-%d'), ssex='女'),
        Student(sid='08', sname='王菊', sage=datetime.strptime(
            '1990-01-20', '%Y-%m-%d'), ssex='女')
    ]
    courses = [
        Course(cid='01', cname='语文', tid='02'),
        Course(cid='02', cname='数学', tid='01'),
        Course(cid='03', cname='英语', tid='03')
    ]
    teachers = [
        Teacher(tid='01', tname='张三'),
        Teacher(tid='02', tname='李四'),
        Teacher(tid='03', tname='王五')
    ]
    scores = [
        Score(sid='01', cid='02', score=90),
        Score(sid='01', cid='03', score=99),
        Score(sid='02', cid='01', score=70),
        Score(sid='02', cid='02', score=60),
        Score(sid='02', cid='03', score=80),
        Score(sid='03', cid='01', score=80),
        Score(sid='03', cid='02', score=80),
        Score(sid='03', cid='03', score=80),
        Score(sid='04', cid='01', score=50),
        Score(sid='04', cid='02', score=30),
        Score(sid='04', cid='03', score=20),
        Score(sid='05', cid='01', score=76),
        Score(sid='05', cid='02', score=87),
        Score(sid='06', cid='01', score=31),
        Score(sid='06', cid='03', score=34),
        Score(sid='07', cid='02', score=89),
        Score(sid='07', cid='03', score=98)
    ]
    db.session.add_all(students)
    db.session.add_all(courses)
    db.session.add_all(teachers)
    db.session.add_all(scores)
    db.session.commit()


parser = argparse.ArgumentParser(description="Flask-Sqlalchemy Example")
parser.add_argument('-i', '--init', help='初始化数据库并导入数据', action='store_true')
args = parser.parse_args()

if args.init:
    init_database()
