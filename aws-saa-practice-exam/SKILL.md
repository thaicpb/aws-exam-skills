---
name: aws-saa-practice-exam
description: Tạo câu hỏi ôn luyện sát với đề thi thật AWS Certified Solutions Architect - Associate (SAA-C03) và chạy dưới dạng quiz tương tác có chấm điểm ngay trong chat. Dùng skill này bất cứ khi nào người dùng muốn học, ôn luyện, hoặc luyện đề cho kỳ thi AWS SAA-C03 — kể cả các yêu cầu như "tạo đề ôn luyện AWS", "quiz AWS SAA", "practice exam for AWS solutions architect", "give me some AWS SA questions", "kiểm tra kiến thức AWS", hay "luyện thi AWS SAA-C03" — ngay cả khi họ chỉ nêu một chủ đề (ví dụ "quiz mình về S3 storage classes" hoặc "cho tôi vài câu về VPC") mà không nói rõ là "đề thi". Luôn ưu tiên skill này thay vì trả lời bằng câu hỏi-đáp tĩnh dạng text thuần, vì mục đích chính là trải nghiệm tương tác, chấm điểm, với tình huống sát thực tế và các phương án nhiễu giống đề thi thật.
---

# Trình tạo đề ôn luyện AWS SAA-C03

## Mục đích

Tạo ra các câu hỏi ôn luyện có cảm giác giống đề thi SAA-C03 thật — dựa trên tình huống,
có phương án nhiễu hợp lý, không phải câu hỏi học thuộc lòng — và trình bày dưới dạng một
widget quiz tương tác độc lập để người dùng nhận phản hồi ngay lập tức và điểm số cuối cùng,
giống như một bài luyện thi thật.

Hỏi-đáp bằng text tĩnh trong chat là một giải pháp yếu hơn nhiều so với việc này. Luôn dựng
widget tương tác trừ khi người dùng nói rõ họ muốn text thuần hoặc một file tải về.

## Bước 1: Xác định hình thức của buổi luyện

