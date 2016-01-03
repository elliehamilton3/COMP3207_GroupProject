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
import random

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
				userObj = User(key_name=userid, email=email)
				userObj.put()
				key = Key(name="Other", color="gray", user=userObj)
				key.put()
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
		if(self.session.get('user')):
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
		else:
			self.response.write(SPLASH_HTML)

class GroupCalendar(BaseHandler):
	def get(self):
		if(self.session.get('user')):
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
		else:
			self.response.write(SPLASH_HTML)


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
				
				keyObj = db.get(p.event_key.key())
				
				color = keyObj.color
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

				json_entry = {'id': id, 'title': title, 'start':start_time, 'end': end_time, 'location': location, 'color': color, 'textColor': text_color, 'borderColor': border_color, 'type': keyObj.name}

				# print json_entry

				json_list.append(json_entry)

		# return json_list
		return json.dumps(json_list)



class Feed(BaseHandler):
		def get(self):
				# Get user
				if(self.session.get('user')):
					userid = self.session.get('user')
					id = db.Key.from_path('User', userid)
					userObj = db.get(id)
			
					self.response.write(jsonfeed(self.request.get("start"), self.request.get("end"), userObj))
				else:
					self.response.write(SPLASH_HTML)

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
				keyObj = db.get(p.event_key.key())
				
				color = keyObj.color
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

				json_entry = {'id': p.key().id(), 'title': title, 'start':start_time, 'end': end_time, 'location': location, 'color': color, 'textColor': text_color, 'borderColor': border_color, 'type': keyObj.name}

				# print json_entry

				json_list.append(json_entry)

		# return json_list
		return json.dumps(json_list)



class GroupEventFeed(BaseHandler):
		def get(self):
				# Get user
				if(self.session.get('user')):
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
				else:
					self.response.write(SPLASH_HTML)


def taskjsonfeed(startDate, endDate, user):

		json_list = []
		q = user.task_user
		q.order('deadline')

		for p in q.run():
				title = p.name
				deadline = p.deadline
				
				keyObj = db.get(p.task_key.key())
				color = keyObj.color
				
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
				if(self.session.get('user')):
					userid = self.session.get('user')
					id = db.Key.from_path('User', userid)
					userObj = db.get(id)

					self.response.write(taskjsonfeed(self.request.get("start"), self.request.get("end"), userObj))
				else:
					self.response.write(SPLASH_HTML)

def grouptaskjsonfeed(startDate, endDate, group):

		json_list = []
		q = group.task_group
		q.order('deadline')

		for p in q.run():
				title = p.name
				deadline = p.deadline
				
				keyObj = db.get(p.task_key.key())
				color = keyObj.color
				
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
				if(self.session.get('user')):
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
				else:
					self.response.write(SPLASH_HTML)

def taskboxjsonfeed(startDate, endDate, user):

		json_list = []
		q = user.task_user
		q.order('deadline')

		for p in q.run():
				title = p.name
				deadline = p.deadline
				
				keyObj = db.get(p.task_key.key())
				color = keyObj.color
				
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
				if(self.session.get('user')):
					userid = self.session.get('user')
					id = db.Key.from_path('User', userid)
					userObj = db.get(id)

					self.response.write(taskboxjsonfeed(self.request.get("start"), self.request.get("end"), userObj))
				else:
					self.response.write(SPLASH_HTML)

def grouptaskboxjsonfeed(startDate, endDate, group):

		json_list = []
		q = group.task_group
		q.order('deadline')

		for p in q.run():
				title = p.name
				deadline = p.deadline
				keyObj = db.get(p.task_key.key())
				color = keyObj.color

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
				if(self.session.get('user')):
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
				else:
					self.response.write(SPLASH_HTML)

def groupjsonfeed(user):

		json_list = []
		q = user.groups

		for p in q:
				group = db.get(p)

				json_entry = {'key': str(group.key()), 'name': group.name, 'description': group.description}

				json_list.append(json_entry)

		# return json_list
		return json.dumps(json_list)


class GroupFeed(BaseHandler):
		def get(self):
				# Get user
				if(self.session.get('user')):
					userid = self.session.get('user')
					id = db.Key.from_path('User', userid)
					userObj = db.get(id)

					self.response.write(groupjsonfeed(userObj))
				else:
					self.response.write(SPLASH_HTML)

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
				if(self.session.get('user')):
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
				else:
					self.response.write(SPLASH_HTML)

