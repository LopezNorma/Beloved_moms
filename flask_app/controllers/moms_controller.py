from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.mom_model import Mom
from flask_app.models.post_model import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/') 
def create():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_mom():
    if not Mom.validate_mom(request.form):
        return redirect('/')
    data = { 
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
}
    id = Mom.save(data)
    session['mom_id'] = id
    print(request.form)
    return redirect('/dashboard')

@app.route('/login', methods =['POST'])
def login():
    data ={
        'email': request.form['email']
    }
    one_mom = Mom.get_mom_by_email(data)
    if not one_mom:
        flash('invalid email or password!!')
        return redirect('/')
    if not bcrypt.check_password_hash(one_mom.password, request.form['password']):
        flash('invalid email or password!!')
        return redirect('/')
    session['mom_id'] = one_mom.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'mom_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['mom_id']
    }
    post=Post.get_post_w_mom()
    return render_template('dashboard.html', posts = post, mom=Mom.get_by_id(data))
#left posts goes to the jinja, the right goes to controllers

@app.route('/logout')
def logout():
    session.clear
    return redirect('/')
