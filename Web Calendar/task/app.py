import datetime
import sys

from flask import Flask, abort, request
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('date', type=inputs.date,
                    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
                    required=True)
parser.add_argument('event', type=str, help="The event name is required!", required=True)

db = SQLAlchemy(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()

resource_fields = {"id": fields.Integer,
                   "event": fields.String,
                   "date": fields.String}


class EventResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        if start_time and end_time:
            events = Event.query.filter(Event.date >= start_time).filter(Event.date <= end_time).all()            #  new
            if len(events) < 1:
                abort(404, {"message": "The event doesn't exist!"})
            return events
        return Event.query.all()

    def post(self):
        args = parser.parse_args()
        event = Event(event=args['event'], date=args['date'].date())
        db.session.add(event)
        db.session.commit()


        return {"message": "The event has been added!",
                "event": args['event'],
                "date": str(args['date'].date())}



class TodayEventResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return Event.query.filter(Event.date == datetime.date.today()).all()



class EventByID(Resource):

    @marshal_with(resource_fields)
    def get(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()

        if event is None:
            abort(404, "The event doesn't exist!")
        return event

    def put(self, event_id):
        args = parser.parse_args()
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")

        event.event = f"{args['event']}"
        event.date = args['date'].date()
        db.session.commit()
        return {"message": "The event has been updated"}

    def delete(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        Event.query.filter_by(id=event_id).delete()
        db.session.commit()
        return {"message": "The event has been deleted!"}


api.add_resource(EventByID, '/event/<int:event_id>')
api.add_resource(EventResource, '/event', '/')
api.add_resource(TodayEventResource, '/event/today')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()