class User(db.Model):
		#Model for representing a user.
		email = db.StringProperty(indexed=True)
		name = db.StringProperty(indexed=False)
		groups = db.ListProperty(db.Key)

class Group(db.Model):
	#Model for representing a group.
	name = db.StringProperty()
	description = db.TextProperty()
	invited = db.ListProperty(unicode)
	confirmed = db.ListProperty(unicode)
	
class Key(db.Model):
		name = db.StringProperty(indexed=False)
		color = db.StringProperty(indexed=False)
		user = db.ReferenceProperty(User, collection_name='keys', indexed=True)
		group = db.ReferenceProperty(Group, collection_name='keys', indexed=True)
		
class Event(db.Model):
		#Model for representing an individual event.
		name = db.StringProperty(indexed=False)
		start_time = db.DateTimeProperty(auto_now_add=False)
		end_time = db.DateTimeProperty(auto_now_add=False)
		location = db.StringProperty(indexed=False)
		#color = db.StringProperty(indexed=False)
		#event_type = db.StringProperty(
		#		choices=('module', 'sporting', 'society', 'job', 'other'))
		user = db.ReferenceProperty(User, collection_name='event_user')
		group = db.ReferenceProperty(Group, collection_name='event_group')
		event_key = db.ReferenceProperty(Key, collection_name='events', indexed=True)

class Task(db.Model):
		#Model for representing an individual task.
		name = db.StringProperty(indexed=False)
		deadline = db.DateTimeProperty(auto_now_add=False, indexed=True)
		#task_type = db.StringProperty(choices=('assignment', 'work', 'other'))
		user = db.ReferenceProperty(User, collection_name='task_user',indexed=True)
		group = db.ReferenceProperty(Group, collection_name='task_group', indexed=True)
		#color = db.StringProperty(indexed=False)
		task_key = db.ReferenceProperty(Key, collection_name='tasks', indexed=True)
		
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
		
		# Random colour from http://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
		color = "#%06x" % random.randint(0, 0xFFFFFF)
		logging.warn(color)
		key = Key(name=userObj.name + ' (' + userObj.email + ')', color=color, group=group)
		key.put()
		
		self.sendEmails(members, userObj, id, group_key, group)
		# Redirect back to calendar
		self.redirect(self.request.host_url + "/grouppage?group=" + str(group_key))

	def sendEmails(self, recipients, userObj, userId, group_key, group):
		groupid = group_key.id()
		sender_address = userObj.email
		for x in xrange (len(recipients)):
			q2 = User.all()
			q2.filter("email =", recipients[x])
			for p2 in q2.run():
				# Make sure they have an account so the key has their name
				mail.send_mail(sender=sender_address,
					to=recipients[x],
					subject="You've been invited to a group!",
					body= "You have been invited to a group on Sort My Life Out, confirm you want to join by clicking the link: http://testproj-1113.appspot.com/joingroup?groupid=%s&useremail=%s&groupkey=%s" % (str(groupid), recipients[x], group_key)
				)
				key = Key(name=p2.name +  ' (' + p2.email + ')', color="#%06x" % random.randint(0, 0xFFFFFF), group=group)
				key.put()
			
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
		
		self.sendEmails(members, userObj, id, group_key, group)
		# Redirect back to calendar
		self.redirect(self.request.host_url + "/grouppage?group=" + str(group_key) + '#members')

	# TODO - duplication is bad!
	def sendEmails(self, recipients, userObj, userId, group_key, group):
		groupid = group_key.id()
		sender_address = userObj.email
		for x in xrange (len(recipients)):
			q2 = User.all()
			q2.filter("email =", recipients[x])
			for p2 in q2.run():
				# Make sure they have an account so the key has their name
				mail.send_mail(sender=sender_address,
					to=recipients[x],
					subject="You've been invited to a group!",
					body= "You have been invited to a group on Sort My Life Out, confirm you want to join by clicking the link: http://testproj-1113.appspot.com/joingroup?groupid=%s&useremail=%s&groupkey=%s" % (str(groupid), recipients[x], group_key)
				)
				# Random colour from http://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
				color = "#%06x" % random.randint(0, 0xFFFFFF)
				logging.warn(color)
				key = Key(name=p2.name +  ' (' + p2.email + ')', color=color, group=group)
				key.put()
			
							
# EVENT METHODS

