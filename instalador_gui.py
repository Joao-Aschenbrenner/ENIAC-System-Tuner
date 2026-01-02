"""
INSTALADOR ENIAC SYSTEM TUNER v4.0 - VERSÃO CORRIGIDA
Corrige: Atalhos, executáveis, e instalação completa
"""

import os
import sys
import shutil
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from pathlib import Path
import time
import winreg
import subprocess

def corrigir_tela_preta():
    """Correção para tela preta no Windows"""
    if sys.platform == 'win32':
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

class InstaladorENIAC:
    def __init__(self, root):
        corrigir_tela_preta()
        
        self.root = root
        self.root.title("ENIAC System Tuner - Instalador")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#0f0f0f')
        
        self.pagina_atual = 0
        self.caminho_instalacao = "C:\\Program Files\\ESTU"
        self.criar_atalho_desktop = tk.BooleanVar(value=True)
        self.criar_atalho_menu = tk.BooleanVar(value=True)
        self.instalando = False
        self.aceitar_var = tk.BooleanVar(value=False)
        
        if getattr(sys, 'frozen', False):
            self.pasta_atual = os.path.dirname(sys.executable)
        else:
            self.pasta_atual = os.path.dirname(os.path.abspath(__file__))
        
        self.criar_interface()
        self.mostrar_pagina(0)
        self.centralizar_janela()
    
    def centralizar_janela(self):
        self.root.update_idletasks()
        largura = self.root.winfo_width()
        altura = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)
        self.root.geometry(f'{largura}x{altura}+{x}+{y}')
    
    def criar_interface(self):
        header_frame = tk.Frame(self.root, bg='#1a1a1a', height=120)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        logo_label = tk.Label(header_frame, text="⚡", font=("Segoe UI", 48), bg='#1a1a1a', fg='#00ff88')
        logo_label.place(x=30, y=25)
        
        titulo = tk.Label(header_frame, text="ENIAC SYSTEM TUNER", font=("Segoe UI", 24, "bold"), bg='#1a1a1a', fg='#00ff88')
        titulo.place(x=120, y=30)
        
        subtitulo = tk.Label(header_frame, text="Ultimate Edition v4.0 - Assistente de Instalação", font=("Segoe UI", 11), bg='#1a1a1a', fg='#888888')
        subtitulo.place(x=120, y=70)
        
        self.content_frame = tk.Frame(self.root, bg='#0f0f0f')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def limpar_conteudo(self):
        try:
            for widget in self.content_frame.winfo_children():
                widget.destroy()
        except:
            pass
    
    def mostrar_pagina(self, pagina):
        self.pagina_atual = pagina
        self.limpar_conteudo()
        
        if pagina == 0:
            self.pagina_licenca()
        elif pagina == 1:
            self.pagina_configuracao()
        elif pagina == 2:
            self.pagina_instalacao()
        elif pagina == 3:
            self.pagina_concluido()
    
    def pagina_licenca(self):
        main_frame = tk.Frame(self.content_frame, bg='#0f0f0f')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Bem-vindo ao Instalador", font=("Segoe UI", 20, "bold"), bg='#0f0f0f', fg='#00ff88').pack(pady=(0, 10))
        tk.Label(main_frame, text="ENIAC SYSTEM TUNER ULTIMATE v4.0", font=("Segoe UI", 12), bg='#0f0f0f', fg='#888888').pack(pady=(0, 20))
        
        licenca_frame = tk.Frame(main_frame, bg='#1a1a1a')
        licenca_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        licenca_text = scrolledtext.ScrolledText(licenca_frame, font=("Consolas", 10), bg='#1a1a1a', fg='#ffffff', wrap=tk.WORD, height=12, relief=tk.FLAT)
        licenca_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        texto_licenca = """TERMOS DE LICENÇA - ENIAC SYSTEM TUNER ULTIMATE v4.0

Copyright © 2025 ENIAC System Tuner. Todos os direitos reservados.

LICENÇA DE USO:
Este software é fornecido "como está", sem garantias de qualquer tipo.

PERMISSÕES:
✓ Uso pessoal ilimitado
✓ Instalação em múltiplos computadores pessoais
✓ Criar backups do software

RESTRIÇÕES:
✗ Redistribuição comercial não autorizada
✗ Engenharia reversa do código
✗ Remoção de marcas ou créditos

ISENÇÃO DE RESPONSABILIDADE:
O software executa modificações no sistema operacional.
Recomenda-se criar um ponto de restauração antes de usar."""
        
        licenca_text.insert('1.0', texto_licenca)
        licenca_text.config(state='disabled')
        
        controles_frame = tk.Frame(main_frame, bg='#0f0f0f')
        controles_frame.pack(fill=tk.X, pady=(20, 0))
        
        checkbox_frame = tk.Frame(controles_frame, bg='#0f0f0f')
        checkbox_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.cb_aceitar = tk.Checkbutton(checkbox_frame, text="Eu li e aceito os termos de licença", variable=self.aceitar_var, font=("Segoe UI", 11), bg='#0f0f0f', fg='#ffffff', selectcolor='#1a1a1a', command=self.verificar_aceite)
        self.cb_aceitar.pack(side=tk.LEFT, anchor='w')
        
        botoes_frame = tk.Frame(controles_frame, bg='#0f0f0f')
        botoes_frame.pack(side=tk.RIGHT)
        
        tk.Button(botoes_frame, text="Cancelar", font=("Segoe UI", 11), bg='#ff3366', fg='#ffffff', command=self.root.quit, width=15, height=2).pack(side=tk.LEFT, padx=5)
        
        self.btn_aceitar = tk.Button(botoes_frame, text="Aceitar e Continuar", font=("Segoe UI", 11, "bold"), bg='#666666', fg='#ffffff', command=lambda: self.mostrar_pagina(1), state='disabled', width=15, height=2)
        self.btn_aceitar.pack(side=tk.LEFT, padx=5)
        
        self.verificar_aceite()
    
    def verificar_aceite(self):
        try:
            if self.aceitar_var.get():
                self.btn_aceitar.config(state='normal', bg='#00ff88', fg='#000000', activebackground='#00cc66')
            else:
                self.btn_aceitar.config(state='disabled', bg='#666666', fg='#ffffff', activebackground='#666666')
        except:
            pass
    
    def pagina_configuracao(self):
        main_frame = tk.Frame(self.content_frame, bg='#0f0f0f')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Configurar Instalação", font=("Segoe UI", 20, "bold"), bg='#0f0f0f', fg='#00ff88').pack(pady=(0, 20))
        
        local_frame = tk.LabelFrame(main_frame, text="Local de Instalação", font=("Segoe UI", 12, "bold"), bg='#1a1a1a', fg='#00ff88', padx=15, pady=15)
        local_frame.pack(fill=tk.X, pady=(0, 15))
        
        caminho_frame = tk.Frame(local_frame, bg='#1a1a1a')
        caminho_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.caminho_var = tk.StringVar(value=self.caminho_instalacao)
        
        self.caminho_entry = tk.Entry(caminho_frame, textvariable=self.caminho_var, font=("Segoe UI", 10), bg='#0f0f0f', fg='#ffffff', insertbackground='#ffffff')
        self.caminho_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Button(caminho_frame, text="Procurar", font=("Segoe UI", 9), bg='#00aaff', fg='#ffffff', command=self.escolher_pasta, width=10).pack(side=tk.RIGHT)
        
        tk.Label(local_frame, text="Espaço necessário: ~50 MB", font=("Segoe UI", 9), bg='#1a1a1a', fg='#888888').pack(anchor='w')
        
        opcoes_frame = tk.LabelFrame(main_frame, text="Opções Adicionais", font=("Segoe UI", 12, "bold"), bg='#1a1a1a', fg='#00ff88', padx=15, pady=15)
        opcoes_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Checkbutton(opcoes_frame, text="✓ Criar atalho na Área de Trabalho", variable=self.criar_atalho_desktop, font=("Segoe UI", 10), bg='#1a1a1a', fg='#ffffff', selectcolor='#0f0f0f').pack(anchor='w', pady=3)
        tk.Checkbutton(opcoes_frame, text="✓ Criar atalho no Menu Iniciar", variable=self.criar_atalho_menu, font=("Segoe UI", 10), bg='#1a1a1a', fg='#ffffff', selectcolor='#0f0f0f').pack(anchor='w', pady=3)
        
        tk.Label(main_frame, text="A instalação levará aproximadamente 2-5 minutos", font=("Segoe UI", 10), bg='#0f0f0f', fg='#888888').pack(pady=(0, 30))
        
        botoes_frame = tk.Frame(main_frame, bg='#0f0f0f')
        botoes_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        botoes_container = tk.Frame(botoes_frame, bg='#0f0f0f')
        botoes_container.pack()
        
        tk.Button(botoes_container, text="Voltar", font=("Segoe UI", 11), bg='#3d3d3d', fg='#ffffff', command=lambda: self.mostrar_pagina(0), width=15, height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(botoes_container, text="Cancelar", font=("Segoe UI", 11), bg='#ff3366', fg='#ffffff', command=self.root.quit, width=15, height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(botoes_container, text="Instalar", font=("Segoe UI", 11, "bold"), bg='#00ff88', fg='#000000', command=self.iniciar_instalacao, width=15, height=2).pack(side=tk.LEFT, padx=5)
    
    def iniciar_instalacao(self):
        self.caminho_instalacao = self.caminho_var.get()
        self.mostrar_pagina(2)
    
    def pagina_instalacao(self):
        main_frame = tk.Frame(self.content_frame, bg='#0f0f0f')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Instalando...", font=("Segoe UI", 20, "bold"), bg='#0f0f0f', fg='#00ff88').pack(pady=(0, 20))
        
        self.status_label = tk.Label(main_frame, text="Preparando instalação...", font=("Segoe UI", 12), bg='#0f0f0f', fg='#ffffff')
        self.status_label.pack(pady=(0, 15))
        
        self.progresso = ttk.Progressbar(main_frame, length=700, mode='determinate')
        self.progresso.pack(pady=(0, 10))
        
        self.porcentagem_label = tk.Label(main_frame, text="0%", font=("Segoe UI", 14, "bold"), bg='#0f0f0f', fg='#00ff88')
        self.porcentagem_label.pack(pady=(0, 20))
        
        log_frame = tk.LabelFrame(main_frame, text="Detalhes da Instalação", font=("Segoe UI", 10, "bold"), bg='#1a1a1a', fg='#00ff88', padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.log_texto = scrolledtext.ScrolledText(log_frame, font=("Consolas", 8), bg='#0d0d0d', fg='#00ff88', height=8, relief=tk.FLAT)
        self.log_texto.pack(fill=tk.BOTH, expand=True)
        
        self.btn_cancelar = tk.Button(main_frame, text="Cancelar Instalação", font=("Segoe UI", 11), bg='#ff3366', fg='#ffffff', command=self.cancelar_instalacao, width=20, height=2)
        self.btn_cancelar.pack(pady=(10, 0))
        
        self.instalando = True
        self.thread_instalacao = threading.Thread(target=self.executar_instalacao, daemon=True)
        self.thread_instalacao.start()
    
    def pagina_concluido(self):
        main_frame = tk.Frame(self.content_frame, bg='#0f0f0f')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(main_frame, text="✓", font=("Segoe UI", 72, "bold"), bg='#0f0f0f', fg='#00ff88').pack(pady=(0, 20))
        tk.Label(main_frame, text="Instalação Concluída!", font=("Segoe UI", 20, "bold"), bg='#0f0f0f', fg='#00ff88').pack(pady=(0, 20))
        tk.Label(main_frame, text=f"O ENIAC System Tuner foi instalado em:\n{self.caminho_instalacao}\n\nAtalhos criados com sucesso!", font=("Segoe UI", 11), bg='#0f0f0f', fg='#ffffff', justify=tk.CENTER).pack(pady=(0, 30))
        
        tk.Button(main_frame, text="Concluir", font=("Segoe UI", 12, "bold"), bg='#00ff88', fg='#000000', command=self.root.quit, width=20, height=2).pack()
        
        tk.Label(self.content_frame, text="Execute o ENIAC System Tuner como ADMINISTRADOR", font=("Segoe UI", 10, "italic"), bg='#0f0f0f', fg='#888888').pack(side=tk.BOTTOM, pady=10)
    
    def buscar_arquivos_necessarios(self):
        arquivos_necessarios = ['eniac_tuner.py', 'launcher.py']
        arquivos_encontrados = []
        
        locais_possiveis = [
            self.pasta_atual,
            os.path.join(self.pasta_atual, '..'),
            os.path.join(self.pasta_atual, 'dist'),
            os.getcwd(),
        ]
        
        if getattr(sys, 'frozen', False):
            try:
                base_path = sys._MEIPASS
                locais_possiveis.insert(0, base_path)
            except:
                pass
        
        locais_possiveis.extend([
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'),
        ])
        
        for local in locais_possiveis:
            if not os.path.exists(local):
                continue
                
            for arquivo in arquivos_necessarios:
                caminho_arquivo = os.path.join(local, arquivo)
                if os.path.exists(caminho_arquivo) and arquivo not in [a[0] for a in arquivos_encontrados]:
                    arquivos_encontrados.append((arquivo, caminho_arquivo))
                    self.log(f"✓ Encontrado {arquivo}")
        
        return arquivos_encontrados
    
    def escolher_pasta(self):
        pasta = filedialog.askdirectory(title="Escolher Local de Instalação", initialdir="C:\\Program Files")
        if pasta:
            self.caminho_instalacao = os.path.join(pasta, "ESTU")
            self.caminho_var.set(self.caminho_instalacao)
    
    def cancelar_instalacao(self):
        self.instalando = False
        messagebox.showinfo("Cancelado", "A instalação foi cancelada.")
        self.mostrar_pagina(1)
    
    def atualizar_progresso(self, valor, texto):
        try:
            if hasattr(self, 'progresso') and self.progresso.winfo_exists():
                self.progresso['value'] = valor
                self.porcentagem_label.config(text=f"{int(valor)}%")
                self.status_label.config(text=texto)
                self.root.update_idletasks()
        except:
            pass
    
    def log(self, mensagem):
        try:
            if hasattr(self, 'log_texto') and self.log_texto.winfo_exists():
                self.log_texto.insert(tk.END, f"{mensagem}\n")
                self.log_texto.see(tk.END)
                self.root.update_idletasks()
        except:
            pass
    
    def criar_atalho_windows(self, caminho_destino, nome_atalho, caminho_executavel, descricao="", icone=None):
        """Cria atalho no Windows usando VBScript"""
        try:
            script_vbs = f"""
Set objShell = CreateObject("WScript.Shell")
Set objShortcut = objShell.CreateShortcut("{caminho_destino}\\{nome_atalho}.lnk")
objShortcut.TargetPath = "{caminho_executavel}"
objShortcut.WorkingDirectory = "{os.path.dirname(caminho_executavel)}"
objShortcut.Description = "{descricao}"
objShortcut.WindowStyle = 1
"""
            if icone and os.path.exists(icone):
                script_vbs += f'objShortcut.IconLocation = "{icone}"\n'
            
            script_vbs += "objShortcut.Save\n"
            
            # Salvar script temporário
            script_path = Path(os.environ.get('TEMP')) / "criar_atalho.vbs"
            with open(script_path, 'w') as f:
                f.write(script_vbs)
            
            # Executar script
            subprocess.run(['cscript', '//NoLogo', str(script_path)], 
                         capture_output=True, timeout=10)
            
            # Remover script
            try:
                script_path.unlink()
            except:
                pass
            
            return True
        except Exception as e:
            self.log(f"⚠️ Erro ao criar atalho: {e}")
            return False
    
    def executar_instalacao(self):
        try:
            caminho = self.caminho_instalacao
            
            # 1. Preparar
            self.atualizar_progresso(10, "Preparando instalação...")
            self.log("=" * 50)
            self.log("🚀 INSTALAÇÃO ENIAC SYSTEM TUNER v4.0")
            self.log("=" * 50)
            time.sleep(1)
            
            if not self.instalando:
                return
            
            # 2. Buscar arquivos
            self.atualizar_progresso(20, "Buscando arquivos...")
            arquivos_encontrados = self.buscar_arquivos_necessarios()
            
            if not arquivos_encontrados:
                self.log("❌ ERRO: Arquivos não encontrados!")
                messagebox.showerror("Erro", "Arquivos principais não encontrados!\n\nVerifique se estão na mesma pasta:\n• eniac_tuner.py\n• launcher.py")
                self.mostrar_pagina(1)
                return
            
            # 3. Criar pasta
            self.atualizar_progresso(30, "Criando pasta de instalação...")
            pasta_destino = Path(caminho)
            if pasta_destino.exists():
                try:
                    shutil.rmtree(pasta_destino)
                except:
                    pass
            
            pasta_destino.mkdir(parents=True, exist_ok=True)
            self.log(f"📁 Pasta criada: {caminho}")
            time.sleep(1)
            
            if not self.instalando:
                return
            
            # 4. Copiar arquivos
            self.atualizar_progresso(40, "Copiando arquivos Python...")
            
            for nome_arquivo, caminho_origem in arquivos_encontrados:
                try:
                    destino = pasta_destino / nome_arquivo
                    shutil.copy2(caminho_origem, destino)
                    self.log(f"✓ Copiado: {nome_arquivo}")
                except Exception as e:
                    self.log(f"✗ Erro ao copiar {nome_arquivo}: {e}")
            
            time.sleep(1)
            
            if not self.instalando:
                return
            
            # 5. Criar executável Python melhorado
            self.atualizar_progresso(50, "Criando executável...")
            
            exe_principal = pasta_destino / "ENIAC_Tuner.pyw"
            conteudo_pyw = """import sys
import os
import subprocess

# Garantir que está no diretório correto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Executar o programa principal
try:
    import eniac_tuner
    eniac_tuner.main()
except Exception as e:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Erro", f"Erro ao iniciar ENIAC System Tuner:\\n\\n{e}\\n\\nExecute como ADMINISTRADOR!")
    root.destroy()
"""
            
            with open(exe_principal, 'w', encoding='utf-8') as f:
                f.write(conteudo_pyw)
            
            self.log("✓ Executável Python criado")
            
            # Criar também um .bat de backup
            bat_file = pasta_destino / "ENIAC_Tuner.bat"
            conteudo_bat = f"""@echo off
title ENIAC System Tuner v4.0
cd /d "{pasta_destino}"
pythonw eniac_tuner.py
if errorlevel 1 (
    python eniac_tuner.py
    pause
)
"""
            with open(bat_file, 'w', encoding='utf-8') as f:
                f.write(conteudo_bat)
            
            self.log("✓ Arquivo de inicialização criado")
            
            time.sleep(1)
            
            if not self.instalando:
                return
            
            # 6. Criar atalhos
            self.atualizar_progresso(70, "Criando atalhos...")
            
            # Atalho na Área de Trabalho
            if self.criar_atalho_desktop.get():
                try:
                    desktop = Path.home() / "Desktop"
                    if not desktop.exists():
                        desktop = Path.home() / "OneDrive" / "Desktop"
                    
                    if desktop.exists():
                        sucesso = self.criar_atalho_windows(
                            str(desktop),
                            "ENIAC System Tuner",
                            str(exe_principal),
                            "ENIAC System Tuner Ultimate v4.0 - Otimizador de Sistema"
                        )
                        if sucesso:
                            self.log("✓ Atalho criado na Área de Trabalho")
                        else:
                            self.log("⚠️ Não foi possível criar atalho no desktop")
                except Exception as e:
                    self.log(f"⚠️ Erro ao criar atalho desktop: {e}")
            
            # Atalho no Menu Iniciar
            if self.criar_atalho_menu.get():
                try:
                    menu_iniciar = Path(os.environ.get('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
                    menu_iniciar.mkdir(parents=True, exist_ok=True)
                    
                    sucesso = self.criar_atalho_windows(
                        str(menu_iniciar),
                        "ENIAC System Tuner",
                        str(exe_principal),
                        "ENIAC System Tuner Ultimate v4.0"
                    )
                    if sucesso:
                        self.log("✓ Atalho criado no Menu Iniciar")
                    else:
                        self.log("⚠️ Não foi possível criar atalho no menu")
                except Exception as e:
                    self.log(f"⚠️ Erro ao criar atalho menu: {e}")
            
            time.sleep(1)
            
            if not self.instalando:
                return
            
            # 7. Adicionar ao registro (desinstalador)
            self.atualizar_progresso(85, "Registrando programa...")
            try:
                chave = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\ENIACSystemTuner")
                winreg.SetValueEx(chave, "DisplayName", 0, winreg.REG_SZ, "ENIAC System Tuner Ultimate v4.0")
                winreg.SetValueEx(chave, "DisplayVersion", 0, winreg.REG_SZ, "4.0.0")
                winreg.SetValueEx(chave, "Publisher", 0, winreg.REG_SZ, "ENIAC System Tuner")
                winreg.SetValueEx(chave, "InstallLocation", 0, winreg.REG_SZ, str(pasta_destino))
                winreg.SetValueEx(chave, "DisplayIcon", 0, winreg.REG_SZ, str(exe_principal))
                winreg.CloseKey(chave)
                self.log("✓ Programa registrado no sistema")
            except Exception as e:
                self.log(f"⚠️ Não foi possível registrar: {e}")
            
            # 8. Criar desinstalador
            self.atualizar_progresso(90, "Criando desinstalador...")
            desinstalador = pasta_destino / "Desinstalar.bat"
            conteudo_desinst = f"""@echo off
title Desinstalador ENIAC System Tuner
echo ========================================
echo    DESINSTALADOR ENIAC SYSTEM TUNER
echo ========================================
echo.
echo AVISO: Isso removerá o programa completamente.
echo.
set /p confirm="Digite 'S' para confirmar: "
if /i "%confirm%" neq "S" (
    echo Cancelado.
    pause
    exit
)

echo.
echo Removendo arquivos...
cd /d "{pasta_destino.parent}"
rmdir /s /q "{pasta_destino.name}"

echo Removendo atalhos...
del "%USERPROFILE%\\Desktop\\ENIAC System Tuner.lnk" 2>nul
del "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\ENIAC System Tuner.lnk" 2>nul

echo Removendo registro...
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ENIACSystemTuner" /f 2>nul

echo.
echo Desinstalação concluída!
pause
"""
            with open(desinstalador, 'w', encoding='utf-8') as f:
                f.write(conteudo_desinst)
            
            self.log("✓ Desinstalador criado")
            
            # 9. Finalizar
            self.atualizar_progresso(100, "Instalação concluída!")
            self.log("=" * 50)
            self.log("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
            self.log(f"📁 Local: {pasta_destino}")
            self.log("🎯 Atalhos criados com sucesso")
            self.log("=" * 50)
            
            time.sleep(2)
            
            if self.instalando:
                self.mostrar_pagina(3)
            
        except Exception as e:
            self.log(f"\n❌ ERRO NA INSTALAÇÃO: {str(e)}")
            self.atualizar_progresso(0, "Erro na instalação!")
            
            if self.instalando:
                messagebox.showerror("Erro", f"Erro durante a instalação:\n\n{str(e)}")
                self.mostrar_pagina(1)

def main():
    try:
        if sys.platform == 'win32':
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
        
        root = tk.Tk()
        app = InstaladorENIAC(root)
        root.mainloop()
        
    except Exception as e:
        try:
            tk.Tk().withdraw()
            messagebox.showerror("Erro no Instalador", f"Erro crítico:\n\n{str(e)}")
        except:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()