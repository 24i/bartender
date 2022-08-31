from gpiozero import Device,OutputDevice
from http.server import BaseHTTPRequestHandler,HTTPServer
import sqlite3
import json
import collections
import sys
from threading import Timer

from gpiozero.pins.mock import MockFactory
args = sys.argv[1:]

try:
	if (args[0] == 'local'):
		Device.pin_factory = MockFactory()
except:
	print("Running in PI mode")

db = sqlite3.connect('drinks.db')
cursor = db.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS pumps (id INTEGER PRIMARY KEY, drink TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS recipes_drinks (recipe_id INTEGER, drink TEXT, percentage INTEGER, PRIMARY KEY (recipe_id, drink))')

## Setup all pump values
pumps = [ (1, 'UNKNOWN'), (2, 'UNKNOWN'), (3, 'UNKNOWN'), (4, 'UNKNOWN'), (5, 'UNKNOWN'), (6, 'UNKNOWN') ]
cursor.executemany('INSERT OR IGNORE INTO pumps(id,drink) VALUES(?,?)', pumps)

# red = PWMLED(16)
# green = PWMLED(20)
# blue = PWMLED(21)

pump1 = OutputDevice(17, active_high=False)
pump2 = OutputDevice(16, active_high=False)
pump3 = OutputDevice(22, active_high=False)
pump4 = OutputDevice(23, active_high=False)
pump5 = OutputDevice(24, active_high=False)
pump6 = OutputDevice(26, active_high=False)

# pump1.off()
# pump2.off()
# pump3.off()
# pump4.off()
# pump5.off()
# pump6.off()

PORT_NUMBER = 8080

BASELINE_TIMING_AMOUNT = 100 # Baseline amount of ML
BASELINE_TIMING_TIME = 5 # Baseline seconds for amount

#This class will handles any incoming request from
#the browser
class handler(BaseHTTPRequestHandler):

	def default_headers(self):
		self.send_header('Content-type','application/json')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,OPTIONS')
		self.send_header('Access-Control-Allow-Headers', 'Content-Type')

	def do_OPTIONS(self):
		self.send_response(200)
		self.default_headers()
		self.end_headers()
		return

	#Handler for the GET requests
	def do_GET(self):

		if self.path == '/pumps':
			self.send_response(200)
			self.default_headers()
			self.end_headers()

			cursor.execute('SELECT * FROM pumps')
			pumps = cursor.fetchall()

			pumplist = []
			for pump in pumps:
				d = collections.OrderedDict()
				d['id'] = pump[0]
				d['drink'] = pump[1]
				pumplist.append(d)

			self.wfile.write(bytes(json.dumps(pumplist), 'utf-8'))
			return

		if self.path == '/recipes':
			self.send_response(200)
			self.default_headers()
			self.end_headers()

			cursor.execute('SELECT * FROM recipes')
			recipes = cursor.fetchall()

			recipelist = []
			for recipe in recipes:
				r = collections.OrderedDict()
				r['id'] = recipe[0]
				r['name'] = recipe[1]
				recipelist.append(r)

			self.wfile.write(bytes(json.dumps(recipelist), 'utf-8'))
			return

	def do_POST(self):

		if self.path == '/test_pump':
			content_len = int(self.headers.get('content-length', 0))
			body = json.loads(self.rfile.read(content_len))
			pump = globals()['pump' + body['pump']]
			method = getattr(pump, body['method'])
			method(pump)

		if self.path == '/recipes':
			content_len = int(self.headers.get('content-length', 0))
			body = json.loads(self.rfile.read(content_len))

			cursor.execute('INSERT INTO recipes(name) VALUES(?)', (body['name'],))
			for part in body['parts']:
				cursor.execute('INSERT INTO recipes_drinks(recipe_id, drink, percentage) VALUES(?, ?, ?)', (cursor.lastrowid, part['drink'].lower(), part['percentage']))
			db.commit()

			self.send_response(200)
			self.default_headers()
			self.end_headers()
			self.wfile.write(bytes('{"message": "Recipe created"}', 'utf-8'))

			return

		if self.path == '/pour-recipe':
			content_len = int(self.headers.get('content-length', 0))
			body = json.loads(self.rfile.read(content_len))

			cursor.execute('SELECT drink FROM PUMPS ORDER BY id ASC')
			drinks = cursor.fetchall()
			drinkslist = []
			for drink in drinks:
				drinkslist.append(drink[0])

			cursor.execute('SELECT drink,percentage from recipes_drinks WHERE recipe_id=?', str(body['recipeId']))
			parts = cursor.fetchall()

			pumps = []
			for part in parts:
				if part[0] not in drinkslist:
					self.send_response(400)
					self.default_headers()
					self.end_headers()
					self.wfile.write(bytes('{"message": "Non compatible drink"}', 'utf-8'))
					return
				else:
					# Yes this is really really shitty, but it works and I can't be arsed
					# to do it properly
					pumps.append({
						'number': drinkslist.index(part[0]) + 1,
						'percentage': part[1]
					})

			self.send_response(200)
			self.default_headers()
			self.end_headers()

			# Turn on each pump that we have in our given recipe
			for pump in pumps:
				globals()['pump' + str(pump['number'])].on()

			for pump in pumps:
				time_for_pump = ( ( ( body['amount'] / 100 ) * pump['percentage'] ) / BASELINE_TIMING_AMOUNT ) * BASELINE_TIMING_TIME
				timer = Timer(time_for_pump, turn_off, ['pump' + str(pump['number'])])
				timer.start();

			self.wfile.write(bytes('{"message": "Drink pour started", "time": ' + str(time_for_pump) + '}', 'utf-8'))
		
		if self.path == '/pour':
			content_len = int(self.headers.get('content-length', 0))
			body = json.loads(self.rfile.read(content_len))

			cursor.execute('SELECT drink FROM PUMPS ORDER BY id ASC')
			drinks = cursor.fetchall()
			drinkslist = []
			for drink in drinks:
				drinkslist.append(drink[0])

			pumps = []
			for part in body['parts']:
				if part['drink'] not in drinkslist:
					self.send_response(400)
					self.default_headers()
					self.end_headers()
					self.wfile.write(bytes('{"message": "Non compatible drink"}', 'utf-8'))
					return
				else:
					# Yes this is really really shitty, but it works and I can't be arsed
					# to do it properly
					pumps.append({
						'number': drinkslist.index(part['drink']) + 1,
						'percentage': part['percentage']
					})

			self.send_response(200)
			self.default_headers()
			self.end_headers()

			# Turn on each pump that we have in our given recipe
			for pump in pumps:
				globals()['pump' + str(pump['number'])].on()

			for pump in pumps:
				time_for_pump = ( ( ( body['amount'] / 100 ) * pump['percentage'] ) / BASELINE_TIMING_AMOUNT ) * BASELINE_TIMING_TIME
				timer = Timer(time_for_pump, turn_off, ['pump' + str(pump['number'])])
				timer.start();

			self.wfile.write(bytes('{"message": "Drink pour started"}', 'utf-8'))


	def do_PUT(self):
		if self.path == '/pumps':
			content_len = int(self.headers.get('content-length', 0))
			body = json.loads(self.rfile.read(content_len))

			if body['id'] > 6:
				self.send_response(400)
				self.default_headers()
				self.end_headers()
				self.wfile.write(bytes('{"message": "This pump cannot be set"}', 'utf-8'))
				return

			cursor.execute('UPDATE pumps SET drink=? WHERE id=?', (body['drink'].lower(), body['id']))
			db.commit()

			self.send_response(200)
			self.default_headers()
			self.end_headers()
			self.wfile.write(bytes('{"message": "Pump updated"}', 'utf-8'))
		return

def turn_off(pump):
	globals()[pump].off()

def main(argv):
	try:
		#Create a web server and define the handler to manage the
		#incoming request
		server = HTTPServer(('', PORT_NUMBER), handler)
		print('Started httpserver on port ' , PORT_NUMBER)

		#Wait forever for incoming htto requests
		server.serve_forever()

	except KeyboardInterrupt:
		print('^C received, shutting down the web server')
		pump1.off()
		pump2.off()
		pump3.off()
		pump4.off()
		pump5.off()
		pump6.off()
		cursor.close()
		server.socket.close()

if __name__ == "__main__":
   main(sys.argv[1:])
