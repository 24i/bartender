from gpiozero import LED
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import sqlite3
import json
import collections

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

pump1 = LED(17)
pump2 = LED(27)
pump3 = LED(22)
pump4 = LED(23)
pump5 = LED(24)
pump6 = LED(25)

pump1.off()
pump2.off()
pump3.off()
pump4.off()
pump5.off()
pump6.off()

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser
class handler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):

		if self.path == '/start':
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()
			pump1.on()
			pump2.on()
			pump3.on()
			pump4.on()
			pump5.on()
			pump6.on()
			self.wfile.write('{"message":"start"}')
			return

		if self.path == '/end':
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()
			pump1.off()
			pump2.off()
			pump3.off()
			pump4.off()
			pump5.off()
			pump6.off()
			self.wfile.write('{"message":"start"}')
			return

		if self.path == '/pumps':
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()

			cursor.execute('SELECT * FROM pumps')
			pumps = cursor.fetchall()

			pumplist = []
			for pump in pumps:
				d = collections.OrderedDict()
				d['id'] = pump[0]
				d['drink'] = pump[1]
				pumplist.append(d)

			self.wfile.write(json.dumps(pumplist))
			return

		if self.path == '/recipes':
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()

			cursor.execute('SELECT * FROM recipes')
			recipes = cursor.fetchall()

			recipelist = []
			for recipe in recipes:
				r = collections.OrderedDict()
				r['id'] = recipe[0]
				r['name'] = recipe[1]
				recipelist.append(r)

			self.wfile.write(json.dumps(recipelist))
			return

	def do_POST(self):

		if self.path == '/recipes':
			content_len = int(self.headers.getheader('content-length', 0))
			body = json.loads(self.rfile.read(content_len))

			cursor.execute('INSERT INTO recipes(name) VALUES(?)', (body['name'],))
			for part in body['parts']:
				cursor.execute('INSERT INTO recipes_drinks(recipe_id, drink, percentage) VALUES(?, ?, ?)', (cursor.lastrowid, part['drink'].lower(), part['percentage']))

			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()
			self.wfile.write('{"message": "Recipe created"}')

			return

		if self.path == '/pour':
			content_len = int(self.headers.getheader('content-length', 0))
			body = json.loads(self.rfile.read(content_len))

			cursor.execute('SELECT drink FROM PUMPS')
			drinks = cursor.fetchall()
			drinkslist = []
			for drink in drinks:
				drinkslist.append(drink[0])

			for part in body['parts']:
				if part['drink'] not in drinkslist:
					self.send_response(400)
					self.send_header('Content-type','application/json')
					self.end_headers()
					self.wfile.write('{"message": "Non compatible drink"}')
					return

			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()
			self.wfile.write('{"message": "Drink pour started"}')


	def do_PUT(self):
		if self.path == '/pumps':
			content_len = int(self.headers.getheader('content-length', 0))
			body = json.loads(self.rfile.read(content_len))

			if body['id'] > 6:
				self.send_response(400)
				self.send_header('Content-type','application/json')
				self.end_headers()
				self.wfile.write('{"message": "This pump cannot be set"}')
				return

			cursor.execute('UPDATE pumps SET drink=? WHERE id=?', (body['drink'].lower(), body['id']))
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()
			self.wfile.write('{"message": "Pump updated"}')
		return


try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), handler)
	print 'Started httpserver on port ' , PORT_NUMBER

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	pump1.off()
	pump2.off()
	pump3.off()
	pump4.off()
	pump5.off()
	pump6.off()
	cursor.close()
	server.socket.close()
