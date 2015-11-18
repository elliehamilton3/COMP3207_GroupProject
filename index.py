import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb, db
from google.appengine.api import oauth
from oauth2client import client, crypt
import logging
import traceback
import webapp2
import datetime
import json



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

  			<script src="https://apis.google.com/js/platform.js" async defer></script>
        <meta name="google-signin-client_id" content="110052355668-ill69eihnsdnai3piq6445qvc0e19et6.apps.googleusercontent.com">

  			<script>
  			  function signOut() {
  			    var auth2 = gapi.auth2.getAuthInstance();
  			    auth2.signOut().then(function () {
  			      console.log('User signed out.');
  			    });
  			  }
  			</script>

        <!-- DatePicker -->
        <link rel='stylesheet' href='js/datepicker/css/bootstrap-datepicker.css' />
        <link rel='stylesheet' href='js/datepicker/css/bootstrap-datepicker.min.css' />
        <script src='js/datepicker/js/bootstrap-datepicker.js'></script>
        <script src='js/datepicker/js/bootstrap-datepicker.min.js'></script>
        <script src='js/datepicker/locales/bootstrap-datepicker.uk.min.js'></script>

        <!-- TimePicker -->
        <script src='js/timepicker/js/bootstrap-timepicker.min.js'></script>
        <link rel='stylesheet' href='js/timepicker/css/bootstrap-timepicker.min.css' />

        <!-- Drop Down Picker -->
        <script>
        $( document.body ).on( 'click', '.dropdown-menu li', function( event ) {

           var $target = $( event.currentTarget );

           $target.closest( '.btn-group' )
              .find( '[data-bind="label"]' ).text( $target.text() )
                 .end()
              .children( '.dropdown-toggle' ).dropdown( 'toggle' );

           return false;

        });
        </script>

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
        </div><!--/.navbar-collapse -->
      </div>
    </nav>
	
	<br><br>

    <div class="container">
        <div class="row">
            <div class="col-xs-9">
                <div class="btn-group btn-group-justified" role="group" aria-label="...">
                    <div class="btn-group" role="group">
                    <button type="button" class="btn btn-default">Module Timetable</button>
                  </div>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-default">Events</button>
                  </div>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-default">Deadlines</button>
                  </div>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-default">Group Work Deadlines</button>
                  </div>
                </div>
            </div>
        </div>

        <br>

        <div class="row">
            <div class="col-xs-9">
                <div id="calendar"></div>
            </div>
            <div class="col-xs-3">

                <div class="panel panel-default">
                  <div class="panel-heading">Add/ edit contents</div>
                  <div class="panel-body">
                    <ul>
                      <li><a href="#" data-toggle="modal" data-target="#addModuleModal">Add Events</a></li>

                      <!-- Modal -->
                      <div id="addModuleModal" class="modal fade" role="dialog">
                        <div class="modal-dialog">

                          <!-- Modal content-->
                          <div class="modal-content">
                            <div class="modal-header">
                              <button type="button" class="close" data-dismiss="modal">&times;</button>
                              <h4 class="modal-title">Add Modules</h4>
                            </div>
                            <div class="modal-body">

                              
                              <!-- Form within Modal -->
                              <form class="form-horizontal" role="form" method="post" action="/event">
                                <div class="row">

                                  <div class="col-lg-6">
                                   <div style="width:100%" class="input-group">
                                     <input type="text" name="name" placeholder="Event Name" class="form-control" aria-label="...">
                                     <br/>
                                     <br/>
                                     <div style="width:100%" class="btn-group btn-input clearfix">
                                      <select name="event_type" style="width:100%">
                                          <option value="module">Module</option>
                                          <option value="society">Society</option>
                                          <option value="job">Job</option>
                                          <option value="other">Other</option>
                                      </select>
                                    </div>
                                   
                                  </div><!-- /input-group -->
                                  <br/>
                                    <div class="input-group" style="width:100%">
                                      <input name="location" type="text" placeholder="Location - Building/Room Number" class="form-control" aria-label="...">
                                    </div><!-- /input-group -->
                                    <div class="col-sm-6">
                                      <div class="input-group" style-width:100%">
                                        <br>
                                        <p>Start Date & Time</p>
                                          <!-- date picker -->
                                              <input name="start_date" type="text" data-provide="datepicker" placeholder="Deadline Date" class="form-control" aria-label="...">
                                              <script>
                                                  $('.datepicker').datepicker()
                                              </script>
                                          <!-- date picker -->
                                          <br>
                                          <!-- time picker -->
                                              <input name="start_time" id="timepicker5" data-provide="timepicker" class="form-control" type="text" class="input-small">
                                          
                                          <script type="text/javascript"> 
                                              $('#timepicker5').timepicker({
                                                  showInputs: false,
                                                  minuteStep: 5,
                                                  showMeridian: false
                                              });
                                          </script>
                                          <!-- time picker -->
                                      </div>
                                    </div>
                                    <div class="col-sm-6">
                                      <div class="input-group" style-width:100%">
                                      </script>
                                        <br>
                                        <p>End Date & Time</p>
                                          <!-- date picker -->
                                              <input type="text" data-provide="datepicker" placeholder="Deadline Date" class="form-control" aria-label="...">
                                              <script>
                                                  $('.datepicker').datepicker()
                                              </script>
                                          <!-- date picker -->
                                          <br>
                                          <!-- time picker -->
                                              <input id="timepicker5" data-provide="timepicker" class="form-control" type="text" class="input-small">
                                              <i class="icon-time"></i>
                                          <!-- time picker -->
                                      </div>
                                    </div>
                                  </div><!-- /.col-lg-6 -->
                                </div><!-- /.row -->
                                <br/>
                                <br/>

                                <div class="modal-footer">
                                  <button type="submit" class="btn btn-default">Submit</button>
                                </form>     <!-- //Form within Modal -->
                              </div>
                            </div>
                          </div>
                          <!-- //Modal Content -->
                        </div>
                      </div>
                      <!-- //Modal -->


                      <li><a href="#" data-toggle="modal" data-target="#addAssignmentModal">Add assignment</a></li>
                      <!-- Modal -->
                      <div id="addAssignmentModal" class="modal fade" role="dialog">
                        <div class="modal-dialog">

                          <!-- Modal content-->
                          <div class="modal-content">
                            <div class="modal-header">
                              <button type="button" class="close" data-dismiss="modal">&times;</button>
                              <h4 class="modal-title">Add Assignments</h4>
                            </div>
                            <div class="modal-body">

                            <!-- Form within Modal -->
                            <form class="form-horizontal" role="form" action="/task">
                              <div class="row">

                                <div class="col-lg-6">
                                  <div style="width:100%" class="input-group">
                                    <input type="text" name="name" placeholder="Event Name" class="form-control" aria-label="...">
                                    <br/>
                                    <br/>

                                    <div style="width:100%" class="btn-group btn-input clearfix">
                                      <select name="task_type" style="width:100%">
                                          <option value="assignment">Assignment</option>
                                          <option value="work">Work</option>
                                          <option value="other">Other</option>
                                      </select>
                                    </div>
                                    
                                  </div><!-- /input-group -->
                                  <br>
                                  <div class="col-sm-6">
                                  <p>Start Date & Time</p>
                                    <!-- date picker -->
                                        <input type="text" data-provide="datepicker" placeholder="Deadline Date" class="form-control" aria-label="...">
                                        <script>
                                            $('.datepicker').datepicker()
                                        </script>
                                    <!-- date picker -->
                                    <br>
                                    <!-- time picker -->
                                        <input id="timepicker5" data-provide="timepicker" class="form-control" type="text" class="input-small">
                                        <i class="icon-time"></i>
                                    <!-- time picker -->
                                  </div>
                                  <div class="col-sm-6">
                                  <p>End Date & Time</p>
                                  <!-- date picker -->
                                      <input type="text" data-provide="datepicker" placeholder="Deadline Date" class="form-control" aria-label="...">
                                      <script>
                                          $('.datepicker').datepicker()
                                      </script>
                                  <!-- date picker -->
                                  <br>
                                  <!-- time picker -->
                                      <input id="timepicker5" data-provide="timepicker" class="form-control" type="text" class="input-small">
                                      <i class="icon-time"></i>
                                  <!-- time picker -->
                                  </div>
                                </div><!-- /.col-lg-6 -->
                              </div><!-- /.row -->
                            </form>
                            <!-- //Form within Modal -->

                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-default" data-dismiss="modal">Submit</button>
                            </div>
                          </div>
                          <!-- //Modal Content -->
                        </div>
                      </div>
                      <!-- //Modal -->
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

