from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///student.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class student(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    mobile = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(150), nullable=False)
    # date created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
       return f"{self.sno} - {self.name}"


    @app.route('/', methods=['GET', 'POST'])
    def hello():

        if request.method=='POST':
            name = request.form['name']
            email = request.form['email']
            department = request.form['department']
            mobile = request.form['mobile']
            address = request.form['address']

            info = student(name = name, email = email, department = department, mobile = mobile,address = address)
            db.session.add(info)
            db.session.commit()

        student_new = student.query.all() # display info on home page using repr method
        #print(student_new)
        return render_template('home.html', student_new=student_new)



@app.route('/show')
def products():
    student_new = student.query.all()
    print(student_new)
    return 'this is my page'



@app.route('/delete/<int:sno>')
def delete(sno):
    delete_new = student.query.filter_by(sno=sno).first()
    db.session.delete(delete_new)
    db.session.commit()
    return redirect("/")


    
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=="POST":

        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        mobile = request.form['mobile']
        address = request.form['address']
        update_new = student.query.filter_by(sno=sno).first()
        update_new.name = name
        update_new.email = email
        update_new.department = department
        update_new.mobile = mobile
        update_new.address = address

        db.session.add(update_new)
        db.session.commit()
        return redirect("/")

    update_new = student.query.filter_by(sno=sno).first()
    return render_template('update.html', update_new=update_new)
   
if __name__ == '__main__':
    app.run(debug=True)