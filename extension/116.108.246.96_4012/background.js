
var config = {
    mode: "fixed_servers",
    rules: {
    singleProxy: {
        scheme: "http",
        host: "116.108.246.96",
        port: parseInt(4012)
    },
    bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
return {
    authCredentials: {
        username: "SgqbJkvG",
        password: "aWRg1QDN"
    }
};
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);