SPLASH_HTML = """<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Creative - Start Bootstrap Theme</title>

    <!-- Bootstrap Core CSS -->
    <link rel="stylesheet" href="css/bootstrap.min.css" type="text/css">

    <!-- Custom Fonts -->
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Merriweather:400,300,300italic,400italic,700,700italic,900,900italic' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css" type="text/css">

    <!-- Plugin CSS -->
    <link rel="stylesheet" href="css/animate.min.css" type="text/css">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="css/creative.css" type="text/css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
    <script src="https://apis.google.com/js/platform.js" async defer></script>
    <meta name="google-signin-client_id" content="110052355668-ill69eihnsdnai3piq6445qvc0e19et6.apps.googleusercontent.com">

    <script>
	    function onSignIn(googleUser) {
			var profile = googleUser.getBasicProfile();
        	var id_token = googleUser.getAuthResponse().id_token;
				console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
				console.log('Name: ' + profile.getName());
				console.log('Image URL: ' + profile.getImageUrl());
				console.log('Email: ' + profile.getEmail());
				
				var xhr = new XMLHttpRequest();
				xhr.open('POST', 'http://testproj-1113.appspot.com/calendar');
				xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
				xhr.onload = function() {
				  document.write(xhr.responseText);

				};
				xhr.send('idtoken=' + id_token);
				//window.location.replace('/calendar');

			}
		</script>
</head>

<body id="page-top">

    <header>
        <div class="header-content">
            <div class="header-content-inner" >
                <h1 style="color:black">Sort My Life Out</h1>
                <hr>
                <p style="color:black">Blah blah bio Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.</p>
                <div class="g-signin2" data-onsuccess="onSignIn"></div>
                <a href="login" class="btn btn-primary btn-xl page-scroll">Start Organising</a>
            </div>
        </div>
    </header>

    

    <!-- jQuery -->
    <script src="js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

    <!-- Plugin JavaScript -->
    <script src="js/jquery.easing.min.js"></script>
    <script src="js/jquery.fittext.js"></script>
    <script src="js/wow.min.js"></script>

    <!-- Custom Theme JavaScript -->
    <script src="js/creative.js"></script>

</body>

</html>
"""

