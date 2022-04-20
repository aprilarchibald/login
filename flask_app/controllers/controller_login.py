from flask_app import app, bcrypt
from flask import render_template, redirect,request, session
from flask_app.models.models_login import User


@app.route('/')
def index():
    if 's_id' in session:
        return redirect('/success')
    return render_template("index.html")

@app.route('/success')
def success():
    if 's_id' not in session:
        return redirect('/')
    context ={
        'user': User.get_one({'id' : session['s_id']})
    }
    return render_template("success.html", **context)

@app.route('/login', methods=["POST"])
def login():
    if not User.login_validator(request.form):
        return redirect('/')
    # User.create(request.form)
    return redirect('/success')

@app.route('/logout')
def logout():
    del session['s_id']
    return redirect('/')

@app.route('/register', methods=["POST"])
def register():
    if not User.reg_validator(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data ={
        **request.form,
        'password': pw_hash
    }
    id = User.create(data)
    session['s_id'] = id
    return redirect('/success')
