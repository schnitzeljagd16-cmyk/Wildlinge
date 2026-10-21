#!/usr/bin/env python3
"""Erzeugt aus wildlinge.html eine PC- und eine Handy-Variante (gleiches Spiel, gleiche Spielstände)."""
import re,sys
import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src')+'/'
src=open(D+'wildlinge.html',encoding='utf8').read()
i=src.index('<script>');script=src[i:]
FONT='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&display=swap">'
SAVES='''<section class="saves" id="saves" aria-label="Spielstand">
  <div class="saves-head"><b>SPIELSTAND</b><span id="cloudState">3 Slots in diesem Browser · Datei oder Code für andere Geräte</span></div>
  <div class="saves-row"><button class="pill" id="btnExport">Als Datei sichern</button><button class="pill" id="btnImport">Datei laden</button></div>
  <div class="saves-row"><button class="pill alt" id="btnCopy">Code kopieren</button><button class="pill alt" id="btnPaste">Code einfügen</button></div>
  <textarea id="codeBox" hidden spellcheck="false" aria-label="Spielstand-Code"></textarea>
  <button class="pill" id="btnCodeLoad" hidden>Code laden</button>
  <p id="saveMsg" role="status"></p>
  <input type="file" id="fileIn" accept=".json,.txt,application/json,text/plain" hidden>
</section>'''
DPAD='''<div class="dpad">
      <button class="up" data-btn="up" aria-label="Hoch"></button>
      <button class="left" data-btn="left" aria-label="Links"></button>
      <div class="hub"></div>
      <button class="right" data-btn="right" aria-label="Rechts"></button>
      <button class="down" data-btn="down" aria-label="Runter"></button>
    </div>'''
AB='''<div class="ab">
      <div class="btn"><button data-btn="b" aria-label="B"></button><span>B</span></div>
      <div class="btn"><button data-btn="a" aria-label="A"></button><span>A</span></div>
    </div>'''
META='''<div class="meta">
      <div class="btn"><button data-btn="select" aria-label="Ton an oder aus"></button><span>TON</span></div>
      <div class="btn"><button data-btn="start" aria-label="Start"></button><span>START</span></div>
    </div>'''
