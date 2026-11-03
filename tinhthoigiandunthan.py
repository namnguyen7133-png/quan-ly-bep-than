import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
import pystray
from PIL import Image, ImageDraw
import time
import threading

# ========== CỐ ĐỊNH DUY NHẤT 1 TỆP DỮ LIỆU CHUẨN ==========
FILE_MAC_DINH = r"D:\QUAN_LY_BEP_THAN\backup_bep_20261013_1613.json"
FILE_LUU_DUONG_DAN = "cauhinh_duong_dan.json"

os.makedirs(os.path.dirname(FILE_MAC_DINH), exist_ok=True)

def cau_truc_du_lieu_mac_dinh():
    return {
        "than": [],
        "viec": [],
        "nut_0_ten": "Nước chín sôi",
        "nut_0_tep_txt": "",
        "nut_0_dang_phat": 0,
        "nut_0_link_danh_sach": [],
        "nut_1_ten": "Báo hết than",
        "nut_1_tep_txt": "",
        "nut_1_dang_phat": 0,
        "nut_1_link_danh_sach": [],
        "nut_2_ten": "Cần nhóm than mới",
        "nut_2_tep_txt": "",
        "nut_2_dang_phat": 0,
        "nut_2_link_danh_sach": [],
        "nut_3_ten": "Than bén lửa",
        "nut_3_tep_txt": "",
        "nut_3_dang_phat": 0,
        "nut_3_link_danh_sach": [],
        "nut_4_ten": "Thông báo khác",
        "nut_4_tep_txt": "",
        "nut_4_dang_phat": 0,
        "nut_4_link_danh_sach": [],
        "nut_5_ten": "Ấm 5L (1) sôi",
        "nut_5_tep_txt": "",
        "nut_5_dang_phat": 0,
        "nut_5_link_danh_sach": [],
        "nut_6_ten": "Ấm 5L (2) sôi",
        "nut_6_tep_txt": "",
        "nut_6_dang_phat": 0,
        "nut_6_link_danh_sach": [],
        "nut_7_ten": "Ấm 3 (5L) sôi",
        "nut_7_tep_txt": "",
        "nut_7_dang_phat": 0,
        "nut_7_link_danh_sach": [],
        "nut_8_ten": "Nồi 7L xong",
        "nut_8_tep_txt": "",
        "nut_8_dang_phat": 0,
        "nut_8_link_danh_sach": [],
        "lap_lai_video": True,
        
        # --- CẤU HÌNH THỜI GIAN NHÓM & VÒNG ĐỜI THAN MAC DINH ---
        "thoi_gian_nhom_bén": 22.0,         
        "vong_doi_to_phut": 96.0,            
        "vong_doi_nho_phut": 780.0,          
        "vong_doi_ket_hop_phut": 480.0,      
        
        # --- 5 Ô NHẬP ĐUN NƯỚC SÔI TO ---
        "phut_to_1": 30.0,
        "phut_to_2": 26.0,
        "phut_to_3": 22.0,
        "phut_to_4": 40.0,
        "phut_to_5": 35.0,

        # --- 5 Ô NHẬP ĐUN NƯỚC SÔI NHỎ ---
        "phut_nho_1": 127.0,
        "phut_nho_2": 150.0,
        "phut_nho_3": 180.0,
        "phut_nho_4": 200.0,
        "phut_nho_5": 220.0,

        # --- 5 Ô NHẬP ĐUN KẾT HỢP & CHẾ ĐỘ ---
        "phut_kethop_1": 33.0,  "che_do_kethop_1": "dun_to",
        "phut_kethop_2": 90.0,  "che_do_kethop_2": "dun_nho",
        "phut_kethop_3": 120.0, "che_do_kethop_3": "dun_nho",
        "phut_kethop_4": 150.0, "che_do_kethop_4": "dun_nho",
        "phut_kethop_5": 180.0, "che_do_kethop_5": "dun_nho",

        "dung_tich_am_l": 5.0
    }

def doc_json():
    if os.path.exists(FILE_MAC_DINH):
        try:
            with open(FILE_MAC_DINH, "r", encoding="utf-8") as f:
                data = json.load(f)
                base = cau_truc_du_lieu_mac_dinh()
                if isinstance(data, dict):
                    for k in base:
                        if k not in data:
                            data[k] = base[k]
                    return data
        except Exception as e:
            messagebox.showwarning("⚠️ Lỗi đọc tệp", f"Không đọc được:\n{FILE_MAC_DINH}\nLỗi: {e}")
    dl_moi = cau_truc_du_lieu_mac_dinh()
    luu_json(dl_moi)
    return dl_moi

def luu_json(du_lieu):
    try:
        with open(FILE_MAC_DINH, "w", encoding="utf-8") as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        messagebox.showerror("❌ Lỗi lưu tệp", f"Không lưu được:\n{FILE_MAC_DINH}\nLỗi: {e}")
        return False

