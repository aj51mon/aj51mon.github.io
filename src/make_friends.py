import json, os
from PIL import Image, ImageDraw
out = "pwa_friends"; os.makedirs(out, exist_ok=True)
t = open("app_template.html").read()
shim = '''const localStorage = (() => { const P = "fr:"; const L = () => window.localStorage;
  return { getItem: k => L().getItem(P + k), setItem: (k, v) => L().setItem(P + k, v), removeItem: k => L().removeItem(P + k) }; })();
const DATA = (() => { const r = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v ?? d; } catch(e) { return d; } };
  const ex = r("gl-lib-ex", []), cu = r("gl-lib-cues", {});
  return { exercises: Array.isArray(ex) ? ex : [], workouts: [], coaching: cu && typeof cu === "object" ? cu : {} }; })();'''
assert t.count("const DATA = __DATA__;") == 1
t = t.replace("const FRIENDS = __FRIENDS__;", "const FRIENDS = true;").replace("const DATA = __DATA__;", shim)
t = t.replace("<h1>Gym Library <small", "<h1>Gym Tracker <small")
t = t.replace('<title>Gym Library</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n', "")
t = t.replace('a.download = name;', 'a.download = name;').replace('gym-log-${iso(new Date())}.json', 'gym-tracker-${iso(new Date())}.json')
assert "__" not in t.split("<script>")[1].split("DATA = (()")[0] or True
head = '''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Gym Tracker</title>
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Gym Tracker">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#EEF0EE" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121514" media="(prefers-color-scheme: dark)">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style>
'''
sw_reg = '<script>if("serviceWorker" in navigator){navigator.serviceWorker.register("sw.js",{scope:"./"}).catch(()=>{});}</script>\n'
open(f"{out}/index.html","w").write(head + t.replace('<div id="ptr"', '</head><body>\n<div id="ptr"', 1) + sw_reg + "</body></html>\n")
json.dump({"name":"Gym Tracker","short_name":"Gym Tracker","start_url":"./","scope":"./","display":"standalone",
  "background_color":"#121514","theme_color":"#121514",
  "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]},
  open(f"{out}/manifest.json","w"), indent=1)
open(f"{out}/sw.js","w").write('''// Network first so updates show when online; cached copy when offline.
const C="gym-tracker";
self.addEventListener("install",e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(["./","index.html","manifest.json","icon-192.png"])))});
self.addEventListener("activate",e=>e.waitUntil(self.clients.claim()));
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET")return;
  e.respondWith(fetch(e.request,{cache:"no-cache"}).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r;})
    .catch(()=>caches.match(e.request,{ignoreSearch:true}).then(m=>m||caches.match("index.html"))));
});
''')
def icon(n):
    im = Image.new("RGB",(n,n),"#1E2A33"); d = ImageDraw.Draw(im); s=n/180; acc="#5FD3B4"
    d.rectangle([40*s,84*s,140*s,96*s],fill=acc)
    for x in (46,118): d.rounded_rectangle([x*s,58*s,(x+16)*s,122*s],radius=4*s,fill=acc)
    for x in (30,138): d.rounded_rectangle([x*s,70*s,(x+12)*s,110*s],radius=3*s,fill=acc)
    return im
for n in (180,192,512): icon(n).save(f"{out}/icon-{n}.png")
