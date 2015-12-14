import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb, db
from google.appengine.api import oauth
from google.appengine.api import mail
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

#TEST_HTML = JINJA_ENVIRONMENT.get_template('calendar.html').render()
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
			else:
				userObj = User(key_name=userid, email=email, keys='[{"key":"other", "color":"gray"}]')
				userObj.put()
				self.session['user'] = userid
				
			template_values = {
				'user': userObj,
			}

			template = JINJA_ENVIRONMENT.get_template('calendar.html')
			self.response.write(template.render(template_values))

			
		except crypt.AppIdentityError:
			# Invalid token
			self.response.write(SPLASH_HTML)
	def get(self):
		
		sess = self.session.get('user')
		
		userid = self.session.get('user')
		id = db.Key.from_path('User', userid)
		userObj = db.get(id)
		
		template_values = {
			'user': userObj,
		}

		template = JINJA_ENVIRONMENT.get_template('calendar.html')
		self.response.write(template.render(template_values))

		#self.response.write(TEST_HTML)

class GroupCalendar(BaseHandler):
	def get(self):
		groupid = self.request.get("group")

		# Get user details
		userid = self.session.get('user')
		id = db.Key.from_path('User', userid)
		userObj = db.get(id)
		
		# Get user's groups
		q = userObj.groups
		logging.warn(q)
		for p in q:
			#logging.warn("here")
			logging.warn(str(p))
			#logging.warn(taskid)
			#if str(p.key().id()) == str(taskid):
			#	p.delete()
			#	break;
			if( str(p) == groupid ):
				group = db.get(p)
				#self.response.write(group.name)
				template_values = {
					'group': group,
				}

				template = JINJA_ENVIRONMENT.get_template('group-calendar.html')
				self.response.write(template.render(template_values))
				#self.response.write(TEST_HTML)
				return;
		
		self.response.write("Error - group id invalid or you do not belong to this group")


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
				id = p.key().id()
				title = p.name
				start_time = p.start_time
				end_time = p.end_time
				location = p.location
				event_type = p.event_type

				color = p.color
				text_color = '#ffffff'
				border_color = ''
				color_int = ''

				if(color is not None):
					color_check = list(color)

					try:
						x = color_check.index("#")
						del(color_check[x])
					except ValueError:
						pass
					
					color_int = "0x".join(color_check)

					if(color_int > 0xffffff/2):
						text_color = '#000000'
						border_color = '#bbbbbb'

				start_time = start_time.strftime('%Y') + "-" + start_time.strftime('%m') + "-" + start_time.strftime('%d') + "T" + start_time.strftime('%H') + ":" + start_time.strftime('%M') + ":" + "00";
				end_time = end_time.strftime('%Y') + "-" + end_time.strftime('%m') + "-" + end_time.strftime('%d') + "T" + end_time.strftime('%H') + ":" + end_time.strftime('%M') + ":" + "00";

				json_entry = {'id': id, 'title': title, 'start':start_time, 'end': end_time, 'location': location, 'color': color, 'textColor': text_color, 'borderColor': border_color, 'type': event_type}

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

def groupeventjsonfeed(startDate, endDate, group):

		json_list = []
		q = group.event_group
		# # Query interface constructs a query using instance methods
		#q = Event.all()
		# # q.filter("last_name =", "Smith")
		# # q.filter("height <=", max_height)
		# # q.order("-height")

		# # Query is not executed until results are accessed
		for p in q.run():
				logging.warn(p)

				# for entry in entries:
				title = p.name
				start_time = p.start_time
				end_time = p.end_time
				location = p.location
				event_type = p.event_type

				color = p.color
				text_color = '#ffffff'
				border_color = ''
				color_int = ''

				if(color is not None):
					color_check = list(color)
					
					try:
						x = color_check.index("#")					
						del(color_check[x])
					except ValueError:
						pass
						
					color_int = "0x".join(color_check)	
					if(color_int > 0xffffff/2):
						text_color = '#000000'
						border_color = '#bbbbbb'

				start_time = start_time.strftime('%Y') + "-" + start_time.strftime('%m') + "-" + start_time.strftime('%d') + "T" + start_time.strftime('%H') + ":" + start_time.strftime('%M') + ":" + "00";
				end_time = end_time.strftime('%Y') + "-" + end_time.strftime('%m') + "-" + end_time.strftime('%d') + "T" + end_time.strftime('%H') + ":" + end_time.strftime('%M') + ":" + "00";

				json_entry = {'title': title, 'start':start_time, 'end': end_time, 'location': location, 'color': color, 'textColor': text_color, 'borderColor': border_color, 'type': event_type}

				# print json_entry

				json_list.append(json_entry)

		# return json_list
		return json.dumps(json_list)