COMMON_CSS='''
:root{--ground:#141c17;--pad:#242727;--berry:#b8475a;--berry-deep:#7e2b3b;--hint:#9db09f;--label:#5e5a4c;--pixel:'Fredoka','Nunito',system-ui,sans-serif;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(120% 80% at 50% 0%,#1d2a22 0%,var(--ground) 60%) fixed,var(--ground);color:var(--hint);font-family:var(--pixel);-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}
canvas#screen{display:block;background:#fbf8ee;border-radius:4px;image-rendering:auto}
.dpad{position:relative;width:var(--dp);height:var(--dp)}
.dpad button,.dpad .hub{position:absolute;width:calc(var(--dp)/3);height:calc(var(--dp)/3);background:var(--pad);border:none;padding:0;cursor:pointer;box-shadow:0 3px 0 #0d0f0f}
.dpad .up{left:calc(var(--dp)/3);top:0;border-radius:6px 6px 0 0}.dpad .down{left:calc(var(--dp)/3);bottom:0;border-radius:0 0 6px 6px}
.dpad .left{left:0;top:calc(var(--dp)/3);border-radius:6px 0 0 6px}.dpad .right{right:0;top:calc(var(--dp)/3);border-radius:0 6px 6px 0}
.dpad .hub{left:calc(var(--dp)/3);top:calc(var(--dp)/3);box-shadow:none}.dpad .hub::after{content:"";position:absolute;inset:30%;border-radius:50%;background:#1a1c1c}
.dpad button::after{content:"";position:absolute;left:50%;top:50%;width:0;height:0;border:7px solid transparent;transform:translate(-50%,-50%)}
.dpad .up::after{border-bottom-color:#4d5251;margin-top:-4px}.dpad .down::after{border-top-color:#4d5251;margin-top:4px}.dpad .left::after{border-right-color:#4d5251;margin-left:-4px}.dpad .right::after{border-left-color:#4d5251;margin-left:4px}
.ab{display:flex;gap:calc(var(--ab)*.35);transform:rotate(-20deg)}.ab .btn{display:flex;flex-direction:column;align-items:center;gap:6px}.ab .btn:first-child{margin-top:calc(var(--ab)*.6)}
.ab button{width:var(--ab);height:var(--ab);border-radius:50%;border:none;background:var(--berry);cursor:pointer;box-shadow:0 4px 0 var(--berry-deep),inset 3px 3px 0 rgba(255,255,255,.18)}
.ab span,.meta span{font-size:12px;font-weight:600;color:#8a9a8c;letter-spacing:.1em}
.meta{display:flex;justify-content:center;gap:22px}.meta .btn{display:flex;flex-direction:column;align-items:center;gap:6px}
.meta button{width:58px;height:16px;border-radius:8px;border:none;background:#6a6a5c;cursor:pointer;box-shadow:0 2px 0 #4a4a40}
button.on,button:active{transform:translateY(2px);box-shadow:none!important}.ab button.on,.ab button:active{transform:translateY(2px)}
.saves{background:#1c2620;border:1px solid #2e3d33;border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:10px}
.saves-head{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 12px}.saves-head b{font-size:14px;font-weight:700;color:#e6efe2;letter-spacing:.08em}
#cloudState{font-family:system-ui,sans-serif;font-size:12px;color:#9db09f}
.saves-row{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.saves button.pill{font-family:var(--pixel);font-size:13px;font-weight:600;line-height:1.6;color:#f3f7f0;background:#2f4a3a;border:1px solid #476b55;border-radius:8px;padding:9px 8px;cursor:pointer}
.saves button.pill.alt{background:#5a2f3a;border-color:#7e4553}
#codeBox{width:100%;min-height:64px;resize:vertical;font-family:ui-monospace,monospace;font-size:11px;color:#dfe9db;background:#121a15;border:1px solid #33433a;border-radius:8px;padding:8px;word-break:break-all;-webkit-user-select:text;user-select:text}
#saveMsg{font-family:system-ui,sans-serif;font-size:12px;color:#ffe09a;min-height:1em;margin:0}
'''
PC_CSS=COMMON_CSS+'''
html,body{height:100%}
body{display:flex;align-items:center;justify-content:center;padding:2vh 2vw;gap:28px;overflow:hidden}
.stage{position:relative;flex:0 0 auto;display:flex;align-items:center;justify-content:center}
canvas#screen{height:min(94vh,calc((100vw - 400px)*0.9));width:auto;aspect-ratio:160/144;box-shadow:0 0 0 10px #2a302c,0 0 0 12px #3a423c,0 30px 60px rgba(0,0,0,.6);border-radius:6px}
.side{width:320px;flex:0 0 320px;display:flex;flex-direction:column;gap:16px;max-height:94vh;overflow:auto}
.brand{color:#e6efe2}.brand b{font-size:26px;font-weight:700;letter-spacing:.06em;display:block}.brand i{font-style:normal;font-size:12px;font-weight:600;color:#9db09f;letter-spacing:.2em}
.keys{background:#1c2620;border:1px solid #2e3d33;border-radius:12px;padding:14px 16px;font-size:14px;line-height:2.1;color:#cfe3c9}
.keys kbd{font-family:var(--pixel);font-size:12px;background:#2a362e;border:1px solid #3e5244;border-radius:4px;padding:1px 7px;color:#fff}
.keys .t{display:block;font-weight:700;color:#e6efe2;letter-spacing:.08em;margin-bottom:4px}
.pcbtns{display:flex;gap:8px}.pcbtns button{flex:1;font-family:var(--pixel);font-size:13px;font-weight:600;color:#f3f7f0;background:#2f4a3a;border:1px solid #476b55;border-radius:8px;padding:9px;cursor:pointer}
.hidden-controls{display:none}
:fullscreen canvas#screen{height:100vh;box-shadow:none;border-radius:0}
@media (max-width:900px){body{flex-direction:column;overflow:auto}canvas#screen{height:auto;width:min(96vw,80vh)}.side{width:min(96vw,520px);flex:none;max-height:none}}
'''
PC_BODY=f'''<main class="stage" id="stage"><canvas id="screen" width="960" height="864" aria-label="Spielbildschirm"></canvas></main>
<aside class="side">
  <div class="brand"><b>WILDLINGE</b><i>MOOS-EDITION · PC</i></div>
  <div class="keys"><span class="t">STEUERUNG</span>
    <kbd>Pfeile</kbd> / <kbd>WASD</kbd> laufen<br><kbd>Z</kbd> / <kbd>Leertaste</kbd> = A (bestätigen)<br><kbd>X</kbd> = B (zurück, rennen)<br><kbd>Enter</kbd> = START-Menü<br>
    B halten = rennen · A halten = schneller Text<br>Mausklick ins Bild = hinlaufen<br><b>Controller</b> (DualSense, Joy-Con, Xbox): Steuerkreuz/Stick, A/B, Start/+ = START, Select/− = Ton</div>
  <div class="pcbtns"><button id="btnFull">Vollbild</button><button id="btnSnd" data-btn="select">Ton an/aus</button></div>
  {SAVES}
  <div class="hidden-controls">{DPAD}{AB}<div class="meta"><div class="btn"><button data-btn="start"></button></div></div></div>
</aside>'''
PC_EXTRA='''<script>
document.getElementById('btnFull').onclick=()=>{const s=document.getElementById('stage');if(!document.fullscreenElement)(s.requestFullscreen||s.webkitRequestFullscreen).call(s);else document.exitFullscreen();};
</script>'''
M_CSS=COMMON_CSS+'''
html,body{height:100%;overflow:hidden;overscroll-behavior:none;touch-action:none;position:fixed;inset:0;width:100%}
.m{position:fixed;inset:0;display:grid;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);--dp:clamp(118px,36vmin,210px);--ab:clamp(52px,16vmin,88px)}
.scr{grid-area:scr;display:flex;align-items:center;justify-content:center;min-height:0;min-width:0}
canvas#screen{width:100%;height:100%;max-width:100%;max-height:100%;aspect-ratio:160/144;object-fit:contain;border-radius:0}
.lp{grid-area:lp;display:flex;align-items:center;justify-content:center}.rp{grid-area:rp;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px}
.mp{grid-area:mp;display:flex;justify-content:center;align-items:center}
.topbar{position:fixed;top:calc(env(safe-area-inset-top) + 6px);right:calc(env(safe-area-inset-right) + 8px);z-index:5}
.topbar button{font-family:var(--pixel);font-size:12px;font-weight:600;color:#e6efe2;background:rgba(30,40,34,.8);border:1px solid #3e5244;border-radius:16px;padding:5px 10px}
#saves{position:fixed;left:8px;right:8px;bottom:8px;z-index:6;display:none;max-height:70vh;overflow:auto;box-shadow:0 10px 40px rgba(0,0,0,.6)}
#saves.open{display:flex}
/* Hochformat: Bild oben, Steuerung unten */
.rp .meta-l{display:none}
@media (orientation:portrait){.m{grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr auto;grid-template-areas:"scr scr" "lp rp" "mp mp"}
 .scr{width:100vw;height:min(100vw*0.9,62dvh)} canvas#screen{width:auto;height:100%;max-width:100vw}.mp{padding-bottom:14px}}
/* Querformat: Steuerkreuz links, Bild Mitte, Tasten rechts */
@media (orientation:landscape){.m{display:block;--dp:clamp(96px,34vh,170px);--ab:clamp(44px,15vh,76px)}
 .scr{position:fixed;inset:0;z-index:0} canvas#screen{width:100vw;height:100vh;height:100dvh;max-width:none;max-height:none;aspect-ratio:auto;object-fit:fill}
 .lp{position:fixed;left:calc(env(safe-area-inset-left) + 14px);bottom:calc(env(safe-area-inset-bottom) + 12px);z-index:3;opacity:.6}
 .rp{position:fixed;right:calc(env(safe-area-inset-right) + 14px);bottom:calc(env(safe-area-inset-bottom) + 8px);z-index:3;opacity:.6;gap:10px}
 .mp{display:none}.rp .meta-l{display:flex}}
.rp .meta-l{}
body.bigpad .m{--dp:clamp(140px,44vmin,240px);--ab:clamp(62px,20vmin,104px)}
'''
M_META='<div class="btn"><button data-btn="select" aria-label="Ton"></button><span>TON</span></div><div class="btn"><button data-btn="start" aria-label="Start"></button><span>START</span></div>'
M_BODY=f'''<div class="m">
  <div class="scr"><canvas id="screen" width="960" height="864" aria-label="Spielbildschirm"></canvas></div>
  <div class="lp">{DPAD}</div>
  <div class="rp">{AB}<div class="meta meta-l">{M_META}</div></div>
  <div class="mp"><div class="meta">{M_META}</div></div>
</div>
<div class="topbar"><button id="btnSaves">💾 Spielstand</button></div>
{SAVES}'''
M_EXTRA='''<script>
(()=>{const b=document.getElementById('btnSaves'),s=document.getElementById('saves');b.onclick=e=>{e.stopPropagation();s.classList.toggle('open');b.textContent=s.classList.contains('open')?'✕ Schließen':'💾 Spielstand';};
 document.addEventListener('gesturestart',e=>e.preventDefault());document.addEventListener('dblclick',e=>e.preventDefault(),{passive:false});
 document.addEventListener('touchmove',e=>{if(!e.target.closest('#saves'))e.preventDefault();},{passive:false});})();
(()=>{const fit=()=>{if(window.__setWide)window.__setWide(innerWidth>innerHeight?144*innerWidth/innerHeight:160);};addEventListener('resize',fit);addEventListener('orientationchange',()=>setTimeout(fit,250));fit();})();
</script>'''
def page(title,meta,css,body,extra):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
{meta}
<title>{title}</title>
{FONT}
<style>{css}</style>
</head>
<body>
{body}
{script}
{extra}
</body>
</html>
'''
pc=page('Wildlinge – PC','<meta name="viewport" content="width=device-width, initial-scale=1">',PC_CSS,PC_BODY,PC_EXTRA)
HANDY_S=True
mo=page('Wildlinge – Handy','<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="theme-color" content="#141c17">',M_CSS,M_BODY,M_EXTRA)
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','app')+'/';os.makedirs(OUT,exist_ok=True)
open(OUT+'pc.html','w',encoding='utf8').write(pc)
assert 'const S=6,H=144;let W=160;' in mo
mo=mo.replace('const S=6,H=144;let W=160;','const S=Math.max(3,Math.min(5,Math.ceil(Math.min(innerWidth||400,innerHeight||400)*(window.devicePixelRatio||1)/144))),H=144;let W=160;',1)
open(OUT+'handy.html','w',encoding='utf8').write(mo)
print('ok',len(pc),len(mo))

