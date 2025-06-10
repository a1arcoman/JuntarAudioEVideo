import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import threading
import re
from pathlib import Path

class VideoAudioMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("Juntar Vídeo e Áudio")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Variáveis para armazenar os caminhos dos arquivos
        self.video_path = tk.StringVar()
        self.audio_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.output_filename = tk.StringVar()
        
        # Variáveis para controlar processos de preview
        self.video_preview_process = None
        self.audio_preview_process = None
        
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
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Seleção de vídeo
        ttk.Label(main_frame, text="Arquivo de Vídeo:").grid(row=1, column=0, 
                                                            sticky=tk.W, pady=5)
        video_entry = ttk.Entry(main_frame, textvariable=self.video_path, width=40)
        video_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        ttk.Button(main_frame, text="Procurar", 
                  command=self.select_video_file).grid(row=1, column=2, pady=5, padx=(5, 5))
        self.video_preview_btn = ttk.Button(main_frame, text="▶ Preview", 
                                          command=self.preview_video, state='disabled')
        self.video_preview_btn.grid(row=1, column=3, pady=5)
        
        # Seleção de áudio
        ttk.Label(main_frame, text="Arquivo de Áudio:").grid(row=2, column=0, 
                                                            sticky=tk.W, pady=5)
        audio_entry = ttk.Entry(main_frame, textvariable=self.audio_path, width=40)
        audio_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        ttk.Button(main_frame, text="Procurar", 
                  command=self.select_audio_file).grid(row=2, column=2, pady=5, padx=(5, 5))
        self.audio_preview_btn = ttk.Button(main_frame, text="🔊 Preview", 
                                          command=self.preview_audio, state='disabled')
        self.audio_preview_btn.grid(row=2, column=3, pady=5)
        
        # Pasta de saída
        ttk.Label(main_frame, text="Pasta de Saída:").grid(row=3, column=0, 
                                                          sticky=tk.W, pady=5)
        folder_entry = ttk.Entry(main_frame, textvariable=self.output_folder, width=40)
        folder_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        ttk.Button(main_frame, text="Procurar", 
                  command=self.select_output_folder).grid(row=3, column=2, pady=5, padx=(5, 5))
        
        # Nome do arquivo de saída
        ttk.Label(main_frame, text="Nome do Arquivo:").grid(row=4, column=0, 
                                                           sticky=tk.W, pady=5)
        filename_entry = ttk.Entry(main_frame, textvariable=self.output_filename, width=40)
        filename_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        
        # Bind para validar nome do arquivo em tempo real
        filename_entry.bind('<KeyRelease>', self.validate_filename)
        
        # Label para mostrar extensão
        self.extension_label = ttk.Label(main_frame, text=".mp4", foreground="gray")
        self.extension_label.grid(row=4, column=2, pady=5, sticky=tk.W, padx=(5, 5))
        
        # Frame para botões de controle de preview
        preview_control_frame = ttk.Frame(main_frame)
        preview_control_frame.grid(row=5, column=0, columnspan=4, pady=10)
        
        ttk.Button(preview_control_frame, text="⏹ Parar Previews", 
                  command=self.stop_all_previews).pack(side=tk.LEFT, padx=5)
        
        # Botão de processar
        self.process_button = ttk.Button(main_frame, text="Juntar Vídeo e Áudio", 
                                        command=self.start_merge_process)
        self.process_button.grid(row=6, column=0, columnspan=4, pady=20)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # Área de status
        self.status_text = tk.Text(main_frame, height=8, width=70)
        self.status_text.grid(row=8, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), 
                             pady=10)
        
        # Scrollbar para o texto de status
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=8, column=4, sticky=(tk.N, tk.S), pady=10)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Configurar weights para redimensionamento
        main_frame.rowconfigure(8, weight=1)
        
    def preview_video(self):
        """Abre o vídeo no player padrão do sistema"""
        video_file = self.video_path.get()
        if not video_file or not os.path.exists(video_file):
            messagebox.showerror("Erro", "Arquivo de vídeo não encontrado.")
            return
            
        try:
            # Parar preview anterior se estiver rodando
            self.stop_video_preview()
            
            # Usar FFplay para preview (mais controle) ou player padrão do sistema
            try:
                # Tentar usar FFplay primeiro (melhor controle)
                self.video_preview_process = subprocess.Popen([
                    'ffplay', 
                    '-window_title', f'Preview: {os.path.basename(video_file)}',
                    '-autoexit',  # Fechar automaticamente no final
                    video_file
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.update_status(f"🎬 Preview do vídeo iniciado: {os.path.basename(video_file)}")
            except FileNotFoundError:
                # Se FFplay não estiver disponível, usar player padrão do sistema
                if os.name == 'nt':  # Windows
                    os.startfile(video_file)
                elif os.name == 'posix':  # Linux/Mac
                    subprocess.Popen(['xdg-open', video_file])
                self.update_status(f"🎬 Abrindo vídeo no player padrão: {os.path.basename(video_file)}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir preview do vídeo: {str(e)}")
            self.update_status(f"❌ Erro no preview do vídeo: {str(e)}")
    
    def preview_audio(self):
        """Reproduz o áudio no player padrão do sistema"""
        audio_file = self.audio_path.get()
        if not audio_file or not os.path.exists(audio_file):
            messagebox.showerror("Erro", "Arquivo de áudio não encontrado.")
            return
            
        try:
            # Parar preview anterior se estiver rodando
            self.stop_audio_preview()
            
            # Usar FFplay para preview (melhor controle) ou player padrão do sistema
            try:
                # Tentar usar FFplay primeiro (melhor controle)
                self.audio_preview_process = subprocess.Popen([
                    'ffplay', 
                    '-window_title', f'Preview Audio: {os.path.basename(audio_file)}',
                    '-autoexit',  # Fechar automaticamente no final
                    '-nodisp',    # Não mostrar vídeo (apenas áudio)
                    audio_file
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.update_status(f"🔊 Preview do áudio iniciado: {os.path.basename(audio_file)}")
            except FileNotFoundError:
                # Se FFplay não estiver disponível, usar player padrão do sistema
                if os.name == 'nt':  # Windows
                    os.startfile(audio_file)
                elif os.name == 'posix':  # Linux/Mac
                    subprocess.Popen(['xdg-open', audio_file])
                self.update_status(f"🔊 Abrindo áudio no player padrão: {os.path.basename(audio_file)}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir preview do áudio: {str(e)}")
            self.update_status(f"❌ Erro no preview do áudio: {str(e)}")
    
    def stop_video_preview(self):
        """Para o preview do vídeo"""
        if self.video_preview_process and self.video_preview_process.poll() is None:
            try:
                self.video_preview_process.terminate()
                self.update_status("⏹ Preview do vídeo parado")
            except:
                pass
            self.video_preview_process = None
    
    def stop_audio_preview(self):
        """Para o preview do áudio"""
        if self.audio_preview_process and self.audio_preview_process.poll() is None:
            try:
                self.audio_preview_process.terminate()
                self.update_status("⏹ Preview do áudio parado")
            except:
                pass
            self.audio_preview_process = None
    
    def stop_all_previews(self):
        """Para todos os previews ativos"""
        self.stop_video_preview()
        self.stop_audio_preview()
        self.update_status("⏹ Todos os previews foram parados")
        
    def sanitize_filename(self, filename):
        """Remove ou substitui caracteres especiais inválidos do nome do arquivo"""
        # Caracteres inválidos no Windows: < > : " | ? * \ /
        invalid_chars = r'[<>:"|?*\\/]'
        
        # Substituir caracteres inválidos por underscore
        sanitized = re.sub(invalid_chars, '_', filename)
        
        # Remover caracteres de controle (ASCII 0-31)
        sanitized = re.sub(r'[\x00-\x1f]', '', sanitized)
        
        # Remover espaços no início e fim
        sanitized = sanitized.strip()
        
        # Remover pontos no final (inválido no Windows)
        sanitized = sanitized.rstrip('.')
        
        # Se o nome ficou vazio, usar um nome padrão
        if not sanitized:
            sanitized = "video_output"
        
        # Limitar tamanho do nome (255 caracteres é o limite do Windows)
        if len(sanitized) > 200:  # Deixar espaço para extensão
            sanitized = sanitized[:200]
        
        return sanitized
    
    def validate_filename(self, event=None):
        """Valida e corrige o nome do arquivo em tempo real"""
        current_name = self.output_filename.get()
        sanitized_name = self.sanitize_filename(current_name)
        
        # Se o nome foi alterado, atualizar o campo
        if current_name != sanitized_name:
            # Salvar posição do cursor
            cursor_pos = event.widget.index(tk.INSERT) if event else len(sanitized_name)
            
            # Atualizar o valor
            self.output_filename.set(sanitized_name)
            
            # Restaurar posição do cursor (ajustada se necessário)
            try:
                new_pos = min(cursor_pos, len(sanitized_name))
                event.widget.icursor(new_pos)
            except:
                pass
        
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
            self.video_preview_btn.config(state='normal')
            self.update_status(f"Vídeo selecionado: {os.path.basename(filename)}")
            
            # Auto-sugerir nome do arquivo baseado no vídeo
            if not self.output_filename.get():
                video_name = Path(filename).stem
                suggested_name = self.sanitize_filename(f"{video_name}_com_audio")
                self.output_filename.set(suggested_name)
            
    def select_audio_file(self):
        filetypes = [
            ('Arquivos de Áudio e Vídeo', '*.mp3 *.wav *.aac *.flac *.ogg *.m4a *.wma *.mp4 *.avi *.mov *.mkv'),
            ('Arquivos de Áudio', '*.mp3 *.wav *.aac *.flac *.ogg *.m4a *.wma'),
            ('Arquivos de Vídeo', '*.mp4 *.avi *.mov *.mkv'),
            ('Todos os arquivos', '*.*')
        ]
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo de áudio",
            filetypes=filetypes
        )
        if filename:
            self.audio_path.set(filename)
            self.audio_preview_btn.config(state='normal')
            self.update_status(f"Áudio selecionado: {os.path.basename(filename)}")
            
    def select_output_folder(self):
        folder = filedialog.askdirectory(
            title="Selecionar pasta de saída"
        )
        if folder:
            self.output_folder.set(folder)
            self.update_status(f"Pasta de saída: {folder}")
            
    def get_output_path(self):
        """Constrói o caminho completo do arquivo de saída"""
        folder = self.output_folder.get()
        filename = self.output_filename.get()
        
        if not folder or not filename:
            return None
            
        # Garantir que o nome do arquivo tenha extensão
        if not filename.lower().endswith(('.mp4', '.avi', '.mkv')):
            filename += '.mp4'
            
        return os.path.join(folder, filename)
            
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
            
        if not self.output_folder.get():
            messagebox.showerror("Erro", "Por favor, selecione a pasta de saída.")
            return
            
        if not self.output_filename.get():
            messagebox.showerror("Erro", "Por favor, defina o nome do arquivo de saída.")
            return
            
        # Verificar se os arquivos existem
        if not os.path.exists(self.video_path.get()):
            messagebox.showerror("Erro", "Arquivo de vídeo não encontrado.")
            return
            
        if not os.path.exists(self.audio_path.get()):
            messagebox.showerror("Erro", "Arquivo de áudio não encontrado.")
            return
            
        # Verificar se a pasta de saída existe
        if not os.path.exists(self.output_folder.get()):
            messagebox.showerror("Erro", "Pasta de saída não encontrada.")
            return
            
        # Parar todos os previews antes de iniciar o merge
        self.stop_all_previews()
        
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
            output_file = self.get_output_path()
            
            if not output_file:
                self.update_status("❌ Erro: Não foi possível determinar o arquivo de saída.")
                return
            
            self.update_status("Iniciando processo de junção...")
            self.update_status(f"Arquivo de saída: {output_file}")
            
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
    
    def __del__(self):
        """Limpar recursos ao fechar o programa"""
        self.stop_all_previews()

def main():
    root = tk.Tk()
    app = VideoAudioMerger(root)
    
    # Garantir que os previews sejam parados ao fechar a janela
    def on_closing():
        app.stop_all_previews()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()