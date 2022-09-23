from flask import session
from sqlalchemy import or_, and_
from app import app, db
from .models import Group, Calendar, Event

class EventValidator:
    def __init__(self, start=None, end=None, description=None):
        self.start = start
        self.end = end
        self.description = description

    def duration_validation(self):
        """
        duration of the event must be above then 5 minutes and below then 8 hours
        """
        diff = self.end - self.start
        if diff.total_seconds() < 300:
            err_message = "Событие не может длиться меньше 5 минут"
            return False, err_message
        elif diff.total_seconds() > 28800:
            err_message = "Событие не может длиться дольше 8 часов"
            return False, err_message
        return True, ''

    def collision_validation(self, edit=False, event_id=None):
        if edit and event_id:
            events = Event.query.filter(or_(and_(Event.start < self.start, Event.end > self.start), and_(
                Event.start < self.end, Event.end > self.end))).filter(Event.id!=event_id).all()
        else:
            events = Event.query.filter(or_(and_(Event.start < self.start, Event.end > self.start), and_(
                Event.start < self.end, Event.end > self.end))).all()

        if events:
            err_message = "Это время уже занято"
            for event in events:
                author = f"@{event.author_username}" if event.author_username else f"{event.author_firstname}"
                start_hour = event.start.hour if event.start.hour > 9 else f'0{event.start.hour}'
                start_minute = event.start.minute if event.start.minute > 9 else f'0{event.start.minute}'
                end_hour = event.end.hour if event.end.hour > 9 else f'0{event.end.hour}'
                end_minute = event.end.minute if event.end.minute > 9 else f'0{event.end.minute}'
                text = f'\t\t{event.start.day}.{event.start.month}.{event.start.year} {start_hour}:{start_minute} - {end_hour}:{end_minute} {event.description} [{author}] \n'
                err_message += text
            return False, err_message
        return True, ''

    def get_group(self):

        self.group = Group.query.first()
        return True, self.group

    def get_calendar(self):
        group = self.get_group()
        if not group[0]:
            return group

        self.calendar = Calendar.query.filter(Calendar.group_id == self.group.id).first()
        return True, self.calendar

    def create_event(self, uid, ufirstname, uname):
        calendar = self.get_calendar()
        if not calendar[0]:
            return calendar
        if not uname:
            uname = ''
        self.event = Event(
            start=self.start,
            end=self.end,
            description=self.description,
            calendar_id=self.calendar.id,
            author_id=uid,
            author_firstname=ufirstname,
            author_username=uname,
        )
        db.session.add(self.event)
        db.session.commit()
        return True, ''

    def update_event(self, event):
        Event.query.filter(Event.id == event.id).update(
            {'description': self.description, 'start': self.start, 'end': self.end}, synchronize_session = False)
        db.session.commit()
        db.session.close()
        return True, ''
