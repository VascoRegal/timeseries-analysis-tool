import json
import yaml

def json_parser(path):
	fp = open(path, 'r')
	data = json.load(fp)
	fp.close()
	return data

def yaml_parser(path):
	fp = open(path, 'r')
	data = yaml.load(fp)
	fp.close()
	return data


