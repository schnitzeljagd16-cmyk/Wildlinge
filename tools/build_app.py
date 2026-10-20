#!/usr/bin/env python3
"""Baut die installierbare Web-App (PWA) nach app/: PC- und Handy-Version, Startseite, Manifest, Offline-Cache."""
import os,subprocess,sys,json,hashlib,shutil
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
APP=os.path.join(ROOT,'app')
subprocess.check_call([sys.executable,os.path.join(ROOT,'tools','make_variants.py')])
for f in os.listdir(os.path.join(ROOT,'icons')):shutil.copy(os.path.join(ROOT,'icons',f),os.path.join(APP,f))
HEAD='<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#2f5a3a"><link rel="icon" href="icon-192.png"><link rel="apple-touch-icon" href="icon-192.png">'
SW='<script>if("serviceWorker"in navigator)addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{}));</script>'
for f in ('pc.html','handy.html'):
  p=os.path.join(APP,f);s=open(p,encoding='utf8').read()
  s=s.replace('<meta charset="utf-8">','<meta charset="utf-8">'+HEAD,1).replace('</body>',SW+'</body>',1)
  open(p,'w',encoding='utf8').write(s)
open(os.path.join(APP,'index.html'),'w',encoding='utf8').write('''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'''+HEAD+'''<title>Wildlinge</title>
<style>html,body{margin:0;height:100%;background:#141c17;color:#e8f2e4;font-family:system-ui,sans-serif;display:flex;align-items:center;justify-content:center;text-align:center}
a{display:inline-block;margin:8px;padding:14px 22px;border-radius:12px;background:#2f5a3a;color:#fff;text-decoration:none;font-weight:600}img{width:160px;border-radius:24px}</style></head>
<body><div><img src="icon-512.png" alt=""><h1>Wildlinge</h1><p id="t">Einen Moment...</p><p><a href="pc.html">PC-Version</a><a href="handy.html">Handy-Version</a></p></div>
<script>const touch=matchMedia("(pointer:coarse)").matches||"ontouchstart"in window;const pick=localStorage.getItem("wildlinge-geraet");
if(!location.hash.includes("wahl")){location.replace(pick||(touch?"handy.html":"pc.html"));}else document.getElementById("t").textContent="Welche Version möchtest du spielen?";
document.querySelectorAll("a").forEach(a=>a.onclick=()=>localStorage.setItem("wildlinge-geraet",a.getAttribute("href")));</script>'''+SW+'''</body></html>''')
json.dump({"name":"Wildlinge – Moos-Edition","short_name":"Wildlinge","start_url":"./index.html","scope":"./","display":"fullscreen","orientation":"any","background_color":"#141c17","theme_color":"#2f5a3a",
  "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},
  open(os.path.join(APP,'manifest.webmanifest'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
files=['./','index.html','pc.html','handy.html','manifest.webmanifest','icon-192.png','icon-512.png']
ver=hashlib.sha1(b''.join(open(os.path.join(APP,f),'rb').read() for f in files[1:])).hexdigest()[:10]
open(os.path.join(APP,'sw.js'),'w',encoding='utf8').write('''const C="wildlinge-'''+ver+'''",F='''+json.dumps(files)+''';
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(F)).then(()=>self.skipWaiting()));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",e=>{if(e.request.method!=="GET")return;e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{if(res.ok&&(e.request.url.startsWith(self.location.origin)||e.request.url.includes("fonts.")))caches.open(C).then(c=>c.put(e.request,res.clone()));return res;}).catch(()=>caches.match("index.html"))));});''')
print('App gebaut, Version',ver)
