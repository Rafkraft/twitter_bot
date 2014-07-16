## Twitter_bot

Si vous n'avez pas entendu parler de  , c'est une fonctionnalité lancée par amazon permettant aux utilisateurs de twitter d'ajouter un produit à leur panier amazon directement depuis le fil d'actualité twitter, simplement en tweetant #AmazonCart en réponse à un tweet du compte officiel AmazonCart contenant un lien vers un produit amazon.

Le but de ce tutoriel sera de construire un script semblable en python, nous y ajouterons une fonctionnalité permettant aux utilisateurs de déterminer une taille avec le hashtag \#Taille_M par exemple. 

Nous utiliserons pour cela la plateforme de développement et d'hébergement d'application Google App Engine qui nous simplifiera le travail, notamment pour la gestion de la base de donnée.

La première étape consiste à construire le formulaire qui permet aux utilisateurs d'entrer leurs informations (compte twitter et email sont celles qui nous intéressent le plus). Grâce à cette correspondance, nous pourrons identifier l’émetteur du tweet contenant le hashtag #Modizy_Bot et ajouter l'article en question au panier du compte Amazon, Modizy ou autre.

Le tutoriel se divisera en trois étapes:
*L'ajout des utilisateurs à la base de donnée (appelée datastore), et l'enregistrement des informations dont nous auront besoin: mail, nom, prénom et pseudonyme twitter. Ces informations nous permettront, de faire le lien entre l'auteur du tweet trouvés et le compte utilisateur sur notre utilisant la technologie Iceberg. Nous pourront ainsi intervenir sur son pannier via l'api Iceberg.
*Le scan périodique des tweets grâce à l'api twitter, l'identification de l'auteur et du compte Iceberg associé.
*L'ajout de l'article au pannier de l'utilisateur via l'api Iceberg.

### Prérequis

