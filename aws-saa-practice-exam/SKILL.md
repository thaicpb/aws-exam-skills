---
name: aws-saa-practice-exam
description: Tạo và chạy quiz ôn AWS SAA-C03, luyện theo dịch vụ/domain hoặc mô phỏng thi có chấm điểm và giải thích. Dùng khi người dùng yêu cầu câu hỏi luyện tập, kiểm tra kiến thức hoặc đề thi Solutions Architect Associate; không dùng cho yêu cầu chỉ giải thích AWS, xử lý sự cố hay review kiến trúc.
---

# Luyện thi AWS SAA-C03

## Chọn phạm vi

Tuân theo số câu, chủ đề, độ khó, ngôn ngữ và định dạng người dùng yêu cầu; giữ tên dịch vụ AWS bằng tiếng Anh. Nếu chưa nêu số câu, tạo 15 câu `practice`, phạm vi `mixed`, và thông báo mặc định ngắn gọn. Nếu chỉ nói “quiz AWS” mà chưa rõ chứng chỉ, hỏi xác định chứng chỉ trước khi tạo đề.

- `practice`: phản hồi sau khi xác nhận từng câu; giải thích mọi lựa chọn.
- `exam`: mặc định 65 câu, 130 phút; ẩn điểm/đáp án đến khi nộp hoặc hết giờ; cho quay lại và đánh dấu câu.
- Sau khi nộp, cả hai chế độ đều có màn hình kết quả và xem lại từng câu.
- Luyện dịch vụ/domain cụ thể dùng `focused`; không ép tỷ trọng đề tổng hợp.

## Soạn và kiểm chứng dữ liệu

1. Đọc [exam-rules.md](references/exam-rules.md) để áp dụng loại câu, cách chấm và phân bổ; đọc [domains.md](references/domains.md) để gắn task và dàn trải nội dung.
2. Lập ma trận câu theo domain/task/dịch vụ trước khi viết. Dùng `scripts/validate_exam.py --allocate N` cho đề `mixed`.
3. Viết tình huống 2–5 câu, có ràng buộc quyết định đáp án; độ khó associate. Đọc [question-quality.md](references/question-quality.md) và rà soát từng câu theo checklist trước khi xuất.
4. Tạo JSON theo [exam.schema.json](schemas/exam.schema.json). Mẫu có trong [sample-exam.json](examples/sample-exam.json). Mỗi câu cần domain, task, service tags, giải thích từng lựa chọn và nguồn AWS hỗ trợ đáp án. Mẫu chỉ minh họa hợp đồng dữ liệu, không phải ngân hàng đề đầy đủ.
5. Xác minh nguồn cho kiến thức dễ thay đổi. Không đánh dấu đã xác minh nếu chưa đọc nguồn. Nếu không truy cập được nguồn, nêu giới hạn và giữ bản nháp thay vì giao đề như đã kiểm chứng.
6. Chạy validator rồi builder; sửa mọi lỗi trước khi giao. Validator kiểm tra cấu trúc và bất biến, không chứng minh đáp án đúng về kỹ thuật.

Chạy từ thư mục skill (Python 3.10+):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/validate_exam.py exam.json
.venv/bin/python scripts/build_exam.py exam.json --output output/exam.html
```

Chỉ cần tạo virtualenv và cài dependency một lần. Script nhận đường dẫn tuyệt đối nếu đang ở thư mục khác. Không tự thay đổi mode, số câu hoặc đáp án khi build.

## Trình bày

Ưu tiên widget nếu môi trường có công cụ tương thích: kiểm tra công cụ thực tế và đọc hướng dẫn của công cụ, dùng dữ liệu đã validate và giữ hành vi của template. Không giả định tên API cụ thể luôn tồn tại.

Nếu không có widget, giao HTML độc lập do builder tạo và mở bằng trình duyệt/preview có sẵn. HTML chạy offline, không dùng CDN hay lưu trữ trình duyệt; tải lại sẽ mất lượt làm hiện tại. Nêu điều này trước khi bắt đầu. Đồng hồ chỉ chạy khi người học bấm bắt đầu.

Nếu môi trường chỉ hỗ trợ chat hoặc người dùng muốn chat, hỏi từng câu và theo dõi lựa chọn trong hội thoại. Với `exam`, không lộ đáp án trước khi nộp; nói rõ chat không có đồng hồ tự nộp nền. Nếu người dùng yêu cầu file/text khác, giữ định dạng đó thay vì ép widget.

## Kết quả

Hiển thị số đúng/tổng, tỷ lệ đúng và số câu theo từng domain; không quy đổi tỷ lệ đúng sang điểm AWS hoặc kết luận đỗ kỳ thi thật. Với domain có ít câu, nêu rằng dữ liệu còn ít để kết luận năng lực.

Trong HTML, kết quả thuộc phiên trình duyệt; không giả định agent đọc được thao tác của người học. Gợi ý họ gửi bảng kết quả nếu muốn tạo bài tiếp theo tập trung điểm yếu. Lưu lịch sử/xuất nhập kết quả và chống lặp qua nhiều buổi thuộc nâng cấp sau.
