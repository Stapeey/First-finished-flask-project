from flask import Blueprint, render_template, flash, request, redirect, url_for
from .models import Note
from . import db
from time import time, gmtime


views = Blueprint('views', __name__) 
finalload = []

@views.route('/', methods=['POST', 'GET'])
def home():
    from .auth import logged
    global finalload
    if logged:
        if request.method == 'GET':
            from .auth import current_user
            notes = db.session.execute(db.select(Note).where(Note.user_id == current_user))
            finalload = []
            notes = notes.all()
            datatemp = [ i[0].data for i in notes]
            datetemp = [ i[0].date for i in notes]
            for i, j in zip(datatemp, datetemp):
                formatted_date = gmtime(j/1000000+7200)
                finalload.append([i, f'{formatted_date.tm_year}.{formatted_date.tm_mon}.{formatted_date.tm_mday} {formatted_date.tm_hour}:{formatted_date.tm_min}'])

        if request.method == "POST":
            note = request.form.get('note')
            if note != "":
                date = int(time()*1000000)
                from .auth import current_user
                newNote = Note(data=note, date=date, user_id = current_user)
                db.session.add(newNote)
                db.session.commit()
                flash("New note added!", category='success')
                formatted_date = gmtime(date/1000000+7200)
                finalload.append([note, f'{formatted_date.tm_year}.{formatted_date.tm_mon}.{formatted_date.tm_mday} {formatted_date.tm_hour}:{formatted_date.tm_min}'])
                return render_template('notes.html')
            else:
                flash("No notes were added", category='error')
        return render_template('notes.html')
    else:
        return render_template('home.html')
    
@views.route('/DELLOCALDB')
def remover():
    global finalload
    from .auth import logged
    if logged:
        from .auth import current_user
        Note.query.filter_by(user_id=current_user).delete()
        db.session.commit()
        finalload = []
        return redirect(url_for('views.home')+ '#latest')
    else:
        flash('You are not logged in!', category='error')
        return redirect(url_for('views.home'))