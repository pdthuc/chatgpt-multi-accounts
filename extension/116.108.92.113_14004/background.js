
var config = {
    mode: "fixed_servers",
    rules: {
    singleProxy: {
        scheme: "http",
        host: "116.108.92.113",
        port: parseInt(14004)
    },
    bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
return {
    authCredentials: {
        username: "idITOfli",
        password: "5loradJ1"
    }
};
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);
