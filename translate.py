import json
import xml.etree.ElementTree as ElementTree
from pprint import pprint

from link import Link
from module import Module

# Go from web name to vt name
def rename(name):
	return {
		'Integer' : 'Integer',
		'String' : 'String',
		'List' : 'List',
		'ConcatenateString' : 'ConcatenateString',
		'WriteFile' : 'WriteFile',
		'FileSink' : 'FileSink',
		'Sum' : 'Sum'
	}[name]

# Get the package name from the vt name
def get_package(name):
	return {
		'Integer' : 'org.vistrails.vistrails.basic',
		'String' : 'org.vistrails.vistrails.basic',
		'List' : 'org.vistrails.vistrails.basic',
		'ConcatenateString' : 'org.vistrails.vistrails.basic',
		'WriteFile' : 'org.vistrails.vistrails.basic',
		'FileSink' : 'org.vistrails.vistrails.basic',
		'Sum' : 'org.vistrails.vistrails.control_flow'
	}[name]

def get_signature(mod_type, port_type):
	return {
		'Integer' : {
			'out' : '(org.vistrails.vistrails.basic:Integer)',
			'val' : '(org.vistrails.vistrails.basic:Integer)'
		},
		'String' : {
			'out' : '(org.vistrails.vistrails.basic:String)',
			'string' : '(org.vistrails.vistrails.basic:String)'
		},
		'List' : {
			'in0' : '(org.vistrails.vistrails.basic:Module)',
			'in1' : '(org.vistrails.vistrails.basic:Module)',
			'out' : '(org.vistrails.vistrails.basic:List)'
		},
		'ConcatenateString' : {
			'val1' : '(org.vistrails.vistrails.basic:String)',
			'val2' : '(org.vistrails.vistrails.basic:String)',
			'out' : '(org.vistrails.vistrails.basic:String)'
		},
		'WriteFile' : {
			'in' : '(org.vistrails.vistrails.basic:String)',
			'out' : '(org.vistrails.vistrails.basic:File)'
		},
		'FileSink' : {
			'in' : '(org.vistrails.vistrails.basic:File)',
		},
		'Sum' : {
			'val' : '(org.vistrails.vistrails.basic:List)',
			'out' : '(org.vistrails.vistrails.basic:Variant)'
		}
	}[mod_type][port_type]

# Get the version from the vt name
def get_version(name):
	return {
		'Integer' : '2.1',
		'String' : '2.1',
		'List' : '2.1',
		'ConcatenateString' : '2.1',
		'WriteFile' : '2.1',
		'FileSink' : '2.1',
		'Sum' : '0.2.4'
	}[name]

def get_port_name(mod_type, port_type):
	return {
		'Integer' : {
			'out' : 'value',
			'val' : 'value'
		},
		'String' : {
			'out' : 'value',
			'string' : 'value'
		},
		'List' : {
			'in0' : 'head',
			'in1' : 'head',
			'out' : 'value'
		},
		'ConcatenateString' : {
			'val1' : 'str1',
			'val2' : 'str2',
			'out' : 'value'
		},
		'WriteFile' : {
			'in' : 'in_value',
			'out' : 'out_value'
		},
		'FileSink' : {
			'in' : 'file'
		},
		'Sum' : {
			'val' : 'InputList',
			'out' : 'Result'
		}
	}[mod_type][port_type]

def get_port_type(mod_type, port_type):
	return {
		'Integer' : {
			'out' : 'source',
			'val' : 'destination'
		},
		'String' : {
			'out' : 'source',
			'string' : 'destination'
		},
		'List' : {
			'in0' : 'destination',
			'in1' : 'destination',
			'out' : 'source'
		},
		'ConcatenateString' : {
			'val1' : 'destination',
			'val2' : 'destination',
			'out' : 'source'
		},
		'WriteFile' : {
			'out' : 'source',
			'in' : 'destination'
		},
		'FileSink' : {
			'in' : 'destination'
		},
		'Sum' : {
			'val' : 'destination',
			'out' : 'source'
		}
	}[mod_type][port_type]

