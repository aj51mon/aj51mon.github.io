// Network first so updates show when online; cached copy when offline.
const C="gym-library";
self.addEventListener("install",e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(["./","index.html","manifest.json","icon-192.png"])))});
self.addEventListener("activate",e=>e.waitUntil(self.clients.claim()));
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET")return;
  e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r;})
    .catch(()=>caches.match(e.request,{ignoreSearch:true}).then(m=>m||caches.match("index.html"))));
});
