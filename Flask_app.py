from flask import Flask, render_template, request  # render_template will render out HTML templates.
# request we will be able to access these HTTP request that is being made from the browser and then we
# can read this request so we can fetch this email address and the height.
from flask_sqlalchemy import SQLAlchemy
from emailsender import send_mail
from sqlalchemy.sql import func

app = Flask(__name__)
# app knows where to look for a database (connection to your database)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gnbuaxjsquccyz:bfbd0bb4816876c2d72f94551a7f3dce63be87af11fdad7586e2c6b04f0b53b2@ec2-3-215-207-12.compute-1.amazonaws.com:5432/ddebc9ekcut022?sslmode=require'

db = SQLAlchemy(app)  # create an SQL alchemy object.
print(db)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)  # not be accepting values that are more than 120 characters long.
    height_ = db.Column(db.Float)
    phoneno_ = db.Column(db.String, unique=True)

    # initializing our instance variables because this method is the first to be
    # executed when you call the class instance.
    def __init__(self, email_, height_, phoneno_):
        self.email_ = email_
        self.height_ = height_
        self.phoneno_ = phoneno_


@app.route("/")
def index():
    return render_template("index.html")
# go to template folder and get the index.html file and render it in the home page.


@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height_name"]
        if len(str(request.form["Phone_number"])) == 0:
            phoneno = None
        else:
            phoneno = request.form["Phone_number"]
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            if db.session.query(Data).filter(Data.phoneno_ == phoneno).count() == 0:
                data = Data(email, height, phoneno)
                db.session.add(data)
                db.session.commit()
                average_height = db.session.query(func.avg(Data.height_)).scalar()
                average_height = round(average_height,3)
                count = db.session.query(Data.height_).count()
                send_mail(email, height, average_height, count)
                return render_template("success.html")
            elif phoneno == None:
                data = Data(email, height, phoneno)
                db.session.add(data)
                db.session.commit()
                average_height = db.session.query(func.avg(Data.height_)).scalar()
                average_height = round(average_height,3)
                count = db.session.query(Data.height_).count()
                send_mail(email, height, average_height, count)
                return render_template("success.html")
            else:
                return render_template("index.html", text="There was an Error <br> this error occured because you or someone else used the same phone number!!")
        else:
            return render_template("index.html", text="There was an Error <br> this error occured because you or someone else used the same email!!")


if __name__ == '__main__':  # which means if the script is being executed and not being imported
    app.debug = True
    app.run(port=5001)  # port若不设置则默认为5000


#  https://n-collector.herokuapp.com/

'''
You need less secure apps turned ON:
https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4O25xD4yQ8ivd2_9sHIyN7Et0lm2tsWBwCZJVmRmwqXeY9OIGO1p3cL6-qVevbnlU-x8cy_-4UA5uNQGMhgcnV1tlaohg
https://accounts.google.com/DisplayUnlockCaptcha
Finally, I found a google support page telling me I needed to enable IMAP for it to work. 
'''
