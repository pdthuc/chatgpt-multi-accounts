
var config = {
    mode: "fixed_servers",
    rules: {
    singleProxy: {
        scheme: "http",
        host: "115.76.115.0",
        port: parseInt(7003)
    },
    bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
return {
    authCredentials: {
        username: "yoalqUDq",
        password: "BDhkltNQ"
    }
};
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);