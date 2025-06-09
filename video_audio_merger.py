import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import threading
from pathlib import Path

class VideoAudioMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("Juntar Vídeo e Áudio")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Variáveis para armazenar os caminhos dos arquivos
        self.video_path = tk.StringVar()
        self.audio_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Juntar Vídeo e Áudio", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seleção de vídeo
        ttk.Label(main_frame, text="Arquivo de Vídeo:").grid(row=1, column=0, 
                                                            sticky=tk.W, pady=5)
        video_entry = ttk.Entry(main_frame, textvariable=self.video_path, width=50)
        video_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        ttk.Button(main_frame, text="Procurar", 
                  command=self.select_video_file).grid(row=1, column=2, pady=5)
        
        # Seleção de áudio
        ttk.Label(main_frame, text="Arquivo de Áudio:").grid(row=2, column=0, 
                                                            sticky=tk.W, pady=5)
        audio_entry = ttk.Entry(main_frame, textvariable=self.audio_path, width=50)
        audio_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        ttk.Button(main_frame, text="Procurar", 
                  command=self.select_audio_file).grid(row=2, column=2, pady=5)
        
        # Seleção de saída
        ttk.Label(main_frame, text="Arquivo de Saída:").grid(row=3, column=0, 
                                                           sticky=tk.W, pady=5)
        output_entry = ttk.Entry(main_frame, textvariable=self.output_path, width=50)
        output_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        ttk.Button(main_frame, text="Salvar Como", 
                  command=self.select_output_file).grid(row=3, column=2, pady=5)
        
        # Botão de processar
        self.process_button = ttk.Button(main_frame, text="Juntar Vídeo e Áudio", 
                                        command=self.start_merge_process)
        self.process_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Área de status
        self.status_text = tk.Text(main_frame, height=8, width=70)
        self.status_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                             pady=10)
        
        # Scrollbar para o texto de status
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=6, column=3, sticky=(tk.N, tk.S), pady=10)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Configurar weights para redimensionamento
        main_frame.rowconfigure(6, weight=1)
        
    def select_video_file(self):
        filetypes = [
            ('Arquivos de Vídeo', '*.mp4 *.avi *.mov *.mkv *.ts *.flv *.webm *.m4v'),
            ('Todos os arquivos', '*.*')
        ]
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo de vídeo",
            filetypes=filetypes
        )
        if filename:
            self.video_path.set(filename)
            self.update_status(f"Vídeo selecionado: {os.path.basename(filename)}")
            
    def select_audio_file(self):
        filetypes = [
            ('Arquivos de Áudio', '*.mp3 *.wav *.aac *.flac *.ogg *.m4a *.wma'),
            ('Arquivos de Vídeo (áudio)', '*.mp4 *.avi *.mov *.mkv'),
            ('Todos os arquivos', '*.*')
        ]
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo de áudio",
            filetypes=filetypes
        )
        if filename:
            self.audio_path.set(filename)
            self.update_status(f"Áudio selecionado: {os.path.basename(filename)}")
            
    def select_output_file(self):
        filetypes = [
            ('Arquivo MP4', '*.mp4'),
            ('Arquivo AVI', '*.avi'),
            ('Arquivo MKV', '*.mkv'),
            ('Todos os arquivos', '*.*')
        ]
        filename = filedialog.asksaveasfilename(
            title="Salvar arquivo como",
            filetypes=filetypes,
            defaultextension=".mp4"
        )
        if filename:
            self.output_path.set(filename)
            self.update_status(f"Saída definida: {os.path.basename(filename)}")
            
    def update_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_merge_process(self):
        if not self.video_path.get():
            messagebox.showerror("Erro", "Por favor, selecione um arquivo de vídeo.")
            return
            
        if not self.audio_path.get():
            messagebox.showerror("Erro", "Por favor, selecione um arquivo de áudio.")
            return
            
        if not self.output_path.get():
            messagebox.showerror("Erro", "Por favor, defina o arquivo de saída.")
            return
            
        # Verificar se os arquivos existem
        if not os.path.exists(self.video_path.get()):
            messagebox.showerror("Erro", "Arquivo de vídeo não encontrado.")
            return
            
        if not os.path.exists(self.audio_path.get()):
            messagebox.showerror("Erro", "Arquivo de áudio não encontrado.")
            return
            
        # Iniciar processo em thread separada
        self.process_button.config(state='disabled')
        self.progress.start()
        
        thread = threading.Thread(target=self.merge_video_audio)
        thread.daemon = True
        thread.start()
        
    def merge_video_audio(self):
        try:
            video_file = self.video_path.get()
            audio_file = self.audio_path.get()
            output_file = self.output_path.get()
            
            self.update_status("Iniciando processo de junção...")
            
            # Comando FFmpeg para juntar vídeo e áudio
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', audio_file,
                '-c:v', 'copy',  # Copiar vídeo sem recodificar
                '-c:a', 'aac',   # Codificar áudio em AAC
                '-map', '0:v:0', # Mapear primeiro stream de vídeo
                '-map', '1:a:0', # Mapear primeiro stream de áudio
                '-shortest',     # Terminar quando o menor arquivo acabar
                '-y',            # Sobrescrever arquivo de saída
                output_file
            ]
            
            self.update_status(f"Executando: {' '.join(cmd)}")
            
            # Executar FFmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Capturar saída
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.update_status("✅ Processo concluído com sucesso!")
                self.update_status(f"Arquivo salvo em: {output_file}")
                messagebox.showinfo("Sucesso", "Vídeo e áudio foram juntados com sucesso!")
            else:
                self.update_status("❌ Erro durante o processo:")
                self.update_status(stderr)
                messagebox.showerror("Erro", f"Erro durante o processo:\n{stderr}")
                
        except FileNotFoundError:
            error_msg = "FFmpeg não encontrado. Por favor, instale o FFmpeg e adicione-o ao PATH do sistema."
            self.update_status(f"❌ {error_msg}")
            messagebox.showerror("Erro", error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            self.update_status(f"❌ {error_msg}")
            messagebox.showerror("Erro", error_msg)
        finally:
            # Restaurar interface
            self.progress.stop()
            self.process_button.config(state='normal')

def main():
    root = tk.Tk()
    app = VideoAudioMerger(root)
    root.mainloop()

if __name__ == "__main__":
    main()