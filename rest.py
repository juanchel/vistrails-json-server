import web
import subprocess

urls = (
	'/vistrails', 'vistrails'
)

class vistrails:

	def POST(self):
		i = web.data()
		print i
		subprocess.call(['rm','-f','nodes.json'])
		subprocess.call(['rm','-f','/Users/chen/Desktop/result.txt'])

		with open('nodes.json', 'w') as f:
			f.write(i)

		subprocess.call(['python','translate.py'])
		subprocess.call(['python','/Users/chen/Desktop/vistrials/vistrails/run.py','-b','/Users/chen/Desktop/web-vt/nodes-to-vt/output.xml'])

		with open('/Users/chen/Desktop/result.txt', 'r') as f:
			s = f.read()
			f.close()

		web.header('Access-Control-Allow-Origin', '*')
		return s

if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()
