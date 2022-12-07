from datetime import date, datetime
from helpers import file_hanlder
from init.init_globals import PATHS

class Logger():
	EMAIL_ERROR = 1
	PASS_ERROR = 2
	PROXY_ERROR = 3
	CAPTCHA_ERROR = 4
	VERIFICATION_ERROR = 5
	BLOCKED_ACC_ERROR = 6
	UNKNOWN_ERROR = 7

	def get_time_stamp():
		now = date.today()
		timestamp = now.strftime("%Y/%m/%d")
		timestamp += " - "
		timestamp += datetime.now().strftime("%H:%M:%S")
		return timestamp

	def logger(level: int, email: str):
		line = '[' + Logger.get_time_stamp() + '] '
		if level == globals.EMAIL_ERROR:
			line += 'EMAIL_ERROR\t\t\t\t: invalid email address: (' + email + ')'
		elif level == globals.PASS_ERROR:
			line += 'PASS_ERROR\t\t\t\t: invalid password: (' + email + ')'
		elif level == globals.PROXY_ERROR:
			line += 'PROXY_ERROR\t\t\t\t: invalid proxy address: (' + email + ')'
		elif level == globals.CAPTCHA_ERROR:
			line += 'CAPTCHA_ERROR\t\t\t: Captcha error accured!'
		elif level == globals.VERIFICATION_ERROR:
			line += 'VERIFICATION_ERROR\t\t: account requires verifcation: (' + email + ')'
		elif level == globals.BLOCKED_ACC_ERROR:
			line += 'BLOCKED_ACC_ERROR\t\t: account is temporarily blocked: (' + email + ')'
		else:
			line += 'Unknown error\t\t\t: (' + email + ')'
		line += '\n'
		file_hanlder.write_file(PATHS.STORAGE + PATHS.SEP + 'logs', line, 'a')