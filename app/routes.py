from . import app, db, bcrypt, stripe_keys
from flask import render_template, url_for, flash, redirect, request
from .forms import RegistrationForm, LoginForm, UpdateProfileForm, SalaryInfoForm
from .models import User
from flask_login import login_user, current_user, login_required, logout_user
import secrets
import os
from PIL import Image
import stripe
import pickle



@app.route('/')
@app.route('/home')
def home():
    
    return render_template('home.html')




@app.route('/register', methods=['POST', 'GET'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('task'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Register')
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('task'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('task'))
        else:
            flash('Login Fail!. Please check username and password', 'danger')
    
    return render_template('login.html', form=form, title='Login')

@app.route('/task')
@login_required
def task():
    
    return render_template('pay.html', key=stripe_keys['publishable_key'])

def save_picture(form_picture):
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file )
    
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

@app.route('/logout')
def logout():
    
    logout_user()
    return redirect(url_for('home'))

@app.route('/charge', methods=['POST'])
@login_required
def charge():

    # amount in cents
    amount = 99

    customer = stripe.Customer.create(
        email=current_user.email,
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )
    form = SalaryInfoForm()
    return render_template('operate.html', amount=amount, title='Income Predictor', form=form)

def input_arragement(hrwkwk_input, educa_n_intput, age_input):
    
    cap_gn = 0
    cap_lss = 0
    hrwkwk = float(hrwkwk_input)
    educa_n = float(educa_n_intput)
    age = float(age_input)
    new_feature = hrwkwk*educa_n*age + 0.223013*cap_gn - 0.147554*cap_lss
    X_input = [[new_feature, educa_n, age, hrwkwk]]
    return X_input

model = pickle.load(open('./app/checkpoints/model.pkl','rb'))

@app.route('/predict', methods=['POST','GET'])
@login_required
def predict():
    
    form = SalaryInfoForm()
    if request.method == 'POST':
        X_input = input_arragement(form.hrwkwk.data, form.education.data, form.age.data)
        prediction = model.predict(X_input)
        return render_template('result.html', prediction=prediction, title='Your Income')
    
    return render_template('home.html')

@app.route("/free_trial", methods=["POST"])
@login_required
def free_trial():

    form = SalaryInfoForm()
    return render_template('operate.html', title='Income Predictor', form=form)
