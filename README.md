# aws-exam-skills

Bộ sưu tập các skill của Claude để tạo và chạy đề ôn luyện tương tác cho các chứng chỉ AWS.
Mỗi chứng chỉ có một skill riêng, cài đặt độc lập với nhau.

## Danh sách skill

| Skill | Chứng chỉ | Trạng thái |
|---|---|---|
| [`aws-saa-practice-exam`](./aws-saa-practice-exam) | Solutions Architect - Associate (SAA-C03) | Sẵn sàng |

Các chứng chỉ khác (ví dụ Cloud Practitioner, Developer Associate, SysOps Administrator) có
thể được thêm vào dưới dạng thư mục ngang hàng, theo cùng một khuôn mẫu.

## Cấu trúc

Mỗi thư mục skill độc lập và tuân theo định dạng skill của Claude:

```
<tên-skill>/
├── SKILL.md          — hướng dẫn hoạt động của skill (bắt buộc)
├── README.md         — tóm tắt cho người đọc về chức năng của skill
└── references/        — tài liệu bổ trợ mà skill đọc khi cần
```

## Cài đặt một skill

Tải hoặc clone repo này, sau đó trỏ Claude (claude.ai, Claude Code, hoặc Cowork) vào đúng
thư mục skill muốn cài — ví dụ `aws-saa-practice-exam/`. README riêng của từng skill có ví dụ
sử dụng cụ thể.

## Thêm skill cho chứng chỉ mới

1. Tạo một thư mục mới đặt tên theo skill, ví dụ `aws-clf-practice-exam/`.
2. Viết `SKILL.md`, `README.md`, và các file `references/` cần thiết riêng cho skill đó (tỷ
   trọng domain của kỳ thi, dịch vụ chính theo từng domain, hướng dẫn phong cách câu hỏi).
3. Thêm một dòng vào bảng ở trên.
