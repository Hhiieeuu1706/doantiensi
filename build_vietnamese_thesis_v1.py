from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parent
pkg=ROOT/'SUBMISSION_PACKAGE_V10'
out=pkg/'05_manuscript'/'BATTERY_RUL_PHD_THESIS_V28_VIETNAMESE_FINAL.docx'
doc=Document()
sec=doc.sections[0]
sec.top_margin=Inches(.75); sec.bottom_margin=Inches(.75); sec.left_margin=Inches(.85); sec.right_margin=Inches(.85)
styles=doc.styles; styles['Normal'].font.name='Arial'; styles['Normal'].font.size=Pt(10.5)
for s in ['Heading 1','Heading 2','Heading 3']:
    styles[s].font.name='Arial'; styles[s].font.color.rgb=RGBColor(31,78,121)

def heading(t,l=1): doc.add_heading(t,level=l)
def para(t=''): doc.add_paragraph(t)
def table(headers,rows):
    t=doc.add_table(rows=1,cols=len(headers)); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for c,x in zip(t.rows[0].cells,headers): c.text=x
    for row in rows:
        cs=t.add_row().cells
        for c,x in zip(cs,row): c.text=x
    for ri,r in enumerate(t.rows):
        for c in r.cells:
            c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(2)
                for run in p.runs:
                    run.font.name='Arial'; run.font.size=Pt(8.5)
                    if ri==0: run.bold=True; run.font.color.rgb=RGBColor(255,255,255)
            if ri==0:
                shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),'1F4E79'); c._tc.get_or_add_tcPr().append(shd)
    return t

doc.add_heading('Ước lượng RUL có xét lịch sử cho pin lithium-ion',0)
q=doc.add_paragraph('Lựa chọn LOBO có kiểm soát rò rỉ và kiểm chứng ngoài miền HUST'); q.alignment=WD_ALIGN_PARAGRAPH.CENTER
q=doc.add_paragraph('Bản tiếng Việt của luận văn nghiên cứu Battery RUL'); q.alignment=WD_ALIGN_PARAGRAPH.CENTER

heading('Tóm tắt',1)
para('Dự báo thời gian sử dụng còn lại (Remaining Useful Life – RUL) của pin phải đáng tin cậy khi pin kiểm tra chưa từng xuất hiện trong dữ liệu huấn luyện, lịch sử vận hành khác nhau và dữ liệu được quan sát tuần tự theo thời gian. Nghiên cứu này xây dựng một quy trình có kiểm soát rò rỉ gồm: audit dữ liệu V/I/T/time, tạo health indicator, định nghĩa EOL có xét censoring, chọn model bằng battery-level LOBO, hiệu chỉnh uncertainty trên tập riêng và đánh giá ngoài miền trên HUST. Random Forest là model tốt nhất trong nhóm đã đánh giá dưới protocol khóa; đây không phải tuyên bố về một thuật toán học mới hay numerical SOTA.')
para('Kết quả cho thấy current state thường có thông tin mạnh hơn cycle count. History có thông tin dự báo nhưng hiệu quả phụ thuộc checkpoint: có thể làm xấu dự báo sớm và cải thiện dự báo ở giai đoạn quan sát dài hơn. Trên HUST final untouched, sai số RUL giảm từ 116.5 xuống 20.3 cycles khi quan sát tăng từ 20% lên 80% đời pin. Prediction intervals đạt coverage mục tiêu nhưng còn rộng, đặc biệt ở early life; do đó hệ thống hiện là research prototype, chưa phải BMS production-ready.')
para('Từ khóa: dự báo RUL; SOH; LOBO; health indicator; external validation; conformal prediction; HUST; battery prognostics.')

heading('Hướng dẫn đọc nhanh',1)
para('Câu hỏi trung tâm của luận văn là: một hệ thống RUL có còn đáng tin khi pin kiểm tra chưa từng thấy, protocol thay đổi, không được dùng dữ liệu tương lai và phải báo cáo uncertainty trung thực hay không? Câu trả lời được kiểm chứng theo chuỗi: audit dữ liệu → HI → EOL/RUL → split theo pin → LOBO → adaptation phát triển → calibration → test ngoài miền → replay tuần tự.')
table(['Thuật ngữ','Ý nghĩa đơn giản'],[
('SOH','Trạng thái sức khỏe hiện tại của pin, thường biểu diễn bằng capacity tương đối so với ban đầu.'),
('RUL','Số chu kỳ còn lại trước khi pin chạm ngưỡng EOL.'),
('HI','Health indicator – biến đo hoặc biến suy ra có thông tin về degradation.'),
('EOL','End of life – quy tắc xác định pin đã đạt ngưỡng cuối đời.'),
('LOBO','Leave-one-battery-out – bỏ toàn bộ một pin khỏi training rồi kiểm tra trên pin chưa từng thấy.'),
('Censored','Pin chưa quan sát được EOL; không được gán RUL giả.'),
('Zero-shot/adaptation','Zero-shot dùng model nguồn trực tiếp; adaptation cho phép dùng development data để hiệu chỉnh.'),
('Prediction interval','Khoảng dự báo có coverage mục tiêu; phải xem cả độ rộng chứ không chỉ coverage.')])

