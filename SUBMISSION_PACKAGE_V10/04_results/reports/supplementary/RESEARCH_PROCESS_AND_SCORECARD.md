# Báo cáo tiến trình nghiên cứu hệ thống dự báo SOH/RUL pin

## 1. Kết luận điều hành

Dự án đã đi theo đúng phương hướng nghiên cứu được xác lập ban đầu:

`Data → degradation insight → Health Indicators → SOH/EOL/RUL → model ladder → LOBO/early prediction/uncertainty → online replay → external validation`

Nghiên cứu hiện đã hoàn thành phần lớn giai đoạn nghiên cứu và chứng minh trên NASA, đã có prototype online bằng replay, đồng thời đã thực hiện external validation trên CALCE. Tuy nhiên, mô hình chưa vượt qua cổng generalization cross-domain vì uncertainty coverage trên CALCE chưa đạt yêu cầu. Do đó, trạng thái đúng là **research prototype có kiểm chứng nội bộ, chưa phải hệ thống sẵn sàng triển khai thực tế**.

## 2. Các công việc đã thực hiện

### Dữ liệu và ground truth

- Kiểm kê các tệp NASA, tính SHA-256, phát hiện duplicate và lập manifest dữ liệu đã xử lý.
- Parse charge/discharge/EIS và chuẩn hóa dữ liệu theo battery/cycle/operation.
- Tạo bảng đặc trưng theo chu kỳ: capacity, duration, energy, Ah throughput, voltage, current, temperature và lịch sử vận hành.
- Lập quality flags và quyết định xử lý anomaly/missing capacity.
- Định nghĩa SOH, EOL và RUL; khóa công thức `RUL = max(EOL cycle − current cycle, 0)`.
- Không tạo nhãn RUL giả cho B0007 trong protocol chính; xử lý cell không quan sát EOL như censored.
- Kiểm tra độ nhạy ngưỡng EOL 70%, 75%, 80%.

### Insight degradation và Health Indicators

- Phân tích correlation theo battery và toàn bộ tập.
- So sánh cycle-only, capacity history, V/I/T statistics và operating history.
- Thực hiện ablation, kiểm định nhiều seed, feature-rank stability, redundancy audit và condition-shift audit.
- Phân tích partial discharge curve và alignment theo voltage grid.
- Khóa HI v2 cho ba chế độ: online 10%, online 20% và after-cycle.
- Áp dụng leakage control: lag history, imputation và scaling chỉ trên training fold.

### Model và protocol đánh giá

- Xây linear và tree-based baselines cho capacity/SOH/RUL.
- Xây trajectory models với raw/median/isotonic/Savitzky–Golay và robust-linear/piecewise/power-law/template dynamics.
- Cải thiện uncertainty bằng bootstrap/calibration và audit lỗi theo battery/checkpoint.
- Cài PyTorch CUDA và huấn luyện GRU/TCN dưới cùng protocol.
- Đánh giá LOBO, không random-split cycle cùng battery.
- Khóa checkpoint quan sát 20%, 40%, 60%, 80% và chạy 10 seeds cho deep models.
- TCN được chọn trên NASA; GRU/TCN chỉ được chấp nhận khi so sánh cùng protocol với baseline.

### Online và external validation

- Tạo online cycle replay: chu kỳ mới → cập nhật SOH/RUL và prediction interval.
- Online replay TCN: B0005 MAE 14.01, B0006 10.34, B0018 6.97 cycles.
- Tải và parse bộ CALCE CS2_35–CS2_38 từ nguồn chính thức, gồm 3,921 discharge cycles.
- Định nghĩa EOL CALCE không dùng thông tin test để fit model; EOL quan sát tại 545–692 cycles.
- Thực hiện zero-shot NASA→CALCE, calibration-only LOBO, checkpoint calibration LOBO, fine-tuning LOBO và external classical baseline.
- Checkpoint calibration giảm mean MAE 74.4% so với zero-shot, còn 43.26 cycles, nhưng coverage chỉ 68.8% so với cổng tối thiểu 80%.
- Khóa kết luận external validation: chưa chấp nhận deployment cross-domain.

## 3. Scorecard theo tám bước ban đầu

