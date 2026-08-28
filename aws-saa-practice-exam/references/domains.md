# Tài liệu tham chiếu domain SAA-C03

Dùng tài liệu này để giữ cho câu hỏi được tạo ra có nền tảng kỹ thuật chính xác và dàn trải
đúng phạm vi đề thi thật — thay vì cứ xoay quanh vài dịch vụ quen thuộc mỗi lần. Đây không
phải danh sách đầy đủ tuyệt đối; hãy dùng nó như một checklist/gợi nhớ, không phải giới hạn
cứng về những gì có thể xuất hiện.

## Domain 1: Design Secure Architectures (30%)

**Task statement:**
1. Thiết kế quyền truy cập an toàn vào tài nguyên AWS
2. Thiết kế workload và ứng dụng an toàn
3. Xác định các biện pháp kiểm soát bảo mật dữ liệu phù hợp

**Dịch vụ/khái niệm nên khai thác:** IAM (role, policy, permission boundary, SCP), AWS
Organizations, IAM Identity Center, Cognito (user pool vs identity pool), STS/AssumeRole,
Security Group vs NACL, KMS (key policy, envelope encryption, multi-region key), các tuỳ chọn
mã hoá của S3 (SSE-S3/SSE-KMS/SSE-C), Secrets Manager vs Parameter Store, VPC endpoint
(interface vs gateway) để giữ traffic không đi ra internet công cộng, AWS Shield/WAF,
GuardDuty, Security Hub, Macie, CloudTrail vs CloudWatch Logs, AWS Certificate Manager, các
mẫu hình truy cập chéo tài khoản (cross-account), S3 Object Lock/bucket policy phục vụ tuân
thủ, mã hoá khi truyền (TLS), Network Firewall.

**Các kiểu tình huống thường gặp:** quyền truy cập tối thiểu (least-privilege) trên nhiều tài
khoản, bảo vệ dữ liệu khi lưu trữ/truyền tải để đáp ứng yêu cầu tuân thủ (kiểu ràng buộc
HIPAA/PCI mà không nêu tên quy định cụ thể), bảo mật ứng dụng public khỏi các cuộc tấn công
phổ biến, tập trung hoá kết quả bảo mật/logging trên toàn AWS Organization, xoay vòng
credential/secret một cách an toàn.

## Domain 2: Design Resilient Architectures (26%)

**Task statement:**
1. Thiết kế kiến trúc có khả năng mở rộng và liên kết lỏng lẻo (loosely coupled)
2. Thiết kế kiến trúc có tính sẵn sàng cao và/hoặc chịu lỗi tốt

**Dịch vụ/khái niệm nên khai thác:** Multi-AZ vs Multi-Region, Auto Scaling Group, các loại
ELB (ALB/NLB/GWLB) và health check, SQS (standard vs FIFO) và dead-letter queue, SNS,
EventBridge, Step Functions, RDS Multi-AZ vs read replica, Aurora Global Database, DynamoDB
Global Tables, DynamoDB on-demand vs provisioned, S3 cross-region replication, các chính sách
định tuyến của Route 53 (failover, weighted, latency, geolocation) và health check, chiến lược
backup/DR (backup & restore, pilot light, warm standby, multi-site active/active) cùng đánh
đổi RTO/RPO, tách rời (decouple) hệ thống monolith liên kết chặt bằng queue/event, mẫu hình
circuit breaker.

**Các kiểu tình huống thường gặp:** tách rời một hệ thống đồng bộ bị lỗi khi quá tải, chọn
chiến lược DR cho một mục tiêu RTO/RPO cụ thể, thiết kế chịu được lỗi AZ hoặc region, xử lý
traffic tăng đột biến mà không cần can thiệp thủ công, yêu cầu về thứ tự message/idempotency.

## Domain 3: Design High-Performing Architectures (24%)

**Task statement:**
1. Xác định giải pháp lưu trữ hiệu năng cao và/hoặc có khả năng mở rộng
2. Thiết kế giải pháp compute hiệu năng cao và co giãn linh hoạt
3. Xác định giải pháp database hiệu năng cao
4. Xác định kiến trúc mạng hiệu năng cao và/hoặc có khả năng mở rộng
5. Xác định giải pháp thu thập và xử lý dữ liệu hiệu năng cao

**Dịch vụ/khái niệm nên khai thác:** các storage class của S3 và lifecycle policy, S3 Transfer
Acceleration, EFS vs FSx (cho Windows/Lustre/NetApp) vs instance store vs các loại EBS
(gp3/io2/st1/sc1), lựa chọn dòng instance EC2, placement group, Spot vs Reserved vs Savings
Plans vs On-Demand, Lambda vs container (ECS/Fargate/EKS) cho compute co giãn linh hoạt,
DynamoDB DAX, RDS read replica và Aurora để scale read, ElastiCache (Redis vs Memcached),
Redshift, CloudFront (caching behavior, loại origin), Global Accelerator, Direct Connect vs
Site-to-Site VPN, VPC peering vs Transit Gateway, Kinesis (Data Streams/Firehose/Analytics) vs
Glue vs EMR cho việc thu thập/ETL dữ liệu.

**Các kiểu tình huống thường gặp:** giảm độ trễ cho người dùng phân tán toàn cầu, chọn đúng
tầng lưu trữ theo kiểu truy cập, mở rộng khả năng đọc mà không over-provision, chọn compute
phù hợp cho tải bùng phát vs tải ổn định, thu thập/streaming khối lượng dữ liệu lớn một cách
hiệu quả.

## Domain 4: Design Cost-Optimized Architectures (20%)

**Task statement:**
1. Thiết kế giải pháp lưu trữ tối ưu chi phí
2. Thiết kế giải pháp compute tối ưu chi phí
3. Thiết kế giải pháp database tối ưu chi phí
4. Thiết kế kiến trúc mạng tối ưu chi phí

**Dịch vụ/khái niệm nên khai thác:** chuyển đổi lifecycle của S3 sang IA/Glacier/Deep Archive,
S3 Intelligent-Tiering, Compute Savings Plans vs Reserved Instances vs Spot, right-sizing bằng
Compute Optimizer, Aurora Serverless vs provisioned, DynamoDB on-demand vs provisioned +
auto-scaling, đánh đổi chi phí giữa NAT Gateway vs NAT instance, VPC endpoint để giảm chi phí
NAT/data-transfer, Trusted Advisor / Cost Explorer / AWS Budgets, chọn giữa Direct Connect và
VPN dựa trên khối lượng dữ liệu và chi phí, gỡ bỏ tài nguyên nhàn rỗi, nhận thức về chi phí
truyền dữ liệu liên vùng.

**Các kiểu tình huống thường gặp:** một giải pháp hiện tại vẫn hoạt động về mặt kỹ thuật nhưng
đang trả dư tiền (sai storage class, compute cấp dư thừa, tài nguyên không dùng đến), chọn mô
hình tính giá cho tải dự đoán được vs không dự đoán được, giảm chi phí truyền dữ liệu, giảm
chi phí gánh nặng vận hành (dịch vụ managed vs tự vận hành).
