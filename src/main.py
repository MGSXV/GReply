# -*- coding: utf-8 -*-
"""
	@Author:	Soufiane Elkhamlichi
	@Date:		11/08/2022
	@Credit:	Soufiane Elkhamlichi
	@Links:		https://github.com/MGS15/
"""

from init.init_globals import COLORS, ACTIONS
from app import route
import sys

def print_help():
	print(f"""
		{COLORS.DODGER_BLUE_2 + COLORS.BOLD}--filter{COLORS.DEFAULT} : {COLORS.BOLD}Create / Update account's inbox filter.{COLORS.DEFAULT}
		{COLORS.DODGER_BLUE_2 + COLORS.BOLD}--config{COLORS.DEFAULT} : {COLORS.BOLD}Create / Update account's config, including:{COLORS.DEFAULT}
				{COLORS.DODGER_BLUE_2}+{COLORS.DEFAULT} From alias.
				{COLORS.DODGER_BLUE_2}+{COLORS.DEFAULT} Conversation view.
		{COLORS.DODGER_BLUE_2 + COLORS.BOLD}--send{COLORS.DEFAULT}   : {COLORS.BOLD}Start sending messages.{COLORS.DEFAULT}
	""")

def args_error():
	print(f"{COLORS.RED}Invalid arguments!\nTry \"{COLORS.BOLD}--help{COLORS.DEFAULT + COLORS.RED}\" for more information!{COLORS.DEFAULT}")

def get_args() -> int:
	argc = len(sys.argv)
	if argc == 1:
		args_error()
		return ACTIONS.ERROR
	elif argc == 2:
		if sys.argv[1] == '--help':
			print_help()
			return ACTIONS.HELP
		elif sys.argv[1] == '--filter':
			print('Starting filter...')
			return ACTIONS.FILTER
		elif sys.argv[1] == '--config':
			print('Starting config...')
			return ACTIONS.CONFIG
		elif sys.argv[1] == '--send':
			print('Starting sending proccess...')
			return ACTIONS.SEND
		else:
			args_error()
			return ACTIONS.ERROR
	elif argc == 3:
		if '--filter' in sys.argv and '--config' in sys.argv:
			print('Starting filter...')
			print('Starting config...')
			return ACTIONS.FILTER + ACTIONS.CONFIG
		else:
			args_error()
			return ACTIONS.ERROR
	else:
		args_error()
		return ACTIONS.ERROR
	

def main():
	args_res = get_args()
	if args_res == ACTIONS.ERROR:
		exit(1)
	elif args_res == ACTIONS.HELP:
		return
	route.entry_point(args_res)

if __name__ == "__main__":
	main()
	exit(0)