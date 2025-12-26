[app]
title = Remote Control
package.name = remotecontrol
package.domain = org.local

source.dir = .
source.include_exts = py
source.main = remote_control_client_v1.2.py

version = 1.2
requirements = python3,kivy==2.2.1,zeroconf,ifaddr

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_MULTICAST_STATE,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
