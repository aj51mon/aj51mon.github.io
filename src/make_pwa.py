import json, re
from PIL import Image, ImageDraw
body = open("gym-library.html").read()
title_meta = '<title>Gym Library</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
body = body.replace(title_meta, "")
head = '''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Gym Library</title>
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Gym Library">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#EEF0EE" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121514" media="(prefers-color-scheme: dark)">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style>
'''
sw_reg = '<script>if("serviceWorker" in navigator){navigator.serviceWorker.register("sw.js").catch(()=>{});}</script>\n'
open("pwa/index.html","w").write(head + body.replace("<div class=\"wrap\">", "</head><body>\n<div class=\"wrap\">",1) + sw_reg + "</body></html>\n")
json.dump({"name":"Gym Library","short_name":"Gym Library","start_url":"./","scope":"./","display":"standalone",
  "background_color":"#121514","theme_color":"#121514",
  "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]},
  open("pwa/manifest.json","w"), indent=1)
open("pwa/sw.js","w").write('''// Network first so updates show when online; cached copy when offline.
const C="gym-library";
self.addEventListener("install",e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(["./","index.html","manifest.json","icon-192.png"])))});
self.addEventListener("activate",e=>e.waitUntil(self.clients.claim()));
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET")return;
  e.respondWith(fetch(e.request,{cache:"no-cache"}).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r;})
    .catch(()=>caches.match(e.request,{ignoreSearch:true}).then(m=>m||caches.match("index.html"))));
});
''')
def icon(n):
    im = Image.new("RGB",(n,n),"#171A19"); d = ImageDraw.Draw(im); s=n/180
    acc="#F2B92B"
    d.rectangle([40*s,84*s,140*s,96*s],fill=acc)                      # bar
    for x in (46,118):
        d.rounded_rectangle([x*s,58*s,(x+16)*s,122*s],radius=4*s,fill=acc)  # plates
    for x in (30,138):
        d.rounded_rectangle([x*s,70*s,(x+12)*s,110*s],radius=3*s,fill=acc)
    return im
for n in (180,192,512): icon(n).save(f"pwa/icon-{n}.png")