heading('1. Bối cảnh, xuất phát điểm và câu hỏi nghiên cứu',1)
para('Nghiên cứu không bắt đầu bằng việc chọn LSTM, GRU hay Transformer. Điểm xuất phát là một vấn đề khoa học: một model có thể đạt MAE thấp trong random cycle split nhưng vẫn thất bại khi gặp pin mới hoặc protocol mới. Vì vậy, mục tiêu ban đầu là tìm hiểu dữ liệu trước, chứng minh degradation phụ thuộc state và history, sau đó mới chọn estimator.')
para('Bộ tài liệu PDF được đọc như một không gian phương pháp gồm trajectory/PF/GP, recurrent và convolutional sequence models, feature learning, ANFIS, hybrid digital twin, transfer learning và uncertainty-aware RUL. Điểm chung của các nghiên cứu là model rất đa dạng nhưng protocol chưa đồng nhất: split, horizon, EOL, adaptation và metric khác nhau. Khoảng trống này dẫn tới lựa chọn integrated evaluation framework thay vì tuyên bố một kiến trúc mới.')
table(['Câu hỏi','Kết luận được hỗ trợ'],[
('Cycle count có đủ đại diện tuổi pin không?','Không hoàn toàn; state thường mạnh hơn, nhưng cycle-only không yếu hơn ở mọi checkpoint.'),
('History có luôn cải thiện RUL không?','Không. History có ích có điều kiện và phụ thuộc observation horizon.'),
('Model có generalize không?','RF tốt nhất trong nhóm được đánh giá dưới NASA LOBO; HUST cần phân biệt zero-shot và adaptation.'),
('Hệ thống đã sẵn sàng triển khai chưa?','Chưa. Có replay phần mềm, nhưng interval còn rộng và chưa có electrical HIL/BMS thật.')])

heading('2. Lộ trình nghiên cứu và quyết định phương pháp',1)
for s in [
('Bước 1 – Hiểu và chuẩn hóa dữ liệu.','Tách charge/discharge, cycle index, V/I/T/time/capacity; kiểm tra duplicate, anomaly, incomplete cycle và censoring.'),
('Bước 2 – Tìm insight degradation.','Kiểm tra voltage sag, duration, temperature, energy throughput, capacity trajectory và history.'),
('Bước 3 – Chọn health indicator.','Dùng correlation, ablation và importance để phân biệt cycle-only, state-only, history-only và state+history.'),
('Bước 4 – Khóa ground truth.','EOL là hai chu kỳ liên tiếp dưới 75% median của năm chu kỳ đầu; RUL(k)=N_EOL−k; B0007 không tạo EOL giả.'),
('Bước 5 – Xây model ladder.','So sánh baseline tuyến tính, Huber, trajectory, GP, monotone, RF, XGBoost và ensemble trước khi xem deep model.'),
('Bước 6 – Kiểm chứng generalization.','Dùng LOBO, checkpoint 20/40/60/80%, bootstrap và HUST final untouched.'),
('Bước 7 – Online adaptive replay.','Cycle mới được thêm tuần tự; model cập nhật SOH/RUL và interval mà không dùng future cycle.'),
('Bước 8 – Prototype.','Đóng gói pipeline, figures, manifests, replay và giới hạn rõ phần chưa có BMS/HIL.')]: para(s[0]+' '+s[1])

heading('3. Dữ liệu và định nghĩa bài toán',1)
para('NASA PCoE được dùng làm development benchmark. HUST gồm 77 cell LFP/graphite với protocol discharge nhiều giai đoạn. HUST được khóa thành 46 development, 15 calibration và 16 final untouched cells. Final set không được dùng để chọn feature, hyperparameter hoặc sửa phương pháp.')
para('EOL chính là chu kỳ đầu tiên trong hai chu kỳ liên tiếp có capacity dưới 75% median capacity của năm chu kỳ đầu. Các cell không quan sát EOL được giữ trong audit nhưng loại khỏi point-RUL metric. Sensitivity 70/75/80% được báo cáo; 75% là threshold chính đã đăng ký.')

heading('4. Khung phương pháp',1)
para('Khung gồm data contract, health-indicator extraction, censoring-aware labels, battery-level split, LOBO model ladder, development-only adaptation, calibration-only uncertainty, final untouched evaluation và chronological replay. State features gồm capacity/SOH, duration và V/I/T summaries. History features gồm lagged capacity, rolling slope và cumulative throughput.')

heading('5. Kết quả state/history ablation',1)
para('Cycle-only nhìn chung yếu hơn state-only, nhưng không phải tại mọi checkpoint: ở 60%, cycle-only MAE là 14.47 còn state-only là 15.19. History-only có thông tin nhưng không ổn định. State+history kém hơn ở 20–40% và tốt hơn ở 60–80%; vì vậy kết luận an toàn là history có giá trị checkpoint-dependent, không phải history luôn cần thiết.')

