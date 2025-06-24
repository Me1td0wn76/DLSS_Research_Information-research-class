import cv2
import os
from tkinter import Tk, filedialog

def upscale_image_opencv(input_image_path, output_image_path, scale_factor=2):
    # 画像を読み込む
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("入力画像が見つかりません。パスを確認してください。")
    # 新しいサイズを計算
    height, width = image.shape[:2]
    new_size = (int(width * scale_factor), int(height * scale_factor))
    # 画像をアップスケール
    upscaled_image = cv2.resize(image, new_size, interpolation=cv2.INTER_CUBIC)
    # 保存先ディレクトリを作成
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    # 保存
    cv2.imwrite(output_image_path, upscaled_image)
    print(f"アップスケールされた画像が {output_image_path} に保存されました。")

if __name__ == "__main__":
    # ファイル選択ダイアログを表示
    Tk().withdraw()  # Tkinterのメインウィンドウを表示しない
    input_path = filedialog.askopenfilename(title="アップスケールする画像を選択", filetypes=[("画像ファイル", "*.jpg;*.jpeg;*.png;*.bmp")])
    print(f"選択されたファイル: {input_path}")  # 追加
    if input_path:
        output_path = filedialog.asksaveasfilename(title="保存先を選択", defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")])
        if output_path:
            upscale_image_opencv(input_path, output_path, scale_factor=2)
        else:
            print("保存先が選択されませんでした。")
    else:
        print("画像が選択されませんでした。")
