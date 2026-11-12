# Báo cáo thực hành Day 3 — Image Segmentation

- Mã học viên theo lớp: 2A202603275
- Họ và tên: Hoàng Minh Hải
- Ngày thực hành: 11/11/2026
- Ngày kiểm tra và chuẩn bị bài nộp: 12/11/2026
- Môi trường: CVAT local; Git/GitHub để quản lý bài nộp.
- Công cụ kiểm tra: scripts/inspect_submissions.py.
- Ghi chú: Các thông tin về thao tác tự vẽ, gợi ý tự động và sửa mask chỉ được xác nhận khi có bằng chứng; không suy ra từ cấu trúc ZIP.

## 1. Bài đã nộp

Ba ZIP đã có trong thư mục submissions/ và đã vượt qua kiểm tra cấu trúc. Số ảnh dưới đây là số ảnh có dữ liệu mask trong bản export, không phải xác nhận mọi vùng hoặc vật đều đã được gán nhãn chính xác.

| Task | File ZIP đúng tên | Số ảnh có dữ liệu mask | Điểm tối đa (coach chấm sau) |
| --- | --- | ---: | ---: |
| easy_semantic | submissions/easy_semantic.zip | 3 / 3 | 20 |
| medium_instance | submissions/medium_instance.zip | 3 / 3 | 32 |
| hard_panoptic | submissions/hard_panoptic.zip | 2 / 2 | 30 |
| cp1_holes | Chưa có | 0 / 1 | 3 |
| cp2_slice | Chưa có | 0 / 1 | 3 |
| cp5_occlusion | Chưa có | 0 / 1 | 3 |
| cp3_thin | Chưa có | 0 / 1 | 3 |
| cp4_curb | Chưa có | 0 / 1 | 3 |
| cp6_coverage | Chưa có | 0 / 1 | 3 |
| **Tổng tối đa** | | | **100** |

### Kết quả kiểm tra cấu trúc

- easy_semantic.zip: OK; có mask semantic cho đúng ba ảnh.
- medium_instance.zip: OK; có 72 annotations dạng RLE trên ba ảnh, đúng danh sách class của task.
- hard_panoptic.zip: OK; có 77 annotations dạng RLE trên hai ảnh, đúng danh sách class của task.
- Sáu checkpoint chưa có ZIP trong bài nộp hiện tại.

Kết quả OK chỉ xác nhận cấu trúc export, tên ảnh, class và dạng biểu diễn mask. Kết quả này không xác nhận biên chính xác, đủ object hoặc chất lượng panoptic.

## 2. Một quyết định trước khi dùng gợi ý

Bản export Medium hiện có dữ liệu cho các ảnh:

- 000000181542.jpg
- 000000373353.jpg
- 000000458325.jpg

Chưa có nhật ký thao tác đủ để xác nhận object nào được tự vẽ đầu tiên trước khi xem gợi ý, công cụ vẽ cụ thể hoặc quyết định sửa/giữ một đề xuất tự động. Vì vậy, tôi chưa khai nhận một object cụ thể là bằng chứng tự vẽ trước gợi ý.

Quy tắc áp dụng để rà soát Medium:

- Mỗi vật nhìn thấy thuộc class của task cần được xác định theo từng instance.
- Hai vật cùng class đứng sát nhau vẫn là hai instance.
- Chỉ gán nhãn phần nhìn thấy; không suy đoán phần nằm sau vật che.
- Một vật bị che thành nhiều mảng nhìn thấy không mặc nhiên được tách thành nhiều instance.
- Mọi gợi ý tự động cần được kiểm lại class, biên và số object trước khi giữ.

Phần bằng chứng object đầu tiên tự vẽ hiện còn thiếu; cần được đối chiếu với lịch sử thao tác hoặc xác nhận trong CVAT.

## 3. Một lỗi tôi tìm thấy và sửa

### Vấn đề đã xác định trong quá trình chuẩn bị bài nộp

- Phạm vi: thư mục gốc của repository.
- Loại lỗi: quản lý file bài nộp.
- Bằng chứng: repository có file tiers_gt.zip, trong khi quy định không cho đưa ground truth lên fork.
- Hành động: file tiers_gt.zip đã được đánh dấu xóa trong working tree trên máy.
- Trạng thái: cần commit và push thay đổi để việc xóa có hiệu lực trên GitHub.

Việc này không thay đổi các ZIP bài làm trong submissions/.

### Trạng thái kiểm tra lỗi annotation

Chưa có bằng chứng trước/sau để mô tả trung thực một lỗi mask cụ thể đã được sửa và export lại. Vấn đề quản lý ground truth ở trên không thay thế yêu cầu chứng minh một lỗi annotation nếu coach yêu cầu.

### Kết quả tự kiểm

Đã kiểm tra cấu trúc bằng lệnh:

python3 scripts/inspect_submissions.py --dir submissions

Kết quả:

- Easy: OK.
- Medium: OK, 72 annotations dạng RLE.
- Hard: OK, 77 annotations dạng RLE.
- Sáu checkpoint: THIẾU.

Chưa ghi nhận giá trị điểm hoặc metric trong báo cáo này vì chưa đối chiếu nội dung scorecard. Điểm tự đánh giá ba tier, nếu có, tối đa 82 và không phải điểm cuối trên 100.

## 4. Ba ca chưa chắc hoặc cần rà soát

Các mục dưới đây là câu hỏi QC cần kiểm lại trên ảnh/mask, chưa được khai nhận là ba tình huống đã quan sát và xử lý trong phiên thực hành.

| Task / ảnh cần rà soát | Hai cách hiểu cần phân biệt | Quy tắc/chứng cứ cần kiểm | Quyết định hoặc câu hỏi cho coach |
| --- | --- | --- | --- |
| Easy — 817bca71-00000000.jpg; vùng road–sidewalk | Phân lớp theo màu bề mặt hoặc theo chức năng của vùng | Kiểm bó vỉa, mép đường và chức năng sử dụng; màu gần giống không có nghĩa cùng class | Cần xác nhận ranh road–sidewalk trong mask hiện tại có theo chức năng/bó vỉa không |
| Medium — 000000181542.jpg; các vật sát nhau hoặc bị che nếu xuất hiện | Gộp nhiều vật thành một instance, hoặc tách một vật bị che thành nhiều instance | Đối chiếu phần nhìn thấy và định danh từng vật; không chỉ dựa vào việc các mảng mask có nối liền nhau | Cần kiểm số instance và xác nhận các mảng bị che được gán đúng định danh |
| Hard — 000000350023.jpg; ranh stuff–thing | Cho vùng stuff kéo qua vật phía trước hoặc loại phần vật nhìn thấy khỏi stuff | Đối chiếu ảnh gốc, kiểm chồng lấn và khoảng trống giữa stuff với từng thing | Cần xác nhận độ phủ và thứ tự che khuất; COCO hợp lệ chưa đủ chứng minh panoptic đúng |

## Phần còn thiếu

- Sáu checkpoint chưa có bài export.
- Chưa có bằng chứng xác nhận object Medium đầu tiên tự vẽ trước gợi ý.
- Chưa có bằng chứng trước/sau của một lỗi annotation đã sửa.
- Ba câu hỏi QC ở mục 4 cần đối chiếu trực quan để trở thành các ca cụ thể đã kiểm tra.
- Cần commit/push việc xóa ground truth, đổi tên và cập nhật báo cáo.
- Trạng thái nộp bài trên LMS được xác nhận riêng sau khi gửi link repository.