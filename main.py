import requests
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient 
from settings import *

class Connect():
	def __init__(self):
		self.session = requests.Session()

		self.verify()
		self.session_id = self.get_session()

	def verify(self):
		url = (base_url + 'verify.jsp?nonBrowser=true&username=%s&password=%s') % (username, password)
		cookies = dict(appName=app_name)
		self.session.get(url, cookies=cookies)
		print(self.session.cookies)

	def get_session(self):
		url = 'http://campus.hauppauge.k12.ny.us/campus/prism?x=portal.PortalOutline&appName=%s' % app_name
		cookies = dict(appName=app_name)

		self.session.get(url, cookies=cookies)

	def get_info(self):
		params = person_id, cal_id, (cal_id + 2), person_id, first_name, last_name, school_id, cal_id, (cal_id + 2)
		url = base_url + 'portal/portal.xsl?x=portal.PortalOutline&lang=en&context=%s-%s-%s&'\
		                 'personID=%s&firstName=%s&lastName=%s&schoolID=%s&mode=grades&calendarID=%s&'\
			             'structureID=%s&x=portal.PortalGrades' % (params)
		cookies = dict(appName=app_name, JSESSIONID=self.session_id)

		r = self.session.get(url, cookies=cookies)
		return r.text


def send_message(msg):
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	 
	client.messages.create(
	    to=number_to, 
	    from_=number_from, 
	    body=msg, 
	)

def check(i):
	tr = table.find_all('tr')[i]
	tds = tr.find_all('td')
	if (int(tds[0].get_text()) <= 60 and tds[1].get_text() == ' minutes ago'):
		send_message('%s on %s' % (tds[4].get_text(), tds[3].get_text()))
		check(i + 1)

connection = Connect()
document = connection.get_info()

soup = BeautifulSoup(document, 'html.parser')
table = soup.find(id='recentAssignments').find_all('table')[2]

check(0)