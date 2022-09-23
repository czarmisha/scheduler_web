import datetime, hmac, hashlib 
from sqlalchemy import or_, desc
from flask import jsonify, request,session
from app import app, db
from .models import Event
from .validators import EventValidator

TZ = datetime.timezone(datetime.timedelta(hours=5), 'Uzbekistan/UTC+5')

@app.get('/api/get-auth-data')
def get_auth_data():
    data = {'bot_name': app.config['BOT_USERNAME'], 'bot_url': app.config['BOT_AUTH_REDIRECT']}
    return jsonify(data)

@app.get('/api/check-user-auth')
def check_user_auth():
    res = {'success': True} if 'tg_data' in session else {'success': False}
    return jsonify(res)

def string_generator(data_incoming):
    data = data_incoming.copy()
    del data['hash']
    keys = sorted(data.keys())
    string_arr = []
    for key in keys:
        if data[key]:
            string_arr.append(key+'='+str(data[key]))
    string_cat = '\n'.join(string_arr)
    return string_cat

@app.post('/api/login')
def login():
    tg_data = {
		"id" : request.json.get('id',None),
		"first_name" : request.json.get('first_name',None),
		"username" : request.json.get('username', None),
		"auth_date":  request.json.get('auth_date', None),
		"hash" : request.json.get('hash', None),
        "photo_url": request.json.get('photo_url', None)
	}
    data_check_string = string_generator(tg_data)
    secret_key = hashlib.sha256(app.config['BOT_TOKEN'].encode('utf-8')).digest()
    secret_key_bytes = secret_key
    data_check_string_bytes = bytes(data_check_string,'utf-8')
    hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
    if hmac_string == tg_data['hash']:
        session['tg_data'] = tg_data
        response = {
            "id" : tg_data['id'],
            "first_name" : tg_data['first_name'],
            "username" : tg_data['username'],
            "photo_url": tg_data['photo_url']
        }
        return jsonify({
                'success': True,
                'user': response
    })

    return jsonify({
                'success': False
    })

@app.get('/api/get-events/<period>')
def get_events_by_period(period):
    today = datetime.datetime.now(TZ)
    if period == 'today':
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = today.replace(hour=23, minute=59, second=59)
    elif period == 'tomorrow':
        start = today.replace(
            hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        end = start.replace(hour=23, minute=59, second=59)
    elif period == 'thisweek':
        start = today.replace(hour=0, minute=0, second=0, microsecond=0) - \
            datetime.timedelta(days=today.isoweekday() - 1)
        end = today.replace(hour=23, minute=59, second=59) + \
            datetime.timedelta(days=5 - today.isoweekday())
    else:
        return '', 400

    events = Event.query.filter(Event.start > start, Event.end < end).order_by(desc(Event.start)).all()
    response = [event.to_json_api() for event in events]
    return jsonify(response)

@app.get('/api/get-all-events')
def get_all_events():
    events = Event.query.all()
    response = [event.to_json_api() for event in events]
    return jsonify(response)

@app.get('/api/get-events-by-id/<int:user_id>')
def get_events_by_user(user_id):
    events = Event.query.filter(Event.author_id==user_id, or_(Event.is_archive==False, Event.is_archive==None)).order_by(desc(Event.start)).all()
    response = [event.to_json_api() for event in events]
    return jsonify(response)

@app.route('/api/get-event-detail/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get(event_id) # TRY
    response = event.to_json_api()
    return jsonify(response)

@app.route('/api/delete-event/<int:event_id>')
def delete_event(event_id):
    response = {'success': False}
    event = Event.query.get(event_id) # TRY
    if event:
        db.session.delete(event)
        db.session.commit()
        response['success'] = True
    return jsonify(response)

@app.post('/api/edit-event/<int:event_id>')
def edit_event(event_id):
    response = {'success': False}
    if not request.json['start'] or not request.json['end'] or not request.json['description']:
        print('********************ERROR******************', 'All data is required')
        response['error'] = True
        response['message'] = 'Все поля должны быть заполнены'
        return jsonify(response)
    event_start = datetime.datetime.strptime(request.json.get('start'), '%Y-%m-%d %H:%M')
    event_end = datetime.datetime.strptime(request.json.get('end'), '%Y-%m-%d %H:%M')
    event_description = request.json.get('description')
    validator = EventValidator(event_start, event_end, event_description)
    success, mess = validator.duration_validation()
    if not success:
        print('********************ERROR******************', mess)
        response['error'] = True
        response['message'] = mess
        return jsonify(response)
    collision = validator.collision_validation(edit=True, event_id=event_id)
    if not collision[0]:
        print('********************ERROR******************', collision[1])
        response['error'] = True
        response['message'] = collision[1]
        return jsonify(response)
    curr_event = Event.query.get(event_id)
    event = validator.update_event(curr_event)
    if not event[0]:
        print('********************ERROR******************', event[1])
        response['error'] = True
        response['message'] = event[1]
        return jsonify(response)
    # send_message('-733843248', 'Новая бронь была создана через сайт')
    response['success'] = True
    return jsonify(response)


@app.post('/api/create-event')
def create_event():
    print(request.json)
    response = {'success': False}
    if not request.json['start'] or not request.json['end'] or not request.json['description']:
        print('********************ERROR******************', 'All data is required')
        response['error'] = True
        response['message'] = 'Все поля должны быть заполнены'
        return jsonify(response)
    event_start = datetime.datetime.strptime(request.json.get('start'), '%Y-%m-%d %H:%M')
    event_end = datetime.datetime.strptime(request.json.get('end'), '%Y-%m-%d %H:%M')
    event_description = request.json.get('description')
    validator = EventValidator(event_start, event_end, event_description)
    success, mess = validator.duration_validation()
    if not success:
        print('********************ERROR******************', mess)
        response['error'] = True
        response['message'] = mess
        return jsonify(response)
    collision = validator.collision_validation()
    if not collision[0]:
        print('********************ERROR******************', collision[1])
        response['error'] = True
        response['message'] = collision[1]
        return jsonify(response)
    event = validator.create_event(request.json.get('u_id'), request.json.get('u_firstname'), request.json.get('u_name'))
    if not event[0]:
        print('********************ERROR******************', event[1])
        response['error'] = True
        response['message'] = event[1]
        return jsonify(response)
    response['success'] = True
    return jsonify(response)
