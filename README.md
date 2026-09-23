# TH_LT_ANTT – Buổi 1

Bài thực hành môn An Toàn Thông Tin – các lab về lập trình bảo mật cơ bản.

## Cấu trúc

```
├── Lab01/    SecureValidator – thư viện kiểm tra và làm sạch đầu vào
├── Lab02/    GitSecure – pre-commit hook phát hiện thông tin nhạy cảm
└── Lab03/    SecureLogger – hệ thống ghi log bảo mật tích hợp Flask
```

## Lab01 – SecureValidator

Thư viện validate và sanitize input gồm 5 hàm: `validate_email`, `validate_url`, `validate_filename`, `sanitize_sql_input`, `sanitize_html_input`.

`Exploit.md` phân tích các điểm yếu: SSRF qua URL nội bộ, SQL injection bằng toán tử `||`, XSS qua thuộc tính `href`.

## Lab02 – GitSecure Pre-commit Hook

Hook tự động chặn commit nếu phát hiện thông tin nhạy cảm (password, token, API key) hoặc file có quyền world-writable.

```bash
cd Lab02
pip install -r requirements.txt
git init && git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

## Lab03 – SecureLogger

Flask API `/validate` tích hợp logging bảo mật: tự động che PII, ghi JSON, nén log cũ bằng gzip, hash SHA-256 để phát hiện giả mạo log.

```bash
cd Lab03
pip install -r requirements.txt
python app.py
```
