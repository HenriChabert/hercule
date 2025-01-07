function sendToAllClients(type, event) {
    self.clients.matchAll().then(clients => {
        console.log({clients});
        clients.forEach(client => {
            client.postMessage({
                type: type,
                timestamp: new Date().getTime(),
                data: event.data ? event.data.text() : null
            });
        });
    });
}

self.addEventListener('push', function(event) {
    console.log("Push received", event);
    sendToAllClients('PUSH_RECEIVED', event);
});

self.addEventListener('activate', function(event) {
    event.waitUntil(self.clients.claim());
    console.log("Service worker activated", event);
    sendToAllClients('SERVICE_WORKER_ACTIVATED', event);
});

self.addEventListener('install', function(event) {
    console.log("Service worker installed", event);
    sendToAllClients('SERVICE_WORKER_INSTALLED', event);
});