class NewEvent(BaseHandler):
		def post(self):
				#logging.warn("new event")
				event = Event()
			
				##id = db.Key.from_path('User', user.user_id())
				##groupId = db.Key.from_path('Group', self.request.get('group'))
				sDate = self.request.get('start_date')
				sTime = self.request.get('start_time')
				startDatetime = sDate + " " + sTime
				startDatetime = datetime.strptime(startDatetime, "%d/%m/%Y %H:%M")
				eDate = self.request.get('end_date')
				eTime = self.request.get('end_time')
				endDatetime = eDate + " " + eTime
				endDatetime = datetime.strptime(endDatetime, "%d/%m/%Y %H:%M")
				event.name = self.request.get('eventName')
				event.start_time = startDatetime
				event.end_time = endDatetime
				event.location = self.request.get('eventLocation')
								
				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)
					
				keykey = self.request.get('event_type')				
				key = db.Key(keykey)
				event.event_key = key
				
				event.user = userObj
				##event.group = db.get(groupId)
				event.put()
				# Redirect back to calendar
				self.redirect(self.request.host_url + "/calendar#events")

class NewGroupEvent(BaseHandler):
		def post(self):
				event = Event()

				sDate = self.request.get('start_date')
				sTime = self.request.get('start_time')
				startDatetime = sDate + " " + sTime
				startDatetime = datetime.strptime(startDatetime, "%d/%m/%Y %H:%M")
				eDate = self.request.get('end_date')
				eTime = self.request.get('end_time')
				endDatetime = eDate + " " + eTime
				endDatetime = datetime.strptime(endDatetime, "%d/%m/%Y %H:%M")
				event.name = self.request.get('eventName')
				event.start_time = startDatetime
				event.end_time = endDatetime
				event.location = self.request.get('eventLocation')

				keykey = self.request.get('event_type')				
				key = db.Key(keykey)
				event.event_key = key
				
				group = db.get(self.request.get('id'))
				event.group = group
				##event.group = db.get(groupId)
				event.put()
				# Redirect back to calendar
				self.redirect(self.request.host_url + "/grouppage?group=" + str(self.request.get('id') + '#events'))
				
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
			self.redirect(self.request.host_url + "/calendar#events")

class RemoveGroupEvent(BaseHandler):

		def post(self):
			logging.debug("Starting to delete an event.")

			event_id = self.request.get('event_id')
			logging.debug("The event to be deleted is: " + event_id)

			user = self.session.get('user')
			userKey = db.Key.from_path('User', user)
			userObj = db.get(userKey)

			# Security stuff - make sure they belong to the group their accessing
			q = userObj.groups
			groupid = self.request.get('group_id')

			for p in q:
				logging.warn(str(p))
				logging.warn(groupid)
			
				if( str(p) == groupid ):
					group = db.get(p)
					q2 = group.event_group
					for p2 in q2.run():
						logging.warn("here")
						logging.warn(p2.key().id())
						logging.warn(event_id)
						if str(p2.key().id()) == str(event_id):
							p2.delete()
							break;

			logging.debug("The event " + event_id + " should be deleted.")

			# Redirect back to calendar
			self.redirect(self.request.host_url + "/grouppage?group=" + str(self.request.get('group_id')) + '#events')
			
class GetEvent(BaseHandler):
		def get(self):
			if(self.session.get('user')):
				json_list = []
				event_id = self.request.get('eventid')
				logging.warn(event_id)

				user = self.session.get('user')
				userKey = db.Key.from_path('User', user)
				userObj = db.get(userKey)

				q = userObj.event_user
				for p in q.run():
					if str(p.key().id()) == str(event_id):
						start_time = p.start_time
						end_time = p.end_time

						start_time = start_time.strftime('%m') + "/" + start_time.strftime('%d') + "/" + start_time.strftime('%Y') + "T" + start_time.strftime('%H') + ":" + start_time.strftime('%M');
						end_time = end_time.strftime('%m') + "/" + end_time.strftime('%d') + "/" + end_time.strftime('%Y') + "T" + end_time.strftime('%H') + ":" + end_time.strftime('%M');
						
						json_entry = {'name': p.name, 'start_time':start_time, 'end_time': end_time, 'location': p.location, 'event_type': str(p.event_key.key())}
						json_list.append(json_entry)
						logging.warn(json_entry)

				self.response.write(json.dumps(json_list))
			else:
				self.response.write(SPLASH_HTML)

