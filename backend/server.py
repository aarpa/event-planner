from flask import Flask, render_template, request, flash, redirect, session, jsonify, abort
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, User, Event, RSVP_Type, Invitation
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'something&super&duper&secretive'


# Standalone function to convert query result into dict
def as_dict(row):
       return {c.name: getattr(row, c.name) for c in row.__table__.columns}

# API routes and responses
# ------------------------------------------------------------------- #

@app.route('/api/users')
def get_all_users():
    """Return all users in a JSON format."""

    users = User.query.all()  # list of objs

    users_list = []

    for user in users:
        users_list.append(as_dict(user))

    return jsonify(users_list)

# ------------------------------------------------------------------- #

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    """Return a specific user's data in a JSON format."""

    user = User.query.get(user_id)

    if user:
        return as_dict(user)
    else:
        abort(404)

# ------------------------------------------------------------------- #

@app.route('/api/users', methods=['POST'])
def create_user():
    """Add a new user into database."""
    
    # POST reqs have a body, so extract out the parsed JSON data
    # Don't use HTML form requests --> request.form.args()
    req_body = request.get_json()

    # Note: ** is used to "spread" an object into keyword arguments, where (key=argument name), and (value=argument value)
    user = User(**req_body)

    db.session.add(user)
    db.session.commit()

    return {}

# ------------------------------------------------------------------- #

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a specific user using JSON data in request."""

    user = User.query.get(user_id)

    req_body = request.get_json()

    # Call instance method to update self by passing in the request body
    user.update(**req_body)

    db.session.commit()

    return as_dict(user)

# ------------------------------------------------------------------- #

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user from the DB."""

    del_user = User.query.get(user_id)

    if del_user:
        db.session.delete(del_user)
        db.session.commit()
    else:
        abort(404)

    return {}

# ------------------------------------------------------------------- #
@app.route('/api/users/<int:user_id>/hosted-events')
def get_user_hosted_events(user_id):
    """Return events hosted by a user in a JSON format."""

    user = User.query.get(user_id)

    events = user.events    # list of objs

    hosted_events = []

    for event in events:
        hosted_events.append(as_dict(event))

    return jsonify(hosted_events)


# ------------------------------------------------------------------- #

@app.route('/api/users/<int:user_id>/invites')
def get_user_invites(user_id):
    """Return events to which a user is invited in a JSON format."""

    user = User.query.get(user_id)

    invites = user.invites    # list of objs

    invites_list = []

    for invite in invites:
        invite_dict = as_dict(invite)
        
        # query in and add event details as another property of invite dict
        event = Event.query.get(invite_dict['event_id'])
        event_dict = as_dict(event)
        invite_dict['event'] = event_dict

        invites_list.append(invite_dict)

    return jsonify(invites_list)

# ------------------------------------------------------------------- #

@app.route('/api/events')
def get_all_events():
    """Return list of events in a JSON format."""

    events = Event.query.all()  # list of objs

    events_list = []

    for event in events:
        events_list.append(as_dict(event))

    return jsonify(events_list)

# ------------------------------------------------------------------- #

@app.route('/api/events/<int:event_id>')
def get_event(event_id):
    """Return a specific event in JSON format."""

    event = Event.query.get(event_id)

    if event:
        return as_dict(event)
    else:
        abort(404)

# ------------------------------------------------------------------- #

@app.route('/api/events/<int:event_id>/guests')
def get_event_guests(event_id):
    """Return users who are invited to an event in a JSON format."""

    event = Event.query.get(event_id)

    invites = event.invites

    guest_list = []

    for invite in invites:
        invite_dict = as_dict(invite)

        user = User.query.get(invite_dict['user_id'])
        user_dict = as_dict(user)

        guest_list.append(user_dict)

    return jsonify(guest_list)

# ------------------------------------------------------------------- #

@app.route('/api/events', methods=['POST'])
def create_event():
    """Add a new event into database."""
    
    # POST reqs have a body, so extract out the parsed JSON data
    # Don't use HTML form requests --> request.form.args()
    req_body = request.get_json()

    datetime_format = "%m/%d/%Y %H:%M"

    req_body['start_on'] = datetime.strptime(req_body['start_on'], datetime_format)
    req_body['end_on'] = datetime.strptime(req_body['end_on'], datetime_format)
    req_body['created_on'] = datetime.strptime(req_body['created_on'], datetime_format)


    # Note: ** is used to "spread" an object into keyword arguments, where (key=argument name), and (value=argument value)
    event = Event(**req_body)

    db.session.add(event)
    db.session.commit()

    return as_dict(event)

# ------------------------------------------------------------------- #

@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update a specific event using JSON data in request."""

    event = Event.query.get(event_id)

    req_body = request.get_json()

    # Call instance method to update self by passing in the request body
    event.update(**req_body)

    db.session.commit()

    return as_dict(event)

# ------------------------------------------------------------------- #

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event from the DB."""

    del_event = Event.query.get(event_id)

    if del_event:
        db.session.delete(del_event)
        db.session.commit()
    else:
        abort(404)

    return {}

# ------------------------------------------------------------------- #

@app.route('/api/rsvp-types')
def get_rsvp_types():
    """Return types of rsvp in a JSON format."""

    rsvp_types = RSVP_Type.query.filter_by(is_active=True).all()

    rsvp_types_list = []

    for obj in rsvp_types:
        rsvp_types_list.append(as_dict(obj))

    return jsonify(rsvp_types_list)

# ------------------------------------------------------------------- #

@app.route('/api/invites')
def get_all_invites():
    """Return list of invites in a JSON format."""

    invites = Invitation.query.all()  # list of objs

    invites_list = []

    for invite in invites:
        invites_list.append(as_dict(invite))

    return jsonify(invites_list)

# ------------------------------------------------------------------- #

@app.route('/api/invites', methods=['POST'])
def create_invite():
    """Add a new invite into database."""
    
    # POST reqs have a body, so extract out the parsed JSON data
    # Don't use HTML form requests --> request.form.args()
    req_body = request.get_json()

    # Note: ** is used to "spread" an object into keyword arguments, where (key=argument name), and (value=argument value)
    invite = Invitation(**req_body)

    db.session.add(invite)
    db.session.commit()

    return as_dict(invite)

# ------------------------------------------------------------------- #

@app.route('/api/invites/<int:invite_id>', methods=['PUT'])
def update_invite(invite_id):
    """Update a specific invite using JSON data in request."""

    invite = Invitation.query.get(invite_id)

    req_body = request.get_json()

    # Call instance method to update self by passing in the request body
    invite.update(**req_body)

    db.session.commit()

    return as_dict(invite)

# ------------------------------------------------------------------- #

if __name__ == "__main__":
  app.debug = True

  connect_to_db(app)

  DebugToolbarExtension(app)

  app.run(host="0.0.0.0")