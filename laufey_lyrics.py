import tkinter as tk
import random
import time
import sys
import winsound
import os
import threading
import ctypes

# =======================================================================
# KONFIGURASI LIRIK DAN TEMPO (BISA ANDA UBAH SENDIRI)
# word_delay = Kecepatan mengetik per kata (dalam milidetik)
# post_delay = Jeda waktu (dalam milidetik) setelah lirik ini selesai 
#              diketik, sebelum memunculkan jendela lirik selanjutnya.
# =======================================================================
LYRICS_DATA = [
    {"text": "I swear to God, I almost drowned", "word_delay": 440, "post_delay": 1900},
    {"text": "You asked me how I've been", "word_delay": 400, "post_delay": 1500},
    {"text": "but how could I begin", "word_delay": 500, "post_delay": 2000},
    
    # Efek SHAKING & FLASHING diset agar aktif TEPAT di baris ini
    # menggunakan kunci "trigger_effects": True
    {"text": "To tell you I should've chased you", "word_delay": 320, "post_delay": 1800, "trigger_effects": True},
    
    {"text": "I should be who you're engaged to", "word_delay": 300, "post_delay": 2000},
    {"text": "Lost my fight with fate", "word_delay": 300, "post_delay": 2000},
    {"text": "A tug-of-war of leave and stay", "word_delay": 340, "post_delay": 2000},
    {"text": "I give in, I abdicate", "word_delay": 400, "post_delay": 1800},
    {"text": "I lay my sword down anyway", "word_delay": 350, "post_delay": 1800},
    {"text": "I'll see you at Heaven's gate", "word_delay": 350, "post_delay": 1800},
    
    # Baris terakhir: durasi post_delay lebih lama agar tidak langsung tertutup
    {"text": "'Cause it's too little, way too late", "word_delay": 340, "post_delay": 7000}
]

def play_music():
    try:
        # Menggunakan mciSendStringW dari ctypes.windll.winmm 
        # API Windows ini memutar multimedia secara background tanpa membuat UI app.
        ctypes.windll.winmm.mciSendStringW('open "laufey_tkinter.mpeg" alias media', None, 0, None)
        ctypes.windll.winmm.mciSendStringW('play media', None, 0, None)
    except Exception as e:
        print("Error memutar musik:", e)

class LyricsApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw() # Sembunyikan window utama (root)
        
        # Jalankan musik di background thread
        threading.Thread(target=play_music, daemon=True).start()
        
        self.windows = [] # Menyimpan semua window agar tidak dihapus
        self.stage_idx = 0
        self.special_effects_active = False 
        
        # Variabel global agar kelap-kelip hitam-putih konsisten di semua window
        self.is_black_bg = False
        
        self.run_next_stage()
        
    def get_random_position(self, width, height):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        max_x = max(0, screen_w - width)
        max_y = max(0, screen_h - height)
        
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        return x, y
        
    def create_popup(self, stage_data, is_last=False):
        text = stage_data["text"]
        word_delay = stage_data.get("word_delay", 300)
        post_delay = stage_data.get("post_delay", 1500)
        
        win = tk.Toplevel(self.root)
        # win.overrideredirect(True) # Di-comment agar title bar ('tulisan tkinter') kembali muncul
        win.title("tkinter-By-Zael") # Memastikan tulisan tkinter muncul di bagian atas
        win.attributes("-topmost", True)
        
        # Set label (Font dibuat SANGAT BESAR agar full-fill area 500x500)
        label = tk.Label(win, text="", font=('Helvetica', 55, 'bold'), 
                         wraplength=495, justify="center", anchor="center")
        
        # Pengecekan trigger efek Shaking & Flashing tepat untuk lirik yang ditetapkan
        if stage_data.get("trigger_effects", False) and not self.special_effects_active:
            self.special_effects_active = True
            self.shake_all_windows()
            self.flash_all_windows()

        # Jika jendela baru muncul di tengah-tengah efek flashing, sinkronkan warnanya
        if self.special_effects_active:
            bg_color = "black" if self.is_black_bg else "white"
            fg_color = "white" if self.is_black_bg else "black"
            win.configure(bg=bg_color)
            label.configure(bg=bg_color, fg=fg_color)
            
        label.pack(expand=True, fill='both') # Expand & Fill area window
        
        x, y = self.get_random_position(500, 500)
        win.geometry(f'500x500+{x}+{y}')
        win.base_x = x
        win.base_y = y
        
        win.bind("<Button-1>", lambda e: sys.exit(0))
        label.bind("<Button-1>", lambda e: sys.exit(0))
        
        self.windows.append({"win": win, "label": label})
        
        # Pisahkan lirik menjadi kata per kata
        words = text.split(" ")
        self.word_by_word_effect(win, label, words, 0, word_delay, post_delay, is_last)
        
        return win

    def word_by_word_effect(self, win, label, words, word_idx, word_delay, post_delay, is_last):
        if not win.winfo_exists():
            return

        if word_idx <= len(words):
            displayed_text = " ".join(words[:word_idx])
            label.config(text=displayed_text)
            self.root.after(word_delay, self.word_by_word_effect, win, label, words, word_idx + 1, word_delay, post_delay, is_last)
        else:
            if not is_last:
                self.root.after(post_delay, self.run_next_stage)
            else:
                self.root.after(post_delay, lambda: sys.exit(0))

    def run_next_stage(self):
        if self.stage_idx < len(LYRICS_DATA):
            stage_data = LYRICS_DATA[self.stage_idx]
            is_last = (self.stage_idx == len(LYRICS_DATA) - 1)
            self.create_popup(stage_data, is_last)
            self.stage_idx += 1

    def shake_all_windows(self):
        if not self.special_effects_active:
            return
            
        for obj in self.windows:
            win = obj["win"]
            if win.winfo_exists():
                dx = random.randint(-6, 6) # Dikurangi agar getaran lebih halus
                dy = random.randint(-6, 6)
                win.geometry(f'500x500+{win.base_x + dx}+{win.base_y + dy}')
                
        self.root.after(30, self.shake_all_windows) # Delay ditambah sedikit agar gerakannya lebih smooth

    def flash_all_windows(self):
        if not self.special_effects_active:
            return
            
        # Balik state warna sekali saja per iterasi untuk semua windows
        self.is_black_bg = not self.is_black_bg
        new_bg = "black" if self.is_black_bg else "white"
        new_fg = "white" if self.is_black_bg else "black"
        
        # Aplikasikan warna yang sama ke semua window
        for obj in self.windows:
            win = obj["win"]
            label = obj["label"]
            if win.winfo_exists():
                win.configure(bg=new_bg)
                label.configure(bg=new_bg, fg=new_fg)
                
        self.root.after(100, self.flash_all_windows)

if __name__ == "__main__":
    root = tk.Tk()
    app = LyricsApp(root)
    root.mainloop()