heading('6. Model selection và LOBO',1)
para('LOBO là protocol chính vì mỗi test fold đại diện cho một battery chưa từng xuất hiện. RF đạt LOBO MAE 63.1 cycles và là model tốt nhất trong nhóm được đánh giá dưới protocol này. Kết luận phải đọc là “best among evaluated models under the locked protocol”, không phải RF luôn thắng mọi deep model.')

heading('7. So sánh literature và external HUST',1)
para('Không xếp hạng raw MAE giữa các bài báo khi split, horizon, EOL và adaptation khác nhau. Thay vào đó, luận văn dùng protocol-comparison matrix. Trên HUST final untouched sau development-only adaptation, RF có MAE 116.5, 116.1, 85.2 và 20.3 cycles tại 20%, 40%, 60% và 80% đời pin. Zero-shot NASA→HUST có MAE 1618.4, 1213.9, 809.4 và 404.9 cycles; chênh lệch này cho thấy domain shift lớn và adaptation gần như cần thiết trong setup hiện tại.')

heading('8. Uncertainty và online replay',1)
para('Uncertainty được báo cáo ở coverage mục tiêu 80%, 90% và 95%, cùng actual coverage, interval width và normalized width. Coverage cao nhưng interval còn rộng, nhất là early life; vì vậy không gọi uncertainty là operationally sharp. RF sequential replay dùng dữ liệu đến cycle k để xuất SOH, RUL, lower interval, upper interval và observation fraction. Electrical HIL, partial-cycle API hoàn chỉnh và BMS thật vẫn là future work.')

heading('9. Các audit E1–E11',1)
table(['Audit','Đã làm','Kết luận'],[
('E1 Protocol sensitivity','Random-cycle, battery holdout, LOBO','Split theo battery khó hơn và đáng tin hơn random-cycle.'),
('E2 Ranking stability','Per-battery ranking và bootstrap','RF đứng đầu trong classical ladder dưới protocol khóa.'),
('E3 Fair family','RF/XGBoost/classical; deep artifacts nhiều seed','Deep comparison vẫn conditional vì tuning/convergence chưa đồng nhất hoàn toàn.'),
('E4 History ablation','NASA và HUST-development','History có ích theo checkpoint, chưa chứng minh phổ quát.'),
('E5 Statistical uncertainty','Bootstrap CI và per-cell distributions','Có độ bất định thống kê; NASA có n nhỏ.'),
('E6 EOL sensitivity','70/75/80%','75% giữ làm threshold chính.'),
('E7 External HUST','46/15/16 split và final untouched','Sai số cải thiện khi quan sát dài hơn.'),
('E8 Uncertainty usefulness','Coverage-width 80/90/95%','Coverage hợp lệ nhưng interval rộng.'),
('E9 Leakage audit','Manifest, freeze, future-data checks','Split và final freeze có thể audit.'),
('E10 Sequential replay','RF replay tuần tự','Có bằng chứng phần mềm; chưa có HIL/BMS.'),
('E11 Benchmark matrix','So sánh protocol literature','Không tuyên bố numerical SOTA khi protocol khác.')])

heading('10. Đóng góp và giới hạn',1)
para('Đóng góp của luận văn là một integrated, leakage-controlled evaluation-and-estimation framework: fixed state/history schema, LOBO selection, tách development/calibration/final, checkpoint-aware uncertainty và sequential replay. Đây là một đóng góp phương pháp luận và phân tích, không phải thuật toán học mới.')
para('Các giới hạn chính gồm: NASA chỉ có ba cell observed-EOL cho RUL point metric; history chưa được chứng minh tổng quát trên mọi chemistry/protocol; deep-family comparison cuối cùng chưa đủ để tuyên bố RF vượt deep learning; interval còn rộng; CALCE chưa có RUL/EOL harmonization hoàn chỉnh; chưa có electrical HIL và BMS thật.')

heading('11. Kết luận',1)
para('Nghiên cứu chứng minh rằng đánh giá RUL đáng tin cậy cần kiểm soát leakage, giữ battery-level split, phân biệt current state với history, báo cáo external-domain behavior và xem uncertainty cùng sharpness. RF là lựa chọn thực dụng tốt nhất trong nhóm đã đánh giá dưới protocol khóa. Tuy nhiên, kết luận đúng mức là một research prototype được audit tốt, chưa phải production BMS và chưa phải numerical SOTA.')

heading('Phụ lục: tái lập và tài liệu tham khảo',1)
para('Bản tiếng Việt này dùng cùng bộ artifact, SHA-256 manifest, figures, tables và references đã xác minh trong package V28. Các file raw HUST không được đóng gói; người dùng tái lập cần tải theo DOI và kiểm tra hash manifest. Các kết quả V8 freeze không bị thay đổi.')
para('Tài liệu tham khảo chính: Ma et al. (2022), You et al. (2026), Njathi et al. (2026) và HUST Mendeley Data DOI 10.17632/nsc7hnsg4s.2. Bibliography đầy đủ và metadata publisher record nằm trong bản tiếng Anh/package.')

doc.save(out)
print(out)