with open('nodes.json', 'r') as webfile:
	data = json.load(webfile)
	webfile.close()

modules = []
links = []
count = {'action' : 1, 'add' : 0, 'module' : 0, 'location' : 0, 'connection' : 0, 'port' : 0, 'function' : 0, 'parameter' : 0}

# Read in all the nodes from json
for node in data['nodes']:
	id = node['nid']
	type = rename(node['type'])
	x = node['x']
	y = node['y']
	if type == 'String':
		value = node['fields']['in'][0]['val']
	else:
		value = ''
	modules.append(Module(id, type, x, y, value))

# Read in all the connections from json
for conn in data['connections']:
	par1 = conn['from_node']
	prt1 = conn['from']
	par2 = conn['to_node']
	prt2 = conn['to']
	links.append(Link(par1, par2, prt1, prt2))

# Define the initial vistrail xml tree
vt = ElementTree.Element('vistrail')
vt.attrib['id'] = ''
vt.attrib['name'] = ''
vt.attrib['version'] = '1.0.3'
vt.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
vt.attrib['xsi:schemaLocation'] = 'http://www.vistrails.org/vistrail.xsd'

# Translate all of the json nodes to xml modules
for mod in modules:
	act = ElementTree.SubElement(vt, 'action')
	act.attrib['date'] = '2014-01-01 00:00:00'
	act.attrib['id'] = str(count['action'])
	act.attrib['prevId'] = str(count['action'] - 1)
	act.attrib['session'] = '0'
	act.attrib['user'] = 'translate'

	add = ElementTree.SubElement(act, 'add')
	add.attrib['id'] = str(count['add'])
	add.attrib['objectId'] = str(count['module'])
	add.attrib['parentObjId'] = ''
	add.attrib['parentObjType'] = ''
	add.attrib['what'] = 'module'

	inner = ElementTree.SubElement(add, 'module')
	inner.attrib['cache'] = '1'
	inner.attrib['id'] = str(count['module'])
	inner.attrib['name'] = mod.type
	inner.attrib['namespace'] = ''
	inner.attrib['package'] = get_package(mod.type)
	inner.attrib['version'] = get_version(mod.type)

	mod.vt_id = count['module']
	mod.package = get_package(mod.type)
	count['add'] += 1
	count['action'] += 1
	count['module'] += 1

	add2 = ElementTree.SubElement(act, 'add')
	add2.attrib['id'] = str(count['add'])
	add2.attrib['objectId'] = str(count['module'] - 1)
	add2.attrib['parentObjId'] = str(count['module'] - 1)
	add2.attrib['parentObjType'] = 'module'
	add2.attrib['what'] = 'location'

	loc = ElementTree.SubElement(add2, 'location')
	loc.attrib['id'] = str(count['location'])
	loc.attrib['x'] = str(mod.x)
	loc.attrib['y'] = str(mod.y)

	count['add'] += 1
	count['location'] += 1

	add_value = False

	if mod.type == 'String' and mod.value != '':
		add_value = True
		add_type = 'org.vistrails.vistrails.basic:String'
		add_name = 'value'

	if mod.type == 'FileSink':
		# Location is hard coded for now
		mod.value = '/Users/chen/Desktop/result.txt'
		add_value = True
		add_type = 'org.vistrails.vistrails.basic:OutputPath'
		add_name = 'outputPath'

	if add_value == True:
		in_act = ElementTree.SubElement(vt, 'action')
		in_act.attrib['date'] = '2014-01-01 00:00:00'
		in_act.attrib['id'] = str(count['action'])
		in_act.attrib['prevId'] = str(count['action'] - 1)
		in_act.attrib['session'] = '0'
		in_act.attrib['user'] = 'translate'

		in_add = ElementTree.SubElement(in_act, 'add')
		in_add.attrib['id'] = str(count['add'])
		in_add.attrib['objectId'] = str(count['function'])
		in_add.attrib['parentObjId'] = str(count['module'] - 1)
		in_add.attrib['parentObjType'] = 'module'
		in_add.attrib['what'] = 'function'

		in_func = ElementTree.SubElement(in_add, 'function')
		in_func.attrib['id'] = str(count['function'])
		in_func.attrib['name'] = add_name
		in_func.attrib['pos'] = '0'

		count['add'] += 1
		count['action'] += 1
		count['function'] += 1

		in_add2 = ElementTree.SubElement(in_act, 'add')
		in_add2.attrib['id'] = str(count['add'])
		in_add2.attrib['objectId'] = str(count['parameter'])
		in_add2.attrib['parentObjId'] = str(count['parameter'])
		in_add2.attrib['parentObjType'] = 'function'
		in_add2.attrib['what'] = 'parameter'

		in_param = ElementTree.SubElement(in_add2, 'parameter')
		in_param.attrib['alias'] = ''
		in_param.attrib['id'] = str(count['parameter'])
		in_param.attrib['name'] = '<no description>'
		in_param.attrib['pos'] = '0'
		in_param.attrib['type'] = add_type
		in_param.attrib['val'] = mod.value

		count['add'] += 1
		count['parameter'] += 1

