[app]
title = Point Hunter
package.name = pointhunter
package.domain = org.niootee
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# QUAN TRỌNG: Google Play giờ yêu cầu API 33 hoặc 34
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools = 33.0.0
android.accept_sdk_license = True

# KIẾN TRÚC: Giữ nguyên như bạn đã viết là đúng (hỗ trợ cả máy cũ và mới)
android.archs = arm64-v8a, armeabi-v7a

# YÊU CẦU: Bỏ 'random' và 'struct' vì chúng là thư viện chuẩn của Python (đã có sẵn)
# Nếu bạn dùng Pygame-sd2 (cho Android), nên ghi rõ là 'pygame'
requirements = python3, pygame

# PHÂN QUYỀN: Nếu game có lưu điểm cao hoặc dùng internet, hãy mở thêm (tùy chọn)
# android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE
