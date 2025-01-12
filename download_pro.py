import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading
import os
import re
from datetime import datetime

class YoutubeDownloader:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("YouTube Downloader")
        self.app.geometry("600x500")
        self.app.resizable(False, False)
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.configure("Download.TButton", 
                           padding=10, 
                           font=("Arial", 12))
        
        self.create_widgets()
        self.current_download = None
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.app, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL Entry
        ttk.Label(main_frame, 
                 text="URL do Vídeo:", 
                 font=("Arial", 12)).pack(pady=5)
        self.url_entry = ttk.Entry(main_frame, width=60, font=("Arial", 12))
        self.url_entry.pack(pady=5)
        
        # Diretório de download
        ttk.Label(main_frame, 
                 text="Salvar em:", 
                 font=("Arial", 12)).pack(pady=5)
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        self.path_entry = ttk.Entry(path_frame, font=("Arial", 12))
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(path_frame, 
                  text="Selecionar", 
                  command=self.select_folder).pack(side=tk.RIGHT)
        
        # Opções de formato
        format_frame = ttk.LabelFrame(main_frame, text="Formato", padding=10)
        format_frame.pack(fill=tk.X, pady=10)
        
        self.format_var = tk.StringVar(value="video")
        ttk.Radiobutton(format_frame, 
                       text="Vídeo (MP4)", 
                       variable=self.format_var, 
                       value="video").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(format_frame, 
                       text="Áudio (MP3)", 
                       variable=self.format_var, 
                       value="audio").pack(side=tk.LEFT, padx=10)
        
        # Qualidade de vídeo
        quality_frame = ttk.LabelFrame(main_frame, text="Qualidade", padding=10)
        quality_frame.pack(fill=tk.X, pady=10)
        
        self.quality_var = tk.StringVar(value="highest")
        qualities = [("1080p", "1080"), 
                    ("720p", "720"), 
                    ("480p", "480"), 
                    ("360p", "360")]
        
        for text, value in qualities:
            ttk.Radiobutton(quality_frame, 
                          text=text, 
                          variable=self.quality_var, 
                          value=value).pack(side=tk.LEFT, padx=10)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, 
                                      variable=self.progress_var, 
                                      maximum=100)
        self.progress.pack(fill=tk.X, pady=10)
        
        # Status
        self.status_label = ttk.Label(main_frame, 
                                    text="", 
                                    font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, 
                  text="Iniciar Download", 
                  style="Download.TButton",
                  command=self.start_download).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, 
                  text="Cancelar", 
                  style="Download.TButton",
                  command=self.cancel_download).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, 
                  text="Limpar", 
                  style="Download.TButton",
                  command=self.clear_fields).pack(side=tk.LEFT, padx=5)
    
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
    
    def validate_url(self, url):
        youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
        return bool(re.match(youtube_regex, url))
    
    def start_download(self):
        url = self.url_entry.get().strip()
        save_path = self.path_entry.get().strip()
        
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL!")
            return
        
        if not self.validate_url(url):
            messagebox.showerror("Erro", "URL inválida! Use uma URL do YouTube.")
            return
        
        if not save_path:
            messagebox.showerror("Erro", "Por favor, selecione um local para salvar!")
            return
        
        if not os.path.exists(save_path):
            messagebox.showerror("Erro", "Diretório de destino não existe!")
            return
        
        self.current_download = threading.Thread(target=self.download_video, 
                                               args=(url, save_path))
        self.current_download.start()
    
    def download_video(self, url, save_path):
        try:
            self.status_label.config(text="Obtendo informações do vídeo...")
            self.progress_var.set(0)
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    p = d.get('_percent_str', '0%').replace('%', '')
                    try:
                        self.progress_var.set(float(p))
                    except ValueError:
                        pass
                    self.status_label.config(
                        text=f"Baixando: {d.get('_percent_str', '0%')}")
            
            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'cookiefile': 'F:/videos/cookie/cookies.txt',
                'progress_hooks': [progress_hook],
            }

            # Configuração do formato baseado na seleção do usuário
            if self.format_var.get() == 'audio':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                # Configuração da qualidade do vídeo
                quality = self.quality_var.get()
                if quality == 'highest':
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                else:
                    ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
            
            self.status_label.config(text="Download concluído com sucesso!")
            self.progress_var.set(100)
            messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
            
        except Exception as e:
            self.status_label.config(text="Erro ao baixar o vídeo.")
            messagebox.showerror("Erro", f"Falha ao baixar o vídeo:\n{str(e)}")
    
    def cancel_download(self):
        if self.current_download and self.current_download.is_alive():
            self.status_label.config(text="Cancelando download...")
            # Implementar lógica de cancelamento aqui
            self.status_label.config(text="Download cancelado.")
            self.progress_var.set(0)
    
    def clear_fields(self):
        self.url_entry.delete(0, tk.END)
        self.path_entry.delete(0, tk.END)
        self.status_label.config(text="")
        self.progress_var.set(0)
        self.format_var.set("video")
        self.quality_var.set("highest")
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = YoutubeDownloader()
    app.run()