from flask import Flask,render_template,request,flash,redirect,url_for
from wtforms import Form,StringField,FileField,validators,TimeField
from wtforms.fields.html5 import DateField,IntegerField,TimeField,EmailField
from flask_uploads import UploadSet,configure_uploads,IMAGES

from sqlalchemy import create_engine, Column, Integer, String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Profile(Base):
    __tablename__="profile"

    id=Column("id",Integer,primary_key=True)
    username=Column("username",String)
    name=Column("name",String)
    age=Column("age",String)
    mobile=Column("moblie",String)
    email=Column("email",String)
    location=Column("location",String)
    filename30=Column("filename30",String)

    def __init__(self,username,name,age,mobile,email,location,filename30):
        self.username=username
        self.name=name
        self.age=age
        self.mobile=mobile
        self.email=email
        self.location=location
        self.filename30=filename30

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_name(self):
        return self.name

    def get_age(self):
        return self.name

    def get_mobile(self):
        return self.mobile

    def get_email(self):
        return self.email

    def get_location(self):
        return self.location

    def get_filename30(self):
        return self.filename30


#sql
engine=create_engine('sqlite:///profile.db',echo=True)
Base.metadata.create_all(bind=engine)
Session30= sessionmaker(bind=engine)
list30=[]


def profiledb_retrieve():
    global list30
    list30.clear()
    session30= Session30()
    profiles = session30.query(Profile).all()
    for profile in profiles:
        list30.append(profile)
    session30.close()
    return len(list30)


app = Flask(__name__)

photos=UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static'
configure_uploads(app,photos)


class createprofile(Form):
    Username = StringField("Username",[validators.Length(min=4,max=30)])
    Name = StringField("name",[validators.Length(min=4,max=30)])
    Age =StringField("age")
    Mobile = StringField("Moblie")
    Email = StringField("Email")
    Location = StringField("location")


@app.route('/createProfile', methods=["GET", "POST"])
def create():
    form30=createprofile(request.form)
    if request.method == "POST" and form30.validate() and "photo" in request.files:
        username=form30.Username.data
        name = form30.Name.data
        age = form30.Age.data
        mobile = form30.Mobile.data
        email = form30.Email.data
        location = form30.Location.data
        filename= photos.save(request.files['photo'])
        print(age)
        #sql
        session30 = Session30()
        session30.add(Profile(username,name,age,mobile,email,location,filename))
        session30.commit()
        session30.close()

        flash("Tournament has been created!","success")
        return redirect(url_for('profile'))
    return render_template('createprofile.html', form=form30)


@app.route('/Profile')
def profile():
    global list30
    listlen = profiledb_retrieve()
    return render_template('profile.html',list=list30,listlen=listlen)

if __name__=="__main__":
    app.secret_key="secret123"
    app.run(debug=True)
