# aws-saa-practice-exam

Một skill của Claude để tạo câu hỏi ôn luyện sát với đề thi thật AWS Certified Solutions
Architect - Associate (SAA-C03) và chạy dưới dạng quiz tương tác có chấm điểm.

## Skill này làm gì

- Viết câu hỏi ôn luyện theo phong cách dựa trên tình huống giống đề thi thật (không phải
  câu đố kiến thức), phân bổ theo đúng bốn domain chính thức và tỷ trọng thật của kỳ thi:
  - Design Secure Architectures — 30%
  - Design Resilient Architectures — 26%
  - Design High-Performing Architectures — 24%
  - Design Cost-Optimized Architectures — 20%
- Trình bày bài quiz dưới dạng widget tương tác (phản hồi ngay lập tức, giải thích cho cả đáp
  án đúng lẫn sai, điểm số đang chạy, phân tích theo từng domain ở cuối bài).
- Hỗ trợ luyện nhanh, luyện tập trung theo domain, hoặc mô phỏng đầy đủ 65 câu.

## Cách dùng

Cài skill này vào Claude (claude.ai, Claude Code, hoặc Cowork), sau đó nhắn những câu như:

- "Cho tôi 15 câu ôn AWS SAA-C03"
- "Quiz mình về VPC và networking cho kỳ thi AWS SA"
- "Cho mình một bài mô phỏng đầy đủ 65 câu SAA-C03"

## Các file

- `SKILL.md` — hướng dẫn hoạt động của skill
- `README.md` — tóm tắt cho người đọc về chức năng của skill
- `references/domains.md` — task statement của từng domain SAA-C03 và các dịch vụ AWS liên
  quan, dùng để giữ cho câu hỏi được tạo ra có nền tảng kỹ thuật chính xác và đa dạng
