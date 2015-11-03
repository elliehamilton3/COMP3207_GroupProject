import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb, db

import webapp2

TEST_HTML = """<html class="no-js" lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>COMP3207</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="stylesheet" href="css/bootstrap.min.css">
        <style>
            body {
                padding-top: 50px;
                padding-bottom: 20px;
            }
        </style>
        <link rel="stylesheet" href="css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="css/main.css">

        <script src="js/vendor/modernizr-2.8.3-respond-1.4.2.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.11.2.min.js"><\/script>')</script>

        <!-- Full Calendar imports -->
        	<link rel='stylesheet' href='js/fullcalendar/fullcalendar.css' />
			<script src='js/moment.js'></script>
			<script src='js/fullcalendar/fullcalendar.js'></script>
    </head>


    <body>
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">COMP3207</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <form class="navbar-form navbar-right" role="form">
            <div class="form-group">
              <input type="text" placeholder="Email" class="form-control">
            </div>
            <div class="form-group">
              <input type="password" placeholder="Password" class="form-control">
            </div>
            <button type="submit" class="btn btn-success">Sign in</button>
          </form>
        </div><!--/.navbar-collapse -->
      </div>
    </nav>
	
	<br><br>

    <div class="container">
        <div class="row">
            <div class="col-xs-12">
                <div class="btn-group" role="group" aria-label="...">
                  <button type="button" class="btn btn-default">Module Timetable</button>
                  <button type="button" class="btn btn-default">Events</button>
                  <button type="button" class="btn btn-default">Deadlines</button>
                  <button type="button" class="btn btn-default">Group Work Deadlines</button>
                </div>
            </div>
        </div>

        <br>

        <div class="row">
            <div class="col-xs-9">
                <div id='calendar'></div>
            </div>
            <div class="col-xs-3">

                <div class="panel panel-default">
                  <div class="panel-heading">Add/ edit contents</div>
                  <div class="panel-body">
                    <ul>
                        <li><a href="#">Add modules</a></li>
                        <li><a href="#">Add events</a></li>
                        <li><a href="#">Add assignment</a></li>
                    </ul>
                  </div>
                </div>

                <div class="panel panel-default">
                  <div class="panel-heading">Group Hub</div>
                  <div class="panel-body">
                    <ul>
                        <li><a href="#">Group 1</a></li>
                        <li><a href="#">Group 2</a></li>
                        <li><a href="#">Group 3</a></li>
                    </ul>
                  </div>
                </div>

                <div class="panel panel-default">
                  <div class="panel-heading">Deadlines</div>
                  <div class="panel-body">
                    <ul>
                        <li>Deadline 1 - 10/10/2015</li>
                        <li>Deadline 2 - 16/11/2015</li>
                        <li>Deadline 3 - 25/12/2015</li>
                    </ul>
                  </div>
                </div>

            </div>
        </div>
        
    </div>
	
	<div class="container">
	 	<hr>
     	<footer>
        	<p>&copy; Company 2015</p>
		</footer>
    </div> <!-- /container -->        

        <script src="js/vendor/bootstrap.min.js"></script>

        <script src="js/main.js"></script>
    </body>
</html>"""

class Test(webapp2.RequestHandler):
	def get(self):
		self.response.write(TEST_HTML)


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

class User(db.Model):
    #Model for representing a user.
    identity = db.StringProperty(indexed=False)
    email = db.StringProperty(indexed=False)
    name = db.StringProperty(indexed=False)
    groups = db.ListProperty(db.Key)


class Group(db.Model):
    #Model for representing a group.
    name = db.StringProperty()
    description = db.TextProperty()


class Event(db.Model):
    #Model for representing an individual event.
    name = db.StringProperty(indexed=False)
    date = db.DateTimeProperty(auto_now_add=False)
    location = db.StringProperty(indexed=False)
    event_type = db.StringProperty(
        choices=('module', 'sporting', 'society', 'job', 'other'))
    user = db.ReferenceProperty(User, collection_name='event_user')
    group = db.ReferenceProperty(Group, collection_name='event_group')


class Task(db.Model):
    #Model for representing an individual task.
    name = db.StringProperty(indexed=False)
    deadline = db.DateTimeProperty(auto_now_add=False)
    task_type = db.StringProperty(choices=('assignment', 'work', 'other'))
    user = db.ReferenceProperty(User, collection_name='task_user')
    group = db.ReferenceProperty(Group, collection_name='task_group')
    event = db.ReferenceProperty(Event, collection_name='linked_event')

# Here for reference only
'''class Guestbook (webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))
class League(BaseModel):
    name = ndb.StringProperty()    
    managers = ndb.ListProperty(ndb.Key) #all the users who can view/edit this league
    coaches = ndb.ListProperty(ndb.Key) #all the users who are able to view this league

    def get_managers(self):
        # This returns the models themselves, not just the keys that are stored in teams
        return UserPrefs.get(self.managers)

    def get_coaches(self):
        # This returns the models themselves, not just the keys that are stored in teams
        return UserPrefs.get(self.coaches)      

    def __str__(self):
        return self.name

    # Need to delete all the associated games, teams and players
    def delete(self):
        for player in self.leagues_players:
            player.delete()
        for game in self.leagues_games:
            game.delete()
        for team in self.leagues_teams:
            team.delete()            
        super(League, self).delete()

class UserPrefs(ndb.Model):
    user = ndb.UserProperty()
    league_ref = ndb.ReferenceProperty(reference_class=League,
                            collection_name='users') #league the users are managing

    def __str__(self):
        return self.user.nickname

    # many-to-many relationship, a user can coach many leagues, a league can be
    # coached by many users
    @property
    def managing(self):
        return League.gql('WHERE managers = :1', self.key())

    @property
    def coaching(self):
        return League.gql('WHERE coaches = :1', self.key())

    # remove all references to me when I'm deleted
    def delete(self):
        for manager in self.managing:
            manager.managers.remove(self.key())
            manager.put()
        for coach in self.managing:
            coach.coaches.remove(self.key())
            coaches.put()            
        super(UserPrefs, self).delete()    

'''
app = webapp2.WSGIApplication([
    ('/', Test),
], debug=True)