Connectez-vous sur le site appengine.google.com, et installez le logiciel googleappenginelauncher sur votre ordinateur, créez une nouvelle application, elle contient par défaut 4 fichiers. Nous n'expliquerons pas comment créer l'application de A à Z, le projet est récupérable à cette [adresse](https://github.com/Rafkraft/twitter_bot).

### Configuration initiale:

Il est tout d'abord nécessaire de configurer votre fichier app.yaml, définissez les trois variables admin_mail, hashtag et website_name, ainsi que les clés de l'api twitter et la variable PRIVATE_CRYPTO_KEY qui sera utilisée pour vérifier les requêtes POST reçues.

### Datastore

Nous utiliserons deux tables dans le datastore, la table «User» qui contiendra comme son nom l'indique les profils utilisateurs des inscrits ( pseudo, mail, compte actif, date de naissance ), et la table «Operation» qui contiendra les opérations effectuées par le script checkTweets.py , un modèle par tweet traité sera créé dans la table «Operation».

Avec google app engine, les tables sont des attributs de l'objet db, on les défini dans le fichier models.py .

## addUser.py

Comme vous pouvez le voir dans les routes (handlers dans le fichier app.yaml) c'est le fichier main.py qui est sollicité par défaut, cependant c'est dans le fichier addUser.py que nous allons gérer les requêtes POST reçues et ainsi ajouter nos utilisateurs au programme #Modizy_Bot.

Dans l'exemple ci-dessous, la requête est envoyée depuis un serveur node en utilisant le module request.js, l'important est quelle contienne les informations suivantes: dans l'ordre:
    *twitterUsername: Pseudonyme Twitter (la majuscule doit être respectée)
    *lastName: Nom de famille
    *firstName: Prénom
    *mail: Adresse email
    *date1: Jour de naissance
    *date2: Mois de naissance
    *date3: Année de naissance 
    *message_auth: résultat du hashing en sha1 de la chaîne de caractère toCompose contenant toutes les variables envoyées (de manière à signer la requête)
    *timestamp: variable de temps

<pre>
var timestamp = Math.round(+new Date()/1000);

var toCompose = [mail, firstName, lastName, twitterUsername, date1, date2, date3, timestamp];
toCompose = toCompose.join(';');
var message_auth = crypto.createHmac('sha1', secret_key).update(toCompose).digest('hex');

request({
    uri: "http://twitterbotid.appspot.com/addUser",
    method: "POST",
    form: {
        twitterUsername:XXXX,
        lastName:XXXX,
        firstName:XXXX,
        mail:XXXX,
        date1:XXX,
        date2:XXX,
        date3:XXX,
        message_auth:XXXX,
        timestamp:XXXX
    }
}, function(error, response, body) {
    console.log(body);
});
</pre>

À la réception, c'est la fonction post au sein de la classe addUser qui s'exécute:

### \#Get variables from post

Les variables sont récupérées, rien d'incroyable jusque là

### \#Hash data using the secret_key defined in app.yaml

Le hashing est réalisé à nouveau avec les variables récupérées, on fait appel à la variable d'environnement PRIVATE_CRYPTO_KEY, bien gardée dans le fichier app.yaml, puis, on compare la variable obtenue (message_auth) et la variable issue du hashing à l'emission (recieved_crypto), si elles diffèrent, un message d'erreur est envoyé et l'éxecution s'arrête.


### \#verify twitter mail is not taken

On vérifie que l'adresse mail reçue n'est pas déjà associée à un compte dans le datastore:
    *Si c'est le cas, les données sont mises à jour et aucun nouveau compte n'est créé.
    *Si l'adresse mail n'est pas utilisée, un nouveau compte est créé.

Des messages de confirmation sont envoyés selon l'action réalisée.


## CheckTweets.py

C'est le script qui va réaliser des requêtes envers l'api twitter, récupérer les tweets, identifier l'auteur, le comparer avec la base de donnée du datastore.

### Identification auprès de l'api twitter

<pre>
    ckey =os.environ['ckey']
    csecret =os.environ['csecret']
    atoken =os.environ['atoken']
    asecret =os.environ['asecret']

    auth=tweepy.OAuthHandler(ckey,csecret)
    auth.set_access_token(atoken,asecret)

    api = tweepy.API(auth)
</pre>

Pour utiliser l'api twitter, il est nécessaire d'avoir déclaré les clés qui nous identifient auprès de l'api, les variables doivent être déclarée dans le fichier de configuration app.yaml, le script CheckTweets.py ne fait que récupérer les variables d'environnement.

### Récupération des tweets

<pre>
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
</pre>

La première fonction qui s'exécute est TweetHandler, qui récupère le hashtag à chercher parmi le fil de tweets, et exécute la fonction getTweets.

La fonction getTweets utilise la fonction Tweepy api.search(), qui va retourner la liste des tweets contenant la variable hashtag définie dans le fichier app.yaml, la fonction analyseTweet() est exécutée pour chaque tweet trouvé.

### Analyse des tweets


On récupère d'abord les variables d'environnement et les attributs du tweet qui vont nous être utiles.

### \#determine if user exists

On recherche une correspondance entre l'auteur du tweet et notre base de donnée GAE, si aucune correspondance n'est trouvée, un message d'erreur est envoyé.

### \#determine if operation has already been treated

Si une correspondance est bien trouvée, on peut lancer l'opération, une vérification est faite pour savoir si le tweet, identifié par son id unique, n'a pas déjà été traité.

### \#Obtain url from parent tweet

On récupère l'url présent dans le tweet parent, dans notre cas nous extrayons avec la fonction split l'id du produit en question.

### \#Obtain size if there is one

On récupère la taille: tout ce qui se trouve après l'underscore dans le hashtag #Taille_      si il existe. Puis ont transmet les arguments nécéssaires à la fonction suivante: confirmation qui va confirmer l'opératio auprès de l'utilisateur par mail et twitter.

### \#Passing data to the Iceberg API

On exécute la fonction add_to_cart avec les quatre attributs dont elle a besoin: id du product à ajouter au pannier, mail, nom et prénom de l'utilisateur.

### \#Confirmation mail

On envoie un mail de confirmation. 

### \#Confirmation Tweet

On envoie un tweet de confirmation.

### \#add the operation to the datastore

On ajoute l'opération dans le datastore, de manière à ce qu'elle ne soit pas executée à nouveau au prochain scan. La commande est alors traitée.

## CartHandler

Nous passons maintenant à l'utilisation de l'API python Iceberg, solicitée par la fonction add_to_cart dans le fichier CartHandler.py . On peut en quelques lignes ajouter un produit au pannier d'un utilisateur donné.

<pre>
from icebergsdk.api import IcebergAPI

def add_to_cart(id,email,first_name,last_name):
    import logging
    logging.basicConfig(level=logging.DEBUG)

    api_handler = IcebergAPI()

    #Identification 
    api_handler.sso(email, first_name, last_name)

    #Get cart
    user_cart = api_handler.Cart.mine()

    #Find product
    product = api_handler.ProductOffer.find(id)
   
    #Add product to cart
    user_cart.addOffer(product)
</pre>

Après avoir importé le module Iceberg API, on s'identifie à la place de l'utilisateur avec les identifiants reçus en paramètre (pas besoin du mot de passe), on récupère le pannier, on trouve l'offre associée à l'id du produit, puis, on ajoute l'offre au pannier.

## Cron.yaml

À chaque fois que la page /checkTweets est sollicitée, un scan des tweets via l'api twitter est fait, nous allons maintenant automatiser cette tâche grâce au programme cron, paramétré dans le fichier cron.yaml.

<pre>
cron:
- description: check new tweets
  url: /checkTweets
  schedule: every 5 mins
</pre>

Il est très facile de configurer ce fichier: nommer la tâche, renseigner l'url du script qui doit être executé puis définir la fréquence, ici les tweets seront donc scannés toutes les 5 minutes.



Notre application est maintenant fonctionnelle, les tweets seront scannés toutes les cinq minutes, le produit identifié ajouté au pannier de l'utilisateur si celui-ci est bien partenaire de l'offre.

