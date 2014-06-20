from google.appengine.ext import db

class User(db.Model):
    lastName = db.StringProperty()
    firstName = db.StringProperty()
    twitterUsername = db.StringProperty()
    timestamp = db.DateTimeProperty()
    mail = db.EmailProperty()
    active = db.BooleanProperty(default = True)


class Operation(db.Model):
    tweet_id = db.IntegerProperty()
    tweet_message = db.StringProperty()
    iceberg_product_id = db.IntegerProperty()
    iceberg_offer_id = db.IntegerProperty()
    iceber_variation = db.StringProperty()
    mail_sent=db.BooleanProperty()
    timestamp=db.DateTimeProperty() # Creation Date
    date = db.DateTimeProperty() # Tweet Date
    user = db.ReferenceProperty(User)


