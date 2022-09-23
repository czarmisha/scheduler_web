from app import app, db


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.SmallInteger, primary_key=True)
    tg_id = db.Column(db.BigInteger, nullable=False)  # tg group id
    name = db.Column(db.String(50), nullable=False)
    calendar = db.relationship("Calendar", back_populates="group", uselist=False)

    def __repr__(self):
        return f'<Telegram group - {self.name}, id: {self.id}>'
    

class Calendar(db.Model):
    __tablename__ = 'calendar'

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    group = db.relationship("Group", back_populates="calendar")
    event = db.relationship("Event", back_populates="calendar")

    def __repr__(self):
        return f'<Calendar - name: {self.name}, group id: {self.group_id}>'


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.SmallInteger, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    calendar_id = db.Column(db.Integer, db.ForeignKey("calendar.id"))
    calendar = db.relationship("Calendar", back_populates="event")
    author_id = db.Column(db.Integer, nullable=False)
    author_firstname = db.Column(db.String(255), nullable=False)
    author_username = db.Column(db.String(255), nullable=True)
    is_archive = db.Column(db.Boolean, default=False, nullable=True)

    def __repr__(self):
        return f'<Event - start: {self.start}, end: {self.end}>'
    
    def to_json_api(self):
        return {
            'id': self.id,
            'start': self.start,
            'end': self.end,
            'description': self.description,
            'author_firstname': self.author_firstname,
            'author_username': self.author_username,
        }
