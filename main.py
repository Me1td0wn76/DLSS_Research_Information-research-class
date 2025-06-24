import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

# 既存のモデルファイルとモデル名、倍率を指定
MODEL_PATH = "ESPCN_x2.pb"  # 例: 正しいモデルファイル名に修正
MODEL_NAME = "espcn"
SCALE = 2                   # 例: 倍率

root = tk.Tk()
root.withdraw()  # メインウィンドウを表示しない

# 入力画像ファイル選択
image_path = filedialog.askopenfilename(
    title="入力画像ファイルを選択",
    filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg;*.bmp"), ("すべてのファイル", "*.*")]
)
if not image_path:
    messagebox.showerror("エラー", "入力画像ファイルが選択されていません。")
    exit()

messagebox.showinfo("選択完了", f"選択された画像ファイル:\n{image_path}")

# 保存ファイル名選択
output_path = filedialog.asksaveasfilename(
    title="保存するファイル名を選択",
    defaultextension=".jpg",
    filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("すべてのファイル", "*.*")]
)
if not output_path:
    messagebox.showerror("エラー", "保存ファイル名が選択されていません。")
    exit()

def print_progress(percent, message=""):
    bar_length = 30
    filled_length = int(bar_length * percent // 100)
    bar = "█" * filled_length + '-' * (bar_length - filled_length)
    print(f"\r[{bar}] {percent:3d}% {message}", end='', flush=True)
    if percent == 100:
        print()  # 改行

# モデル読み込み
print_progress(10, "モデルを読み込んでいます...")
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(MODEL_PATH)

# GPU(CUDA)を使用する設定を追加
# sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

sr.setModel(MODEL_NAME, SCALE)
print_progress(30, "モデルの読み込みが完了しました。")

# 入力画像
print_progress(40, "画像を読み込んでいます...")
img = cv2.imread(image_path)
if img is None:
    print_progress(100, "画像の読み込みに失敗しました。")
    messagebox.showerror("エラー", "画像の読み込みに失敗しました。")
    exit()
print_progress(50, "画像の読み込みが完了しました。")

# 超解像処理（拡大される）
print_progress(60, "超解像処理を実行中...")
result = sr.upsample(img)
print_progress(80, "超解像処理が完了しました。")

# 元のサイズにリサイズして大きさを維持
print_progress(85, "リサイズ処理を実行中...")
result_resized = cv2.resize(result, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
print_progress(90, "リサイズ処理が完了しました。")

# 保存
print_progress(95, "画像を保存しています...")
cv2.imwrite(output_path, result_resized)
print_progress(100, "画像の保存が完了しました。")
messagebox.showinfo("完了", "画像の保存が完了しました。")

# CPU 30minutes
# GPU