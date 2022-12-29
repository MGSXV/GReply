from helpers import file_hanlder
from modules.Account import Account
from init.init_globals import PATHS, COLORS

def set_account_info(acc: list) -> Account:
	account = Account()
	try:
		account.setEmail(acc[0].strip())
	except Exception as e:
		print(e)
		exit(1)
	try:
		account.setPassword(acc[1].strip())
	except Exception as e:
		print(e)
		exit(1)
	return account

def set_accounts_list():
	i = 0
	accounts = []
	while True:
		try:
			acc = file_hanlder.read_csv_file(PATHS.RESOURCES_FILE, i)
			account = set_account_info(acc)
			accounts.append(account)
		except IndexError:
			break
		except Exception as e:
			print(e)
			exit(1)
		i += 1
	# COLORS.success_messgae('Initializing accounts is done!')
	return accounts
