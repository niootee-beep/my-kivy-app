[app]

title = Point Hunter
package.name = pointhunter
package.domain = org.niootee

version = 0.1

android.api = 31
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

requirements = python3, pygame, random, struct

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Thêm 2 dòng dưới đây
android.accept_sdk_license = True
android.build_tools = 33.0.0
