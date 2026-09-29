from pathlib import Path
from docx import Document

ROOT=Path(__file__).resolve().parent; pkg=ROOT/'SUBMISSION_PACKAGE_V10'
en_src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V28_READER_GUIDE_FINAL.docx'
en_dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V29_12_STEP_FINAL.docx'
vi_src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V28_VIETNAMESE_FINAL.docx'
vi_dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V29_VIETNAMESE_12_STEP_FINAL.docx'

en_steps=('The complete research route is: (0) literature review and research-gap mapping; (1) data understanding and normalization; '
          '(2) data-quality and censoring audit; (3) degradation insight discovery; (4) health-indicator selection and ablation; '
          '(5) ground-truth, EOL and RUL definition; (6) protocol registration and leakage audit; (7) model ladder and fair model-family comparison; '
          '(8) LOBO, statistical uncertainty and checkpoint evaluation; (9) external HUST validation and domain-shift analysis; '
          '(10) online sequential replay; and (11) prototype, reproducibility and claim control. Each arrow is a decision gate: later results are not allowed to revise an earlier locked definition.')
en=Document(en_src)
for p in en.paragraphs:
    if p.text.startswith('The complete workflow is:'):
        p.text=en_steps
        break
en.save(en_dst)

vi_steps=('Lộ trình đầy đủ là: (0) đọc literature và lập bản đồ research gap; (1) hiểu và chuẩn hóa dữ liệu; '
          '(2) audit chất lượng dữ liệu và censoring; (3) tìm insight degradation; (4) chọn và ablation health indicator; '
          '(5) định nghĩa ground truth, EOL và RUL; (6) đăng ký protocol và audit leakage; (7) model ladder và fair comparison giữa các model family; '
          '(8) LOBO, uncertainty thống kê và đánh giá theo checkpoint; (9) external validation HUST và phân tích domain shift; '
          '(10) online sequential replay; và (11) prototype, reproducibility và claim control. Mỗi mũi tên là một cổng quyết định: kết quả về sau không được sửa lại định nghĩa đã khóa trước đó.')
vi=Document(vi_src)
for p in vi.paragraphs:
    if p.text.startswith('Câu trả lời được kiểm chứng theo chuỗi:'):
        p.text=vi_steps
        break
vi.save(vi_dst)
print(en_dst); print(vi_dst)