class GetGroupEvent(BaseHandler):
		def get(self):
			if(self.session.get('user')):
				json_list = []
				event_id = self.request.get('eventid')
				logging.warn(event_id)

				user = self.session.get('user')
				userKey = db.Key.from_path('User', user)
				userObj = db.get(userKey)

				# Security stuff - make sure they belong to the group their accessing
				q = userObj.groups
				groupid = self.request.get('groupid')

				for p in q:
			
					if( str(p) == groupid ):
						group = db.get(p)
						q2 = group.event_group
						for p2 in q2.run():
				
							if str(p2.key().id()) == str(event_id):
								start_time = p2.start_time
								end_time = p2.end_time

								start_time = start_time.strftime('%m') + "/" + start_time.strftime('%d') + "/" + start_time.strftime('%Y') + "T" + start_time.strftime('%H') + ":" + start_time.strftime('%M');
								end_time = end_time.strftime('%m') + "/" + end_time.strftime('%d') + "/" + end_time.strftime('%Y') + "T" + end_time.strftime('%H') + ":" + end_time.strftime('%M');
								
								json_entry = {'name': p2.name, 'start_time':start_time, 'end_time': end_time, 'location': p2.location, 'event_type': str(p2.event_key.key())}
								json_list.append(json_entry)
								logging.warn(json_entry)

				self.response.write(json.dumps(json_list))
			else:
				self.response.write(SPLASH_HTML)
				
				
class EditEvent(BaseHandler):
		def post(self):
			event_id = self.request.get('event_id')
			user = self.session.get('user')
			userKey = db.Key.from_path('User', user)
			userObj = db.get(userKey)

			q = userObj.event_user
			for p in q.run():
				if str(p.key().id()) == str(event_id):
					sDate = self.request.get('start_date')
					sTime = self.request.get('start_time')
					startDatetime = sDate + " " + sTime
					startDatetime = datetime.strptime(startDatetime, "%d/%m/%Y %H:%M")
					eDate = self.request.get('end_date')
					eTime = self.request.get('end_time')
					endDatetime = eDate + " " + eTime
					endDatetime = datetime.strptime(endDatetime, "%d/%m/%Y %H:%M")
					
					p.start_time = startDatetime
					p.end_time = endDatetime
					p.location = self.request.get('eventLocation')
					p.name = self.request.get('eventName')
					
					
					keykey = self.request.get('event_type')				
					key = db.Key(keykey)
					p.event_key = key
					
					p.user = userObj
					p.put()
					break;

			# Redirect back to calendar
			self.redirect(self.request.host_url + "/calendar#events")

class EditGroupEvent(BaseHandler):
		def post(self):
			event_id = self.request.get('event_id')
			
			user = self.session.get('user')
			userKey = db.Key.from_path('User', user)
			userObj = db.get(userKey)
			
			group = db.get(self.request.get('group_id'))
			
			q = group.event_group
			for p in q.run():
				if str(p.key().id()) == str(event_id):
					sDate = self.request.get('start_date')
					sTime = self.request.get('start_time')
					startDatetime = sDate + " " + sTime
					startDatetime = datetime.strptime(startDatetime, "%d/%m/%Y %H:%M")
					eDate = self.request.get('end_date')
					eTime = self.request.get('end_time')
					endDatetime = eDate + " " + eTime
					endDatetime = datetime.strptime(endDatetime, "%d/%m/%Y %H:%M")
					
					p.start_time = startDatetime
					p.end_time = endDatetime
					p.location = self.request.get('eventLocation')
					p.name = self.request.get('eventName')
					
					keykey = self.request.get('event_type')				
					key = db.Key(keykey)
					p.event_key = key
					
					p.user = userObj
					p.put()
					break;

			# Redirect back to calendar
			self.redirect(self.request.host_url + "/grouppage?group=" + str(self.request.get('group_id')) + '#events')

class DragEvent(BaseHandler):
	def get(self):
		if(self.session.get('user')):
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
			self.redirect(self.request.host_url + "/calendar#events")
		else:
			self.response.write(SPLASH_HTML)