class GroupEventFeed(BaseHandler):
		def get(self):
				# Get user
				groupid = self.request.get('id')
								
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)
				
				logging.warn(groupid)
				
				# Security stuff
				# Get user's groups
				q = userObj.groups
				for p in q:
					logging.warn(p)

					#logging.warn("here")
					#logging.warn(p.key().id())
					#logging.warn(taskid)
					#if str(p.key().id()) == str(taskid):
					#	p.delete()
					#	break;
					if( str(p) == groupid ):
						group = db.get(p)
						logging.warn("IT@S A MATCH")
						self.response.write(groupeventjsonfeed(self.request.get("start"), self.request.get("end"), group))

						return;
								
# JSON Feed

def taskjsonfeed(startDate, endDate, user):

		json_list = []
		q = user.task_user
		q.order('deadline')

		for p in q.run():
				title = p.name
				deadline = p.deadline
				color = p.color
				keyid = p.key().id()

				deadlineTime = deadline.strftime('%H') + ":" + deadline.strftime('%M')
				if deadlineTime == "00:00":
						deadlineStr = deadline.strftime('%d')
				else:
						deadlineStr = deadline.strftime('%d') + " - " + deadlineTime
				
				month = deadline.strftime('%B') + " " + deadline.strftime('%Y')

				if month == "January 3000":
						month = "Other"
						deadlineStr = ""

				json_entry = {'month': month, 'title': title, 'datetime':deadlineStr, 'color': color, 'id': keyid}

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

def grouptaskjsonfeed(startDate, endDate, group):

		json_list = []
		q = group.task_group
		q.order('deadline')

		for p in q.run():
				title = p.name
				deadline = p.deadline
				color = p.color
				keyid = p.key().id()

				deadlineTime = deadline.strftime('%H') + ":" + deadline.strftime('%M')
				if deadlineTime == "00:00":
						deadlineStr = deadline.strftime('%d')
				else:
						deadlineStr = deadline.strftime('%d') + " - " + deadlineTime
				
				month = deadline.strftime('%B') + " " + deadline.strftime('%Y')

				if month == "January 3000":
						month = "Other"
						deadlineStr = ""

				json_entry = {'month': month, 'title': title, 'datetime':deadlineStr, 'color': color, 'id': keyid}

				json_list.append(json_entry)

		# return json_list
		return json.dumps(json_list)


class GroupTaskFeed(BaseHandler):
		def get(self):

				# Get user
				groupid = self.request.get('id')
								
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)
				
				logging.warn(groupid)
				
				# Security stuff
				# Get user's groups
				q = userObj.groups
				for p in q:
						logging.warn(p)

						#logging.warn("here")
						#logging.warn(p.key().id())
						#logging.warn(taskid)
						#if str(p.key().id()) == str(taskid):
						#	p.delete()
						#	break;
						if( str(p) == groupid ):
								group = db.get(p)
								logging.warn("IT@S A MATCH")
								self.response.write(grouptaskjsonfeed(self.request.get("start"), self.request.get("end"), group))

								return;

def taskboxjsonfeed(startDate, endDate, user):

		json_list = []
		q = user.task_user
		q.order('deadline')

		for p in q.run():
				title = p.name
				deadline = p.deadline
				color = p.color

				deadlineTime = deadline.strftime('%H') + ":" + deadline.strftime('%M')
				if deadlineTime == "00:00":
						deadlineStr = deadline.strftime('%B') + " " + deadline.strftime('%d')
				else:
						deadlineStr = deadline.strftime('%B') + " " + deadline.strftime('%d') + " - " + deadlineTime
		
				deadlineFinal = datetime.strptime("12/31/2999 00:00", "%m/%d/%Y %H:%M")

				if deadline < deadlineFinal:
					json_entry = {'title': title, 'datetime':deadlineStr, 'color': color}
					json_list.append(json_entry)

				if len(json_list) > 2:
						break;

		# return json_list
		return json.dumps(json_list)


class TaskBoxFeed(BaseHandler):
		def get(self):
				# Get user
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)

				self.response.write(taskboxjsonfeed(self.request.get("start"), self.request.get("end"), userObj))


