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


# JSON Feed

def jsonfeed(startDate, endDate, user):

		json_list = []
		q = user.event_user
		# # Query interface constructs a query using instance methods
		#q = Event.all()
		# # q.filter("last_name =", "Smith")
		# # q.filter("height <=", max_height)
		# # q.order("-height")

		# # Query is not executed until results are accessed
		for p in q.run():

				# for entry in entries:
				title = p.name
				start_time = p.start_time
				end_time = p.end_time
				color = p.color
				text_color = '#ffffff'
				border_color = ''
				color_int = ''

				if(color is not None):
					color_check = list(color)
					p = color_check.index("#")
					del(color_check[p])
					color_int = "0x".join(color_check)

					if(color_int > 0xffffff/2):
						text_color = '#000000'
						border_color = '#bbbbbb'

				start_time = start_time.strftime('%Y') + "-" + start_time.strftime('%m') + "-" + start_time.strftime('%d') + "T" + start_time.strftime('%H') + ":" + start_time.strftime('%M') + ":" + "00";
				end_time = end_time.strftime('%Y') + "-" + end_time.strftime('%m') + "-" + end_time.strftime('%d') + "T" + end_time.strftime('%H') + ":" + end_time.strftime('%M') + ":" + "00";

				json_entry = {'title': title, 'start':start_time, 'end': end_time, 'color': color, 'textColor': text_color, 'borderColor': border_color}

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


# JSON Feed

def taskjsonfeed(startDate, endDate, user):

		json_list = []
		q = user.task_user
		q.order('deadline')

		for p in q.run():
				title = p.name
				deadline = p.deadline
				color = p.color

				deadlineStr = deadline.strftime('%d') + " - " + deadline.strftime('%H') + ":" + deadline.strftime('%M')
				
				month = deadline.strftime('%B') + " " + deadline.strftime('%Y')

				json_entry = {'month': month, 'title': title, 'datetime':deadlineStr, 'color': color}

				json_list.append(json_entry)

		# return json_list
		return json.dumps(json_list)


class TaskFeed(BaseHandler):
		def get(self):
				# Get user
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)

				self.response.write(taskjsonfeed(self.request.get("start"), self.request.get("end"), userObj))


class User(db.Model):
		#Model for representing a user.
		email = db.StringProperty(indexed=False)
		name = db.StringProperty(indexed=False)
		groups = db.ListProperty(db.Key)


class Group(db.Model):
	#Model for representing a group.
	name = db.StringProperty()
	description = db.TextProperty()
	users = db.ListProperty(unicode)


class Event(db.Model):
		#Model for representing an individual event.
		name = db.StringProperty(indexed=False)
		start_time = db.DateTimeProperty(auto_now_add=False)
		end_time = db.DateTimeProperty(auto_now_add=False)
		location = db.StringProperty(indexed=False)
		color = db.StringProperty(indexed=False)
		event_type = db.StringProperty(
				choices=('module', 'sporting', 'society', 'job', 'other'))
		user = db.ReferenceProperty(User, collection_name='event_user')
		group = db.ReferenceProperty(Group, collection_name='event_group')


class Task(db.Model):
		#Model for representing an individual task.
		name = db.StringProperty(indexed=False)
		deadline = db.DateTimeProperty(auto_now_add=False, indexed=True)
		task_type = db.StringProperty(choices=('assignment', 'work', 'other'))
		user = db.ReferenceProperty(User, collection_name='task_user',indexed=True)
		group = db.ReferenceProperty(Group, collection_name='task_group')
		event = db.ReferenceProperty(Event, collection_name='linked_event')
		color = db.StringProperty(indexed=False)

class NewGroup(BaseHandler):
	def post(self):
		group = Group()
		group.name = self.request.get('group_name')
		group.description = self.request.get('group_description')
		members = self.request.get('group_members')
		userid = self.session.get('user')
		id = db.Key.from_path('User', userid)
		userObj = db.get(id)
		userEmail = userObj.email
		members = members.decode('unicode-escape')
		group.users = [userEmail, members]
		group.put()
		# Redirect back to calendar
		self.redirect(self.request.host_url + "/calendar")

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
				event.color = self.request.get('color2')
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)
				event.user = userObj
				##event.group = db.get(groupId)
				event.put()
				# Redirect back to calendar
				self.redirect(self.request.host_url + "/calendar")

class NewTask(BaseHandler):
		
		def post(self):
				logging.warn("new task")
				task = Task()
				
				##id = db.Key.from_path('User', user.user_id())
				##groupId = db.Key.from_path('Group', self.request.get('group'))
				
				deadlineDate = self.request.get('deadline_date')
				deadlineTime = self.request.get('deadline_time')
				logging.warn(deadlineTime)
				logging.warn(deadlineDate)
				if not deadlineTime:
					deadlineTime = "00:00"
					# no time do this
				# if not deadlineDate:
					# no date do this
				deadlineDatetime = deadlineDate + " " + deadlineTime
				deadline = datetime.strptime(deadlineDatetime, "%m/%d/%Y %H:%M")
				task.deadline = deadline
				task.name = self.request.get('task_name')
				task.color = self.request.get('color')
				logging.warn(self.request.get('color'))
				task.task_type = self.request.get('task_type')
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)
				task.user = userObj
				##task.group = db.get(groupId)
				task.put()
				# Redirect back to calendar
				self.redirect(self.request.host_url + "/calendar")


app = webapp2.WSGIApplication([
		('/', Test),('/calendar', Calendar),('/event', NewEvent),('/feed', Feed), ('/taskfeed', TaskFeed),('/task', NewTask),('/group', NewGroup)
], debug=True, config=config)