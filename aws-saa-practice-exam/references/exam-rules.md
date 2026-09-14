# Quy tắc đề SAA-C03

Đối chiếu ngày 2026-09-14:
- [AWS Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html)
- [Thông tin kỳ thi](https://aws.amazon.com/certification/certified-solutions-architect-associate/)
- [Điểm chuẩn hóa](https://aws.amazon.com/blogs/training-and-certification/demystifying-your-aws-certification-exam-score/)

## Thông tin chính thức

SAA-C03 có 65 câu, thời lượng chuẩn 130 phút. Có 50 câu tính điểm và 15 câu không tính điểm; thí sinh không được biết câu nào thuộc nhóm sau. Điểm đạt là 720 trên thang chuẩn hóa 100–1000, không phải đúng 72% câu hỏi.

Câu chọn một có bốn lựa chọn, một đáp án đúng. Câu chọn nhiều có ít nhất năm lựa chọn, ít nhất hai đáp án đúng. Tài liệu trên không công bố tỷ lệ cố định giữa hai loại câu. Câu bỏ trống tính sai, không trừ điểm do đoán.

## Quy ước của bộ luyện tập

- Chấm tất cả câu, mỗi câu đúng được một điểm; không giả lập 15 câu không tính điểm.
- Chọn nhiều: phải khớp toàn bộ tập đáp án, không có điểm từng phần. Đây là quy ước luyện tập.
- Hiển thị rõ “Chọn N đáp án”; N lấy từ `correct_option_ids`. Có ít nhất một phương án sai.
- Không gắn nhãn đỗ/trượt AWS. Báo số đúng và phần trăm, không nhân tỷ lệ với 1000.
- Có thể dùng khoảng 20% câu chọn nhiều như lựa chọn thiết kế, không gọi là tỷ lệ chính thức. Không ép tỷ lệ này khi người dùng yêu cầu khác.
- `exam` chỉ bắt đầu đồng hồ sau nút Bắt đầu; tự nộp khi hết giờ; nộp sớm có bước xác nhận và báo số câu chưa đủ lựa chọn. Câu chọn thiếu vẫn được giữ và chấm theo quy tắc khớp tập đáp án.
- `practice` chỉ khóa câu sau khi xác nhận đủ số lựa chọn; xem lại không cộng điểm lần nữa. Nộp sớm chấm câu chưa xác nhận là sai.

## Phân bổ nguyên

Tỷ trọng nội dung tính điểm chính thức theo domain 1–4 là 30/26/24/20. Đề luyện `mixed` áp dụng tỷ trọng đó cho toàn bộ câu bằng phương pháp phần dư lớn nhất:

1. Lấy phần nguyên của `N * weight / 100`.
2. Phân các câu còn lại theo phần dư giảm dần.
3. Khi bằng phần dư, ưu tiên domain có số nhỏ hơn.

| Tổng câu | Domain 1 | Domain 2 | Domain 3 | Domain 4 |
|---|---|---|---|---|
| 15 | 4 | 4 | 4 | 3 |
| 65 | 19 | 17 | 16 | 13 |

Đây là phân bổ xấp xỉ của bộ luyện, không phải cam kết số câu trong đề thật. `focused` yêu cầu `focus` mô tả chủ đề và không kiểm tra tỷ trọng; người viết phải kiểm tra câu thuộc chủ đề đó. Khi tổng hợp kết quả luôn hiện mẫu số, không kết luận chắc chắn về domain chỉ có vài câu.