Nếu người dùng đã nói rõ số lượng câu hỏi, domain muốn tập trung, hoặc độ khó, hãy dùng đúng
yêu cầu đó. Nếu không, mặc định tạo **bộ 15 câu luyện tập trộn đều**, phân bổ theo đúng tỷ
trọng domain chính thức của kỳ thi (xem bên dưới), và nói ngắn gọn về việc dùng mặc định để
người dùng có thể yêu cầu khác nếu muốn ("Mình sẽ tạo 15 câu hỏi trộn đều theo tỉ trọng domain
chính thức, bạn có thể yêu cầu khác nếu muốn — ví dụ tập trung riêng một domain, hay làm bộ
65 câu mô phỏng đầy đủ").

Đừng chờ hỏi trước khi bắt tay vào làm — cứ dùng mặc định rồi để người dùng yêu cầu làm lại
nếu họ muốn khác. Chỉ hỏi trước khi bắt đầu nếu yêu cầu thực sự mơ hồ về *chủ đề* (ví dụ họ
nói "quiz AWS" mà không có ngữ cảnh gì và không rõ có phải SAA-C03 hay chứng chỉ khác — nhưng
vì skill này đã được giới hạn riêng cho SAA-C03 nên trường hợp này hiếm khi xảy ra).

Các hình thức luyện tập thường gặp:
- **Luyện nhanh**: 10-15 câu, trộn đều các domain — phù hợp làm mặc định cho các yêu cầu kiểu
  "quiz mình đi".
- **Luyện tập trung**: người dùng nêu tên một domain hoặc dịch vụ cụ thể (ví dụ "quiz mình về
  S3", "câu hỏi về VPC và networking") — lấy phần lớn hoặc toàn bộ câu hỏi từ khu vực đó thay
  vì phân bổ theo tỷ trọng domain.
- **Mô phỏng đầy đủ**: người dùng muốn trải nghiệm giống thi thật — 65 câu (đề thi thật có 50
  câu tính điểm + 15 câu thử nghiệm không tính điểm, nhưng để luyện tập thì cứ trình bày 65
  câu hỏi sát thực tế), phân bổ theo tỷ trọng domain bên dưới.

## Bước 2: Nắm rõ khung nội dung đề thi

Tỷ trọng domain chính thức của SAA-C03 (theo nội dung tính điểm):

| Domain | Tỷ trọng |
|---|---|
| Design Secure Architectures | 30% |
| Design Resilient Architectures | 26% |
| Design High-Performing Architectures | 24% |
| Design Cost-Optimized Architectures | 20% |

Đọc file `references/domains.md` để biết các task statement và những dịch vụ/khái niệm AWS
gắn liền với từng domain — dùng nó để giữ cho tình huống có nền tảng kỹ thuật chính xác và để
dàn trải câu hỏi qua nhiều dịch vụ khác nhau thay vì cứ xoay quanh 3-4 dịch vụ quen thuộc
(EC2/S3/VPC) mỗi lần. Hãy thay đổi dịch vụ làm trọng tâm của câu hỏi giữa các buổi luyện.

## Bước 3: Viết câu hỏi giống đề thi thật, không phải câu đố kiến thức

Đây là phần quan trọng nhất của skill này. Đề thi thật hiếm khi hỏi "dịch vụ X dùng để làm
gì" — nó mô tả một tình huống kinh doanh và hỏi tổ hợp dịch vụ/cấu hình nào đáp ứng tốt nhất
các ràng buộc đã nêu (chi phí, độ trễ, tuân thủ, gánh nặng vận hành, RTO/RPO, v.v.). Hãy mô
phỏng đúng phong cách đó:

- **Đoạn tình huống (stem)**: 2-5 câu mô tả một công ty/hệ thống và các ràng buộc của nó. Cung
  cấp đủ thông tin để người đọc có thể suy luận về sự đánh đổi (trade-off), chứ không chỉ là
  nhớ lại một sự kiện.
- **Câu hỏi** nên yêu cầu chọn phương án *tốt nhất* dựa trên các ràng buộc đã nêu — ngụ ý rằng
  có thể nhiều hơn một phương án về mặt kỹ thuật là khả thi, nhưng chỉ một phương án là tối ưu.
- **Bốn phương án trả lời.** Phần lớn câu hỏi chọn một đáp án; thỉnh thoảng (khoảng 1 trong
  5-8 câu) hãy làm câu "chọn HAI" (multi-response), đúng theo tỷ lệ của đề thi thật.
- **Phương án nhiễu phải hợp lý**, không được ngớ ngẩn. Các kiểu nhiễu hay gặp trong đề thi thật:
  - Một giải pháp về mặt kỹ thuật vẫn hoạt động nhưng vi phạm một ràng buộc đã nêu (ví dụ tốn
    chi phí hơn, không phải Multi-AZ trong khi tình huống yêu cầu HA, tạo thêm gánh nặng vận
    hành không cần thiết)
  - Một dịch vụ nghe rất giống hoặc liên quan nhưng dùng sai (SQS vs SNS vs EventBridge, S3
    Glacier vs Glacier Deep Archive, ALB vs NLB vs Gateway Load Balancer)
  - Một cách làm cũ/lỗi thời mà best practice của AWS đã không còn khuyến nghị
  - Một giải pháp thiếu một mảnh ghép cần thiết (ví dụ đúng dịch vụ nhưng sai cấu hình dự
    phòng/failover)
  - Tránh các đáp án sai một cách hiển nhiên hoặc buồn cười — mọi phương án đều phải khiến
    người đọc thực sự phải suy nghĩ.
- **Độ khó**: cấp độ associate, không phải cấp độ professional. Giả định người học có khoảng
  1 năm kinh nghiệm thực hành AWS. Không đòi hỏi tham số API hiếm gặp hay các đánh đổi kiến
  trúc chuyên sâu vốn dành cho SAP-C02.
- **Không lặp câu trong cùng một buổi** — theo dõi những dịch vụ/tình huống đã dùng trong batch
  này và thay đổi liên tục.
- **Viết bằng ngôn ngữ mà người dùng đang dùng** trong cuộc trò chuyện (viết tình huống/câu hỏi
  bằng tiếng Việt hoàn toàn phù hợp và thường được ưa thích hơn — điều này bình thường với
  người học không phải bản ngữ tiếng Anh khi ôn thi chứng chỉ Mỹ). Dù vậy, vẫn giữ nguyên tên
  dịch vụ AWS chính thức bằng tiếng Anh, vì đó là cách chúng xuất hiện trên đề thi thật.

Với mỗi câu hỏi, cũng cần chuẩn bị sẵn:
- (Các) đáp án đúng
- Giải thích ngắn gọn vì sao đáp án đúng là đúng
- Lý do ngắn gọn vì sao từng phương án *sai* lại sai (đây là chỗ người học thực sự tiếp thu
  kiến thức — đừng bỏ qua phần này dù có bị hối thúc về thời gian)
- Câu hỏi thuộc domain nào (để tính phân tích điểm theo domain)

## Bước 4: Trình bày dưới dạng widget quiz tương tác

Gọi `visualize:read_me` với `modules: ["interactive"]` trước, sau đó dựng bộ đề thành một
widget HTML độc lập bằng `visualize:show_widget`. Đừng chỉ in câu hỏi ra dưới dạng text trong
chat — tính tương tác (bấm chọn đáp án, nhận phản hồi ngay, thấy điểm số đang chạy) mới là
điểm cốt lõi.

Yêu cầu đối với widget:
- Hiển thị một câu hỏi tại một thời điểm, kèm chỉ báo tiến độ ("Câu 3/15").
- Người dùng chọn đáp án (radio cho câu chọn một, checkbox cho câu chọn nhiều) và bấm xác
  nhận — hiển thị ngay đúng/sai kèm phần giải thích (lý do đáp án đúng, và nếu chọn sai thì
  thêm lý do vì sao phương án họ chọn lại sai).
- Có nút "Câu tiếp theo" để chuyển câu.
- Hiển thị điểm số đang chạy hoặc có thể xem được.
- Ở cuối bài: điểm số cuối cùng, so sánh đạt/không đạt dựa trên ngưỡng điểm quy đổi 720/1000
  của đề thi thật nhưng diễn giải đơn giản (ví dụ "bạn cần đúng khoảng 72% trở lên để tương
  đương mức đạt"), và bảng phân tích theo từng domain (ví dụ "Security: 4/5, Resilient:
  3/4...") để người dùng biết nên tập trung ôn thêm ở đâu.
- Toàn bộ trạng thái chỉ lưu trong biến JS/React state trong phiên hiện tại — không bao giờ
  dùng localStorage hay sessionStorage (không được hỗ trợ trong môi trường này).
- Giữ thiết kế gọn gàng, giống môi trường thi thật: màu sắc trầm, chữ rõ ràng, không cần yếu
  tố giải trí thừa thãi. Đây là công cụ học tập, không phải trò chơi.

Nếu bộ câu hỏi lớn (mô phỏng đầy đủ 65 câu), có thể phân trang/render dần, nhưng vẫn nên nhúng
toàn bộ dữ liệu câu hỏi trong một widget duy nhất thay vì cố lấy dữ liệu từ nguồn ngoài.

## Bước 5: Kết thúc

Sau khi làm xong bài quiz, gợi ý bước tiếp theo một cách tự nhiên — ví dụ một bộ câu hỏi khác
tập trung vào các domain họ làm sai, hoặc một bài mô phỏng đầy đủ nếu họ vừa luyện nhanh xong.
Không cần gợi ý quá gượng ép, chỉ cần để lựa chọn đó hiện diện rõ ràng.
