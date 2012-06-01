#/bin/env python3
#
# ThisIsNotBlog for Python 3.x

import sys
import datetime
import re

class BuildEnv:
	def __init__(self):
		self.filename = sys.argv[1]
		self.option = None
		if len(sys.argv) > 2:
			self.option = sys.argv[2]

def parse_file(env,string):
	
	return_string = ""

	parse_state = {
		"title":""
		,"date":""
		,"lines":[]
		,"config":False
		}
	
	valiable = {}
	
	config = {
				"name":None
				,"url":None
				,"author":None
				,"file":None
				,"description":None
			}
	
	if env.option is None:
		build_string = build_string_blog
	elif (env.option == "--rss") or (env.option == "-r"):
		build_string = build_string_rss
	
	is_valiable = re.compile("(^[A-Z][a-zA-Z0-9]*)::").search
	openfile = open(env.filename,encoding="UTF-8").readlines()
	for line in openfile:
		if not parse_state["config"]:
			#
			#This Line is Valiable Parser.
			#
			if is_valiable(line):
				valiable[is_valiable(line).group(1)] = line.split("::")[1]
			elif line.find("---") is 0:
				parse_state["config"] = True
		else:
			if line.find("Title") is 0:
				parse_state["title"] = line.split("::")[1]
			elif line.find("Date") is 0:
				parse_state["date"] = line.split("::")[1]
			elif line.find("---") is 0:
				return_string = return_string + build_string(parse_state)
				parse_state["title"] = ""
				parse_state["lines"] = []
			else:
				parse_state["lines"].append(line)
	
	return_string  = string.replace("{entry_body}",return_string)
	return_string = parse_valiable(return_string,valiable)
	
	return return_string

def parse_valiable(return_string,valiable):
	for key,value in valiable.items():
		if return_string.find("{" + key + "}") > -1 : 
			return_string = return_string.replace("{" + key + "}",value.rstrip())
	return return_string

def build_string_rss(state):
	date_parse = state["date"].split("-")
	pubDate = datetime.datetime(
			int(date_parse[0]),
			int(date_parse[1]),
			int(date_parse[2]),0,0,0,0
			).strftime('%a, %d %B %Y, %H:%M:%S')
	link_count = 0
	if state['title'].rstrip() == "":
		title_s = state['date']
	else:
		title_s = state['title']
	return_string = """
	<item>
		<title>%s</title>
		<link>{Url}{File}#%s</link>
		<description>%s</description>
		<pubDate>%s</pubDate>
	</item>
	""" %(title_s.rstrip(),state["date"].rstrip(),build_string_blog(state),pubDate)
	
	return return_string

def build_string_blog(state):
	link_string = "■"
	link_count = 0
	return_string = "<div><a name='%s'><h2> %s :: %s </h2></a>\n" %(state["date"].rstrip(),state["date"].rstrip(),state["title"].rstrip())
	in_string = ""
	in_p = False
	for line in state["lines"]:
		if line.rstrip() is not "":
			if line.find("+") is 0:
				in_string = "<p>" + in_string + "</p>\n" + ("<p> %s </p>\n" %(line.rstrip()[1:]))
				in_p = True
			else:
				if in_string is not "":
					return_string = return_string + (line_build(link_string,state["date"],link_count,in_p) %(in_string) )
					in_p = False
					link_count += 1
				in_string = "%s" % line.rstrip()
	if in_string is not "":
		return_string = return_string + ( line_build(link_string,state["date"],link_count,in_p) %(in_string) )
	return_string = return_string + "</div>\n\n"
	return return_string

def line_build(link_string,date_state,count,in_p):
	link_name = date_state.rstrip() + str(count)
	if in_p:
		return_string = "<p><a name='" + link_name + "' href='{File}#" + link_name + "'>" + link_string + "</a></p>%s\n"
	else:
		return_string = "<p><a name='" + link_name + "' href='{File}#" + link_name + "'>" + link_string + "</a>%s</p>\n" 
	return return_string

def set_string():
	env = BuildEnv()
	if env.option is None:
		string = open("./template/index.html",encoding="UTF-8").read()
		return parse_file(env,string)
	elif (env.option == "--rss") or (env.option == "-r"):
		string = open("./template/rss.xml",encoding="UTF-8").read()
		return parse_file(env,string)


def main():
	if len(sys.argv) is 1:
		print("Usage: python(or python3) build.py [Filename] > Output File Name")
		exit()
	print(set_string())

if __name__ == "__main__" : main()
