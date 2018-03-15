# -*- coding: utf-8 -*-
"""
A module for handling commands for the Hive Slack app 
"""

import pkgutil
import commands
import re

command_list = []

# Dynamically import all commands at runtime
for importer, module_name, is_pkg in pkgutil.iter_modules(commands.__path__):
	module = importer.find_module(module_name).load_module(module_name)
	exec('%s = module' % module_name)
	print ("Imported the " + module_name + " command.")
	if module_name is 'fallback':		# We want fallback as the last option
		command_list.append(module_name)
	else:
		command_list.insert(0, module_name)

def dispatch_event(event_data):
	print ("Dispatch_event")

	message_text = event_data["event"]['text']
	for command in command_list:
		pattern = getattr(eval(command), 'pattern')()
		if re.compile(pattern).search(message_text) is not None:
			getattr(eval(command), 'execute_event')(event_data)
			return
			
def dispatch_action(action_data):
	callback_types=['team_selection', "note_selection"]
	functions=['set_team', 'review_notes']
	for idx, callback_type in enumerate(callback_types):
		if action_data["callback_id"].startswith(callback_types[idx]):
			getattr(eval(functions[idx]), 'execute_event')(action_data)
			return
			#return eval(functions[idx])(action_data)