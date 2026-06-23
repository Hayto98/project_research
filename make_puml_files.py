"""
Sinh 3000 file .puml KHÔNG TRÙNG LẶP cho MỖI loại trong 6 loại UML diagram
(tổng 18,000 file).

Cơ chế chống trùng: với mỗi loại, lưu lại hash (MD5) của code đã sinh ra.
Nếu sinh trùng (hash đã tồn tại), tự động thử lại với seed khác cho đến khi
ra được 1 bản không trùng, hoặc bỏ cuộc sau N lần thử (an toàn, tránh treo
vô hạn nếu generator hết "không gian" để sinh thêm bản mới).

Cách dùng:
    python3 make_puml_files.py
"""
import os
import random
import hashlib
from generate_puml import GENERATORS

OUTPUT_DIR = "puml_output"
IMAGES_PER_CLASS = 3000      # 6 loại x 3000 = 18,000 ảnh
MAX_RETRY_PER_ITEM = 50      # số lần thử lại tối đa nếu bị trùng


def content_hash(code: str) -> str:
    return hashlib.md5(code.encode("utf-8")).hexdigest()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    grand_total = 0
    seed_counter = 1_000_000  # seed lớn, mỗi label/lần thử đều có seed riêng biệt

    for label, fn in GENERATORS.items():
        label_dir = os.path.join(OUTPUT_DIR, label)
        os.makedirs(label_dir, exist_ok=True)

        seen_hashes = set()
        saved = 0
        attempts = 0
        max_total_attempts = IMAGES_PER_CLASS * MAX_RETRY_PER_ITEM

        while saved < IMAGES_PER_CLASS and attempts < max_total_attempts:
            seed_counter += 1
            attempts += 1
            random.seed(seed_counter)
            code, domain = fn()
            h = content_hash(code)

            if h in seen_hashes:
                continue  # trùng -> bỏ qua, thử seed khác ở vòng lặp tiếp theo

            seen_hashes.add(h)
            fname = f"{label}_{saved:05d}_{domain}.puml"
            fpath = os.path.join(label_dir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(code)
            saved += 1

        grand_total += saved
        status = "OK" if saved == IMAGES_PER_CLASS else "THIẾU (generator hết biến thể)"
        print(f"{label}: {saved}/{IMAGES_PER_CLASS} file (đã thử {attempts} lần) -> {status}")

    print(f"\nTổng cộng: {grand_total} file .puml trong '{OUTPUT_DIR}/'")
    print("Mỗi file đảm bảo nội dung KHÔNG trùng lặp với các file khác cùng loại.")


if __name__ == "__main__":
    main()