def grouptaskboxjsonfeed(startDate, endDate, group):

		json_list = []
		q = group.task_group
		q.order('deadline')

		for p in q.run():
				title = p.name
				deadline = p.deadline
				color = p.color

				deadlineTime = deadline.strftime('%H') + ":" + deadline.strftime('%M')
				if deadlineTime == "00:00":
						deadlineStr = deadline.strftime('%B') + " " + deadline.strftime('%d')
				else:
						deadlineStr = deadline.strftime('%B') + " " + deadline.strftime('%d') + " - " + deadlineTime
		
				deadlineFinal = datetime.strptime("12/31/2999 00:00", "%m/%d/%Y %H:%M")

				if deadline < deadlineFinal:
					json_entry = {'title': title, 'datetime':deadlineStr, 'color': color}
					json_list.append(json_entry)

				if len(json_list) > 2:
						break;

		# return json_list
		return json.dumps(json_list)


class GroupTaskBoxFeed(BaseHandler):
		def get(self):
				# Get user
				groupid = self.request.get('id')
								
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)
				
				logging.warn(groupid)
				
				# Security stuff
				# Get user's groups
				q = userObj.groups
				for p in q:
						logging.warn(p)

						#logging.warn("here")
						#logging.warn(p.key().id())
						#logging.warn(taskid)
						#if str(p.key().id()) == str(taskid):
						#	p.delete()
						#	break;
						if( str(p) == groupid ):
								group = db.get(p)
								logging.warn("IT@S A MATCH")
								self.response.write(grouptaskboxjsonfeed(self.request.get("start"), self.request.get("end"), group))

								return;
def groupjsonfeed(user):

		json_list = []
		q = user.groups

		for p in q:
				group = db.get(p)
				
				name = group.name

				json_entry = {'key': str(group.key()), 'name': name}

				json_list.append(json_entry)

		# return json_list
		return json.dumps(json_list)


class GroupFeed(BaseHandler):
		def get(self):
				# Get user
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)

				self.response.write(groupjsonfeed(userObj))				

def memberjsonfeed(group):

		json_list = []
		q = group.confirmed

		for p in q:
				q2 = User.all()
				q2.filter("email =", p)

				for p2 in q2.run():
					json_entry = {'name': p2.name, 'email': p, 'status': 'Confirmed'}
					json_list.append(json_entry)

				
		q = group.invited
		
		for p in q:
				q2 = User.all()
				q2.filter("email =", p)

				for p2 in q2.run():
					json_entry = {'name': p2.name, 'email': p, 'status': 'Invited'}
					json_list.append(json_entry)
		
		# return json_list
		return json.dumps(json_list)


class MemberFeed(BaseHandler):
		def get(self):
				groupid = self.request.get('id')
								
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)
				
				logging.warn(groupid)
				
				# Security stuff
				# Get user's groups
				q = userObj.groups
				for p in q:
						logging.warn(p)

						#logging.warn("here")
						#logging.warn(p.key().id())
						#logging.warn(taskid)
						#if str(p.key().id()) == str(taskid):
						#	p.delete()
						#	break;
						if( str(p) == groupid ):
								group = db.get(p)
								logging.warn("IT@S A MATCH")
								self.response.write(memberjsonfeed(group))

								return;	
class User(db.Model):
		#Model for representing a user.
		email = db.StringProperty(indexed=True)
		name = db.StringProperty(indexed=False)
		groups = db.ListProperty(db.Key)
		
		# Store key-colour pairs in a json string as GAE can't store a dictonary/hash-map
		keys = db.StringProperty(indexed=False)


class Group(db.Model):
	#Model for representing a group.
	name = db.StringProperty()
	description = db.TextProperty()
	invited = db.ListProperty(unicode)
	confirmed = db.ListProperty(unicode)


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
		group = db.ReferenceProperty(Group, collection_name='task_group', indexed=True)
		color = db.StringProperty(indexed=False)

class URLInvite(db.Model):
	key = db.StringProperty
	userid = db.StringProperty

