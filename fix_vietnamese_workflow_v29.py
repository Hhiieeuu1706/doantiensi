from pathlib import Path
from docx import Document
ROOT=Path(__file__).resolve().parent
pkg=ROOT/'SUBMISSION_PACKAGE_V10'
f=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V29_VIETNAMESE_12_STEP_FINAL.docx'
d=Document(f)
steps=('Câu hỏi trung tâm của luận văn là: một hệ thống RUL có còn đáng tin khi pin kiểm tra chưa từng thấy, protocol thay đổi, không được dùng dữ liệu tương lai và phải báo cáo uncertainty trung thực hay không? Lộ trình đầy đủ là: (0) đọc literature và lập bản đồ research gap; (1) hiểu và chuẩn hóa dữ liệu; (2) audit chất lượng dữ liệu và censoring; (3) tìm insight degradation; (4) chọn và ablation health indicator; (5) định nghĩa ground truth, EOL và RUL; (6) đăng ký protocol và audit leakage; (7) model ladder và fair comparison giữa các model family; (8) LOBO, uncertainty thống kê và đánh giá theo checkpoint; (9) external validation HUST và phân tích domain shift; (10) online sequential replay; và (11) prototype, reproducibility và claim control. Mỗi mũi tên là một cổng quyết định: kết quả về sau không được sửa lại định nghĩa đã khóa trước đó.')
for p in d.paragraphs:
    if p.text.startswith('Câu hỏi trung tâm của luận văn là:'):
        p.text=steps
        break
d.save(f)
print(f)
