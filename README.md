# foorumi-tsoha

Tkt-tsoha project
heroku address: https://foorumi-tsoha22.herokuapp.com/

fly.io address: https://palsta.fly.dev/

!TESTING INSTRUCTIONS!

TEST ADMIN:
- username: admin
- password: admin

TEST USER:
- username: user
- password: user

When testing the app you can also create a new user. Howerer, all users are for testing and will most likely be deleted at some point during the app configuration process. If you cannot log in with your user, please create a new one.

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

ADMINS:

All admins can do everything that a regular user can.
In addition admins can:
- see topic options
- access all secret topics
- create a new public topic
- create a new secret topic and add users to the topic during creation
- add new users to a secret topic after the topic has been created
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
- Base of the app has been created.
- Registering is now possible.
- First version of login/logout complited.
- You can now see the amount of threads and replys every topic has. (The index still looks rough though.)
- First actual versions of the main pages are ready. Threads and replys are visible.
- Users can now create new threads and reply to existing threads.
- Users can now edit and delete their replys.
- Fixed dates, so that they appear in proper format.
- Users can now edit the title and content of the threads that they have created. And delete them.
- I have to figure out how to make redirecting work when deleting threads or replys!
- Admins can delete topics and create new public topics.
- Admins can create secret topics.
- first version of search is working.
- Search feature is fully working. Replys that are left on a thread in a secret topic do not show up in results.
- The creator of a secret topic can add new users to the topic after creation.
- All users who have access to a secret topic are listed on the topic site.
- FUNCTIONALITIES ARE READY! I may or may not add extra features later.
- Added the initial version of layout.html
- Fixed a lot of redirecting issues when creating a topic, deleting a topic etc.
- Finished navigation elements
- overall layout is about finished.
- frontpage layout is about finished.
- Most of the layouts are nearly finished.
- Navigation had some issues but it should work now.
- Added popup error messages and fixed regular error messages.
- Users can no longer access secret areas through the address bar if they aren't allowed into the area.
- CSRF-checks added. Security assets are now done.
- Code is now properly formatted.
- Fixed one final issue with registering. For some reason sql wouldn't raise an error when a username was already in use. Instead it created a transaction issue and the whole app chrashed. The fix isn't the best possible one, but it stops the app from chrashing.
