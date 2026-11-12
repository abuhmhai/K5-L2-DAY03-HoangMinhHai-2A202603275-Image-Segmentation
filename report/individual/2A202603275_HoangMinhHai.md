# Báo cáo thực hành Day 3 — Image Segmentation

- Mã học viên: **2A202603275**
- Họ và tên: **Hoàng Minh Hải**
- Thời gian thực hành và rà soát: 11–12/11/2026.
- Môi trường: CVAT local tại `http://localhost:8080`; SAM 3 local trên Apple MPS; Python/PyCharm.
- Công cụ thực tế: CVAT Mask/AI Tools; SAM 3 theo điểm dương/âm và box; script Python xử lý mask, kiểm cấu trúc và scorer của lab. Có trợ lý Codex hỗ trợ cài đặt, tạo task, chạy SAM, chỉnh sửa và rà soát; không khai nhận các mask hỗ trợ này là toàn bộ tự vẽ tay.

## 1. Bài đã nộp

Các file dưới đây đã Save trên CVAT, xuất vào `submissions/` của bản fork trên máy và kiểm tra cấu trúc. Đây là trạng thái chuẩn bị bài; việc commit/push và nộp link LMS phải được xác nhận riêng. Số ảnh có annotation không có nghĩa mọi vật hoặc mọi biên đều chính xác.

| Task | File ZIP đúng tên | Ảnh có annotation | Điểm tối đa (coach chấm sau) |
| --- | --- | ---: | ---: |
| easy_semantic | `submissions/easy_semantic.zip` | 3 / 3 | 20 |
| medium_instance | `submissions/medium_instance.zip` | 3 / 3 | 32 |
| hard_panoptic | `submissions/hard_panoptic.zip` | 2 / 2 | 30 |
| cp1_holes | `submissions/cp1_holes.zip` | 1 / 1 | 3 |
| cp2_slice | `submissions/cp2_slice.zip` | 1 / 1 | 3 |
| cp5_occlusion | `submissions/cp5_occlusion.zip` | 1 / 1 | 3 |
| cp3_thin | `submissions/cp3_thin.zip` | 1 / 1 | 3 |
| cp4_curb | `submissions/cp4_curb.zip` | 1 / 1 | 3 |
| cp6_coverage | `submissions/cp6_coverage.zip` | 1 / 1 | 3 |
| **Tổng** | **9 ZIP** | **14 / 14** | **100** |

- Semantic xuất `Segmentation mask 1.1`; instance/panoptic xuất `COCO 1.0`, giữ nguyên nội dung do CVAT xuất.
- Medium hiện có 72 mask; Hard 77 mask. Đây là số annotation đã nộp, không phải số vật đúng theo reference.
- Các checkpoint instance: cp1 có 6 mask, cp2 có 13 mask, cp5 có 34 mask.
- Các checkpoint semantic: cp3 có 4 mask lớp, cp4 có 2 mask lớp, cp6 có 6 lớp xuất hiện trong kết quả; không tạo mask rỗng cho lớp không thấy rõ.
- `scripts/inspect_submissions.py` báo **9 task OK, 0 lỗi cấu trúc, 0 task thiếu ZIP**. Kết quả này không chấm biên, recall hay PQ.

## 2. Một quyết định trước khi dùng gợi ý

Trong phiên CVAT, đã lưu một mask `person` cho người phụ nữ áo dài ở giữa ảnh Medium `000000181542.jpg`, vùng xấp xỉ x=188–304, y=131–460. Mask này được giữ nguyên khi bổ sung các đối tượng khác. Quy tắc áp dụng là chỉ lấy phần người nhìn thấy, không gộp xe máy phía sau vào người và không vẽ xuyên qua vật che.

**Giới hạn bằng chứng:** mask được ghi nhận với nguồn `semi-auto`; không có bằng chứng xác nhận đây là object được vẽ tay trước khi xem gợi ý. Vì vậy, mục này không được coi là đã đáp ứng yêu cầu “tự vẽ object đầu tiên trước gợi ý” trong README. Không khai nhận thao tác chưa được xác minh.

Khi tiếp tục bằng SAM, dùng điểm dương trong từng vật và điểm âm ở nền/vật kế bên; mỗi vật cùng class vẫn được giữ thành một instance riêng. Ở checkpoint che khuất, không tách ID chỉ vì các phần nhìn thấy rời nhau.

