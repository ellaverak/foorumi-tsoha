# foorumi-tsoha

Tkt-tsoha project
heroku address: https://foorumi-tsoha22.herokuapp.com/

!TESTING INSTRUCTIONS!

TEST ADMIN:
- username: admin
- password: admin

TEST USER:
- username: user
- password: user

When testing the app you can also create a new user. Howerer all users are for testing and will most likely be deleted at some point during the app configuration process. If you cannot log in with your user, please create a new one.

USERS:
All users can:
- log in and out
- access public topics
- create threads
- reply to threads
- delete and edit threads that they have created
- delete and edit replys that they have send
- see the titles of secret topics
- access secret topics that they've been added to
- search replys

ADMIND:
All admins can do everything that a regular user can.
In addition admins can:
- see topic options
- create a new public topic
- create a new secret topic
- delete topics (the base topics cannot be deleted. These are: Jutustelu, Syvälliset, Kaveriseuraa, Apuja)


Continuation of Keskustelufoorumi-tsoha.

Teen keskustelufoorumin, jonka ominaisuudet ovat:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.

- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi   lähetetyn viestin ajankohdan.

- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.

- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.

- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. 
  Käyttäjä voi myös poistaa ketjun tai viestin. 

- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana. 

- Ylläpitäjä voi lisätä ja poistaa keskustelualueita. 

- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

Saatan yrittää lisätä foorumille vielä muita ominaisuuksia, esim: "palkintojen/kiitosten" jakaminen muille käyttäjille. Yksityisviestien lähettäminen.


Current state:

Base of the app has been created.

Registering is now possible.

First version of login/logout complited.

You can now see the amount of threads and replys every topic has. (The index still looks rough though.)

First actual versions of the main pages are ready. Threads and replys are visible.

Users can now create new threads and reply to existing threads.

Users can now edit and delete their replys.

Fixed dates, so that they appear in proper format.

Users can now edit the title and content of the threads that they have created. And delete them.

I have to figure out how to make redirecting work when deleting threads or replys!

Admins can delete topics and create new public topics.

Admins can create secret topics.

first version of search is working.
