import datetime
import hashlib
import hmac
from pyexpat.errors import messages
from flask import jsonify, render_template, request, redirect, url_for, session, flash
from app import app, db
from .models import Event, Group, Calendar
from .utils import send_message
from .validators import EventValidator

TZ = datetime.timezone(datetime.timedelta(hours=5), 'Uzbekistan/UTC+5')

@app.route('/')
def index():
    data = {'bot_name': app.config['BOT_USERNAME'], 'bot_url': app.config['BOT_AUTH_REDIRECT']}
    return render_template('index.html', data=data)

def string_generator(data_incoming):
    data = data_incoming.copy()
    del data['hash']
    keys = sorted(data.keys())
    string_arr = []
    for key in keys:
        if data[key]:
            string_arr.append(key+'='+data[key])
    string_cat = '\n'.join(string_arr)
    return string_cat

@app.route('/login')
def login():
    tg_data = {
		"id" : request.args.get('id',None),
		"first_name" : request.args.get('first_name',None),
		"username" : request.args.get('username', None),
		"auth_date":  request.args.get('auth_date', None),
		"hash" : request.args.get('hash', None),
        "photo_url": request.args.get('photo_url', None)
	}
    data_check_string = string_generator(tg_data)
    secret_key = hashlib.sha256(app.config['BOT_TOKEN'].encode('utf-8')).digest()
    secret_key_bytes = secret_key
    data_check_string_bytes = bytes(data_check_string,'utf-8')
    hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
    if hmac_string == tg_data['hash']:
        session['tg_data'] = tg_data
        return redirect(url_for('index'))

    return jsonify({
                'hmac_string': hmac_string,
                'tg_hash': tg_data['hash'],
                'tg_data': tg_data
    })

@app.get('/events/<period>')
def get_events_by_period(period):
    today = datetime.datetime.now(TZ)

    if period == 'today':
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = today.replace(hour=23, minute=59, second=59)
    elif period == 'tomorrow':
        start = today.replace(
            hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        end = today.replace(
            hour=23, minute=59, second=59) + datetime.timedelta(days=1)
    elif period == 'thisweek':
        start = today.replace(hour=0, minute=0, second=0, microsecond=0) - \
            datetime.timedelta(days=today.isoweekday() - 1)
        end = today.replace(hour=23, minute=59, second=59) + \
            datetime.timedelta(days=5 - today.isoweekday())
    else:
        return '', 400

    events = Event.query.filter(Event.start > start, Event.end < end).order_by(Event.start).all()
    response = [event.to_json_api() for event in events]
    return jsonify(response)
    # return render_template('event_list.html', events=events)

@app.get('/events/<int:user_id>')
def get_events_by_user(user_id):
    if not "tg_data" in session:
        return '', 400
    events = Event.query.filter(Event.author_id==user_id).all()
    response = [event.to_json_api() for event in events]
    return jsonify(response)
    # return render_template('my_events.html', events=events)

@app.route('/event/detail/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get(event_id) # TRY
    response = event.to_json_api()
    return jsonify(response)
    # return render_template('event_detail.html', event=event)

@app.route('/event/delete/<int:event_id>')
def delete_event(event_id):
    if not "tg_data" in session:
        return '', 400
    event = Event.query.get(event_id) # TRY
    if event:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted', 'info')
        return redirect(f'/events/{session["tg_data"]["id"]}')
    else:
        pass

@app.post('/event/edit/<int:event_id>')
def edit_event(event_id):
    if not "tg_data" in session:
        return '', 400
    if not request.form['start'] or not request.form['end'] or not request.form['description']:
        print('********************ERROR******************', 'All data is required')
        flash('All data is required', 'error')
        return redirect(f'/event/edit/{event_id}')
    event_start = datetime.datetime.strptime(request.form.get('start'), '%Y-%m-%dT%H:%M')
    event_end = datetime.datetime.strptime(request.form.get('end'), '%Y-%m-%dT%H:%M')
    event_description = request.form.get('description')
    validator = EventValidator(event_start, event_end, event_description)
    success, mess = validator.duration_validation()
    if not success:
        print('********************ERROR******************', mess)
        flash(mess, 'error')
        return redirect(f'/event/edit/{event_id}')
    collision = validator.collision_validation(edit=True, event_id=event_id)
    if not collision[0]:
        print('********************ERROR******************', collision[1])
        flash(collision[1], 'error')
        return redirect(f'/event/edit/{event_id}')
    curr_event = Event.query.get(event_id)
    event = validator.update_event(curr_event)
    if not event[0]:
        print('********************ERROR******************', event[1])
        flash(event[1], 'error')
        return redirect(f'/event/edit/{event_id}')
    # send_message('-733843248', 'Новая бронь была создана через сайт')
    flash('Событие было изменено', 'success')
    return redirect(f'/events/{session["tg_data"]["id"]}')

@app.get('/event/edit/<int:event_id>')
def edit_event_form(event_id):
    return render_template('edit_event.html', event_id=event_id)

@app.post('/event/create')
def create_event():
    if not request.form['start'] or not request.form['end'] or not request.form['description']:
        print('********************ERROR******************', 'All data is required')
        flash('All data is required', 'error')
        return redirect('/event/create')
    event_start = datetime.datetime.strptime(request.form.get('start'), '%Y-%m-%dT%H:%M')
    event_end = datetime.datetime.strptime(request.form.get('end'), '%Y-%m-%dT%H:%M')
    event_description = request.form.get('description')
    validator = EventValidator(event_start, event_end, event_description)
    success, mess = validator.duration_validation()
    if not success:
        print('********************ERROR******************', mess)
        flash(mess, 'error')
        return redirect('/event/create')
    collision = validator.collision_validation()
    if not collision[0]:
        print('********************ERROR******************', collision[1])
        flash(collision[1], 'error')
        return redirect('/event/create')
    event = validator.create_event()
    if not event[0]:
        print('********************ERROR******************', event[1])
        flash(event[1], 'error')
        return redirect('/event/create')
    # send_message('-733843248', 'Новая бронь была создана через сайт')
    flash('Событие было создано', 'success')
    return redirect('/')

@app.get('/event/create')
def create_event_form():
    return render_template('create-event.html')