import sys

if 'libs' not in sys.path:
    sys.path[0:0] = ['libs']

import webapp2
import os
import urllib
import jinja2
import datetime
import tweepy

from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import db

from models import Operation

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

ckey ='XXXXXX'
csecret ='XXXXX'
atoken ='XXXXXXX'
asecret ='XXXXXXX'

auth=tweepy.OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

api = tweepy.API(auth)



def analyseTweet(tweet):

    #env variables
    admin_mail = os.environ['admin_mail']
    hashtag = os.environ['hashtag']
    website_name = os.environ['website_name']   

    # Variables   
    date_tweet = tweet.created_at
    twitter_username = tweet._json['user']['name']
    tweet_id = tweet.id
    tweet_message =  tweet.text
    mail_sent = False            

    user = None
    user_mail = False

    users = db.GqlQuery("SELECT * FROM User WHERE twitterUsername ='%s'" %(twitter_username) )

    for res in users:
        user_exists = True
        user = res
        user_mail = res.mail
        user_firstName = res.firstName

    if not user:
        print "user doesn't exists"
        return

    if not user.active:
        print 'account desactivated'
        return


    print "The user exists, great "

    operations = db.GqlQuery("SELECT * FROM Operation WHERE tweet_id =%s" %(478835117641957376) )
    for operation in operations:
        print 'tweet has already been taken into consideration'
        return

    #Obtain url from parent tweet
    product_url = False
    parent_id = tweet.in_reply_to_status_id
    parent_status = api.get_status(str(parent_id))
    for url in parent_status.entities['urls']:
        link = url['expanded_url']
        if application_name in link:
            product_url = link
    product_id = product_url.split('/')[-2]

    #Obtain size id there is one
    size = False
    for hashtag in tweet.entities['hashtags']:
        if hashtag['text'][0] == 'T' or hashtag['text'][0] == 't':
            size =  hashtag['text'].split('_')
            size = size[1]

    #Confirmation tweet
    if product_url:
        if size:
            print ' size '
            #api.update_status('Votre achat a ete enregistre, taille %s'%(size),tweet_id)
        else:
            print 'no size'
            #api.update_status('Votre achat a ete enregistre',tweet_id)
    if not size:
        size='none'

    #obtain today's date
    today = datetime.datetime.today()
    print today

    message = mail.EmailMessage(sender="Admin <%s>"%(admin_mail),
    subject="%s new command"%(hashtag))
    message.to = "%s <%s>" %(user_firstName,user_mail)
    message.body = """ Hi %s
    Your tweet has been taken in consideration and added tou your %s Cart
     """ %(user_firstName, application_name)
    message.send()
    mail_sent = True

    operation = Operation(
        tweet_id=int(tweet_id),
        tweet_message = tweet_message,
        iceberg_product_id = int(product_id),
        iceberg_offer_id = 0,
        iceber_variation = size,
        mail_sent=mail_sent,
        time_stamp=today,
        date=date_tweet,
        user=user
    )
    operation.put()


def getTweet(search_term, periods = 60*60*24):
    results = api.search(q=search_term, rpp=periods)
    for tweet in results:
        print '1 tweet found'
        analyseTweet(tweet)

    return results


class TweeterHandler(webapp2.RequestHandler):
    def get(self):
        looking_for = os.environ['hashtag']
        getTweet(looking_for)

        self.response.write('checking tweets')

app = webapp2.WSGIApplication([
    ('/checkTweets', TweeterHandler)
], debug=True)




