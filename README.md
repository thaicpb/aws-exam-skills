# aws-exam-skills

Bộ skill tạo và chạy đề ôn chứng chỉ AWS. Mỗi skill được đóng gói độc lập với hướng dẫn, nguồn tham chiếu và công cụ cần thiết.

| Skill | Chứng chỉ | Khả năng |
|---|---|---|
| [aws-saa-practice-exam](aws-saa-practice-exam/README.md) | Solutions Architect – Associate (SAA-C03) | Quiz luyện tập, mô phỏng thi, JSON validator và HTML offline |

## Sử dụng

Đưa thư mục `aws-saa-practice-exam/` vào cơ chế nạp skill của môi trường agent đang dùng, hoặc yêu cầu agent đọc `aws-saa-practice-exam/SKILL.md`. Cách đăng ký/cài skill tùy nền tảng; không cần công cụ widget riêng để sinh HTML.

Xem [README của skill](aws-saa-practice-exam/README.md) để cài dependency Python, build mẫu và chạy kiểm thử. Bộ này chưa cung cấp ngân hàng đề đầy đủ: agent soạn và kiểm chứng câu hỏi trước khi builder đóng gói.

## Cấu trúc

```text
aws-saa-practice-exam/
├── SKILL.md
├── README.md
├── references/          # Luật thi, domain/task, checklist chất lượng
├── schemas/             # Hợp đồng dữ liệu JSON
├── scripts/             # Validator và builder
├── assets/              # Template HTML, máy trạng thái JS
├── examples/            # JSON mẫu có nguồn
├── tests/               # Kiểm tra Python, Node và trình duyệt
├── requirements.txt     # Dependency build/validation
└── package.json         # Dependency kiểm thử trình duyệt
```

Để thêm chứng chỉ khác, tạo thư mục ngang hàng và cung cấp nguồn luật thi, schema, phân bổ domain, ví dụ và kiểm thử tương ứng. Không dùng nguyên cấu hình SAA-C03 cho chứng chỉ khác.
