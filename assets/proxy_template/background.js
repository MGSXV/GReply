var config = {
	mode: "fixed_servers",
	rules: {
	singleProxy: {
		scheme: "http",
		host: "%(host)s",
		port: parseInt(%(port)d)
	},
	bypassList: ["http://whatismyipaddress.com"]
	}
};
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
return {
	authCredentials: {
		username: "%(user)s",
		password: "%(pass)s"
	}
};
}
chrome.webRequest.onAuthRequired.addListener(
		callbackFn,
		{urls: ["<all_urls>"]},
		['blocking']
);