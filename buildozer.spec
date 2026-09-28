[app]
title = JARVIS
package.name = jarvis
package.domain = org.artem

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json

version = 1.0
requirements = python3,kivy==2.3.0,speechrecognition,plyer,requests,pyjnius,android,pillow,libffi

orientation = portrait
fullscreen = 0

android.permissions = RECORD_AUDIO, INTERNET, CAMERA, FLASHLIGHT, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS, QUERY_ALL_PACKAGES

android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.branch = develop
p4a.local_recipes = ./p4a-recipes

[buildozer]
log_level = 2
warn_on_root = 0