class NewGroup(BaseHandler):
	def post(self):
	
		logging.warn(self.request);
	
		group = Group()
		group.name = self.request.get('group_name')
		group.description = self.request.get('group_description')
		##members = self.request.get('group_members')
		userid = self.session.get('user')
		id = db.Key.from_path('User', userid)
		userObj = db.get(id)
		userEmail = userObj.email
		i = 1
		members = []
		self.response.write(members)
		while True:
			tmp = self.request.get('email' + str(i))
			self.response.write(tmp)
			if (len(tmp) > 0):
				tmp = tmp.decode('unicode-escape')
				members.append(tmp)
				self.response.write(members)
				i = i + 1
			else:
				break
		group.invited = members
		group.confirmed = [userEmail]
		group_key = group.put()
		userObj.groups.append(group_key)
		userObj.put()
		self.sendEmails(members, userObj, id, group_key)
		# Redirect back to calendar
		self.redirect(self.request.host_url + "/calendar")

	def sendEmails(self, recipients, userObj, userId, group_key):
		groupid = group_key.id()
		sender_address = userObj.email
		for x in xrange (len(recipients)):
			mail.send_mail(sender=sender_address,
							to=recipients[x],
							subject="You've been invited to a group!",
							body= "You have been invited to a group on Sort My Life Out, confirm you want to join by clicking the link: http://testproj-1113.appspot.com/joingroup?groupid=%s&useremail=%s&groupkey=%s" % (str(groupid), recipients[x], group_key)
							)

class Invite(BaseHandler):
	def post(self):
	
		group = db.get(self.request.get('id'))
		userid = self.session.get('user')
		id = db.Key.from_path('User', userid)
		userObj = db.get(id)
		userEmail = userObj.email
		i = 1
		members = []
		while True:
			tmp = self.request.get('email' + str(i))
			self.response.write(tmp)
			if (len(tmp) > 0):
				tmp = tmp.decode('unicode-escape')
				members.append(tmp)
				group.invited.append(tmp)
				self.response.write(members)
				i = i + 1
			else:
				break
		group_key = group.put()
		self.sendEmails(members, userObj, id, group_key)
		# Redirect back to calendar
		self.redirect(self.request.host_url + "/grouppage?group=" + str(group_key))

	# TODO - duplication is bad!
	def sendEmails(self, recipients, userObj, userId, group_key):
		groupid = group_key.id()
		sender_address = userObj.email
		for x in xrange (len(recipients)):
			mail.send_mail(sender=sender_address,
							to=recipients[x],
							subject="You've been invited to a group!",
							body= "You have been invited to a group on Sort My Life Out, confirm you want to join by clicking the link: http://testproj-1113.appspot.com/joingroup?groupid=%s&useremail=%s&groupkey=%s" % (str(groupid), recipients[x], group_key)
							)
							
							
# EVENT METHODS

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

class NewGroupEvent(BaseHandler):
		def post(self):
				event = Event()

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
				
				group = db.get(self.request.get('id'))
				event.group = group
				##event.group = db.get(groupId)
				event.put()
				# Redirect back to calendar
				self.redirect(self.request.host_url + "/grouppage?group=" + str(self.request.get('id')))
				
class RemoveEvent(BaseHandler):

		def post(self):
			logging.debug("Starting to delete an event.")

			event_id = self.request.get('event_id')
			logging.debug("The event to be deleted is: " + event_id)

			user = self.session.get('user')
			userKey = db.Key.from_path('User', user)
			userObj = db.get(userKey)

			q = userObj.event_user
			for p in q.run():
				logging.warn("here")
				logging.warn(p.key().id())
				logging.warn(event_id)
				if str(p.key().id()) == str(event_id):
					p.delete()
					break;

			logging.debug("The event " + event_id + " should be deleted.")

			# Redirect back to calendar
			self.redirect(self.request.host_url + "/calendar")


class DragEvent(BaseHandler):
	def get(self):

		logging.debug("Event dragged start")

		event_id = self.request.get('event_id')
		start = self.request.get('start')
		start = float(start) / 1000.00
		start = datetime.fromtimestamp(start)
		


		all_day = self.request.get('all_day')

		if(all_day == 'false'):
			end = self.request.get('end')
			end = float(end) / 1000.00
			end = datetime.fromtimestamp(end)
			

		# 	logging.debug("An event " + event_id + " has been dragged. All day is " + all_day + " and the new start and end date are " + start + " and " + end)
		# else:
		# 	logging.debug("An event " + event_id + " has been dragged. All day is " + all_day + " and the new start date is " + start)


		# Now get the event from the db and then update properties
		# eventKey = db.Key.from_path('Event', event_id)
		# eventObj = db.get(eventKey)

		user = self.session.get('user')
		userKey = db.Key.from_path('User', user)
		userObj = db.get(userKey)

		q = userObj.event_user
		for p in q.run():
			if str(p.key().id()) == str(event_id):
				p.start_time = start
				
				if(all_day == 'false'):
					p.end_time = end
				else:
					del p.end_time

				p.put()
				break;



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
				if not deadlineDate: 
					deadlineDate =  "1/1/3000"
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


