import customtkinter as ctk
from PIL import Image, ImageTk
import rembg
import threading
from tkinter import filedialog, messagebox
import os

# Cấu hình theme cho customtkinter
ctk.set_appearance_mode("System")  # Chế độ sáng/tối theo hệ thống
ctk.set_default_color_theme("blue")

class BackgroundRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ứng dụng xóa nền ảnh")
        self.geometry("1000x600")
        self.resizable(True, True)

        # Biến lưu ảnh
        self.original_image = None       # PIL Image gốc
        self.result_image = None         # PIL Image kết quả (có alpha)
        self.original_ctk = None         # CTkImage hiển thị
        self.result_ctk = None

        # Khởi tạo giao diện
        self.setup_ui()

    def setup_ui(self):
        # Frame chính chứa hai cột
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Cột trái: ảnh gốc
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(left_frame, text="Ảnh gốc", font=("Arial", 16)).pack(pady=5)
        self.original_label = ctk.CTkLabel(left_frame, text="Chưa có ảnh", width=400, height=400)
        self.original_label.pack(pady=5, fill="both", expand=True)

        # Cột phải: ảnh kết quả
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(right_frame, text="Ảnh sau khi xóa nền", font=("Arial", 16)).pack(pady=5)
        self.result_label = ctk.CTkLabel(right_frame, text="Chưa xử lý", width=400, height=400)
        self.result_label.pack(pady=5, fill="both", expand=True)

        # Frame chứa các nút bấm
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.btn_select = ctk.CTkButton(button_frame, text="Chọn ảnh", command=self.select_image, width=120)
        self.btn_select.pack(side="left", padx=5)

        self.btn_remove = ctk.CTkButton(button_frame, text="Xóa nền", command=self.remove_background, width=120, state="disabled")
        self.btn_remove.pack(side="left", padx=5)

        self.btn_save = ctk.CTkButton(button_frame, text="Lưu ảnh", command=self.save_result, width=120, state="disabled")
        self.btn_save.pack(side="left", padx=5)

        # Thanh trạng thái
        self.status_var = ctk.StringVar(value="Sẵn sàng")
        self.status_bar = ctk.CTkLabel(self, textvariable=self.status_var, anchor="w", height=20)
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=5)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            try:
                # Mở ảnh bằng PIL
                self.original_image = Image.open(file_path).convert("RGB")
                self.display_original()
                self.status_var.set(f"Đã tải ảnh: {os.path.basename(file_path)}")
                self.btn_remove.configure(state="normal")
                self.btn_save.configure(state="disabled")  # Chưa có kết quả
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở ảnh:\n{e}")
                self.status_var.set("Lỗi khi tải ảnh")

    def display_original(self):
        if self.original_image:
            # Resize ảnh để vừa khung hiển thị (giữ tỉ lệ)
            display_size = (400, 400)
            img_copy = self.original_image.copy()
            img_copy.thumbnail(display_size, Image.Resampling.LANCZOS)
            self.original_ctk = ctk.CTkImage(light_image=img_copy, dark_image=img_copy, size=img_copy.size)
            self.original_label.configure(image=self.original_ctk, text="")

    def remove_background(self):
        if self.original_image is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước.")
            return

        # Vô hiệu hóa nút để tránh nhấn nhiều lần
        self.btn_remove.configure(state="disabled")
        self.status_var.set("Đang xóa nền... Vui lòng chờ.")
        self.update_idletasks()

        # Chạy xử lý trong thread riêng để không treo giao diện
        threading.Thread(target=self.process_remove_background, daemon=True).start()

    def process_remove_background(self):
        try:
            # Xóa nền bằng rembg
            # rembg.remove trả về ảnh RGBA (có kênh alpha)
            output_image = rembg.remove(self.original_image)
            self.result_image = output_image

            # Cập nhật giao diện (phải gọi trên main thread)
            self.after(0, self.display_result)
            self.after(0, lambda: self.btn_save.configure(state="normal"))
            self.after(0, lambda: self.status_var.set("Xóa nền thành công!"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi xóa nền", f"Đã xảy ra lỗi:\n{e}"))
            self.after(0, lambda: self.status_var.set("Lỗi xóa nền"))
        finally:
            self.after(0, lambda: self.btn_remove.configure(state="normal"))

    def display_result(self):
        if self.result_image:
            display_size = (400, 400)
            img_copy = self.result_image.copy()
            img_copy.thumbnail(display_size, Image.Resampling.LANCZOS)
            self.result_ctk = ctk.CTkImage(light_image=img_copy, dark_image=img_copy, size=img_copy.size)
            self.result_label.configure(image=self.result_ctk, text="")

    def save_result(self):
        if self.result_image is None:
            messagebox.showwarning("Cảnh báo", "Chưa có ảnh kết quả để lưu.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.result_image.save(file_path, format="PNG")
                messagebox.showinfo("Thành công", f"Đã lưu ảnh tại:\n{file_path}")
                self.status_var.set(f"Đã lưu: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Lỗi lưu", f"Không thể lưu ảnh:\n{e}")
                self.status_var.set("Lỗi khi lưu")

if __name__ == "__main__":
    app = BackgroundRemoverApp()
    app.mainloop()