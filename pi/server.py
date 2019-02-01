# from gpiozero import PWMLED
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import sqlite3
import json

db = sqlite3.connect('drinks.db')

# red = PWMLED(16)
# green = PWMLED(20)
# blue = PWMLED(21)

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser
class handler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):

		if self.path == '/pumps':
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			# Send the html message
			self.wfile.write('LIST OF DRINKS IN JSON')

		return

	def do_POST(self):

		if self.path == '/pumps':


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
	server.socket.close()