# Translate all of the json connections to xml connections
for link in links:
	act = ElementTree.SubElement(vt, 'action')
	act.attrib['date'] = '2014-01-01 00:00:00'
	act.attrib['id'] = str(count['action'])
	act.attrib['prevId'] = str(count['action'] - 1)
	act.attrib['session'] = '0'
	act.attrib['user'] = 'translate'

	add = ElementTree.SubElement(act, 'add')
	add.attrib['id'] = str(count['add'])
	add.attrib['objectId'] = str(count['connection'])
	add.attrib['parentObjId'] = ''
	add.attrib['parentObjType'] = ''
	add.attrib['what'] = 'connection'

	conn = ElementTree.SubElement(add, 'connection')
	conn.attrib['id'] = str(count['connection'])

	count['add'] += 1
	count['action'] += 1

	add2 = ElementTree.SubElement(act, 'add')
	add2.attrib['id'] = str(count['add'])
	add2.attrib['objectId'] = str(count['port'])
	add2.attrib['parentObjId'] = str(count['connection'])
	add2.attrib['parentObjType'] = 'connection'
	add2.attrib['what'] = 'port'

	mod1 = [x for x in modules if x.id == link.parent_a][0]

	port = ElementTree.SubElement(add2, 'port')
	port.attrib['id'] = str(count['port'])
	port.attrib['moduleId'] =  str(mod1.vt_id)
	port.attrib['moduleName'] = mod1.type
	port.attrib['name'] = get_port_name(mod1.type, link.port_a)
	port.attrib['signature'] = get_signature(mod1.type, link.port_a)
	port.attrib['type'] = get_port_type(mod1.type, link.port_a)

	count['add'] += 1
	count['port'] += 1

	add3 = ElementTree.SubElement(act, 'add')
	add3.attrib['id'] = str(count['add'])
	add3.attrib['objectId'] = str(count['port'])
	add3.attrib['parentObjId'] = str(count['connection'])
	add3.attrib['parentObjType'] = 'connection'
	add3.attrib['what'] = 'port'

	mod2 = [x for x in modules if x.id == link.parent_b][0]

	port2 = ElementTree.SubElement(add3, 'port')
	port2.attrib['id'] = str(count['port'])
	port2.attrib['moduleId'] =  str(mod2.vt_id)
	port2.attrib['moduleName'] = mod2.type
	port2.attrib['name'] = get_port_name(mod2.type, link.port_b)
	port2.attrib['signature'] = get_signature(mod2.type, link.port_b)
	port2.attrib['type'] = get_port_type(mod2.type, link.port_b)

	count['add'] += 1
	count['port'] += 1
	count['connection'] += 1



with open('output.xml', 'wr+') as out_file:
	out_file.write(ElementTree.tostring(vt))
