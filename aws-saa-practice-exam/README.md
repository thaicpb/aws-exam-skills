# aws-saa-practice-exam

Skill tạo đề ôn AWS SAA-C03 từ tình huống, kiểm tra JSON và dựng HTML độc lập. Có thể dùng trên môi trường agent đọc được `SKILL.md`; widget là tùy chọn, không phụ thuộc tên API riêng của một nền tảng.

## Chức năng

- `practice`: mặc định 15 câu tổng hợp; xác nhận từng câu rồi xem giải thích mọi lựa chọn.
- `exam`: mặc định 65 câu, 130 phút; đồng hồ chạy khi bấm Bắt đầu, tự nộp khi hết giờ, quay lại câu và đánh dấu xem lại. Đáp án ẩn trên giao diện đến khi nộp.
- Sau khi nộp: tỷ lệ đúng, thống kê domain và xem lại tất cả câu. Chấm toàn bộ câu, không quy đổi sang điểm chuẩn hóa AWS hoặc dự đoán đỗ.
- `focused`: luyện theo chủ đề, không ép tỷ trọng tổng hợp.
- HTML chạy offline, hỗ trợ bàn phím và màn hình nhỏ; giao diện điều khiển tiếng Việt, nội dung câu giữ ngôn ngữ của JSON.

Ví dụ yêu cầu: “Cho tôi 15 câu ôn SAA-C03”, “Quiz về VPC cho SAA-C03”, “Tạo đề mô phỏng 65 câu SAA-C03”. Yêu cầu chỉ giải thích kiến thức hoặc review kiến trúc không kích hoạt quiz.

## Cài dependency và dùng thử

Chạy từ thư mục skill, dùng Python 3.10+:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/validate_exam.py examples/sample-exam.json
.venv/bin/python scripts/build_exam.py examples/sample-exam.json --output output/sample-exam.html
```

Mở `output/sample-exam.html` bằng trình duyệt. Mẫu một câu chỉ minh họa JSON và giao diện, không phải đề tổng hợp. Để tạo đề mới, agent viết JSON theo schema và rà soát nội dung trước khi build; builder không tự sinh câu hỏi.

```bash
.venv/bin/python scripts/validate_exam.py --allocate 15
.venv/bin/python scripts/validate_exam.py --allocate 65
.venv/bin/python scripts/build_exam.py exam.json --output output/exam.html
```

CLI trả mã lỗi khác 0 nếu dữ liệu không hợp lệ; không ghi output khi validation thất bại. Builder giữ mode, thứ tự câu và lựa chọn của JSON.

## Hợp đồng dữ liệu

Xem [schema](schemas/exam.schema.json) và [mẫu](examples/sample-exam.json).

| Trường | Ý nghĩa |
|---|---|
| `schema_version`, `exam_code` | `1`, `SAA-C03` |
| `title`, `language` | Tên bài, mã ngôn ngữ nội dung, ví dụ `vi` |
| `mode`, `scope` | `practice`/`exam`, `mixed`/`focused` |
| `question_count` | Phải bằng số phần tử `questions` |
| `duration_minutes` | Bắt buộc cho `exam`; không dùng cho `practice` |
| `focus` | Bắt buộc cho `focused`; không dùng cho `mixed` |
| `questions[].id`, `stem` | ID và tình huống không trùng trong bài |
| `primary_domain`, `task_id`, `service_tags` | Domain chính 1–4, task thuộc domain, dịch vụ |
| `type`, `options`, `correct_option_ids` | `single` hoặc `multiple`; mỗi option có `id`, `text`, `explanation` |
| `sources` | Mỗi nguồn có `title`, URL HTTPS AWS cụ thể và `verified_on` dạng YYYY-MM-DD |

`mixed` phân bổ phần dư lớn nhất: 15 câu → 4/4/4/3; 65 câu → 19/17/16/13. Khi phần dư hòa, ưu tiên domain có số nhỏ hơn. Chọn một có bốn phương án; chọn nhiều có ít nhất năm phương án và ít nhất hai đáp án đúng. Chọn nhiều phải khớp toàn bộ tập đáp án mới được một điểm.

## Kiểm thử

Python kiểm tra schema/builder; Node kiểm tra máy trạng thái. Playwright chỉ cần khi phát triển và kiểm thử trình duyệt, không cần để build hoặc mở HTML:

```bash
.venv/bin/python -m unittest discover -s tests -v
npm install
npm test
npx playwright install chromium
PYTHON="$PWD/.venv/bin/python" npm run test:browser
```

Browser tests tự tạo fixture 15/65 câu cho cả hai mode trong thư mục tạm và xóa khi xong. Fixture ghi rõ không dùng ôn thi. Đặt `QA_OUTPUT` thành một thư mục nếu muốn giữ ảnh desktop/mobile.

## Phạm vi kiểm chứng và giới hạn

- Validator kiểm tra cấu trúc, liên kết đáp án/task, tỷ trọng, trùng câu chính xác sau chuẩn hóa và hình thức nguồn. Không mở URL hoặc xác nhận tính đúng kỹ thuật; làm theo [checklist](references/question-quality.md).
- Luật kỳ thi và nguồn đối chiếu nằm trong [exam-rules.md](references/exam-rules.md); task/domain nằm trong [domains.md](references/domains.md).
- HTML chứa toàn bộ dữ liệu đáp án để chạy offline; đây là công cụ tự học, không phải hệ thống thi giám sát. Chế độ thi ẩn đáp án trên UI.
- Tải lại/đóng trang mất tiến độ. Khi tab được mở lại sau khi bị trình duyệt tạm ngưng, đồng hồ tính theo thời gian đã trôi và nộp nếu hết giờ.
- Chưa có xuất/nhập lịch sử, luyện thích ứng hoặc chống lặp giữa nhiều buổi (giai đoạn 3).
- Khi không có widget, giao HTML; nếu chỉ có chat thì hỏi từng câu và nói rõ chat không có đồng hồ tự nộp nền.
