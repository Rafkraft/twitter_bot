### Iceberg Twitter Bot

![Img](http://twitterbotid.appspot.com/style/TBBI.png)

**Iceberg Twitter Bot** is a **Google App Engine** driven application allowing you to add a social e-commerce related functionnality to your Iceberg-linked platform. 

People who are part of the operation will be able to add items to their iceberg-linked website directly through the twitter feed, simply by responding to an admin account who will share new products pictures and url through twitter. This application is written in python, it listens to the twitter feed for a specific hashtag, **#Modizy_Bot** for example, when a tweet containing this hashtag is found, the username is compared to the datastore's usernames (datastore is google app engine's database), and if it is found it means that the user is part of the operation, product ID is recovered from the tweet the user responded to. And the product is added to its Iceberg cart through the iceberg Python API.

### Configuration

#### copy files

All these files have to be copied in a main Google App Engine root folder, and the default files can be erased.

#### app.yaml configuration

Rename app_public.yaml to app.yaml

* In the freshly renamed app.yaml file, add:
    * line 1: your google app engine application's name 
    * line 8: the email of the google account you are using with the current GAE Appllication
    * line 9: the hashtag you're going to listen to in the twitter feed
    * line 10: your website name
    * line 11->14 : your twitter api access keys (you have to have a verified twitter account to obtain these keys)
    * line 15 : a random secret key you'll be using to sign your POST requests

Your application, once deployed on google's servers, should be running and working.

#### add users

Your application is working, but no user have been added to your application, in order to add users to the program, you'll have to send POST requests to the /addUser route.

* You'll have to send POST requests to the /addUser route, this request must contain 7 precise fields:
    * twitterUsername: Twitter username (case sensitive)
    * lastName: last name
    * firstName: first name
    * mail: email adress
    * date1: day of birth (JJ)
    * date2: month of birth (MM)
    * date3: year of birth (YYYY)
    * message_auth: result of the sha1 hashing of all these variables, so the request is signed and secured, in our case, the variables are joined with a comma in a big string.
    * timestamp: time variable (not currently used)

This request method must be used to add users to the application, the main identifier for a user is the mail. It means that if a request is sent, and the mail is already taken, the twitter username will be updated.