class DragGroupEvent(BaseHandler):
	def get(self):
		if(self.session.get('user')):
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

			group = db.get(self.request.get('group_id'))
			
			q = group.event_group
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
			self.redirect(self.request.host_url + "/grouppage?group=" + str(self.request.get('group_id')) + '#events')
		else:
			self.response.write(SPLASH_HTML)



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
				deadline = datetime.strptime(deadlineDatetime, "%d/%m/%Y %H:%M")
				task.deadline = deadline
				task.name = self.request.get('taskName')

				keykey = self.request.get('task_type')				
				key = db.Key(keykey)
				task.task_key = key

				userid = self.session.get('user')
				id = db.Key.from_path('User', userid)
				userObj = db.get(id)
				task.user = userObj
				##task.group = db.get(groupId)
				task.put()
				# Redirect back to calendar
				self.redirect(self.request.host_url + "/calendar#tasks")


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
				deadline = datetime.strptime(deadlineDatetime, "%d/%m/%Y %H:%M")
				task.deadline = deadline
				task.name = self.request.get('taskName')
				
				keykey = self.request.get('task_type')				
				key = db.Key(keykey)
				task.task_key = key
				
				group = db.get(self.request.get('id'))
				task.group = group
				
				task.put()
				# Redirect back to calendar
				self.redirect(self.request.host_url + "/grouppage?group=" + str(self.request.get('id')) + '#tasks')
				

				
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
		if self.session.get('user'):
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
			self.redirect(self.request.host_url + "/calendar#groups")
		else:
			self.response.write(SPLASH_HTML)

class SetName(BaseHandler):
	def post(self):
		user = self.session.get('user')
		userKey = db.Key.from_path('User', user)
		userObj = db.get(userKey)
				
		userObj.name = self.request.get('name')
		
		logging.warn(self.request.get('name'));
		userObj.put()
		
		self.redirect(self.request.host_url + "/calendar#events")

class NewKey(BaseHandler):
	def post(self):
		user = self.session.get('user')
		userKey = db.Key.from_path('User', user)
		userObj = db.get(userKey)
		
		# Convert user's key json string into dictonary
		#keys = json.loads(userObj.keys)
		
		#key = {"key": self.request.get('name'), "color": self.request.get('color')}
		#keys.append(key)
		
		# Back to a JSON string
		#userObj.keys = json.dumps(keys)
		#userObj.put()
		
		key = Key(name=self.request.get('name'), color=self.request.get('color'), user=userObj)
		key.put()
		
		self.redirect(self.request.host_url + "/calendar#events")
		
class EditKey(BaseHandler):
		def post(self):
			key_id = self.request.get('key_id')
			user = self.session.get('user')
			userKey = db.Key.from_path('User', user)
			userObj = db.get(userKey)

			q = userObj.keys
			for p in q.run():
				if str(p.key()) == str(key_id):
					p.color = self.request.get('color')
					p.name = self.request.get('name')
					p.put()
					break;

			# Redirect back to calendar
			self.redirect(self.request.host_url + "/calendar#events")

class EditGroupKey(BaseHandler):
		def post(self):
			key_id = self.request.get('key_id')
			groupid = self.request.get('id')
									
			userid = self.session.get('user')
			id = db.Key.from_path('User', userid)
			userObj = db.get(id)
							
			# Security stuff - make sure they belong to the group their accessing
			q = userObj.groups
			json_list = []
			for p in q:
				if( str(p) == groupid ):
					group = db.get(p)
					keys = group.keys
			
					for p in keys.run():
						if str(p.key()) == str(key_id):
							p.color = self.request.get('color')
							p.put()
							break;

			# Redirect back to calendar
			self.redirect(self.request.host_url + "/grouppage?group=" + str(self.request.get('id')))

		
class GetKeys(BaseHandler):
	def get(self):
		if(self.session.get('user')):
			json_list = []
			
			user = self.session.get('user')
			userKey = db.Key.from_path('User', user)
			userObj = db.get(userKey)
			
			# Get user's keys
			keys = userObj.keys;
			
			for p in keys.run():
				json_entry = {'key': str(p.key()), 'name':p.name, 'color': p.color}
				json_list.append(json_entry)
			
			self.response.write(json.dumps(json_list))
		else:
			self.response.write(SPLASH_HTML)

class GetGroupKeys(BaseHandler):
	def get(self):
		if(self.session.get('user')):
			groupid = self.request.get('id')
									
			userid = self.session.get('user')
			id = db.Key.from_path('User', userid)
			userObj = db.get(id)
							
			# Security stuff - make sure they belong to the group their accessing
			q = userObj.groups
			json_list = []
			for p in q:
				if( str(p) == groupid ):
					group = db.get(p)
					keys = group.keys
			
					for p in keys.run():
						json_entry = {'key': str(p.key()), 'name':p.name, 'color': p.color}
						json_list.append(json_entry)

			self.response.write(json.dumps(json_list))
	
		else:
			self.response.write(SPLASH_HTML)