class Calendar(webapp2.RequestHandler):
	def post(self):
		try:
			logging.warn('posted')
			token = self.request.get('idtoken')   
			idinfo = client.verify_id_token(token, '110052355668-ill69eihnsdnai3piq6445qvc0e19et6.apps.googleusercontent.com')
			# If multiple clients access the backend server:
			if idinfo['aud'] not in ['110052355668-ill69eihnsdnai3piq6445qvc0e19et6.apps.googleusercontent.com']:
				raise crypt.AppIdentityError("Unrecognized client.")
			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				raise crypt.AppIdentityError("Wrong issuer.")
			userid = idinfo['sub']
			logging.warn(userid)
			# self.response.write(userid)
			self.response.write(TEST_HTML)
		except crypt.AppIdentityError:
			# Invalid token
			self.response.write(SPLASH_HTML)
	def get(self):
		self.response.write(TEST_HTML)


class Test(webapp2.RequestHandler):
	def get(self):
		self.response.write(SPLASH_HTML)
		'''scope = 'https://www.googleapis.com/auth/userinfo.email'
		self.response.write('\noauth.get_current_user(%s)' % repr(scope))
		try:
			user = oauth.get_current_user(scope)
			allowed_clients = ['110052355668-ill69eihnsdnai3piq6445qvc0e19et6.apps.googleusercontent.com'] # list your client ids here
			token_audience = oauth.get_client_id(scope)
			if token_audience not in allowed_clients:
				raise oauth.OAuthRequestError('audience of token \'%s\' is not in allowed list (%s)'
																						% (token_audience, allowed_clients))
			self.response.write("<h1>User id is " + user.user_id() + "</h1>")
			self.response.write('- email       = %s\n' % user.email())
			self.response.write("<h1>User id is " + scope + "</h1>")
			if user:
				id = db.Key.from_path('User', user.user_id())
				self.response.write("<h1>User id is " + id.name() + "</h1>")
				userObj = db.get(id)
				if userObj:
					self.response.write("<h1>USER FOUND</h1>")
					self.response.write(TEST_HTML)
				else:
					userObj = User(key_name=user.user_id(), email=user.email(), name=user.nickname())
					userObj.put()
					self.response.write("<h1>USER CREATED</h1>")
					self.response.write(SPLASH_HTML)
			else:
				self.response.write(SPLASH_HTML)
		except oauth.OAuthRequestError, e:
			# self.response.write(SPLASH_HTML)
			self.response.set_status(401)
			self.response.write(' -> %s %s\n' % (e.__class__.__name__, e.message))
			logging.warn(traceback.format_exc())'''

		
		'''user = users.get_current_user()
		if user:
			id = db.Key.from_path('User', user.user_id())
			
			self.response.write("<h1>User id is" + id.name() + "</h1>")

			userObj = db.get(id)
			if userObj:
				self.response.write("<h1>USER FOUND</h1>")
				self.response.write(TEST_HTML)
			else:
				userObj = User(key_name=user.user_id(), email=user.email(), name=user.nickname())
				userObj.put()
				self.response.write("<h1>USER CREATED</h1>")
				self.response.write(SPLASH_HTML)
		else:
			self.response.write(SPLASH_HTML)'''


