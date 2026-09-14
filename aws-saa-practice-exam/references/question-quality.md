# Kiểm tra chất lượng trước khi giao đề

## Nội dung

- Stem nêu tình huống và ràng buộc quyết định: RTO/RPO, HA, độ trễ, chi phí hoặc công vận hành. Không buộc người học đoán giả định bị thiếu.
- Phương án nhiễu khả thi ở tình huống khác nhưng vi phạm ràng buộc cụ thể ở đây. Kiểm tra không có phương án thứ hai cũng đáp ứng tối ưu mọi yêu cầu.
- Với chọn nhiều, kiểm tra cả tổ hợp đáp án đúng; từng thành phần cần thiết và tổ hợp đủ giải quyết yêu cầu.
- Giải thích từng lựa chọn, chỉ rõ ràng buộc được đáp ứng/vi phạm. Không dùng độ dài, từ khóa lặp hay vị trí đáp án làm dấu hiệu đoán.
- Độ khó associate; không đánh đố bằng tham số API hiếm. Đổi tình huống/task/dịch vụ; không chỉ đổi tên công ty để tạo câu mới.
- `primary_domain` là mục tiêu chính; `task_id` thuộc domain đó. `service_tags` có thể nhiều dịch vụ.

## Nguồn

- Mỗi câu có ít nhất một URL HTTPS tài liệu AWS, tiêu đề và `verified_on` là ngày đã thực sự đọc nguồn. Nguồn phải hỗ trợ lập luận, không chỉ trang chủ dịch vụ.
- Đối chiếu tính năng, quota, giá và giới hạn region khi câu phụ thuộc chúng; ghi rõ điều kiện trong đề. Không suy từ trí nhớ rằng một khả năng vẫn chưa được hỗ trợ.
- Exam Guide xác định phạm vi, không thay tài liệu dịch vụ khi kiểm tra đáp án. `domains.md` là checklist biên soạn, không xác minh mọi tính năng.
- Khi kiến thức thay đổi hoặc nguồn không đủ rõ, sửa/loại câu thay vì đoán. Không ghi ngày xác minh giả.

## Trước khi build

Chạy validator để kiểm tra schema, task/domain, tỷ trọng, số đáp án, nguồn và câu trùng sau chuẩn hóa khoảng trắng/chữ hoa thường. Kiểm tra ngữ nghĩa vẫn do người soạn thực hiện: validator không mở URL, không phát hiện mọi câu gần nghĩa và không xác nhận tính đúng kỹ thuật.

Kiểm tra một lượt UI ở đúng chế độ: số câu, chọn một/chọn nhiều, xác nhận, quay lại, nộp và xem giải thích. Không coi fixture kỹ thuật trong `tests` là nội dung học đã được duyệt.
