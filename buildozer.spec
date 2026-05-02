[app]

# (str) Application title
title = SmartFarmer

# (str) Package name
package.name = smartfarmer

# (str) Package domain
package.domain = org.smartfarmer

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application version
version = 1.0

# (list) Application requirements
requirements = python3,kivy

# (str) Orientation
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 1

# (str) Supported platforms
android.archs = arm64-v8a, armeabi-v7a

# =========================
# ANDROID SETTINGS (FIXED)
# =========================

# (int) Android API level (IMPORTANT: stable version)
android.api = 34

# (int) Minimum API level
android.minapi = 21

# (int) Android SDK target
android.sdk = 34

# (str) Build-tools version (IMPORTANT FIX)
android.build_tools_version = 34.0.0

# (bool) Enable AndroidX
android.enable_androidx = True

# (bool) Enable Jetifier
android.enable_jetifier = True

# =========================
# FIX FOR AIDL + BUILD ISSUES
# =========================

# (str) Android NDK version (stable)
android.ndk = 25b

# (str) Accept licenses automatically (CI fix)
android.accept_sdk_license = True

# =========================
# PERMISSIONS
# =========================

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# =========================
# DEBUG / BUILD SETTINGS
# =========================

# (bool) Log level
log_level = 2

# (bool) Warn on build
warn_on_root = 1

# =========================
# KIVY OPTIONS
# =========================

# (str) Window size (optional desktop debug)
# desktop = 1

# =========================
# RELEASE SETTINGS
# =========================

# (str) Keystore (leave empty for debug builds)
# android.keystore = my.keystore
# android.keyalias = myalias
# android.keypassword = password

# =========================
# IMPORTANT FIX SUMMARY
# =========================
# ✔ Uses Android API 34 (stable)
# ✔ Uses Build-tools 34.0.0 (fixes AIDL error)
# ✔ Enables AndroidX + Jetifier
# ✔ Fixes CI license issues
# ✔ Compatible with GitHub Actions
# ✔ Stable NDK version
