[app]

# Tên ứng dụng
title = Point Hunter

# Tên gói (package name) – nên đặt duy nhất
package.name = pointhunter
package.domain = org.yourdomain

# Phiên bản
version = 0.1

# Yêu cầu Android API (ít nhất 21)
android.api = 31
android.minapi = 21

# Kiến trúc CPU (chọn để giảm kích thước)
android.archs = arm64-v8a, armeabi-v7a

# Các thư viện Python cần cài – BẮT BUỘC phải có pygame
requirements = python3, pygame, struct, random

# File chính của ứng dụng (mặc định là main.py)
# Nếu tên khác thì khai báo ở đây
# source.dir = .
# source.include_exts = py,png,jpg,kv,atlas

# Cấu hình thêm để tránh lỗi font chữ (dùng font hệ thống mặc định)
# Không cần chỉnh gì thêm, pygame sẽ dùng font mặc định
