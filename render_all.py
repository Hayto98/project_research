import subprocess
import os

JAR = "plantuml-1.2026.6.jar"
ROOT = "puml_output"
CHUNK_SIZE = 100  # render 100 file mỗi lần gọi, tránh quá tải

labels = sorted(os.listdir(ROOT))

for label in labels:
    label_dir = os.path.join(ROOT, label)
    files = [os.path.join(label_dir, f) for f in os.listdir(label_dir) if f.endswith(".puml")]
    files.sort()

    n_chunks = (len(files) + CHUNK_SIZE - 1) // CHUNK_SIZE
    for c in range(n_chunks):
        chunk = files[c*CHUNK_SIZE : (c+1)*CHUNK_SIZE]
        cmd = ["java", "-jar", JAR, "-tpng"] + chunk
        print(f"{label}: rendering chunk {c+1}/{n_chunks} ({len(chunk)} files)...")
        subprocess.run(cmd)

print("Done rendering all diagrams.")