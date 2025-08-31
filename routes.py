from flask import render_template, redirect, url_for, flash, request, jsonify, abort, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
import json
from models import User, HealthEntry, db
from forms import LoginForm, RegistrationForm, HealthEntryForm

# Create a blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=7)
    
    entries = HealthEntry.query.filter(
        HealthEntry.user_id == current_user.id,
        HealthEntry.date >= start_date
    ).order_by(HealthEntry.date).all()
    
    dates = [entry.date.strftime('%Y-%m-%d') for entry in entries]
    mood_data = [entry.mood for entry in entries]
    water_data = [entry.water_intake for entry in entries]
    sleep_data = [entry.sleep_hours for entry in entries]
    
    health_tip = generate_health_tip(entries)
    
    return render_template('dashboard.html', title='Dashboard', 
                          dates=json.dumps(dates),
                          mood_data=json.dumps(mood_data),
                          water_data=json.dumps(water_data),
                          sleep_data=json.dumps(sleep_data),
                          health_tip=health_tip)

@main.route('/add_entry', methods=['GET', 'POST'])
@login_required
def add_entry():
    form = HealthEntryForm()
    if form.validate_on_submit():
        entry = HealthEntry(
            date=form.date.data,
            exercise=form.exercise.data,
            diet=form.diet.data,
            mood=form.mood.data,
            water_intake=form.water_intake.data,
            sleep_hours=form.sleep_hours.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        flash('Your health entry has been saved!')
        return redirect(url_for('main.dashboard'))
    return render_template('add_entry.html', title='Add Entry', form=form)

@main.route('/entries')
@login_required
def entries():
    page = request.args.get('page', 1, type=int)
    entries = HealthEntry.query.filter_by(user_id=current_user.id)\
        .order_by(HealthEntry.date.desc())\
        .paginate(page=page, per_page=10)
    return render_template('entries.html', title='Entries', entries=entries)

@main.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = HealthEntry.query.get_or_404(entry_id)
    if entry.author != current_user:
        abort(403)
    form = HealthEntryForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.entries'))
    return render_template('add_entry.html', title='Edit Entry', form=form)

@main.route('/delete_entry/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = HealthEntry.query.get_or_404(entry_id)
    if entry.author != current_user:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash('Your entry has been deleted.')
    return redirect(url_for('main.entries'))

@main.route('/api/entries')
@login_required
def api_entries():
    entries = HealthEntry.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': entry.id,
        'date': entry.date.isoformat(),
        'exercise': entry.exercise,
        'diet': entry.diet,
        'mood': entry.mood,
        'water_intake': entry.water_intake,
        'sleep_hours': entry.sleep_hours,
        'notes': entry.notes
    } for entry in entries])

@main.route('/healthz')
def health_check():
    return {"status": "healthy", "message": "Service is running"}, 200

def generate_health_tip(entries):
    if not entries:
        return "Start tracking your health habits to receive personalized tips!"
    
    latest = entries[-1]
    
    if latest.water_intake < 8:
        return "Try to drink at least 8 glasses of water daily for optimal hydration."
    
    if latest.sleep_hours < 7:
        return "Aim for 7-9 hours of sleep each night for better health and cognitive function."
    
    if latest.mood < 5:
        return "Consider adding mindfulness or meditation to your routine to improve mood."
    
    if not latest.exercise:
        return "Regular physical activity is important. Try to incorporate at least 30 minutes of exercise daily."
    
    return "Great job maintaining your health habits! Keep up the good work!"