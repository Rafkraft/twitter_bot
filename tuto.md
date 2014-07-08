## Twitter_bot

Si vous n'avez pas entendu parler de \#AmazonCart, c'est une fonctionnalité lancée par amazon permettant aux utilisateurs de twitter d'ajouter un produit à leur panier amazon directement depuis le fil d'actualité twitter, simplement en tweetant #AmazonCart en réponse à un tweet du compte officiel AmazonCart contenant un lien vers un produit amazon.

Le but de ce tutoriel sera de construire un script semblable en python, nous y ajouterons une fonctionnalité permettant aux utilisateurs de déterminer une taille avec le hashtag \#Taille_M par exemple. 

Nous utiliserons pour cela la plateforme de développement et d'hébergement d'application Google App Engine qui nous simplifiera le travail, notamment pour la gestion de la base de donnée.

La première étape consiste à construire le formulaire qui permet aux utilisateurs d'entrer leurs informations (compte twitter et email sont celles qui nous intéressent le plus). Grâce à cette correspondance, nous pourrons identifier l’émetteur du tweet contenant le hashtag #Modizy_Bot et ajouter l'article en question au panier du compte Amazon, Modizy ou autre.

### Prérequis 

Connectez-vous sur le site appengine.google.com, et installez le logiciel googleappenginelauncher sur votre ordinateur, créez une nouvelle application, elle contient par défaut 4 fichiers. Nous n'expliquerons comment créer l'application de A à Z, le projet est récupérable à cette [adresse](https://github.com/Rafkraft/twitter_bot).

### Configuration initiale:

Il est tout d'abord nécessaire de configurer votre fichier app.yaml, définissez les trois variables admin_mail, hashtag et website_name, ainsi que les clés de l'api twitter.

### Datastore

Nous utiliserons deux tables dans le datastore, la table «User» qui contiendra comme son nom l'indique les profils utilisateurs des inscrits ( pseudo, mail, compte actif, date de naissance ), et la table «Operation» qui contiendra les opérations effectuées par le script checkTweets.py , un modèle par tweet traité sera créé dans la table «Operation».

Avec google app engine, les tables sont des attributs de l'objet db, on les défini dans le fichier models.py .

## Main.py

Comme vous pouvez le voir dans les routes (handlers) c'est le fichier main.py qui est sollicité par défaut, c'est dans ce fichier que nous allons gérer les requêtes du formulaire qui permet aux utilisateurs d'entrer leurs informations dans la base de donnée.

La première fonction exécutée au sein de la classe MainHandler est la fonction get() qui va aller chercher et afficher le fichier home.html qui contient le formulaire en question. 

Une fois le formulaire rempli, et le bouton pressé c'est la fonction post qui est sollicitée, elle se divise en trois étapes:

### **\#verify twitter pseudo is not taken**

* Vérification que le pseudonyme n'est pas utilisé:
    * &nbsp;&nbsp;&nbsp; Si il l'est et que le compte est actif, un message d'erreur est envoyé.
    * &nbsp;&nbsp;&nbsp; Si il l'est et que le compte est inactif, le compte est activé et les données mises à jour.

### \#verify twitter mail is not taken

* Vérification que le mail n'est pas utilisé:
    * &nbsp;&nbsp;&nbsp; Si il l'est et que le compte est actif, un message d'erreur est envoyé.
    * &nbsp;&nbsp;&nbsp; Si il l'est et que le compte est inactif, le compte est activé et les données mises à jour.

### **\#Add user**

* Si ni le mail ni le pseudo n'est utilisé, un nouvel utilisateur est créé.

Un mail de confirmation est envoyé après l'ajout de l'utilisateur, via la fonction sendMail()

## unsubscribe.py

Nous allons nous occuper maintenant du formulaire qui permet à l'utilisateur de se désinscrire.
En réalité nous désactiveront seulement son compte.

Lorsqu'on demande l'url /unsubscribe, la fonction get dans la classe Unsubscribe est exécutée, elle va récupérer le formulaire unsubscribe.html, comme précédemment. 
Pour se désinscrire, il suffira de rentrer son pseudonyme twitter.
Une fois le champ rempli et le bouton pressé on cherche l'entity correspondant au Username twitter et on envoie les messages de confirmation/erreur selon les correspondances qui sont trouvées avec le datastore.

L'utilisateur n'est jamais vraiment désinscrit, son compte est seulement désactivé, l'attribut «Active» passe de True à False.

## CheckTweets.py

C'est le script qui va réaliser des requêtes envers l'api twitter, récupérer les tweets, identifier l'auteur, le comparer avec la base de donnée du datastore.

### Identification auprès de l'api twitter

![image](http://s9.postimg.org/4sez7y2e7/Capture_d_e_cran_2014_06_23_a_11_55_01.png)

Pour utiliser l'api twitter, il est nécessaire d'avoir déclaré les clés qui nous identifient auprès de l'api, les variables doivent être déclarée dans le fichier de configuration app.yaml, le script CheckTweets.py ne fait que récupérer les variables d'environnement.

### Récupération des tweets

![image](http://s4.postimg.org/3wv9jyujx/recup_tweets.png)

La première fonction qui s'exécute est TweetHandler, qui récupère le hashtag à chercher parmi le fil de tweets, et exécute la fonction getTweets.

La fonction getTweets utilise la fonction Tweepy api.search(), qui va retourner la liste des tweets contenant la variable hashtag définie dans le fichier app.yaml, la fonction analyseTweet() est exécutée pour chaque tweet trouvé.

### Analyse des tweets

![image](http://s3.postimg.org/sfhpjz01f/analyse_tweets.png)

On récupère d'abord les variables d'environnement et les attributs du tweet qui vont nous être utiles.

### \#determine if user exists

On recherche une correspondance entre l'auteur du tweet et notre base de donnée, si aucune correspondance n'est trouvée, un message d'erreur est envoyé.

### \#determine if operation has already been treated

Si une correspondance est bien trouvée, on peut lancer l'opération, une vérification est faite pour savoir si le tweet, identifié par son id unique, n'a pas déjà été traité.

### \#Obtain url from parent tweet

On récupère l'url présent dans le tweet parent, dans notre cas nous en extrayons l'id du produit en question. 

### \#Obtain size id there is one

On récupère la taille: tout ce qui se trouve après l'underscore dans le hashtag #Taille_      si il existe.

### \#Confirmation mail

On envoie un tweet de confirmation, on envoie un mail de confirmation. 

### \#add the operation to the datastore

On ajoute l'opération dans le datastore, la commande est alors traitée.

## Cron.yaml

À chaque fois que la page /checkTweets est sollicitée, un scan des tweets via l'api twitter est fait, nous allons maintenant automatiser cette tâche grâce au programme cron.

![image](http://s3.postimg.org/sfhpjz01f/analyse_tweets.png)

Il est très facile de configurer ce fichier: nommer la tâche, renseigner l'url du script qui doit être executé puis définir la fréquence, ici les tweets seront donc scannés toutes les 5 minutes.





