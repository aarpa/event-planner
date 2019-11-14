"""Utility file to seed data in DB using data from /seed_data/ directory."""

import datetime
import sqlalchemy

from model import db, User, Event_Type, Event, RSVP_Type, Invitation, Image, Resource_Type, Resource, connect_to_db
from server import app

# -------------------------------------------------------- #
def load_users(user_filename):
  """Load users from user_data.csv into DB."""

    print("Users")

    for i, row in enumerate(open(user_filename)):
        row = row.rstrip()
        user_id, name, email, password, phone, dob = row.split("|")

        if email:
          is_registered = True
        else:
            is_registered = False

        # Instantiate user
        user = User(name=name, 
                    email=email, 
                    password=password, 
                    phone=phone, 
                    dob=dob,
                    is_registered=is_registered)


        # Add user to session
        db.session.add(user)


    # Commit all users to DB
    db.session.commit()


# -------------------------------------------------------- #
def create_event_types(filename):
  """Seed specific types of events in DB."""

    print("Event Types")

    for i, row in enumerate(open(filename)):
        row = row.rstrip()
        code, name, description, is_active = row.split("|")

        # Instantiate event types
        event_type = Event_Type(code=code,
                                name=name,
                                description=description,
                                is_active=is_active)

        # Add user to session
        db.session.add(event_type)

    # Commit all event type instances to DB
    db.session.commit()


# -------------------------------------------------------- #
def load_events(user_filename):
  """Load events from event_data.csv into DB."""

  # Write code here to loop over event data and populate DB.



# -------------------------------------------------------- #
def create_rsvp_types(filename):
  """Seed specific types of rsvps in DB."""

  # Write code here

    print("RSVP Types")

    for i, row in enumerate(open(filename)):
        row = rstrip()
        code, name, is_active = row.split("|")

        rsvp_type = RSVP_Type(code=code,
                              name=name,
                              is_active=is_active)

        # Add rsvp type to session
        db.session.add(rsvp_type)

    # Commit all rsvp type instances to DB
    db.session.commit()


# -------------------------------------------------------- #
def load_invites(invite_filename):
  """Load invite from invite_data.csv into DB."""

  # Write code here to loop over invite data and populate DB.



# -------------------------------------------------------- #
def create_resource_types():
  """Seed specific types of resources in DB."""

  # Write code here 



# -------------------------------------------------------- #
def load_resources(resource_filename):
  """Load resources from resource_data.csv into DB."""




# -------------------------------------------------------- #
def load_images(image_filename):
  """Load images from image_data.csv into DB."""

  # Write code here to loop over image data and populate DB.



# -------------------------------------------------------- #

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

