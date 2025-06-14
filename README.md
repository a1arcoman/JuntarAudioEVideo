# Video Audio Merger
## 📝 Descrição
O Video Audio Merger é um programa Python com interface gráfica intuitiva que permite combinar arquivos de vídeo (sem áudio) com arquivos de áudio de forma simples e eficiente. O programa utiliza a biblioteca tkinter para a interface gráfica e o FFmpeg para o processamento dos arquivos multimídia.

## ✨ Características
- Interface gráfica intuitiva desenvolvida com tkinter
- Suporte a múltiplos formatos de vídeo : MP4, AVI, MOV, MKV, TS, FLV, WebM, M4V
- Suporte a múltiplos formatos de áudio : MP3, WAV, AAC, FLAC, OGG, M4A, WMA
- Possibilidade de extrair áudio de vídeos : MP4, AVI, MOV, MKV
- Barra de progresso durante o processamento
- Área de status em tempo real para acompanhar o processo
- Validação completa de arquivos antes do processamento
- Processamento em thread separada para não travar a interface
- Tratamento de erros com mensagens informativas
- Interface responsiva que pode ser redimensionada
## 🛠️ Pré-requisitos
### Python
- Python 3.6 ou superior
- Bibliotecas padrão: tkinter , subprocess , os , threading , pathlib
### FFmpeg
O programa requer o FFmpeg instalado no sistema:
 Windows:
1. Opção 1 - Download manual :
   
   - Baixe o FFmpeg de https://ffmpeg.org/download.html
   - Extraia o arquivo e adicione a pasta bin ao PATH do sistema
2. Opção 2 - Chocolatey :
   
   ```
   choco install ffmpeg
   ```
3. Opção 3 - Winget :
   
   ```
   winget install FFmpeg
   ``` Verificar instalação:
```
ffmpeg -version
```
## 📁 Estrutura do Projeto
```
juntarAudioEVideo/
├── video_audio_merger.py    # Programa principal
├── run.bat                  # Script para executar o programa
└── README.md               # Este arquivo
```
## 🚀 Como Usar
### Método 1 - Executar diretamente
```
python video_audio_merger.py
```
### Método 2 - Usar o script batch (Windows)
```
run.bat
```
### Passos na interface:
1. Selecionar arquivo de vídeo :
   
   - Clique em "Procurar" na seção "Arquivo de Vídeo"
   - Escolha seu arquivo de vídeo (sem áudio ou com áudio que será substituído)
2. Selecionar arquivo de áudio :
   
   - Clique em "Procurar" na seção "Arquivo de Áudio"
   - Escolha seu arquivo de áudio ou vídeo (para extrair o áudio)
3. Definir arquivo de saída :
   
   - Clique em "Salvar Como" na seção "Arquivo de Saída"
   - Escolha onde salvar e o nome do arquivo final
4. Processar :
   
   - Clique em "Juntar Vídeo e Áudio"
   - Acompanhe o progresso na barra e na área de status
## 🎯 Formatos Suportados
### Vídeo (Entrada)
- MP4, AVI, MOV, MKV, TS, FLV, WebM, M4V
- Qualquer formato suportado pelo FFmpeg
### Áudio (Entrada)
- Arquivos de áudio : MP3, WAV, AAC, FLAC, OGG, M4A, WMA
- Arquivos de vídeo (para extrair áudio): MP4, AVI, MOV, MKV
- Qualquer formato suportado pelo FFmpeg
### Saída
- MP4 (padrão)
- AVI
- MKV
- Outros formatos suportados pelo FFmpeg
## ⚙️ Configurações do FFmpeg
O programa utiliza as seguintes configurações otimizadas:

- Vídeo : Cópia direta ( -c:v copy ) - sem recodificação para preservar qualidade
- Áudio : Codificação AAC ( -c:a aac ) - compatibilidade universal
- Sincronização : Usa o arquivo mais curto ( -shortest )
- Mapeamento : Primeiro stream de vídeo e primeiro stream de áudio
## 🔧 Funcionalidades Técnicas
### Interface Gráfica
- Framework : tkinter (biblioteca padrão do Python)
- Layout : Grid responsivo
- Componentes : Entry, Button, Progressbar, Text, Scrollbar
- Redimensionamento : Interface adaptável
### Processamento
- Threading : Processamento em thread separada
- Validação : Verificação de existência de arquivos
- Tratamento de erros : Captura e exibição de erros do FFmpeg
- Feedback : Status em tempo real e barra de progresso
### Comando FFmpeg Gerado
```
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 
-map 1:a:0 -shortest -y output.mp4
```
## 🐛 Solução de Problemas
### Erro: "FFmpeg não encontrado"
- Verifique se o FFmpeg está instalado
- Confirme se está no PATH do sistema
- Teste com ffmpeg -version no terminal
### Erro durante o processamento
- Verifique se os arquivos de entrada existem
- Confirme se os formatos são suportados
- Verifique se há espaço suficiente no disco
- Consulte a área de status para detalhes do erro
### Interface não responde
- O processamento roda em thread separada
- Aguarde a conclusão ou verifique a área de status
- Em caso de travamento, feche e reabra o programa
## 📋 Requisitos do Sistema
- Sistema Operacional : Windows, Linux, macOS
- Python : 3.6+
- RAM : Mínimo 512MB
- Espaço em disco : Espaço suficiente para arquivos de entrada e saída
- FFmpeg : Versão recente instalada
## 🤝 Contribuições
Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request
## 📄 Licença
Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

## 🆘 Suporte
Para suporte ou dúvidas:

- Verifique a seção de solução de problemas
- Consulte a documentação do FFmpeg
- Abra uma issue no repositório
Desenvolvido com ❤️ em Python