# JSON Feed

def jsonfeed(startDate, endDate):

    json_list = []

    # # Query interface constructs a query using instance methods
    q = Event.all()
    # # q.filter("last_name =", "Smith")
    # # q.filter("height <=", max_height)
    # # q.order("-height")

    # # Query is not executed until results are accessed
    for p in q.run(limit=5):

        # for entry in entries:
        title = p.name
        start_time = p.start_time
        end_time = p.end_time

        json_entry = {'title': title, 'start':start_time, 'end': end_time}

        # print json_entry

        json_list.append(json_entry)

    # return json_list
    return json.dumps(json_list)



class Feed(webapp2.RequestHandler):
    def get(self):
        self.response.write(jsonfeed(self.request.get("start"), self.request.get("end")))


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

class User(db.Model):
    #Model for representing a user.
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
    start_time = db.DateTimeProperty(auto_now_add=False)
    end_time = db.DateTimeProperty(auto_now_add=False)
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
class NewEvent(webapp2.RequestHandler):
    def post(self):
        logging.warn("new event")
        event = Event()
        
        ##id = db.Key.from_path('User', user.user_id())
        ##groupId = db.Key.from_path('Group', self.request.get('group'))
        
        date = self.request.get('start_date')
        time = self.request.get('start_time')
        
        logging.warn(date)
        logging.warn(time)
        
        event.name = self.request.get('name')
        ##event.date = self.request.get('date')
        event.location = self.request.get('location')
        event.event_type = self.request.get('event_type')
        ##event.user = db.get(id)
        ##event.group = db.get(groupId)
        event.put()

class NewTask(webapp2.RequestHandler):
    def post(self):
        logging.warn("new task")
        task = Task()
        
        ##id = db.Key.from_path('User', user.user_id())
        ##groupId = db.Key.from_path('Group', self.request.get('group'))
        
        ##logging.warn("found users")
        task.name = self.request.get('name')
        ##task.deadline = self.request.get('deadline')
        task.location = self.request.get('location')
        task.task_type = self.request.get('task_type')
        ##task.user = db.get(id)
        ##task.group = db.get(groupId)
        task.put()


app = webapp2.WSGIApplication([
    ('/', Test),('/calendar', Calendar),('/event', NewEvent),('/feed', Feed),('/task', NewTask)
], debug=True)
