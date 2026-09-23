# TH_LT_ANTT – Bài 1: Cơ Sở Lập Trình Bảo Mật, Kiểm Tra Đầu Vào

## Cấu trúc thư mục

```
TH_LT_ANTT/
├── bai1_4_2/          ← Bài 1.4.2: Pre-commit Hook (GitSecure)
│   ├── .githooks/
│   │   └── pre-commit
│   ├── pre-commit-hook-test/
│   │   └── bad.py
│   ├── .gitignore
│   └── requirements.txt
└── bai1_6/            ← Bài 1.6: Secure Logger Lab
    ├── app.py
    ├── securevalidator/
    │   ├── __init__.py
    │   └── core.py
    ├── securelogger/
    │   ├── __init__.py
    │   └── logger.py
    └── requirements.txt
```

---

## Bài 1.4.2 – Pre-commit Hook (GitSecure)

### Mô tả

Pre-commit hook tự động ngăn chặn commit nếu phát hiện:
- Thông tin nhạy cảm trong code (API key, secret, password, token, AWS key)
- File có quyền world-writable (`chmod 777`)
- Lỗi bảo mật nghiêm trọng phát hiện bởi `bandit`

Mọi phát hiện được ghi vào file `gitsecure.log`.

### Cài đặt & Chạy

```bash
cd bai1_4_2
pip install -r requirements.txt
git init
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

### Demo – Commit bị chặn

File `pre-commit-hook-test/bad.py` chứa:

```python
password = "123456"
```

Khi thực hiện commit:

```bash
$ git add pre-commit-hook-test/bad.py
$ git commit -m "test"

COMMIT BLOCKED by GitSecure:
 - Sensitive info found in pre-commit-hook-test/bad.py: pattern password\s*=\s*['\"][^\"\\']{4,}['\"]
```

### Demo – Commit sạch thành công

```bash
$ git add .githooks/pre-commit .gitignore requirements.txt
$ git commit -m "add githooks"

GitSecure: All checks passed.
[master (root-commit) 96267b6] add githooks
 3 files changed, 87 insertions(+)
```

### Nội dung `gitsecure.log` sau khi bị chặn

```
[2026-09-23 19:55:07.310674] Sensitive info found in pre-commit-hook-test/bad.py: pattern password\s*=\s*['\"][^\"\\']{4,}['\"]
```

---

## Bài 1.6 – Secure Logger Lab

### Mô tả

Hệ thống ghi nhật ký bảo mật với các tính năng:
- **Multi-level logging**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **PII Masking**: Tự động che thông tin cá nhân (email, token, password) trong log
- **JSON structured logging**: Mỗi dòng log là một JSON object
- **Log rotation + Gzip**: Tự động nén file log cũ
- **Tamper detection**: Mỗi dòng log được hash SHA-256 ghi vào `secure.log.sig`
- **Flask API**: Endpoint `POST /validate` kiểm tra và làm sạch đầu vào

### Cài đặt & Chạy

```bash
cd bai1_6
pip install -r requirements.txt
python app.py
```

Server chạy tại `http://127.0.0.1:5000`.

### Demo – Gọi API với dữ liệu nguy hiểm

**Request (Postman / curl):**

```bash
curl -X POST http://localhost:5000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "email": "phuoc@example.com",
    "url": "https://secure.com",
    "filename": "report.pdf",
    "sql": "'\'' OR 1=1 --",
    "html": "<script>alert(1)</script>"
  }'
```

**Response:**

```json
{
    "email": true,
    "filename": true,
    "html": "&lt;script&gt;alert(1)&lt;/script&gt;",
    "sql": "1=1",
    "url": true
}
```

- `html`: Đã HTML-escape, vô hiệu hóa XSS
- `sql`: Đã loại bỏ `' OR ... --`, chỉ còn `1=1`
- `email`: Hợp lệ → `true`

### Nội dung `secure.log` (PII đã bị che)

```json
{
  "timestamp": "2026-09-23T12:56:06.408064Z",
  "level": "INFO",
  "message": "Validation check performed",
  "data": "{'email': '<email_masked>', 'url': 'https://secure.com', 'filename': 'report.pdf', 'sql': \"' OR 1=1 --\", 'html': '<script>alert(1)</script>'}",
  "results": "{'email': True, 'url': True, 'filename': True, 'sql': '1=1', 'html': '&lt;script&gt;alert(1)&lt;/script&gt;'}"
}
```

Email `phuoc@example.com` đã bị thay bằng `<email_masked>`.

### Nội dung `secure.log.sig` (Tamper detection)

```
1f5719b880273de18966776991d2ed116a113f41486652236d4c1615d08b88bf
```

Mỗi dòng là hash SHA-256 của dòng log tương ứng — dùng để phát hiện log bị chỉnh sửa trái phép.
