import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp


def download_video():
    url = url_entry.get()
    save_path = path_entry.get()
    
    if not url:
        messagebox.showerror("Erro", "Por favor, insira uma URL!")
        return
    if not save_path:
        messagebox.showerror("Erro", "Por favor, selecione um local para salvar o vídeo!")
        return

    try:
        # Configurações do yt-dlp
        ydl_opts = {
            'outtmpl': f"{save_path}/%(title)s.%(ext)s",  # Define o caminho e o nome do arquivo
            'quiet': True,  # Remove mensagens desnecessárias do console
            'format': 'best',  # Baixa o vídeo na melhor qualidade disponível
        }

        # Faz o download do vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao baixar o vídeo:\n{str(e)}")


def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder)


# Configuração da interface gráfica
app = tk.Tk()
app.title("Downloader de Vídeos")
app.geometry("500x300")
app.resizable(False, False)

# Label e campo de entrada para a URL
tk.Label(app, text="URL do Vídeo:", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(app, width=50, font=("Arial", 12))
url_entry.pack(pady=5)

# Botão para selecionar pasta de salvamento
tk.Label(app, text="Salvar em:", font=("Arial", 12)).pack(pady=10)
path_frame = tk.Frame(app)
path_frame.pack(pady=5)
path_entry = tk.Entry(path_frame, width=40, font=("Arial", 12))
path_entry.pack(side=tk.LEFT, padx=5)
tk.Button(path_frame, text="Selecionar", command=select_folder).pack(side=tk.RIGHT)

# Botão para iniciar o download
tk.Button(app, text="Iniciar Download", font=("Arial", 12), command=download_video, bg="#4CAF50", fg="white").pack(pady=20)

# Área de exibição de status
status_label = tk.Label(app, text="", font=("Arial", 10), fg="red")
status_label.pack(pady=5)

# Iniciar a aplicação
app.mainloop()
