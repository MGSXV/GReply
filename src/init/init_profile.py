from helpers import file_hanlder
from modules.Profile import Profile
from modules.Proxy import Proxy
from modules.Account import Account
from init.init_globals import PATHS

def new_proxy(ip: str, port: int, user: str, password: str) -> Proxy:
	proxy = Proxy()
	proxy.setIp(ip)
	proxy.setPort(port)
	proxy.setUser(user)
	proxy.setPassword(password)
	return proxy

def new_account(email: str, password: str) -> Account:
	account = Account()
	account.setEmail(email)
	account.setPassword(password)
	return account

def new_profile(p: list) -> Profile:
	profile = Profile()
	account = new_account(p[1], p[2])
	proxy = new_proxy(p[3], int(p[4]), p[5], p[6])
	profile.setName(p[0].strip())
	profile.setProxy(proxy)
	profile.accounts.append(account)
	return profile

def set_profiles_list() -> list:
	i = 0
	profiles = []
	while True:
		try:
			l = len(profiles)
			profile = Profile()
			p = file_hanlder.read_csv_file(PATHS.RESOURCES_FILE, i)
			if l == 0:
				profile = new_profile(p)
				profiles.append(profile)
			else:
				is_old = False
				for profile in profiles:
					if p[0] == profile.getName():
						profile.accounts.append(new_account(p[1], p[2]))
						is_old = True
						break
				if not is_old:
					profile = new_profile(p)
					profiles.append(profile)
		except IndexError:
			break
		except Exception as e:
			print(e)
			exit(1)
		i = i + 1
	return profiles