def phut_sang_gio(p):
    if p <= 0: return "0 phút"
    g = int(p // 60)
    ph = round(p % 60)
    return f"{g} giờ {ph} phút" if g > 0 else f"{ph} phút"

def lay_gio_hien_tai():
    return datetime.now().strftime("%H:%M")

def lay_ngay_gio():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def phan_tich_gio(gio_str, mac_dinh_gio=None):
    if not gio_str or not gio_str.strip():
        return mac_dinh_gio
    try:
        h, m = map(int, gio_str.strip().split(":"))
        now = datetime.now()
        return datetime(now.year, now.month, now.day, h, m, 0)
    except ValueError:
        return mac_dinh_gio

def doc_tep_txt_link(duong_dan_tep):
    if not duong_dan_tep or not duong_dan_tep.strip():
        return []
    if not os.path.exists(duong_dan_tep):
        return []
    try:
        ds_link = []
        with open(duong_dan_tep, "r", encoding="utf-8") as f:
            for dong in f:
                dong = dong.strip()
                if dong and not dong.startswith("#"):
                    ds_link.append(dong)
        return ds_link
    except Exception as e:
        messagebox.showerror("❌ Lỗi đọc tệp TXT", f"Không đọc được:\n{duong_dan_tep}\nLỗi: {e}")
        return []

def tao_bieu_tuong():
    kich_thuoc = (64, 64)
    anh = Image.new('RGB', kich_thuoc, '#2c3e50')
    ve = ImageDraw.Draw(anh)
    ve.ellipse([8, 8, 56, 56], fill='#e74c3c')
    ve.text((22, 18), "🔥", fill='white')
    return anh

def hoi_gio_nhom_than(so_thu_tu, gio_mac_dinh):
    win = tk.Toplevel()
    win.title(f"🔥 Nhóm than — Viên số {so_thu_tu}")
    win.geometry("450x240")
    win.transient()
    win.grab_set()
    
    kq = {"gio_nhom": None, "huy": True}
    
    ttk.Label(win, text=f"Viên thứ {so_thu_tu}", font=("Arial", 16, "bold")).pack(pady=10)
    ttk.Label(win, text="Giờ nhóm (để trống = lấy giờ hiện tại):", font=("Arial", 13)).pack(pady=(10, 5))
    
    o_gio = ttk.Entry(win, width=21, font=("Arial", 14))
    o_gio.insert(0, gio_mac_dinh)
    o_gio.pack(pady=5)
    o_gio.select_range(0, tk.END)
    o_gio.focus()
    
    def xac_nhan():
        kq["gio_nhom"] = o_gio.get().strip()
        kq["huy"] = False
        win.destroy()
    
    def huy():
        win.destroy()
    
    khung_nut = ttk.Frame(win)
    khung_nut.pack(pady=15)
    ttk.Button(khung_nut, text="✅ Xác nhận", command=xac_nhan).pack(side="left", padx=13)
    ttk.Button(khung_nut, text="❌ Hủy", command=huy).pack(side="left", padx=13)
    
    win.wait_window()
    return None if kq["huy"] else kq["gio_nhom"]


class QuanLyBepThan:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Bếp Than Tổ Ong — Tối Ưu Vận Hành")
        
        try:
            self.root.state('zoomed')
        except:
            self.root.geometry("1366x768")
        
        self.root.withdraw()
        self.giao_dien_dang_mo = False
        
        self.du_lieu = doc_json()
        self.cauhinh = self.du_lieu
        
        self.dang_dung = "dun_to"
        self.dang_dem_nguoc_nhom = False
        self.bat_dau_nhom = None
        self.vien_dang_su_dung = None
        
        self.duoc_chon_than = None
        self.duoc_chon_viec = None
        self._da_phat_canh_bao_het_than = False
        
        self.var_che_do_kethop = {}

        self.bieu_tuong = pystray.Icon(
            "bep_than",
            tao_bieu_tuong(),
            "Bếp Than Tổ Ong",
            menu=pystray.Menu(
                pystray.MenuItem("📋 Mở giao diện", self.mo_giao_dien),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("❌ Thoát hoàn toàn", self.thoat_phan_mem)
            )
        )
        
        self.root.protocol("WM_DELETE_WINDOW", self.anh_ve_khay)
        
        self.xay_dung_giao_dien()
        self.khoi_phuc_tu_du_lieu()
        self.cap_nhat_lich_su()
        self.cap_nhat_tu_dong()

    def xay_dung_giao_dien(self):
        khung_tep = ttk.LabelFrame(self.root, text="📄 TỆP DỮ LIỆU CỐ ĐỊNH")
        khung_tep.pack(fill="x", padx=10, pady=5)
        
        f_t = ttk.Frame(khung_tep)
        f_t.pack(fill="x", padx=8, pady=5)
        
        self.lbl_tep_dl = ttk.Label(f_t, text=f"Đường dẫn: {FILE_MAC_DINH}", font=("Arial", 10, "bold"), foreground="blue")
        self.lbl_tep_dl.pack(side="left", padx=5)
        
        ttk.Button(f_t, text="💾 LƯU TẤT CẢ THÔNG SỐ", command=self.luu_tat_ca_thong_so).pack(side="right", padx=5)
        ttk.Button(f_t, text="🗑️ XÓA HẾT DỮ LIỆU", command=self.xoa_het_du_lieu).pack(side="right", padx=5)
        
        khung_tong = ttk.Frame(self.root)
        khung_tong.pack(fill="both", expand=True, padx=10, pady=5)
        khung_tong.columnconfigure(0, weight=60)
        khung_tong.columnconfigure(1, weight=40)
        khung_tong.rowconfigure(0, weight=1)

        cot_trai = ttk.Frame(khung_tong)
        cot_trai.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.notebook = ttk.Notebook(cot_trai)
        self.notebook.pack(fill="both", expand=True)

        tab1 = ttk.Frame(self.notebook)
        tab2 = ttk.Frame(self.notebook)
        tab3 = ttk.Frame(self.notebook)

        self.notebook.add(tab1, text="⚙️ Tab 1: Cấu hình Đun & Tàn than")
        self.notebook.add(tab2, text="🔥 Tab 2: Vận hành & Hẹn giờ")
        self.notebook.add(tab3, text="📊 Tab 3: Trạng thái & Lịch sử")

        # TAB 1: CẤU HÌNH THỜI GIAN ĐUN TO, ĐUN NHỎ, DỰ TÍNH CỘNG DỒN
        khung_cf_tong = ttk.LabelFrame(tab1, text="⏱️ CẤU HÌNH THỜI GIAN & TÍNH TOÁN LỊCH SỬ TRUNG BÌNH HẾT THAN")
        khung_cf_tong.pack(fill="x", padx=5, pady=5)
        
        khung_cf_chitiet = ttk.LabelFrame(tab1, text="☕ CẤU HÌNH PHÚT ĐUN SÔI (ĐUN TO - ĐUN NHỎ - ĐUN TO NHỎ KẾT HỢP)")
        khung_cf_chitiet.pack(fill="both", expand=True, padx=5, pady=5)

        self.ent_cf = {}

        # Dòng 0: Phút nhóm
        ttk.Label(khung_cf_tong, text="🔥 Phút nhóm bén lửa:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=3, pady=3)
        o_nhom = ttk.Entry(khung_cf_tong, width=10, font=("Arial", 10, "bold"))
        o_nhom.insert(0, str(self.cauhinh.get("thoi_gian_nhom_bén", 22)))
        o_nhom.grid(row=0, column=1, padx=3, pady=3)
        self.ent_cf["thoi_gian_nhom_bén"] = o_nhom
        ttk.Button(khung_cf_tong, text="✏️", width=3, command=lambda: self.sua_o_cauhinh("thoi_gian_nhom_bén")).grid(row=0, column=2, padx=1)
        ttk.Button(khung_cf_tong, text="❌", width=3, command=lambda: self.xoa_o_cauhinh("thoi_gian_nhom_bén")).grid(row=0, column=3, padx=1)

        # Dòng 1: Đun to
        ttk.Label(khung_cf_tong, text="🔴 Tổng phút ĐUN TO:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=3, pady=3)
        o_to = ttk.Entry(khung_cf_tong, width=10, font=("Arial", 10, "bold"))
        o_to.insert(0, str(self.cauhinh.get("vong_doi_to_phut", 96)))
        o_to.grid(row=1, column=1, padx=3, pady=3)
        self.ent_cf["vong_doi_to_phut"] = o_to
        ttk.Button(khung_cf_tong, text="✏️", width=3, command=lambda: self.sua_o_cauhinh("vong_doi_to_phut")).grid(row=1, column=2, padx=1)
        ttk.Button(khung_cf_tong, text="❌", width=3, command=lambda: self.xoa_o_cauhinh("vong_doi_to_phut")).grid(row=1, column=3, padx=1)
        self.lbl_het_to = ttk.Label(khung_cf_tong, text="⏰ Hết (100% To): --:-- | Nhóm mới (trước 25p): --:--", font=("Arial", 9, "bold"), foreground="red")
        self.lbl_het_to.grid(row=1, column=4, sticky="w", padx=5)

        # Dòng 2: Đun nhỏ
        ttk.Label(khung_cf_tong, text="🔵 Tổng phút ĐUN NHỎ:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=3, pady=3)
        o_nho = ttk.Entry(khung_cf_tong, width=10, font=("Arial", 10, "bold"))
        o_nho.insert(0, str(self.cauhinh.get("vong_doi_nho_phut", 780)))
        o_nho.grid(row=2, column=1, padx=3, pady=3)
        self.ent_cf["vong_doi_nho_phut"] = o_nho
        ttk.Button(khung_cf_tong, text="✏️", width=3, command=lambda: self.sua_o_cauhinh("vong_doi_nho_phut")).grid(row=2, column=2, padx=1)
        ttk.Button(khung_cf_tong, text="❌", width=3, command=lambda: self.xoa_o_cauhinh("vong_doi_nho_phut")).grid(row=2, column=3, padx=1)
        self.lbl_het_nho = ttk.Label(khung_cf_tong, text="⏰ Hết (100% Nhỏ): --:-- | Nhóm mới (trước 25p): --:--", font=("Arial", 9, "bold"), foreground="blue")
        self.lbl_het_nho.grid(row=2, column=4, sticky="w", padx=5)

        # Dòng 3: Đun kết hợp dựa trên lịch sử
        ttk.Label(khung_cf_tong, text="🟣 Dự tính đun kết hợp:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=3, pady=3)
        o_kh = ttk.Entry(khung_cf_tong, width=10, font=("Arial", 10, "bold"))
        o_kh.insert(0, str(self.cauhinh.get("vong_doi_ket_hop_phut", 480)))
        o_kh.grid(row=3, column=1, padx=3, pady=3)
        self.ent_cf["vong_doi_ket_hop_phut"] = o_kh
        ttk.Button(khung_cf_tong, text="✏️", width=3, command=lambda: self.sua_o_cauhinh("vong_doi_ket_hop_phut")).grid(row=3, column=2, padx=1)
        ttk.Button(khung_cf_tong, text="❌", width=3, command=lambda: self.xoa_o_cauhinh("vong_doi_ket_hop_phut")).grid(row=3, column=3, padx=1)
        self.lbl_het_ket_hop = ttk.Label(khung_cf_tong, text="⏰ Tàn than dự kiến: --:-- | Nhóm mới: --:--", font=("Arial", 9, "bold"), foreground="purple")
        self.lbl_het_ket_hop.grid(row=3, column=4, sticky="w", padx=5)

        # 5 ô đun to, 5 ô đun nhỏ & 5 ô đun kết hợp (có chọn chế độ đun to/nhỏ)
        f_to = ttk.Frame(khung_cf_chitiet)
        f_to.pack(side="left", fill="both", expand=True, padx=2, pady=5)
        ttk.Label(f_to, text="--- 🔥 5 Ô ĐUN TO ---", font=("Arial", 9, "bold"), foreground="red").pack(anchor="w", pady=3)

        f_nho = ttk.Frame(khung_cf_chitiet)
        f_nho.pack(side="left", fill="both", expand=True, padx=2, pady=5)
        ttk.Label(f_nho, text="--- 💧 5 Ô ĐUN NHỎ ---", font=("Arial", 9, "bold"), foreground="blue").pack(anchor="w", pady=3)

        f_kethop = ttk.Frame(khung_cf_chitiet)
        f_kethop.pack(side="left", fill="both", expand=True, padx=2, pady=5)
        ttk.Label(f_kethop, text="--- 🟣 ĐUN TO NHỎ KẾT HỢP ---", font=("Arial", 9, "bold"), foreground="purple").pack(anchor="w", pady=3)

        for i in range(1, 6):
            # Ô Đun To
            key_to = f"phut_to_{i}"
            row_to = ttk.Frame(f_to)
            row_to.pack(fill="x", pady=2)
            ttk.Label(row_to, text=f"Ô {i} (p):", font=("Arial", 8), width=7).pack(side="left")
            o_to_i = ttk.Entry(row_to, width=6, font=("Arial", 8, "bold"))
            o_to_i.insert(0, str(self.cauhinh.get(key_to, 0)))
            o_to_i.pack(side="left", padx=1)
            self.ent_cf[key_to] = o_to_i
            ttk.Button(row_to, text="✏️", width=2, command=lambda k=key_to: self.sua_o_cauhinh(k)).pack(side="left", padx=1)
            ttk.Button(row_to, text="❌", width=2, command=lambda k=key_to: self.xoa_o_cauhinh(k)).pack(side="left", padx=1)

            # Ô Đun Nhỏ
            key_nho = f"phut_nho_{i}"
            row_nho = ttk.Frame(f_nho)
            row_nho.pack(fill="x", pady=2)
            ttk.Label(row_nho, text=f"Ô {i} (p):", font=("Arial", 8), width=7).pack(side="left")
            o_nho_i = ttk.Entry(row_nho, width=6, font=("Arial", 8, "bold"))
            o_nho_i.insert(0, str(self.cauhinh.get(key_nho, 0)))
            o_nho_i.pack(side="left", padx=1)
            self.ent_cf[key_nho] = o_nho_i
            ttk.Button(row_nho, text="✏️", width=2, command=lambda k=key_nho: self.sua_o_cauhinh(k)).pack(side="left", padx=1)
            ttk.Button(row_nho, text="❌", width=2, command=lambda k=key_nho: self.xoa_o_cauhinh(k)).pack(side="left", padx=1)

            # Ô Đun Kết Hợp (có thêm 2 nút chọn Radiobutton Đun To / Đun Nhỏ)
            key_kh = f"phut_kethop_{i}"
            key_chedo_kh = f"che_do_kethop_{i}"
            row_kh = ttk.Frame(f_kethop)
            row_kh.pack(fill="x", pady=2)
            ttk.Label(row_kh, text=f"Ô {i} (p):", font=("Arial", 8), width=7).pack(side="left")
            
            o_kh_i = ttk.Entry(row_kh, width=6, font=("Arial", 8, "bold"))
            o_kh_i.insert(0, str(self.cauhinh.get(key_kh, 0)))
            o_kh_i.pack(side="left", padx=1)
            self.ent_cf[key_kh] = o_kh_i

            var_cd = tk.StringVar(value=self.cauhinh.get(key_chedo_kh, "dun_nho" if i > 1 else "dun_to"))
            self.var_che_do_kethop[key_chedo_kh] = var_cd

            def khi_doi_che_do(k_cd=key_chedo_kh, v=var_cd):
                self.cauhinh[k_cd] = v.get()
                self.du_lieu[k_cd] = v.get()
                luu_json(self.du_lieu)

            r_to = ttk.Radiobutton(row_kh, text="To", variable=var_cd, value="dun_to", command=khi_doi_che_do)
            r_to.pack(side="left", padx=1)
            r_nho = ttk.Radiobutton(row_kh, text="Nhỏ", variable=var_cd, value="dun_nho", command=khi_doi_che_do)
            r_nho.pack(side="left", padx=1)

            ttk.Button(row_kh, text="✏️", width=2, command=lambda k=key_kh: self.sua_o_cauhinh(k)).pack(side="left", padx=1)
            ttk.Button(row_kh, text="❌", width=2, command=lambda k=key_kh: self.xoa_o_cauhinh(k)).pack(side="left", padx=1)

        # TAB 2: VẬN HÀNH BẾP
        khung_nhom = ttk.LabelFrame(tab2, text="🔥 QUẢN LÝ NHÓM THAN")
        khung_nhom.pack(fill="x", padx=5, pady=5)
        ttk.Button(khung_nhom, text="🔥 BẮT ĐẦU NHÓM THAN", command=self.bam_nhom_than).pack(side="left", padx=8, pady=5)
        self.nhom_label = ttk.Label(khung_nhom, text="🔥 Chưa nhóm", font=("Arial", 11, "bold"))
        self.nhom_label.pack(side="left", padx=8)

        khung_dk = ttk.LabelFrame(tab2, text="🎛️ ĐIỀU KHIỂN VẬN HÀNH BẾP")
        khung_dk.pack(fill="x", padx=5, pady=5)
        ttk.Button(khung_dk, text="🔥 ĐUN TO", command=self.chuyen_dun_to).pack(side="left", padx=5, pady=5)
        ttk.Button(khung_dk, text="💧 ĐUN NHỎ", command=self.chuyen_dun_nho).pack(side="left", padx=5, pady=5)
        ttk.Button(khung_dk, text="⛽ KẾT THÚC VIÊN THAN", command=self.ket_thuc_than).pack(side="left", padx=5, pady=5)

        khung_dang_ky_chinh = ttk.LabelFrame(tab2, text="📝 NHẬP GIỜ BẮT ĐẦU & HẸN GIỜ ĐUN NƯỚC")
        khung_dang_ky_chinh.pack(fill="x", padx=5, pady=5)

        f_dkc = ttk.Frame(khung_dang_ky_chinh)
        f_dkc.pack(fill="x", padx=5, pady=5)

        ttk.Label(f_dkc, text="Tên việc:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=3)
        self.ent_ten_viec = ttk.Entry(f_dkc, width=18, font=("Arial", 10))
        self.ent_ten_viec.insert(0, "Nước chín sôi 5L")
        self.ent_ten_viec.grid(row=0, column=1, padx=3, pady=3)

        self.bien_che_do_chinh = tk.StringVar(value="dun_to")
        ttk.Radiobutton(f_dkc, text="To", variable=self.bien_che_do_chinh, value="dun_to").grid(row=0, column=2, padx=2)
        ttk.Radiobutton(f_dkc, text="Nhỏ", variable=self.bien_che_do_chinh, value="dun_nho").grid(row=0, column=3, padx=2)

        ttk.Label(f_dkc, text="Giờ BĐ:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=3)
        self.ent_gio_bd = ttk.Entry(f_dkc, width=11, font=("Arial", 10))
        self.ent_gio_bd.insert(0, lay_gio_hien_tai())
        self.ent_gio_bd.grid(row=1, column=1, sticky="w", padx=3, pady=3)

        ttk.Label(f_dkc, text="Phút đun:", font=("Arial", 10)).grid(row=1, column=2, sticky="w")
        self.ent_phut_soi = ttk.Entry(f_dkc, width=8, font=("Arial", 10))
        self.ent_phut_soi.insert(0, "30")
        self.ent_phut_soi.grid(row=1, column=3, padx=3)

        ttk.Label(f_dkc, text="Giờ kết thúc:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=3)
        self.ent_gio_kt = ttk.Entry(f_dkc, width=11, font=("Arial", 10))
        self.ent_gio_kt.grid(row=2, column=1, sticky="w", padx=3, pady=3)

        self._dang_cap_nhat_tg = False

        def cap_nhat_gio_kt_tu_phut(event=None):
            if self._dang_cap_nhat_tg: return
            self._dang_cap_nhat_tg = True
            try:
                bd = self.ent_gio_bd.get().strip()
                ps = float(self.ent_phut_soi.get().strip() or 0)
                dt_bd = phan_tich_gio(bd)
                if dt_bd:
                    dt_kt = dt_bd + timedelta(minutes=ps)
                    self.ent_gio_kt.delete(0, tk.END)
                    self.ent_gio_kt.insert(0, dt_kt.strftime("%H:%M"))
            except:
                pass
            self._dang_cap_nhat_tg = False

        def cap_nhat_phut_tu_gio_kt(event=None):
            if self._dang_cap_nhat_tg: return
            self._dang_cap_nhat_tg = True
            try:
                bd = self.ent_gio_bd.get().strip()
                kt = self.ent_gio_kt.get().strip()
                dt_bd = phan_tich_gio(bd)
                dt_kt = phan_tich_gio(kt)
                if dt_bd and dt_kt:
                    hieu = (dt_kt - dt_bd).total_seconds() / 60
                    if hieu < 0: hieu += 24 * 60
                    self.ent_phut_soi.delete(0, tk.END)
                    self.ent_phut_soi.insert(0, f"{round(hieu, 1):g}")
            except:
                pass
            self._dang_cap_nhat_tg = False

        self.ent_gio_bd.bind("<KeyRelease>", cap_nhat_gio_kt_tu_phut)
        self.ent_phut_soi.bind("<KeyRelease>", cap_nhat_gio_kt_tu_phut)
        self.ent_gio_kt.bind("<KeyRelease>", cap_nhat_phut_tu_gio_kt)
        cap_nhat_gio_kt_tu_phut()

        ttk.Button(f_dkc, text="💾 Lưu việc & Hẹn giờ", command=self.dang_ky_viec_truc_tiep_chinh).grid(row=2, column=2, columnspan=2, padx=5, pady=3)

        khung_nhap_dun_truc_tiep = ttk.LabelFrame(tab2, text="⏱️ SỬA TỔNG THỜI GIAN ĐUN THỦ CÔNG")
        khung_nhap_dun_truc_tiep.pack(fill="x", padx=5, pady=5)

        f_ndt = ttk.Frame(khung_nhap_dun_truc_tiep)
        f_ndt.pack(fill="x", padx=5, pady=5)

        ttk.Label(f_ndt, text="Đun to (phút):", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        self.ent_nhap_dun_to = ttk.Entry(f_ndt, width=8, font=("Arial", 10))
        self.ent_nhap_dun_to.insert(0, "0")
        self.ent_nhap_dun_to.grid(row=0, column=1, padx=3)

        ttk.Label(f_ndt, text="Đun nhỏ (phút):", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=(5, 0))
        self.ent_nhap_dun_nho = ttk.Entry(f_ndt, width=8, font=("Arial", 10))
        self.ent_nhap_dun_nho.insert(0, "0")
        self.ent_nhap_dun_nho.grid(row=0, column=3, padx=3)

        ttk.Button(f_ndt, text="💾 Cập nhật", command=self.cap_nhap_thu_cong_thoi_gian_dun).grid(row=0, column=4, padx=5)

        # TAB 3: TRẠNG THÁI HIỆN TẠI & LỊCH SỬ
        khung_tt_tab3 = ttk.LabelFrame(tab3, text="📊 TRẠNG THÁI VẬN HÀNH BẾP")
        khung_tt_tab3.pack(fill="x", padx=5, pady=5)

        self.tt_label_tab3 = ttk.Label(khung_tt_tab3, text="Đang: —", font=("Arial", 11, "bold"))
        self.tt_label_tab3.pack(anchor="w", padx=10, pady=2)
        self.tg_label_tab3 = ttk.Label(khung_tt_tab3, text="Tổng thời gian: —", font=("Arial", 10))
        self.tg_label_tab3.pack(anchor="w", padx=10, pady=2)
        self.phantram_label_tab3 = ttk.Label(khung_tt_tab3, text="Tuổi thọ than: —", font=("Arial", 10))
        self.phantram_label_tab3.pack(anchor="w", padx=10, pady=2)

        khung_ls = ttk.LabelFrame(tab3, text="📋 QUẢN LÝ LỊCH SỬ VIÊN THAN & CÔNG VIỆC")
        khung_ls.pack(fill="both", expand=True, padx=5, pady=5)

        khung_danh_sach = ttk.Frame(khung_ls)
        khung_danh_sach.pack(fill="both", expand=True, padx=5, pady=5)
        khung_danh_sach.columnconfigure(0, weight=1)
        khung_danh_sach.columnconfigure(1, weight=1)

        khung_than = ttk.LabelFrame(khung_danh_sach, text="🔥 DANH SÁCH VIÊN THAN")
        khung_than.grid(row=0, column=0, sticky="nsew", padx=(0, 3))

        self.ls_than = tk.Listbox(khung_than, height=8, font=("Arial", 10))
        self.ls_than.pack(fill="both", expand=True, padx=3, pady=3)
        self.ls_than.bind('<<ListboxSelect>>', self.chon_dong_than)
        ttk.Button(khung_than, text="🗑️ XÓA VIÊN THAN", command=self.xoa_vien_than).pack(fill="x", padx=3, pady=3)

        khung_viec = ttk.LabelFrame(khung_danh_sach, text="📝 CÔNG VIỆC / ĐUN NƯỚC")
        khung_viec.grid(row=0, column=1, sticky="nsew", padx=(3, 0))

        self.ls_viec = tk.Listbox(khung_viec, height=8, font=("Arial", 10))
        self.ls_viec.pack(fill="both", expand=True, padx=3, pady=3)
        self.ls_viec.bind('<<ListboxSelect>>', self.chon_dong_viec)
        ttk.Button(khung_viec, text="🗑️ XÓA CÔNG VIỆC", command=self.xoa_viec).pack(fill="x", padx=3, pady=3)

        # CỘT PHẢI
        cot_phai = ttk.Frame(khung_tong)
        cot_phai.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        khung_tt = ttk.LabelFrame(cot_phai, text="📊 TRẠNG THÁI VẬN HÀNH & CẢNH BÁO THAN")
        khung_tt.pack(fill="x", pady=3)
        self.tt_label = ttk.Label(khung_tt, text="Đang: —", font=("Arial", 11, "bold"))
        self.tt_label.pack(anchor="w", padx=10, pady=2)
        self.tg_label = ttk.Label(khung_tt, text="Tổng thời gian: —", font=("Arial", 10))
        self.tg_label.pack(anchor="w", padx=10, pady=2)
        self.phantram_label = ttk.Label(khung_tt, text="Tuổi thọ than: —", font=("Arial", 10))
        self.phantram_label.pack(anchor="w", padx=10, pady=2)

        f_pb = ttk.Frame(khung_tt)
        f_pb.pack(fill="x", padx=10, pady=3)
        ttk.Label(f_pb, text="Tiến trình viên than:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 2))
        self.thanh_tien_trinh = ttk.Progressbar(f_pb, orient="horizontal", length=300, mode="determinate", maximum=100)
        self.thanh_tien_trinh.pack(fill="x", expand=True)

        self.soi_label = ttk.Label(khung_tt, text="⏰ Sôi ấm tiếp: —", foreground="blue", font=("Arial", 11, "bold"))
        self.soi_label.pack(anchor="w", padx=10, pady=2)

        self.het_label = ttk.Label(khung_tt, text="⛽ Thời gian còn lại & Hết than: —", foreground="#d9534f", font=("Arial", 13, "bold"))
        self.het_label.pack(anchor="w", padx=10, pady=5)

        self.nhom_bao_label = ttk.Label(cot_phai, text="📌 Cảnh báo nhóm bếp: —", font=("Arial", 11, "bold"))
        self.nhom_bao_label.pack(anchor="w", padx=10, pady=3)

        khung_link = ttk.LabelFrame(cot_phai, text="🔊 HỆ THỐNG BÁO ĐỘNG & LIÊN KẾT VIDEO (QUAY VÒNG KHI HẾT LINK)")
        khung_link.pack(fill="both", expand=True, pady=3)

        self.ent_tep_txt = {}
        ten_nut = [
            "Nước chín sôi", 
            "Báo hết than", 
            "Cần nhóm than mới", 
            "Than bén lửa", 
            "Thông báo khác",
            "Ấm 5L (1) sôi",
            "Ấm 5L (2) sôi",
            "Ấm 3 5L sôi",
            "Nồi 7L xong"
        ]

        for i in range(len(ten_nut)):
            dong = ttk.Frame(khung_link)
            dong.pack(fill="x", pady=2, padx=5)
            t_hien_thi = self.du_lieu.get(f"nut_{i}_ten", ten_nut[i])
            ttk.Label(dong, text=f"{i+1}. {t_hien_thi}:", width=18, anchor="w", font=("Arial", 9, "bold")).grid(row=0, column=0)

            o_tep = ttk.Entry(dong, width=30, font=("Arial", 9))
            o_tep.insert(0, self.du_lieu.get(f"nut_{i}_tep_txt", ""))
            o_tep.grid(row=0, column=1, padx=2, sticky="ew")
            self.ent_tep_txt[i] = o_tep

            ttk.Button(dong, text="📂", width=3, command=lambda idx=i, o=o_tep: self.chon_tep_txt(idx, o)).grid(row=0, column=2, padx=1)
            ttk.Button(dong, text="💾", width=3, command=lambda idx=i, o=o_tep: self.luu_tep_txt(idx, o)).grid(row=0, column=3, padx=1)
            ttk.Button(dong, text="▶️", width=3, command=lambda idx=i: self.phat_link(idx)).grid(row=0, column=4, padx=1)

    def lay_trung_binh_lich_su_than(self):
        ds_than = self.du_lieu.get("than", [])
        ds_hoan_thanh = [vi for vi in ds_than if vi.get("gio_tat")]
        
        if not ds_hoan_thanh:
            return (float(self.cauhinh.get("vong_doi_to_phut", 96)), 
                    float(self.cauhinh.get("vong_doi_nho_phut", 780)))
        
        tong_t1 = 0.0
        tong_t2 = 0.0
        dem = 0
        for vi in ds_hoan_thanh:
            stt = vi["stt"]
            t1, t2, _, _ = self.tinh_thoi_gian_vien(stt)
            tong_t1 += t1
            tong_t2 += t2
            dem += 1
            
        tb_t1 = tong_t1 / dem if dem > 0 and tong_t1 > 0 else float(self.cauhinh.get("vong_doi_to_phut", 96))
        tb_t2 = tong_t2 / dem if dem > 0 and tong_t2 > 0 else float(self.cauhinh.get("vong_doi_nho_phut", 780))
        
        return max(tb_t1, 60.0), max(tb_t2, 300.0)

    def sua_o_cauhinh(self, key):
        if key in self.ent_cf:
            try:
                val = float(self.ent_cf[key].get().strip())
                self.cauhinh[key] = val
                self.du_lieu[key] = val
                luu_json(self.du_lieu)
                messagebox.showinfo("✅ Đã cập nhật", f"Đã lưu thông số thành công:\n{key} = {val}")
            except ValueError:
                messagebox.showerror("❌ Lỗi nhập liệu", "Giá trị phải là một số hợp lệ!")

    def xoa_o_cauhinh(self, key):
        if key in self.ent_cf:
            self.ent_cf[key].delete(0, tk.END)
            self.ent_cf[key].insert(0, "0")
            self.cauhinh[key] = 0.0
            self.du_lieu[key] = 0.0
            luu_json(self.du_lieu)
            messagebox.showinfo("🗑️ Đã xóa", f"Đã xóa và đặt giá trị của ô thành 0.")

    def tai_danh_sach_link(self, nut_idx):
        duong_dan_tep = self.du_lieu.get(f"nut_{nut_idx}_tep_txt", "")
        ds_link = doc_tep_txt_link(duong_dan_tep)
        self.du_lieu[f"nut_{nut_idx}_link_danh_sach"] = ds_link
        if not ds_link:
            self.du_lieu[f"nut_{nut_idx}_dang_phat"] = 0
        luu_json(self.du_lieu)
        return ds_link

    def phat_link(self, nut_idx):
        ds_link = self.tai_danh_sach_link(nut_idx)
        if not ds_link:
            return
        
        vi_tri = self.du_lieu.get(f"nut_{nut_idx}_dang_phat", 0)
        if vi_tri < 0 or vi_tri >= len(ds_link):
            vi_tri = 0
        
        link_hien_tai = ds_link[vi_tri]
        if link_hien_tai:
            webbrowser.open(link_hien_tai)
        
        vi_tri_tiep_theo = vi_tri + 1
        if vi_tri_tiep_theo >= len(ds_link):
            if self.du_lieu.get("lap_lai_video", True):
                vi_tri_tiep_theo = 0
            else:
                vi_tri_tiep_theo = len(ds_link) - 1
        
        self.du_lieu[f"nut_{nut_idx}_dang_phat"] = vi_tri_tiep_theo
        luu_json(self.du_lieu)

    def chon_tep_txt(self, nut_idx, o_nhap):
        duong_dan = filedialog.askopenfilename(filetypes=[("Tệp văn bản", "*.txt"), ("Tất cả tệp", "*.*")])
        if duong_dan:
            o_nhap.delete(0, tk.END)
            o_nhap.insert(0, duong_dan)
            self.du_lieu[f"nut_{nut_idx}_tep_txt"] = duong_dan
            self.tai_danh_sach_link(nut_idx)
            luu_json(self.du_lieu)

    def luu_tep_txt(self, nut_idx, o_nhap):
        duong_dan = o_nhap.get().strip()
        self.du_lieu[f"nut_{nut_idx}_tep_txt"] = duong_dan
        ds_link = self.tai_danh_sach_link(nut_idx)
        luu_json(self.du_lieu)
        messagebox.showinfo("✅ Đã lưu", f"Đã nạp thành công {len(ds_link)} liên kết vào tệp JSON cố định.")

    def luu_tat_ca_thong_so(self):
        for k in self.ent_cf:
            try:
                self.cauhinh[k] = float(self.ent_cf[k].get())
            except:
                pass
        for i in range(1, 6):
            key_cd = f"che_do_kethop_{i}"
            if key_cd in self.var_che_do_kethop:
                val_cd = self.var_che_do_kethop[key_cd].get()
                self.cauhinh[key_cd] = val_cd
                self.du_lieu[key_cd] = val_cd
        for i in range(9):
            self.du_lieu[f"nut_{i}_tep_txt"] = self.ent_tep_txt[i].get().strip()
            self.tai_danh_sach_link(i)
        luu_json(self.du_lieu)
        messagebox.showinfo("✅ Đã lưu tất cả", f"Đã lưu mọi cấu hình và tệp TXT vào tệp:\n{FILE_MAC_DINH}")

    def sap_xep_lai_so_thu_tu(self):
        for idx, vi in enumerate(self.du_lieu.get("than", []), start=1):
            vi["stt"] = idx
        if self.vien_dang_su_dung:
            tim_thay = any(vi["stt"] == self.vien_dang_su_dung and not vi.get("gio_tat") for vi in self.du_lieu.get("than", []))
            if not tim_thay:
                self.vien_dang_su_dung = None

    def mo_giao_dien(self, icon=None, item=None):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        try:
            self.root.state('zoomed')
        except:
            pass
        self.giao_dien_dang_mo = True

    def anh_ve_khay(self):
        self.root.withdraw()
        self.giao_dien_dang_mo = False

    def thoat_phan_mem(self, icon=None, item=None):
        try:
            if self.bieu_tuong:
                self.bieu_tuong.stop()
        except:
            pass
        os._exit(0)

    def xoa_het_du_lieu(self):
        if not messagebox.askyesno("⚠️ XÓA HẾT", "Bạn có chắc chắn muốn XÓA TOÀN BỘ dữ liệu?\nKhông thể hoàn tác!"):
            return
        self.du_lieu = cau_truc_du_lieu_mac_dinh()
        self.cauhinh = self.du_lieu
        self.vien_dang_su_dung = None
        self.duoc_chon_than = None
        self.duoc_chon_viec = None
        luu_json(self.du_lieu)
        self.cap_nhat_lich_su()
        messagebox.showinfo("✅ Đã xóa", "Đã xóa toàn bộ dữ liệu!")

    def khoi_phuc_tu_du_lieu(self):
        for vi in reversed(self.du_lieu.get("than", [])):
            if not vi.get("gio_tat"):
                self.vien_dang_su_dung = vi["stt"]
                self.dang_dung = vi.get("che_do", "dun_to")
                if vi.get("viec_da_lam") == "Đang nhóm":
                    gio_nhom_str = vi.get("gio_nhom")
                    if gio_nhom_str:
                        self.bat_dau_nhom = phan_tich_gio(gio_nhom_str)
                    if not self.bat_dau_nhom:
                        self.bat_dau_nhom = datetime.now()
                    
                    thoi_gian_nhom_phut = float(self.cauhinh.get("thoi_gian_nhom_bén", 22.0))
                    thoi_diem_ben_du_kien = self.bat_dau_nhom + timedelta(minutes=thoi_gian_nhom_phut)
                    
                    if datetime.now() >= thoi_diem_ben_du_kien:
                        self.dang_dem_nguoc_nhom = False
                        gio_ben_str = thoi_diem_ben_du_kien.strftime("%H:%M")
                        vi["gio_ben"] = gio_ben_str
                        vi["viec_da_lam"] = "Đang cháy"
                        luu_json(self.du_lieu)
                        self.nhom_label.config(text=f"✅ BÉN LỬA lúc {gio_ben_str}", foreground="green")
                    else:
                        self.dang_dem_nguoc_nhom = True
                        self.cap_nhat_dem_nguoc()
                else:
                    self.dang_dem_nguoc_nhom = False
                    self.bat_dau_nhom = None
                break

    def tinh_thoi_gian_vien(self, stt):
        t1 = 0.0
        t2 = 0.0
        so_lan_to = 0
        so_lan_nho = 0
        for vc in self.du_lieu.get("viec", []):
            if vc.get("vien_stt") == stt:
                ps = float(vc.get("phut_soi", 0))
                cd = vc.get("che_do", "dun_to")
                if cd == "dun_to":
                    t1 += ps; so_lan_to += 1
                else:
                    t2 += ps; so_lan_nho += 1
        for vi in self.du_lieu.get("than", []):
            if vi.get("stt") == stt:
                t1 += float(vi.get("t1_tich_luy", 0.0))
                t2 += float(vi.get("t2_tich_luy", 0.0))
                break
        return t1, t2, so_lan_to, so_lan_nho

    def cap_nhap_thu_cong_thoi_gian_dun(self):
        if not self.vien_dang_su_dung:
            messagebox.showwarning("⚠️ Chưa có than", "Vui lòng nhóm bếp than trước!")
            return
        try:
            p_to = float(self.ent_nhap_dun_to.get().strip() or 0)
            p_nho = float(self.ent_nhap_dun_nho.get().strip() or 0)
            
            for vi in self.du_lieu.get("than", []):
                if vi["stt"] == self.vien_dang_su_dung:
                    vi["t1_tich_luy"] = float(vi.get("t1_tich_luy", 0.0)) + p_to
                    vi["t2_tich_luy"] = float(vi.get("t2_tich_luy", 0.0)) + p_nho
                    break
            
            if p_to > 0:
                self.du_lieu.setdefault("viec", []).append({
                    "ten": "Đun thủ công (To)", "che_do": "dun_to", "phut_soi": p_to,
                    "gio_dat": lay_gio_hien_tai(), "gio_ket_thuc": "Thủ công",
                    "vien_stt": self.vien_dang_su_dung, "thoi_gian": lay_ngay_gio(), "da_bao_ket_thuc": True
                })
            if p_nho > 0:
                self.du_lieu.setdefault("viec", []).append({
                    "ten": "Đun thủ công (Nhỏ)", "che_do": "dun_nho", "phut_soi": p_nho,
                    "gio_dat": lay_gio_hien_tai(), "gio_ket_thuc": "Thủ công",
                    "vien_stt": self.vien_dang_su_dung, "thoi_gian": lay_ngay_gio(), "da_bao_ket_thuc": True
                })
            
            luu_json(self.du_lieu)
            self.cap_nhat_lich_su()
            messagebox.showinfo("✅ Đã cập nhật", "Đã ghi nhận thời gian đun vào lịch sử.")
        except ValueError:
            messagebox.showerror("❌ Lỗi", "Số phút đun phải là số hợp lệ!")

    def tinh_toan(self):
        TG_DUN_TO, TG_DUN_NHO = self.lay_trung_binh_lich_su_than()
        
        if self.dang_dem_nguoc_nhom:
            return {
                "t1": 0.0, "t2": 0.0, "da_dung": 0.0, "con_lai": 1.0,
                "phut_den_sau_am": float(self.cauhinh.get("phut_to_1", 30)),
                "p_con_hien_tai": TG_DUN_TO,
                "trang_thai_nhom": "🔥 Đang nhóm bếp bén lửa, chưa tính tiêu hao than."
            }
        
        t1, t2, _, _ = self.tinh_thoi_gian_vien(self.vien_dang_su_dung) if self.vien_dang_su_dung else (0.0, 0.0, 0, 0)
        da_dung = (t1 / TG_DUN_TO) + (t2 / TG_DUN_NHO)
        con_lai = 1 - da_dung if da_dung < 1 else 0
        
        p_con_to = con_lai * TG_DUN_TO if con_lai > 0 else 0
        p_con_nho = con_lai * TG_DUN_NHO if con_lai > 0 else 0
        
        if self.dang_dung == "dun_to":
            p_sau_am = float(self.cauhinh.get("phut_to_1", 30))
            phut_da_qua = t1 % p_sau_am if p_sau_am > 0 else 0
        else:
            p_sau_am = float(self.cauhinh.get("phut_nho_1", 127))
            phut_da_qua = t2 % p_sau_am if p_sau_am > 0 else 0
        
        phut_den_sau_am = max(0, p_sau_am - phut_da_qua)
        phut_can_nhom = float(self.cauhinh.get("thoi_gian_nhom_bén", 22))
        p_con_hien_tai = p_con_to if self.dang_dung == "dun_to" else p_con_nho
        
        if p_con_hien_tai <= 0 or da_dung >= 1:
            trang_thai_nhom = f"🚨 HẾT THAN (Viên #{self.vien_dang_su_dung or '?'}): CẦN NHÓM VIÊN MỚI NGAY LẬP TỨC."
            if not self._da_phat_canh_bao_het_than:
                self.phat_link(1)
                self._da_phat_canh_bao_het_than = True
        elif p_con_hien_tai <= 30 or p_con_hien_tai <= phut_can_nhom:
            trang_thai_nhom = f"🚨 30 PHÚT NỮA TÀN THAN — Viên #{self.vien_dang_su_dung or '?'} còn {phut_sang_gio(p_con_hien_tai)}! CẦN NHÓM VIÊN MỚI NGAY."
            if not self._da_phat_canh_bao_het_than:
                self.phat_link(2)
                self._da_phat_canh_bao_het_than = True
        else:
            trang_thai_nhom = f"✅ Bếp ổn định (Viên #{self.vien_dang_su_dung or '?'}), vận hành bình thường."
            self._da_phat_canh_bao_het_than = False
        
        return {
            "t1": t1, "t2": t2, "da_dung": da_dung, "con_lai": con_lai,
            "phut_den_sau_am": phut_den_sau_am, "p_con_hien_tai": p_con_hien_tai,
            "trang_thai_nhom": trang_thai_nhom
        }

    def bam_nhom_than(self):
        if self.dang_dem_nguoc_nhom:
            if messagebox.askyesno("⚠️ Đang đếm ngược", "Hủy đếm ngược hiện tại?"):
                self.dang_dem_nguoc_nhom = False
                self.bat_dau_nhom = None
                for vi in self.du_lieu.get("than", []):
                    if vi["stt"] == self.vien_dang_su_dung and not vi.get("gio_tat"):
                        vi["viec_da_lam"] = "Đã hủy nhóm"
                        break
                luu_json(self.du_lieu)
                self.nhom_label.config(text="🔥 Chưa nhóm")
                self.cap_nhat_lich_su()
            return
        
        if self.vien_dang_su_dung:
            gio_tat_cu = lay_gio_hien_tai()
            t1_cu, t2_cu, _, _ = self.tinh_thoi_gian_vien(self.vien_dang_su_dung)
            tong_phut_cu = round(t1_cu + t2_cu, 1)
            for vi in self.du_lieu.get("than", []):
                if vi["stt"] == self.vien_dang_su_dung and not vi.get("gio_tat"):
                    vi["gio_tat"] = gio_tat_cu
                    vi["thoi_gian_dung"] = tong_phut_cu
                    vi["t1_tich_luy"] = t1_cu
                    vi["t2_tich_luy"] = t2_cu
                    vi["viec_da_lam"] = f"Dùng: {phut_sang_gio(tong_phut_cu)}"
                    break
        
        stt_danh_sach = [i["stt"] for i in self.du_lieu.get("than", [])]
        stt_moi = 1 if not stt_danh_sach else max(stt_danh_sach) + 1
        
        gio_mac_dinh = lay_gio_hien_tai()
        gio_nhom_nhap = hoi_gio_nhom_than(stt_moi, gio_mac_dinh)
        if gio_nhom_nhap is None: return
        
        thoi_diem_bat_dau = phan_tich_gio(gio_nhom_nhap) if gio_nhom_nhap else datetime.now()
        thoi_gian_nhom_phut = float(self.cauhinh.get("thoi_gian_nhom_bén", 22.0))
        thoi_diem_ben_du_kien = thoi_diem_bat_dau + timedelta(minutes=thoi_gian_nhom_phut)
        
        ban_ghi = {
            "stt": stt_moi,
            "gio_nhom": gio_nhom_nhap or gio_mac_dinh,
            "gio_ben": None,
            "gio_tat": None,
            "thoi_gian_dung": 0,
            "t1_tich_luy": 0.0,
            "t2_tich_luy": 0.0,
            "che_do": self.dang_dung,
            "viec_da_lam": "Đang nhóm"
        }
        
        if thoi_diem_ben_du_kien <= datetime.now():
            gio_ben_str = thoi_diem_ben_du_kien.strftime("%H:%M")
            ban_ghi["gio_ben"] = gio_ben_str
            ban_ghi["viec_da_lam"] = "Đang cháy"
            self.du_lieu.setdefault("than", []).append(ban_ghi)
            self.vien_dang_su_dung = stt_moi
            self.dang_dem_nguoc_nhom = False
            self.bat_dau_nhom = None
            luu_json(self.du_lieu)
            self.nhom_label.config(text=f"✅ BÉN LỬA lúc {gio_ben_str}", foreground="green")
            self.cap_nhat_lich_su()
            messagebox.showinfo("🔥 Đã ghi nhận", f"Nhóm lúc {gio_nhom_nhap} → Bén lửa lúc {gio_ben_str}.")
        else:
            self.du_lieu.setdefault("than", []).append(ban_ghi)
            self.vien_dang_su_dung = stt_moi
            luu_json(self.du_lieu)
            self.dang_dem_nguoc_nhom = True
            self.bat_dau_nhom = thoi_diem_bat_dau
            self.cap_nhat_lich_su()
            self.cap_nhat_dem_nguoc()

    def cap_nhat_dem_nguoc(self):
        if not self.dang_dem_nguoc_nhom or not self.bat_dau_nhom: return
        thoi_gian_nhom_phut = float(self.cauhinh.get("thoi_gian_nhom_bén", 22.0))
        thoi_diem_ben_du_kien = self.bat_dau_nhom + timedelta(minutes=thoi_gian_nhom_phut)
        
        if datetime.now() >= thoi_diem_ben_du_kien:
            self.dang_dem_nguoc_nhom = False
            gio_ben = thoi_diem_ben_du_kien.strftime("%H:%M")
            for vi in self.du_lieu.get("than", []):
                if vi["stt"] == self.vien_dang_su_dung and not vi.get("gio_tat"):
                    vi["gio_ben"] = gio_ben
                    vi["viec_da_lam"] = "Đang cháy"
                    break
            luu_json(self.du_lieu)
            self.phat_link(3) 
            self.nhom_label.config(text=f"✅ BÉN LỬA lúc {gio_ben}", foreground="green")
            self.cap_nhat_lich_su()
            return
        
        con_lai = (thoi_diem_ben_du_kien - datetime.now()).total_seconds() / 60
        phut = int(con_lai)
        giay = int((con_lai - phut) * 60)
        self.nhom_label.config(text=f"🔥 Nhóm ({thoi_gian_nhom_phut:g}p) — Còn lại: {phut:02d}:{giay:02d}", foreground="orange")
        self.root.after(1000, self.cap_nhat_dem_nguoc)

    def dang_ky_viec_truc_tiep_chinh(self):
        if not self.vien_dang_su_dung:
            messagebox.showwarning("⚠️ Chưa có than", "Vui lòng nhóm bếp than trước!")
            return
        try:
            ten_viec = self.ent_ten_viec.get().strip() or "Đun nước"
            che_do = self.bien_che_do_chinh.get()
            gio_bd = self.ent_gio_bd.get().strip()
            phut_soi = float(self.ent_phut_soi.get().strip())
            gio_kt = self.ent_gio_kt.get().strip()
            
            dt_bd = phan_tich_gio(gio_bd)
            if not dt_bd:
                messagebox.showerror("❌ Lỗi giờ", "Định dạng giờ không đúng!")
                return
            
            ten_che_do_str = "Đun to" if che_do == "dun_to" else "Đun nhỏ"
            
            nut_phat_idx = 0 
            p_to = [float(self.cauhinh.get(f"phut_to_{i}", 0)) for i in range(1, 6)]
            p_nho = [float(self.cauhinh.get(f"phut_nho_{i}", 0)) for i in range(1, 6)]

            if che_do == "dun_to":
                for idx, val in enumerate(p_to):
                    if val > 0 and abs(phut_soi - val) < 1.5:
                        nut_phat_idx = 4 + (idx + 1) if (4 + idx + 1) < 9 else 0
                        break
            else:
                for idx, val in enumerate(p_nho):
                    if val > 0 and abs(phut_soi - val) < 1.5:
                        nut_phat_idx = 4 + (idx + 1) if (4 + idx + 1) < 9 else 0
                        break

            self.du_lieu.setdefault("viec", []).append({
                "ten": f"{ten_viec} ({ten_che_do_str})", 
                "che_do": che_do, 
                "phut_soi": phut_soi,
                "gio_dat": gio_bd, 
                "gio_ket_thuc": gio_kt, 
                "vien_stt": self.vien_dang_su_dung, 
                "thoi_gian": lay_ngay_gio(),
                "nut_phat_idx": nut_phat_idx,
                "da_bao_ket_thuc": False
            })
            luu_json(self.du_lieu)
            self.cap_nhat_lich_su()

            self.phat_link(nut_phat_idx)

            messagebox.showinfo("✅ Đã lưu & Phát video", f"Đã lưu thành công công việc mới và phát video báo nút #{nut_phat_idx + 1}!")
            
        except ValueError:
            messagebox.showerror("❌ Lỗi nhập liệu", "Phút đun phải là số hợp lệ!")

    def chuyen_dun_to(self):
        self.dang_dung = "dun_to"
        self.bien_che_do_chinh.set("dun_to")
        self.tt_label.config(text="Đang: Đun to", foreground="red")
        self.tt_label_tab3.config(text="Đang: Đun to", foreground="red")

    def chuyen_dun_nho(self):
        self.dang_dung = "dun_nho"
        self.bien_che_do_chinh.set("dun_nho")
        self.tt_label.config(text="Đang: Đun nhỏ", foreground="blue")
        self.tt_label_tab3.config(text="Đang: Đun nhỏ", foreground="blue")

    def ket_thuc_than(self):
        if not messagebox.askyesno("⛽ Kết thúc", "Bạn có chắc chắn kết thúc viên than này?"): return
        if self.vien_dang_su_dung:
            gio_tat = lay_gio_hien_tai()
            t1, t2, _, _ = self.tinh_thoi_gian_vien(self.vien_dang_su_dung)
            tong = round(t1 + t2, 1)
            for vi in self.du_lieu.get("than", []):
                if vi["stt"] == self.vien_dang_su_dung and not vi.get("gio_tat"):
                    vi["gio_tat"] = gio_tat
                    vi["thoi_gian_dung"] = tong
                    vi["t1_tich_luy"] = t1
                    vi["t2_tich_luy"] = t2
                    vi["viec_da_lam"] = f"Kết thúc ({phut_sang_gio(tong)})"
                    break
            luu_json(self.du_lieu)
        self.vien_dang_su_dung = None
        self.dang_dem_nguoc_nhom = False
        self.bat_dau_nhom = None
        self._da_phat_canh_bao_het_than = False
        self.cap_nhat_lich_su()
        messagebox.showinfo("⛽ Đã kết thúc", "Viên than đã kết thúc.")

    def cap_nhat_lich_su(self):
        self.ls_than.delete(0, tk.END)
        for vi in self.du_lieu.get("than", []):
            stt = vi["stt"]
            t1, t2, so_lan_to, so_lan_nho = self.tinh_thoi_gian_vien(stt)
            tong_phut = round(t1 + t2, 1)
            gio_nhom = vi.get('gio_nhom', '')
            gio_ben = vi.get('gio_ben', 'Đang nhóm')
            gio_tat = vi.get('gio_tat', 'Đang dùng')
            
            chuoi = (f"Viên #{stt} | Nhóm: {gio_nhom} → Bén: {gio_ben} → Tắt: {gio_tat} | "
                     f"🔥 To: {so_lan_to} lần ({phut_sang_gio(t1)}) | 💧 Nhỏ: {so_lan_nho} lần ({phut_sang_gio(t2)}) | ⏱️ Tổng: {phut_sang_gio(tong_phut)}")
            self.ls_than.insert(tk.END, chuoi)
        
        self.ls_viec.delete(0, tk.END)
        for vc in self.du_lieu.get("viec", []):
            cd_h = "🔥 Đun to" if vc.get('che_do') == "dun_to" else "💧 Đun nhỏ"
            self.ls_viec.insert(tk.END, f"{vc.get('ten','')} [{cd_h}] | Viên #{vc.get('vien_stt','?')} | {vc.get('gio_dat','')} → {vc.get('gio_ket_thuc','')} | {vc.get('phut_soi',0)} phút")

    def chon_dong_than(self, event):
        sel = self.ls_than.curselection()
        self.duoc_chon_than = sel[0] if sel else None

    def chon_dong_viec(self, event):
        sel = self.ls_viec.curselection()
        self.duoc_chon_viec = sel[0] if sel else None

    def xoa_vien_than(self):
        if self.duoc_chon_than is None: return
        if not messagebox.askyesno("⚠️ Xóa", "Xóa viên than này?"): return
        del self.du_lieu["than"][self.duoc_chon_than]
        self.sap_xep_lai_so_thu_tu()
        luu_json(self.du_lieu)
        self.duoc_chon_than = None
        self.cap_nhat_lich_su()

    def xoa_viec(self):
        if self.duoc_chon_viec is None: return
        if not messagebox.askyesno("⚠️ Xóa", "Xóa công việc này?"): return
        del self.du_lieu["viec"][self.duoc_chon_viec]
        luu_json(self.du_lieu)
        self.duoc_chon_viec = None
        self.cap_nhat_lich_su()

    def kiem_tra_hen_gio_viec(self):
        now = datetime.now()
        da_thay_doi = False
        
        for vc in self.du_lieu.get("viec", []):
            if not vc.get("da_bao_ket_thuc", False):
                gio_kt_str = vc.get("gio_ket_thuc", "")
                dt_kt = phan_tich_gio(gio_kt_str)
                if dt_kt:
                    if dt_kt < now - timedelta(hours=12):
                        dt_kt += timedelta(days=1)
                    
                    if now >= dt_kt:
                        vc["da_bao_ket_thuc"] = True
                        da_thay_doi = True
                        nut_idx = vc.get("nut_phat_idx", 0)
                        self.phat_link(nut_idx)
                        break
        
        if da_thay_doi:
            luu_json(self.du_lieu)

    def cap_nhat_tu_dong(self):
        kq = self.tinh_toan()
        txt_trangthai = f"Đang: {self.dang_dung.replace('dun_','Đun ')}"
        txt_tongthoigian = f"Đun to: {phut_sang_gio(kq['t1'])} | Đun nhỏ: {phut_sang_gio(kq['t2'])}"
        txt_tuoitho = f"Đã dùng: {round(kq['da_dung']*100,1)}% | Còn lại: {round(kq['con_lai']*100,1)}%"

        self.tt_label.config(text=txt_trangthai)
        self.tg_label.config(text=txt_tongthoigian)
        self.phantram_label.config(text=txt_tuoitho)

        self.tt_label_tab3.config(text=txt_trangthai)
        self.tg_label_tab3.config(text=txt_tongthoigian)
        self.phantram_label_tab3.config(text=txt_tuoitho)

        gio_nhom_goc = None
        gio_ben_goc = None
        if self.vien_dang_su_dung:
            for vi in self.du_lieu.get("than", []):
                if vi["stt"] == self.vien_dang_su_dung and not vi.get("gio_tat"):
                    gio_nhom_goc = phan_tich_gio(vi.get("gio_nhom"))
                    if vi.get("gio_ben"):
                        gio_ben_goc = phan_tich_gio(vi.get("gio_ben"))
                    break
        if not gio_nhom_goc:
            gio_nhom_goc = datetime.now()

        thoi_diem_ben_thuc_te = gio_ben_goc if gio_ben_goc else (gio_nhom_goc + timedelta(minutes=float(self.cauhinh.get("thoi_gian_nhom_bén", 22))))
        p_to, p_nho = self.lay_trung_binh_lich_su_than()

        dt_het_to = thoi_diem_ben_thuc_te + timedelta(minutes=p_to)
        dt_nhom_moi_to = dt_het_to - timedelta(minutes=25)

        dt_het_nho = thoi_diem_ben_thuc_te + timedelta(minutes=p_nho)
        dt_nhom_moi_nho = dt_het_nho - timedelta(minutes=25)

        now = datetime.now()
        phut_con_hien_tai = kq["p_con_hien_tai"]
        dt_tan_du_kien = now + timedelta(minutes=phut_con_hien_tai)
        dt_nhom_moi_du_kien = dt_tan_du_kien - timedelta(minutes=25)

        self.lbl_het_to.config(text=f"⏰ Hết (100% To): {dt_het_to.strftime('%H:%M')} | Nhóm mới (trước 25p): {dt_nhom_moi_to.strftime('%H:%M')}")
        self.lbl_het_nho.config(text=f"⏰ Hết (100% Nhỏ): {dt_het_nho.strftime('%H:%M')} | Nhóm mới (trước 25p): {dt_nhom_moi_nho.strftime('%H:%M')}")
        self.lbl_het_ket_hop.config(text=f"⏰ Tàn dự kiến: {dt_tan_du_kien.strftime('%H:%M')} | Nhóm mới (trước 25p): {dt_nhom_moi_du_kien.strftime('%H:%M')}")

        self.thanh_tien_trinh['value'] = kq['da_dung'] * 100
        self.soi_label.config(text=f"⏰ Sôi ấm tiếp: {phut_sang_gio(kq['phut_den_sau_am'])}")
        self.het_label.config(text=f"⛽ Còn lại: {phut_sang_gio(kq['p_con_hien_tai'])}")
        self.nhom_bao_label.config(text=f"📌 {kq['trang_thai_nhom']}")
        
        self.kiem_tra_hen_gio_viec()
        self.root.after(1000, self.cap_nhat_tu_dong)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    app = QuanLyBepThan(root)

    def khi_dong_cua_so():
        root.withdraw()
        app.giao_dien_dang_mo = False

    root.protocol("WM_DELETE_WINDOW", khi_dong_cua_so)

    def thoat_chuong_trinh_an_toan(icon, item):
        try:
            icon.stop()
        except:
            pass
        try:
            root.after(0, root.destroy)
        except:
            pass
        os._exit(0)

    app.bieu_tuong.menu = pystray.Menu(
        pystray.MenuItem("📋 Mở giao diện", lambda: root.after(0, app.mo_giao_dien)),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("❌ Thoát hoàn toàn", thoat_chuong_trinh_an_toan)
    )

    def chay_khay_he_thong():
        try:
            app.bieu_tuong.run()
        except Exception:
            pass

    t_tray = threading.Thread(target=chay_khay_he_thong, daemon=True)
    t_tray.start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            if app.bieu_tuong:
                app.bieu_tuong.stop()
        except:
            pass
        os._exit(0)