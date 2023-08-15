from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.post_model import Post, Mom
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/create')
def create_post():
    if 'mom_id' not in session:
        return redirect('/logout')
    return render_template('create_post.html')

@app.route('/create/post', methods=['POST'])
def create_new_post():
    if "mom_id" not in session:
        print('send back to login because not in session')
        return redirect('/')
    if not Post.validate_post(request.form):
        return redirect('/create')
    # post_dict = {
    #     "id": request.form['post_id'],
    #     "name": request.form['name'], 
    #     "type": request.form['type'],
    #     "instructions": request.form['instructions'],
    #     }# we can get the user_id by hidden input
    #     
    Post.save(request.form) # this returns post id
    print('&&&&printing post')
    return redirect('/dashboard')

@app.route('/delete/post/<int:post_id>')
def delete_post_info(post_id):
    if 'mom_id' not in session:
        return redirect('/logout')
    Post.delete_post(post_id)

    return redirect('/dashboard')

@app.route('/edit/<int:post_id>')
def edits(post_id):
    #this is routing my page
    if 'mom_id' not in session:
        return redirect('/logout')
    post = Post.get_one(post_id)
    return render_template('/edit_post.html', post = post)

@app.route('/edit/post/<int:post_id>', methods= ['POST'])
def edit_post(post_id):
    if 'mom_id' not in session:
        return redirect('/logout')
    data = {
        'name' : request.form['name'],
        'type': request.form['type'],
        'description' : request.form['description'],
        'mom_id' : request.form['mom_id'],
           'id': post_id

    }
    if not Post.validate_post(request.form):
        return redirect('/create')
    Post.update_post(data)
    return redirect('/dashboard')


@app.route('/view/post/<int:post_id>')
def view_post(post_id):
    #this is routing my page
    if 'mom_id' not in session:
        return redirect('/logout')
    post = Post.get_one(post_id)
    data = {
        'id' : session['mom_id']
    }
    mom = Mom.get_by_id(data)
    return render_template('view_info.html', mom = mom,  post = post )




    