# Checks a user with a given email exists
class UserCheck(BaseHandler):
	def post(self):
		email = self.request.get('email')
		# Check the user isn't inviting themselves
		user = self.session.get('user')
		userKey = db.Key.from_path('User', user)
		userObj = db.get(userKey)
		
		if( userObj.email == email):
			self.response.write("You can't invite yourself!")
		else:
			q = User.all()
			q.filter("email =", email)
			if q.count(limit=1):
				# If we have a group id, check if the user is in it
				if self.request.get("group"):
					groupkey = self.request.get("group")
					group = db.get(groupkey)
				
					if email in group.invited:
						self.response.write("User has already been invited")
					elif email in group.confirmed:
						self.response.write("User already in group")
					else:
						self.response.write(True)
				else:
					self.response.write(True)
			else:
				self.response.write("No user found with that email address")


class EditGroup(BaseHandler):
	def post(self):
		group = db.get(self.request.get('id'))
		group.name = self.request.get('group_name')
		group.description = self.request.get('group_description')
		key = group.put()
		self.redirect(self.request.host_url + "/grouppage?group=" + str(key))				
			
class Logout(BaseHandler):
	def get(self):
		self.redirect(users.create_logout_url(self.request.host_url, _auth_domain=None))
		
class LeaveGroup(BaseHandler):
	def post(self):
		userKey = db.Key.from_path('User', self.session.get('user'))
		user = db.get(userKey)
		
		group = db.get(self.request.get('groupid'))
		
		# Shouldn't need to check, but better safe then sorry
		if user.email in group.confirmed:
			# Remove user from group's confirmed list
			group.confirmed.remove(user.email)
			group.put()
			
		# Remove group from user's group list
		if group.key() in user.groups:
			user.groups.remove(group.key())
			user.put()
			
		# Find the user's group key
		q = group.keys
		keyName = user.name + ' (' + user.email + ')' 
		for p in q: 
			if p.name == keyName:
				# Delete all events with this key
				q2 = Event.all()
				q2.filter("event_key =", p)
				for p2 in q2:
					p2.delete()
				# and the tasks
				q2 = Task.all()
				q2.filter("task_key =", p)
				for p2 in q2:
					p2.delete()

				# now delete the key
				p.delete()
				

class DeleteKey(BaseHandler):
	def post(self):
		userKey = db.Key.from_path('User', self.session.get('user'))
		user = db.get(userKey)
			
		# Find the key
		q = user.keys
		for p in q:
			if str(p.key()) == self.request.get('keyid'):
				# Delete all events with this key
				q2 = Event.all()
				q2.filter("event_key =", p)
				for p2 in q2:
					p2.delete()
				# and the tasks
				q2 = Task.all()
				q2.filter("task_key =", p)
				for p2 in q2:
					p2.delete()

				# now delete the key
				p.delete()		
			
app = webapp2.WSGIApplication([
		('/', Test),('/calendar', Calendar),('/event', NewEvent),('/feed', Feed), ('/taskfeed', TaskFeed),('/taskboxfeed', TaskBoxFeed),('/removetask', RemoveTask),('/getevent', GetEvent),('/editevent', EditEvent),('/task', NewTask),('/group', NewGroup),('/joingroup', JoinGroup),('/removeevent', RemoveEvent), ('/dragevent', DragEvent), ('/grouppage', GroupCalendar), ('/groupevent', NewGroupEvent), ('/group-event-feed', GroupEventFeed), ('/grouptask', NewGroupTask), ('/group-task-feed', GroupTaskFeed), ('/removegrouptask', RemoveGroupTask), ('/grouptaskboxfeed', GroupTaskBoxFeed), ('/groupfeed', GroupFeed), ('/memberfeed', MemberFeed), ('/invite', Invite), ('/name', SetName), ('/addkey', NewKey), ('/getkeys', GetKeys), ('/editkey', EditKey), ('/getgroupkeys', GetGroupKeys), ('/removegroupevent', RemoveGroupEvent),('/getgroupevent', GetGroupEvent),('/editgroupevent', EditGroupEvent), ('/draggroupevent', DragGroupEvent),('/editgroupkey', EditGroupKey), ('/checkuser', UserCheck), ('/logout', Logout), ('/editgroup', EditGroup), ('/leavegroup', LeaveGroup), ('/deletekey', DeleteKey)
], debug=True, config=config)