
var config = {
    mode: "fixed_servers",
    rules: {
    singleProxy: {
        scheme: "http",
        host: "171.235.184.87",
        port: parseInt(4015)
    },
    bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
return {
    authCredentials: {
        username: "iBePuh2G",
        password: "0egZzv8f"
    }
};
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);
