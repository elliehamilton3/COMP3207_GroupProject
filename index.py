import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb, db
from google.appengine.api import oauth
from oauth2client import client, crypt
from datetime import datetime, date, time
import logging
import traceback
import webapp2
from webapp2_extras import sessions
import json
import jinja2

config = {}
config['webapp2_extras.sessions'] = {
		'secret_key': '9876rujjhtfsgnbll8676543wsdlip',
}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('html'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

TEST_HTML = JINJA_ENVIRONMENT.get_template('calendar.html').render()
SPLASH_HTML = JINJA_ENVIRONMENT.get_template('splash.html').render()

class BaseHandler(webapp2.RequestHandler):
		def dispatch(self):
				# Get a session store for this request.
				self.session_store = sessions.get_store(request=self.request)

				try:
						# Dispatch the request.
						webapp2.RequestHandler.dispatch(self)
				finally:
						# Save all sessions.
						self.session_store.save_sessions(self.response)

		@webapp2.cached_property
		def session(self):
				# Returns a session using the default cookie key.
				return self.session_store.get_session()


class Calendar(BaseHandler):
	def post(self):
		try:
			logging.warn('posted')
			token = self.request.get('idtoken')
			email = self.request.get('email')
			idinfo = client.verify_id_token(token, '110052355668-ill69eihnsdnai3piq6445qvc0e19et6.apps.googleusercontent.com')
			# If multiple clients access the backend server:
			if idinfo['aud'] not in ['110052355668-ill69eihnsdnai3piq6445qvc0e19et6.apps.googleusercontent.com']:
				raise crypt.AppIdentityError("Unrecognized client.")
			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				raise crypt.AppIdentityError("Wrong issuer.")
			userid = idinfo['sub']
			logging.warn(userid)
			
			id = db.Key.from_path('User', userid)
			userObj = db.get(id)

			if userObj:
				self.session['user'] = userid
				# To get a value:
				sess = self.session.get('user')
				self.response.write(TEST_HTML)
			else:
				userObj = User(key_name=userid, email=email)
				userObj.put()
				self.session['user'] = userid
				# To get a value:
				sess = self.session.get('user')
				self.response.write(TEST_HTML)
			
			
		except crypt.AppIdentityError:
			# Invalid token
			self.response.write(SPLASH_HTML)
	def get(self):
		sess = self.session.get('user')
		self.response.write(TEST_HTML)


class Test(BaseHandler):
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

def jsonfeed(startDate, endDate, user):

		json_list = []
		q = user.event_user;
		# # Query interface constructs a query using instance methods
		#q = Event.all()
		# # q.filter("last_name =", "Smith")
		# # q.filter("height <=", max_height)
		# # q.order("-height")

		# # Query is not executed until results are accessed
		for p in q.run(limit=5):

				# for entry in entries:
				title = p.name
				start_time = p.start_time
				end_time = p.end_time

				start_time = start_time.strftime('%Y') + "-" + start_time.strftime('%m') + "-" + start_time.strftime('%d') + "T" + start_time.strftime('%H') + ":" + start_time.strftime('%M') + ":" + "00";
				end_time = end_time.strftime('%Y') + "-" + end_time.strftime('%m') + "-" + end_time.strftime('%d') + "T" + end_time.strftime('%H') + ":" + end_time.strftime('%M') + ":" + "00";

				json_entry = {'title': title, 'start':start_time, 'end': end_time}

				# print json_entry

				json_list.append(json_entry)

		# return json_list
		return json.dumps(json_list)



class Feed(BaseHandler):
		def get(self):
				# Get user
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)
		
				self.response.write(jsonfeed(self.request.get("start"), self.request.get("end"), userObj))


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
class NewEvent(BaseHandler):

        def post(self):
                logging.warn("new event")
                event = Event()
                ##id = db.Key.from_path('User', user.user_id())
                ##groupId = db.Key.from_path('Group', self.request.get('group'))
                sDate = self.request.get('start_date')
                sTime = self.request.get('start_time')
                startDatetime = sDate + " " + sTime
                startDatetime = datetime.strptime(startDatetime, "%m/%d/%Y %H:%M")
                eDate = self.request.get('end_date')
                eTime = self.request.get('end_time')
                endDatetime = eDate + " " + eTime
                endDatetime = datetime.strptime(endDatetime, "%m/%d/%Y %H:%M")
                event.name = self.request.get('name')
                event.start_time = startDatetime
                event.end_time = endDatetime
                event.location = self.request.get('location')
                event.event_type = self.request.get('event_type')
                userid = self.session.get('user')
                id = db.Key.from_path('User', userid)
                userObj = db.get(id)
                event.user = userObj
                ##event.group = db.get(groupId)
                event.put()

class NewTask(BaseHandler):
        
        def post(self):
                logging.warn("new task")
                task = Task()
                
                ##id = db.Key.from_path('User', user.user_id())
                ##groupId = db.Key.from_path('Group', self.request.get('group'))
                
                deadlineDate = self.request.get('deadline_date')
                deadlineTime = self.request.get('deadline_time')
                deadlineDatetime = deadlineDate + " " + deadlineTime
                deadline = datetime.strptime(deadlineDatetime, "%m/%d/%Y %H:%M")
                task.deadline = deadline
                task.name = self.request.get('task_name')
                task.task_type = self.request.get('task_type')
                userid = self.session.get('user')
                id = db.Key.from_path('User', userid)
                userObj = db.get(id)
                task.user = userObj
                ##task.group = db.get(groupId)
                task.put()


app = webapp2.WSGIApplication([
		('/', Test),('/calendar', Calendar),('/event', NewEvent),('/feed', Feed),('/task', NewTask)
], debug=True, config=config)