## 3. Một lỗi tìm thấy và sửa

**Lỗi cụ thể:** ở `cp3_thin`, ảnh `839f7736-abe28069.jpg`, bản SAM đầu tiên chọn một phần thân và kính xe Toyota phía trước vào lớp `road`. Lỗi thấy rõ trong ảnh phủ màu: màu đường xuất hiện trên cốp và kính xe.

**Sửa thực tế:** tạo vùng loại trừ cho toàn bộ xe nhìn thấy, trừ vùng này khỏi mask đường; giữ xe không gán nhãn vì schema cp3 chỉ có `pole`, `traffic sign`, `sky`, `road`. Bổ sung nét cột/giá đỡ mảnh bằng đường 2–3 px ở các đoạn mảnh; cột lớn giữ bề rộng nhìn thấy. Đã kiểm lại preview, lưu vào CVAT và xuất `cp3_thin.zip`. Mask đường sau sửa không còn phủ phần thân xe đó.

Hai lỗi khác đã quan sát trong quá trình làm: Hard có vùng mặt kính phản chiếu cây bị SAM chọn thành vegetation và vùng làn đường bị chọn thành sidewalk. Đã chỉnh theo mặt kính thực và bó vỉa; không coi màu giống nhau là đủ để gán cùng lớp.

### Kết quả tự đánh giá đã chạy trong PyCharm

Đã dùng scorer nguyên bản của lab với gói reference ba tier được cung cấp, sau khi giữ bản sao các ZIP trước khi mở reference. Không dùng đáp án checkpoint vì chưa được cung cấp.

| Task | Metric | Điểm tự đánh giá |
| --- | ---: | ---: |
| Easy | mIoU 0,777 | 16,8 / 20 |
| Medium | mean matched IoU × recall = 0,559 | 11,3 / 32 |
| Hard | PQ 0,351 | 10,1 / 30 |
| **Ba tier** | | **38,2 / 82** |

Đây là kết quả của ba ZIP tier tại thời điểm kiểm tra, không phải điểm chính thức, PASS hoặc xếp hạng. Chưa tự cộng điểm sáu checkpoint. Những phần cần ưu tiên rà là đối tượng thiếu/sai ở Medium và vỉa hè, người, xe máy ở Hard.

## 4. Ba ca chưa chắc hoặc cần rà soát

| Task / ảnh / vị trí | Hai cách hiểu | Quy tắc và quyết định thực tế | Cần rà thêm |
| --- | --- | --- | --- |
| cp1_holes — `000000144300.jpg`, kính chắn gió/chi tiết trong xe máy và giá chống màu đỏ phía dưới | Chi tiết thuộc xe hay vùng nền/đồ rời? | Giữ kính và chi tiết bên trong mask theo quy tắc trạm; giá chống rời không mặc nhiên thuộc thân xe. Đã làm sạch lỗ nội bộ, không sao chép reference. | Rà biên giá chống và các khe nhỏ; không chỉ dựa vào việc chúng chạm nhau. |
| cp4_curb — `7d83710e-4697c3b2.jpg`, vỉa hè qua lối xe vào và ô đất quanh gốc cây | Mặt bê tông là đường cho xe hay lối đi bộ; ô đất có thuộc sidewalk không? | Bám chức năng và bó vỉa; giữ vùng đi bộ nối tiếp qua lối xe vào. Loại ô đất/gốc cây và xe ra khỏi lớp road/sidewalk khi không thuộc schema. | Ranh lối vào, mép bó vỉa và vùng bị xe che cần xem ở zoom lớn. |
| cp6_coverage — `7daa6479-67988f3f.jpg`, xe buýt lớn và xe tải bên trái | Có nên gán chúng thành car để phủ kín ảnh không? | Schema chỉ có road/sidewalk/building/vegetation/sky/car/person, không có bus/truck. Để các xe không thuộc schema không gán nhãn; không đổi class để ép coverage. | Hỏi coach cách tính ignore/coverage của schema; chưa coi độ phủ toàn ảnh thấp là toàn bộ vùng đều thiếu. |

Các checkpoint đã được kiểm lớp, preview và cấu trúc export; vẫn có thể còn vật nhỏ, biên nhòe, khe hở hoặc class cần sửa. Ground truth chỉ giữ local, không đưa vào ZIP bài làm hay chia sẻ lên fork. Chưa xác nhận nộp LMS hoặc được gia hạn.
