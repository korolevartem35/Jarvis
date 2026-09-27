[app]
title = JARVIS
package.name = jarvis
package.domain = org.artem

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json

version = 1.0
requirements = python3,kivy==2.3.0,speechrecognition,plyer,requests,pyjnius,android,pillow

orientation = portrait
fullscreen = 0

android.permissions = RECORD_AUDIO, INTERNET, CAMERA, FLASHLIGHT, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS, QUERY_ALL_PACKAGES

android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
