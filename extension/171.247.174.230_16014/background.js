
var config = {
    mode: "fixed_servers",
    rules: {
    singleProxy: {
        scheme: "http",
        host: "171.247.174.230",
        port: parseInt(16014)
    },
    bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
return {
    authCredentials: {
        username: "895GCVFI",
        password: "EXRV5VP2"
    }
};
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);
