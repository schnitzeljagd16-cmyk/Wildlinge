#!/usr/bin/env python3
"""Passt das von Capacitor erzeugte Android-Projekt an: Vollbild, App-Symbol, Version, feste Signatur."""
import os,re,sys,shutil,glob
from PIL import Image
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..');A=os.path.join(R,'android')
run=int(sys.argv[1]) if len(sys.argv)>1 else 1
# Vollbild ohne Statusleiste
p=os.path.join(A,'app/src/main/res/values/styles.xml');s=open(p).read()
s=re.sub(r'(<style name="AppTheme.NoActionBar"[^>]*>)',r'\1\n        <item name="android:windowFullscreen">true</item>\n        <item name="android:windowLayoutInDisplayCutoutMode">shortEdges</item>',s)
open(p,'w').write(s)
# App-Symbol
src=Image.open(os.path.join(R,'icons/icon-512.png')).convert('RGBA')
for d,n in {'mdpi':48,'hdpi':72,'xhdpi':96,'xxhdpi':144,'xxxhdpi':192}.items():
  dd=os.path.join(A,f'app/src/main/res/mipmap-{d}');os.makedirs(dd,exist_ok=True)
  for f in glob.glob(dd+'/ic_launcher*'):os.remove(f)
  im=src.resize((n,n),Image.LANCZOS);im.save(dd+'/ic_launcher.png');im.save(dd+'/ic_launcher_round.png')
shutil.rmtree(os.path.join(A,'app/src/main/res/mipmap-anydpi-v26'),ignore_errors=True)
# Version und feste Signatur (gleicher Schlüssel = Updates ohne Neuinstallation, Spielstände bleiben)
p=os.path.join(A,'app/build.gradle');s=open(p).read()
s=re.sub(r'versionCode \d+',f'versionCode {run}',s);s=re.sub(r'versionName "[^"]*"',f'versionName "1.{run}"',s)
sign='''    signingConfigs {
        fest {
            storeFile file("../../android-signing/wildlinge.jks")
            storePassword "wildlinge123"
            keyAlias "wildlinge"
            keyPassword "wildlinge123"
        }
    }
    buildTypes {
        debug { signingConfig signingConfigs.fest }
        release {
            signingConfig signingConfigs.fest'''
s=s.replace('    buildTypes {\n        release {',sign,1)
assert 'signingConfigs.fest' in s,'build.gradle-Struktur unerwartet'
open(p,'w').write(s)
# Bildschirm an lassen, Hardware-Beschleunigung
p=os.path.join(A,'app/src/main/AndroidManifest.xml');s=open(p).read()
s=s.replace('<activity','<activity\n            android:screenOrientation="unspecified"',1)
open(p,'w').write(s)
print('Android-Projekt angepasst, Version 1.%d'%run)