| Bước | Nội dung | Điểm | Trạng thái | Cơ sở chấm điểm / phần còn thiếu |
|---:|---|---:|---|---|
| 1 | Hiểu và chuẩn hóa dữ liệu | 9.5/10 | Gần hoàn chỉnh | Có parser, duplicate inventory, manifest, data dictionary, quality flags và canonical cycle table. Còn thiếu versioned dataset release/schema validation tự động đầy đủ. |
| 2 | Tìm insight degradation | 8.5/10 | Tốt | Đã phân tích V/I/T, duration, energy, history, partial curves, condition shift. Novel insight vẫn cần diễn giải cơ chế vật lý và xác nhận trên thêm chemistry/dataset. |
| 3 | Chứng minh insight và chọn HI | 8.5/10 | Tốt | Có ablation, nhiều seed, statistical tests, rank stability, redundancy và HI v2 khóa. Số battery NASA độc lập còn ít, nên chưa thể coi là chứng minh phổ quát. |
| 4 | Ground truth SOH/EOL/RUL | 9.0/10 | Gần hoàn chỉnh | Có EOL/RUL rõ, sensitivity 70/75/80%, censoring và integrity checks. Cần chốt một primary EOL definition xuyên suốt luận án và dùng survival-aware metric cho censored cells. |
| 5 | Xây model dự báo | 8.5/10 | Tốt | Có baseline, trajectory, uncertainty, GRU và TCN. GPR/joint SOH–trajectory–RUL chưa trở thành champion thống nhất; domain-adaptive model chưa có. |
| 6 | Chứng minh RUL/generalization | 7.5/10 | Đã kiểm tra nhưng chưa đạt mục tiêu cuối | LOBO và 20/40/60/80% trên NASA đã đúng. External validation CALCE đã hoàn tất về quy trình nhưng model trượt coverage; mới có bốn CALCE batteries. |
| 7 | Online adaptive RUL | 8.0/10 | Prototype đạt | Có sequential replay và uncertainty theo cycle. Chưa có drift detection, incremental recalibration an toàn, latency/resource benchmark hoặc BMS streaming thật. |
| 8 | Prototype/ứng dụng thực tế | 4.5/10 | Mới ở mức lõi kỹ thuật | Có pipeline và replay, nhưng chưa có dashboard hoàn chỉnh, API/service packaging, container, hardware-in-loop, BMS thật hoặc field test. |

**Điểm trung bình theo tám bước: 8.0/10 (64/80).** Đây là điểm cho tiến độ và độ chặt của process, không phải tuyên bố mô hình đã sẵn sàng thương mại.

## 4. Chấm theo ba giai đoạn lớn

| Giai đoạn | Điểm | Nhận định |
|---|---:|---|
| Nghiên cứu: Data → Insight → HI → RUL definition | 8.9/10 | Phần mạnh nhất; đã có traceability và nhiều audit bổ sung. |
| Chứng minh khoa học: Model → early prediction → uncertainty/generalization | 7.8/10 | NASA tốt và protocol đúng; external generalization chưa đạt. |
| Sản phẩm hóa: Online estimator → app → BMS thật | 5.8/10 | Online replay đã có, nhưng tầng ứng dụng và phần cứng chưa làm. |

**Điểm tổng thể theo trọng số nghiên cứu 40%, chứng minh 40%, sản phẩm 20%: 8.0/10.**

## 5. Có theo đúng một hướng nghiên cứu đã định không?

Có. Các lần bổ sung trajectory dynamics, uncertainty calibration, GRU/TCN, online replay và CALCE không phải các nhánh rời rạc; chúng là các phép thử nối tiếp của cùng giả thuyết trung tâm:

> RUL không nên được suy ra chỉ từ cycle count; phải sử dụng tín hiệu degradation từ V/I/T và lịch sử vận hành, sau đó dự báo trajectory tới EOL với uncertainty, đánh giá trên battery chưa thấy và cập nhật theo dữ liệu online.

Điểm thay đổi hợp lý duy nhất là external validation đã cho thấy mô hình NASA học cả thang thời gian riêng của domain. Vì vậy hướng nghiên cứu tiếp theo phải chuyển từ “thử thêm deep architecture” sang “domain-adaptive/hierarchical trajectory + calibrated uncertainty”. Đây là sự thu hẹp câu hỏi nghiên cứu dựa trên bằng chứng, không phải đổi đề tài.

## 6. Các giới hạn phải công bố

1. NASA observed-EOL set chính chỉ có ba battery độc lập cho RUL evaluation; sai số trung bình có độ bất định lớn.
2. CALCE CS2 chỉ có bốn battery trong phép thử hiện tại.
3. TCN tốt trên NASA nhưng không generalize zero-shot sang CALCE.
4. Prediction interval trên CALCE chưa đạt coverage gate.
5. EOL phụ thuộc threshold; kết quả RUL phải luôn đi kèm định nghĩa EOL.
6. Online hiện là replay, không phải BMS/hardware deployment.

## 7. Thứ tự công việc tiếp theo

1. Khóa research protocol v3 và một primary EOL definition; các ngưỡng khác chỉ dùng sensitivity analysis.
2. Xây hierarchical/domain-adaptive monotonic trajectory model, ưu tiên mô hình có thể giải thích trước khi thử deep model mới.
3. Hiệu chỉnh interval bằng out-of-fold conformal calibration; yêu cầu coverage 85–95% cho nominal 90% interval.
4. Bổ sung một battery family/dataset hoàn toàn untouched để làm final external test.
5. Khi vượt các cổng trên, đóng gói online estimator thành API/dashboard và benchmark latency, memory, drift/fail-safe.
6. Sau cùng mới chuyển sang hardware-in-loop và BMS thật.

## 8. Trạng thái luận án hiện tại

- Có thể viết hoàn chỉnh chương Data, Methodology/Protocol và phần lớn chương NASA Results.
- Có thể viết CALCE External Validation như một kết quả âm có phân tích domain shift.
- Chưa nên viết kết luận rằng mô hình generalizes across datasets hoặc sẵn sàng deployment.
- Novelty tiềm năng mạnh nhất hiện tại là tổ hợp HI partial-curve/history với online trajectory estimation; để trở thành đóng góp vững chắc, cần thêm domain adaptation và external coverage đạt chuẩn.