class NewGroupTask(BaseHandler):
		
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
				if not deadlineDate: 
					deadlineDate =  "1/1/3000"
					# no date do this
				deadlineDatetime = deadlineDate + " " + deadlineTime
				deadline = datetime.strptime(deadlineDatetime, "%m/%d/%Y %H:%M")
				task.deadline = deadline
				task.name = self.request.get('task_name')
				task.color = self.request.get('color')
				logging.warn(self.request.get('color'))
				task.task_type = self.request.get('task_type')
				
				group = db.get(self.request.get('id'))
				task.group = group
				
				task.put()
				# Redirect back to calendar
				self.redirect(self.request.host_url + "/grouppage?group=" + str(self.request.get('id')))
				

				
class RemoveTask(BaseHandler):
		
		def post(self):
				user = self.session.get('user')
				userKey = db.Key.from_path('User', user)
				userObj = db.get(userKey)
				taskid = self.request.get('taskid')
				logging.warn(taskid);

				q = userObj.task_user
				for p in q.run():
						logging.warn("here")
						logging.warn(p.key().id())
						logging.warn(taskid)
						if str(p.key().id()) == str(taskid):
								p.delete()
								break;


class RemoveGroupTask(BaseHandler):
		
		def post(self):
				groupid = self.request.get('groupid')
				taskid = self.request.get('taskid')
				
				logging.warn(taskid);
				
				group = db.get(groupid)

				q = group.task_group
				for p in q.run():
						logging.warn("here")
						logging.warn(p.key().id())
						logging.warn(taskid)
						if str(p.key().id()) == str(taskid):
								p.delete()
								break;								
								
class JoinGroup(BaseHandler):

	def get(self):
		groupid = self.request.get("groupid")
		useremail = self.request.get("useremail")
		userid = self.request.get("userid")
		groupkey = self.request.get("groupkey")
		group = db.get(groupkey)

		confirmed = group.confirmed
		confirmed.append(useremail)
		group.confirmed = confirmed

		invited = group.invited

		if useremail in invited:
			invited.remove(useremail)
		group.invited = invited

		key = group.put()

		# Update user's group list
		q = User.all()
		q.filter("email =", useremail)

		for p in q.run():
			logging.warn(group)
			p.groups.append(key)
			p.put()

		# redirect to calendar
		self.redirect(self.request.host_url + "/calendar")
		
class SetName(BaseHandler):
	def post(self):
		user = self.session.get('user')
		userKey = db.Key.from_path('User', user)
		userObj = db.get(userKey)
				
		userObj.name = self.request.get('name')
		
		logging.warn(self.request.get('name'));
		userObj.put()
		
		self.redirect(self.request.host_url + "/calendar")

class NewKey(BaseHandler):
	def post(self):
		user = self.session.get('user')
		userKey = db.Key.from_path('User', user)
		userObj = db.get(userKey)
		
		# Convert user's key json string into dictonary
		keys = json.loads(userObj.keys)
		
		key = {"key": self.request.get('name'), "color": self.request.get('color')}
		keys.append(key)
		
		# Back to a JSON string
		userObj.keys = json.dumps(keys)
		userObj.put();
		
		self.redirect(self.request.host_url + "/calendar")
		
class GetKeys(BaseHandler):
	def get(self):
		user = self.session.get('user')
		userKey = db.Key.from_path('User', user)
		userObj = db.get(userKey)
		
		# Convert user's key json string into dictonary
		self.response.write(userObj.keys)
		

app = webapp2.WSGIApplication([

		('/', Test),('/calendar', Calendar),('/event', NewEvent),('/feed', Feed), ('/taskfeed', TaskFeed),('/taskboxfeed', TaskBoxFeed),('/removetask', RemoveTask),('/task', NewTask),('/group', NewGroup),('/joingroup', JoinGroup),('/removeevent', RemoveEvent), ('/dragevent', DragEvent), ('/grouppage', GroupCalendar), ('/groupevent', NewGroupEvent), ('/group-event-feed', GroupEventFeed), ('/grouptask', NewGroupTask), ('/group-task-feed', GroupTaskFeed), ('/removegrouptask', RemoveGroupTask), ('/grouptaskboxfeed', GroupTaskBoxFeed), ('/groupfeed', GroupFeed), ('/memberfeed', MemberFeed), ('/invite', Invite), ('/name', SetName), ('/addkey', NewKey), ('/getkeys', GetKeys)
], debug=True, config=config)