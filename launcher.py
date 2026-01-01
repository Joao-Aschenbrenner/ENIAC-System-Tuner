"""
ENIAC SYSTEM TUNER ULTIMATE v4.0 - LAUNCHER
Menu principal com interface moderna compatível com v4.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import sys
import platform
import psutil
import ctypes
import threading
from pathlib import Path
from datetime import datetime

class LauncherV4:
    def __init__(self, root):
        self.root = root
        self.root.title("ENIAC SYSTEM TUNER ULTIMATE v4.0 - Launcher")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#0f0f0f')
        
        # Verificar admin
        self.admin = self.is_admin()
        if not self.admin:
            messagebox.showwarning(
                "Aviso - Privilégios",
                "⚠️ Algumas funcionalidades requerem privilégios de administrador.\n\n"
                "Para melhor experiência:\n"
                "• Clique direito no programa\n"
                "• Selecione 'Executar como administrador'"
            )
        
        self.criar_interface()
        self.iniciar_monitoramento()
        self.centralizar_janela()
    
    def is_admin(self):
        """Verifica se está rodando como administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def centralizar_janela(self):
        """Centraliza janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def criar_interface(self):
        """Cria interface moderna estilo v4.0"""
        
        # Header moderno
        header_frame = tk.Frame(self.root, bg='#1a1a1a', height=130)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo e título
        logo_container = tk.Frame(header_frame, bg='#1a1a1a')
        logo_container.pack(expand=True)
        
        logo = tk.Label(
            logo_container,
            text="⚡",
            font=("Segoe UI", 48),
            bg='#1a1a1a',
            fg='#00ff88'
        )
        logo.pack()
        
        titulo = tk.Label(
            logo_container,
            text="ENIAC SYSTEM TUNER ULTIMATE",
            font=("Segoe UI", 22, "bold"),
            bg='#1a1a1a',
            fg='#00ff88'
        )
        titulo.pack()
        
        versao = tk.Label(
            logo_container,
            text="v4.0 Ultimate Edition • Launcher",
            font=("Segoe UI", 10),
            bg='#1a1a1a',
            fg='#888888'
        )
        versao.pack()
        
        # Container principal
        main_container = tk.Frame(self.root, bg='#0f0f0f')
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Card de boas-vindas
        welcome_card = tk.Frame(main_container, bg='#1a1a1a', relief=tk.FLAT, bd=0)
        welcome_card.pack(fill=tk.X, pady=(0, 20))
        
        welcome_text = tk.Label(
            welcome_card,
            text=f"👋 Bem-vindo ao ENIAC System Tuner!\n\n"
                 f"Sistema: {platform.system()} {platform.release()}\n"
                 f"Privilégios: {'✅ Administrador' if self.admin else '⚠️ Usuário Normal'}",
            font=("Segoe UI", 11),
            bg='#1a1a1a',
            fg='#ffffff',
            justify=tk.LEFT
        )
        welcome_text.pack(padx=20, pady=15)
        
        # Grid de botões principais
        buttons_grid = tk.Frame(main_container, bg='#0f0f0f')
        buttons_grid.pack(expand=True)
        
        botoes = [
            ("⚡ OTIMIZAÇÃO\nCOMPLETA", self.abrir_otimizador, '#00ff88', 
             "Inicia o otimizador completo do sistema"),
            ("🔍 DIAGNÓSTICO\nRÁPIDO", self.diagnostico_rapido, '#00aaff',
             "Análise rápida do estado do sistema"),
            ("📊 RELATÓRIO\nDETALHADO", self.gerar_relatorio, '#ff9900',
             "Gera relatório completo do hardware"),
            ("🛠️ FERRAMENTAS\nDO SISTEMA", self.abrir_ferramentas, '#ff3366',
             "Acesso rápido às ferramentas do Windows"),
        ]
        
        for i, (texto, comando, cor, desc) in enumerate(botoes):
            # Container do botão
            btn_container = tk.Frame(buttons_grid, bg='#0f0f0f')
            btn_container.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew')
            
            # Botão principal
            btn = tk.Button(
                btn_container,
                text=texto,
                font=("Segoe UI", 13, "bold"),
                bg=cor,
                fg='#000000' if cor == '#00ff88' else '#ffffff',
                activebackground=self.escurecer_cor(cor),
                command=comando,
                relief=tk.FLAT,
                bd=0,
                width=20,
                height=4,
                cursor='hand2'
            )
            btn.pack()
            
            # Descrição
            desc_label = tk.Label(
                btn_container,
                text=desc,
                font=("Segoe UI", 8),
                bg='#0f0f0f',
                fg='#666666'
            )
            desc_label.pack(pady=(5, 0))
        
        buttons_grid.grid_rowconfigure(0, weight=1)
        buttons_grid.grid_rowconfigure(1, weight=1)
        buttons_grid.grid_columnconfigure(0, weight=1)
        buttons_grid.grid_columnconfigure(1, weight=1)
        
        # Card de informações do sistema
        info_card = tk.LabelFrame(
            main_container,
            text="💻 INFORMAÇÕES DO SISTEMA",
            font=("Segoe UI", 11, "bold"),
            bg='#1a1a1a',
            fg='#00ff88',
            bd=0
        )
        info_card.pack(fill=tk.X, pady=(20, 0))
        
        self.info_label = tk.Label(
            info_card,
            text=self.get_system_info(),
            font=("Consolas", 9),
            bg='#1a1a1a',
            fg='#ffffff',
            justify=tk.LEFT,
            anchor='w'
        )
        self.info_label.pack(padx=15, pady=10, fill=tk.X)
        
        # Status bar moderno
        self.status_bar = tk.Frame(self.root, bg='#1a1a1a', height=30)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_left = tk.Label(
            self.status_bar,
            text="● Sistema Pronto",
            font=("Segoe UI", 9),
            bg='#1a1a1a',
            fg='#00ff88',
            anchor='w',
            padx=10
        )
        self.status_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.status_right = tk.Label(
            self.status_bar,
            text="",
            font=("Consolas", 9),
            bg='#1a1a1a',
            fg='#888888',
            anchor='e',
            padx=10
        )
        self.status_right.pack(side=tk.RIGHT)
    
    def escurecer_cor(self, cor_hex):
        """Escurece uma cor para efeito hover"""
        try:
            cor_hex = cor_hex.lstrip('#')
            r = int(cor_hex[0:2], 16)
            g = int(cor_hex[2:4], 16)
            b = int(cor_hex[4:6], 16)
            r = max(0, int(r * 0.8))
            g = max(0, int(g * 0.8))
            b = max(0, int(b * 0.8))
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return cor_hex
    
    def get_system_info(self):
        """Obtém informações do sistema"""
        try:
            cpu_name = platform.processor()
            if len(cpu_name) > 50:
                cpu_name = cpu_name[:50] + "..."
            
            ram = psutil.virtual_memory()
            ram_gb = ram.total / (1024**3)
            
            disk = psutil.disk_usage('C:')
            disk_free = disk.free / (1024**3)
            disk_total = disk.total / (1024**3)
            
            info = f"CPU: {cpu_name}\n"
            info += f"RAM: {ram_gb:.1f} GB (Uso: {ram.percent}%)\n"
            info += f"Disco C: {disk_free:.1f}/{disk_total:.1f} GB livres ({disk.percent}% usado)"
            
            return info
        except:
            return "Informações não disponíveis"
    
    def abrir_otimizador(self):
        """Abre o otimizador principal v4.0"""
        self.status_left.config(text="● Abrindo otimizador...", fg='#ff9900')
        self.root.update()
        
        # Caminhos possíveis
        caminhos = [
            Path("eniac_tuner.exe"),
            Path("ENIAC_Tuner.exe"),
            Path("dist/ENIAC_Tuner.exe"),
            Path("C:/Program Files/ESTU/ENIAC_Tuner.exe"),
            Path(__file__).parent / "ENIAC_Tuner.exe",
            Path(sys.executable).parent / "ENIAC_Tuner.exe",
        ]
        
        # Tentar encontrar executável
        otimizador = None
        for caminho in caminhos:
            if caminho.exists():
                otimizador = caminho
                break
        
        if otimizador:
            try:
                subprocess.Popen([str(otimizador)])
                self.status_left.config(text="● Otimizador iniciado!", fg='#00ff88')
                messagebox.showinfo(
                    "Otimizador Iniciado",
                    "✅ O ENIAC System Tuner v4.0 foi aberto!\n\n"
                    "Execute-o como administrador para\n"
                    "acessar todas as funcionalidades."
                )
            except Exception as e:
                self.status_left.config(text="● Erro ao abrir otimizador", fg='#ff3366')
                messagebox.showerror("Erro", f"Erro ao abrir otimizador:\n{e}")
        else:
            self.status_left.config(text="● Otimizador não encontrado", fg='#ff3366')
            messagebox.showerror(
                "Otimizador Não Encontrado",
                "❌ ENIAC_Tuner.exe não foi encontrado!\n\n"
                "Verifique se o programa está instalado:\n"
                "• C:\\Program Files\\ESTU\\ENIAC_Tuner.exe\n\n"
                "Ou execute este launcher da mesma pasta\n"
                "onde está o ENIAC_Tuner.exe"
            )
    
    def diagnostico_rapido(self):
        """Executa diagnóstico rápido"""
        self.status_left.config(text="● Executando diagnóstico...", fg='#00aaff')
        
        janela = tk.Toplevel(self.root)
        janela.title("Diagnóstico Rápido - ENIAC v4.0")
        janela.geometry("700x550")
        janela.configure(bg='#0f0f0f')
        janela.transient(self.root)
        
        # Header
        header = tk.Frame(janela, bg='#1a1a1a')
        header.pack(fill=tk.X)
        
        titulo = tk.Label(
            header,
            text="🔍 DIAGNÓSTICO RÁPIDO DO SISTEMA",
            font=("Segoe UI", 14, "bold"),
            bg='#1a1a1a',
            fg='#00aaff'
        )
        titulo.pack(pady=15)
        
        # Área de texto
        text_area = scrolledtext.ScrolledText(
            janela,
            font=("Consolas", 10),
            bg='#0d0d0d',
            fg='#00aaff',
            wrap=tk.WORD,
            relief=tk.FLAT,
            insertbackground='#00aaff'
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Executar diagnóstico em thread
        def executar():
            text_area.insert('1.0', "⏳ Analisando sistema...\n\n")
            janela.update()
            
            diag = self.coletar_diagnostico()
            text_area.delete('1.0', tk.END)
            text_area.insert('1.0', diag)
            text_area.configure(state='disabled')
            
            self.status_left.config(text="● Diagnóstico concluído", fg='#00ff88')
        
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
        
        # Botão salvar
        btn_salvar = tk.Button(
            janela,
            text="💾 SALVAR RELATÓRIO",
            font=("Segoe UI", 10, "bold"),
            bg='#00aaff',
            fg='#ffffff',
            command=lambda: self.salvar_diagnostico(text_area.get('1.0', tk.END)),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        btn_salvar.pack(pady=15)
    
    def coletar_diagnostico(self):
        """Coleta informações para diagnóstico"""
        diag = "=" * 70 + "\n"
        diag += "DIAGNÓSTICO RÁPIDO - ENIAC SYSTEM TUNER v4.0\n"
        diag += "=" * 70 + "\n"
        diag += f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        diag += "=" * 70 + "\n\n"
        
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            
            diag += "[PROCESSADOR]\n"
            diag += f"  Modelo: {platform.processor()}\n"
            diag += f"  Núcleos: {psutil.cpu_count(logical=False)} físicos, {psutil.cpu_count(logical=True)} lógicos\n"
            diag += f"  Frequência: {cpu_freq.current:.0f} MHz\n" if cpu_freq else "  Frequência: N/A\n"
            diag += f"  Uso Atual: {cpu_percent}%\n"
            if cpu_percent >= 80:
                diag += "  ⚠️ AVISO: CPU sob carga elevada!\n"
            diag += "\n"
            
            # Memória
            mem = psutil.virtual_memory()
            diag += "[MEMÓRIA RAM]\n"
            diag += f"  Total: {mem.total / (1024**3):.2f} GB\n"
            diag += f"  Disponível: {mem.available / (1024**3):.2f} GB\n"
            diag += f"  Em Uso: {mem.used / (1024**3):.2f} GB ({mem.percent}%)\n"
            if mem.percent >= 80:
                diag += "  ⚠️ AVISO: Memória acima de 80%!\n"
            diag += "\n"
            
            # Discos
            diag += "[ARMAZENAMENTO]\n"
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    diag += f"  {partition.device}\n"
                    diag += f"    Total: {usage.total / (1024**3):.2f} GB\n"
                    diag += f"    Livre: {usage.free / (1024**3):.2f} GB\n"
                    diag += f"    Uso: {usage.percent}%\n"
                    if usage.percent >= 90:
                        diag += "    ⚠️ CRÍTICO: Disco quase cheio!\n"
                    elif usage.percent >= 80:
                        diag += "    ⚠️ AVISO: Espaço limitado!\n"
                except:
                    pass
            diag += "\n"
            
            # Processos
            diag += "[PROCESSOS]\n"
            diag += f"  Total de processos: {len(psutil.pids())}\n\n"
            
            # Status geral
            diag += "[STATUS GERAL]\n"
            problemas = []
            if cpu_percent >= 80:
                problemas.append("CPU acima de 80%")
            if mem.percent >= 80:
                problemas.append("Memória acima de 80%")
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    if usage.percent >= 80:
                        problemas.append(f"Disco {partition.device} acima de 80%")
                except:
                    pass
            
            if not problemas:
                diag += "  ✅ Sistema operando normalmente\n"
                diag += "  Todos os componentes dentro dos limites normais\n"
            else:
                diag += "  ⚠️ Problemas detectados:\n"
                for problema in problemas:
                    diag += f"    • {problema}\n"
                diag += "\n  💡 Recomendação: Execute a otimização completa\n"
            
        except Exception as e:
            diag += f"\n❌ Erro ao coletar diagnóstico: {e}\n"
        
        diag += "\n" + "=" * 70 + "\n"
        diag += "Relatório gerado pelo ENIAC System Tuner v4.0\n"
        diag += "=" * 70
        
        return diag
    
    def abrir_ferramentas(self):
        """Abre menu de ferramentas"""
        self.status_left.config(text="● Ferramentas disponíveis", fg='#ff3366')
        
        janela = tk.Toplevel(self.root)
        janela.title("Ferramentas do Sistema - ENIAC v4.0")
        janela.geometry("600x550")
        janela.configure(bg='#0f0f0f')
        janela.transient(self.root)
        
        # Header
        header = tk.Frame(janela, bg='#1a1a1a')
        header.pack(fill=tk.X)
        
        titulo = tk.Label(
            header,
            text="🛠️ FERRAMENTAS DO SISTEMA",
            font=("Segoe UI", 14, "bold"),
            bg='#1a1a1a',
            fg='#ff3366'
        )
        titulo.pack(pady=15)
        
        # Scroll area
        canvas = tk.Canvas(janela, bg='#0f0f0f', highlightthickness=0)
        scrollbar = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#0f0f0f')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Ferramentas
        ferramentas = [
            ("🗑️ Limpeza de Disco", "cleanmgr", '#00aaff'),
            ("💿 Desfragmentador", "dfrgui", '#ff9900'),
            ("📊 Gerenciador de Tarefas", "taskmgr", '#ff3366'),
            ("📈 Monitor de Recursos", "resmon", '#9900ff'),
            ("ℹ️ Informações do Sistema", "msinfo32", '#00ff88'),
            ("🔧 Editor de Registro", "regedit", '#ff0066'),
            ("🌐 Configurações de Rede", "ncpa.cpl", '#0099ff'),
            ("⚙️ Serviços do Windows", "services.msc", '#ff9900'),
            ("💾 Gerenciamento de Disco", "diskmgmt.msc", '#00aaff'),
            ("🖥️ Gerenciador de Dispositivos", "devmgmt.msc", '#9900ff'),
        ]
        
        for texto, comando, cor in ferramentas:
            btn = tk.Button(
                scrollable_frame,
                text=texto,
                font=("Segoe UI", 11, "bold"),
                bg=cor,
                fg='#ffffff',
                command=lambda cmd=comando, txt=texto: self.executar_ferramenta(cmd, txt),
                relief=tk.FLAT,
                width=40,
                height=2,
                cursor='hand2'
            )
            btn.pack(pady=8, padx=20)
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y", pady=15)
    
    def executar_ferramenta(self, comando, nome):
        """Executa ferramenta do Windows"""
        try:
            os.system(comando)
            self.status_left.config(text=f"● {nome} aberto", fg='#00ff88')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir {nome}:\n{e}")
    
    def gerar_relatorio(self):
        """Gera relatório detalhado"""
        self.status_left.config(text="● Gerando relatório...", fg='#ff9900')
        
        janela = tk.Toplevel(self.root)
        janela.title("Relatório Detalhado - ENIAC v4.0")
        janela.geometry("800x650")
        janela.configure(bg='#0f0f0f')
        janela.transient(self.root)
        
        # Header
        header = tk.Frame(janela, bg='#1a1a1a')
        header.pack(fill=tk.X)
        
        titulo = tk.Label(
            header,
            text="📊 RELATÓRIO DETALHADO DO SISTEMA",
            font=("Segoe UI", 14, "bold"),
            bg='#1a1a1a',
            fg='#ff9900'
        )
        titulo.pack(pady=15)
        
        # Área de texto
        text_area = scrolledtext.ScrolledText(
            janela,
            font=("Consolas", 9),
            bg='#0d0d0d',
            fg='#ff9900',
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Gerar relatório
        relatorio = self.gerar_relatorio_completo()
        text_area.insert('1.0', relatorio)
        text_area.configure(state='disabled')
        
        self.status_left.config(text="● Relatório gerado", fg='#00ff88')
        
        # Botão salvar
        btn_salvar = tk.Button(
            janela,
            text="💾 SALVAR RELATÓRIO",
            font=("Segoe UI", 10, "bold"),
            bg='#ff9900',
            fg='#ffffff',
            command=lambda: self.salvar_diagnostico(relatorio),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        btn_salvar.pack(pady=15)
    
    def gerar_relatorio_completo(self):
        """Gera relatório completo"""
        rel = "=" * 80 + "\n"
        rel += "RELATÓRIO DETALHADO DO SISTEMA - ENIAC SYSTEM TUNER v4.0\n"
        rel += "=" * 80 + "\n"
        rel += f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        rel += "=" * 80 + "\n\n"
        
        try:
            # Sistema
            rel += "[SISTEMA OPERACIONAL]\n"
            rel += f"  Nome: {platform.system()}\n"
            rel += f"  Versão: {platform.version()}\n"
            rel += f"  Release: {platform.release()}\n"
            rel += f"  Arquitetura: {platform.machine()}\n"
            rel += f"  Processador: {platform.processor()}\n\n"
            
            # CPU
            rel += "[PROCESSADOR]\n"
            rel += f"  Núcleos Físicos: {psutil.cpu_count(logical=False)}\n"
            rel += f"  Núcleos Lógicos: {psutil.cpu_count(logical=True)}\n"
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                rel += f"  Frequência Atual: {cpu_freq.current:.0f} MHz\n"
                rel += f"  Frequência Mínima: {cpu_freq.min:.0f} MHz\n"
                rel += f"  Frequência Máxima: {cpu_freq.max:.0f} MHz\n"
            rel += f"  Uso Atual: {psutil.cpu_percent(interval=1)}%\n\n"
            
            # Memória
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            rel += "[MEMÓRIA]\n"
            rel += f"  RAM Total: {mem.total / (1024**3):.2f} GB\n"
            rel += f"  RAM Disponível: {mem.available / (1024**3):.2f} GB\n"
            rel += f"  RAM Em Uso: {mem.used / (1024**3):.2f} GB ({mem.percent}%)\n"
            rel += f"  SWAP Total: {swap.total / (1024**3):.2f} GB\n"
            rel += f"  SWAP Usado: {swap.used / (1024**3):.2f} GB ({swap.percent}%)\n\n"
            
            # Discos
            rel += "[DISCOS]\n"
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    rel += f"  {partition.device}\n"
                    rel += f"    Ponto de Montagem: {partition.mountpoint}\n"
                    rel += f"    Tipo: {partition.fstype}\n"
                    rel += f"    Total: {usage.total / (1024**3):.2f} GB\n"
                    rel += f"    Usado: {usage.used / (1024**3):.2f} GB\n"
                    rel += f"    Livre: {usage.free / (1024**3):.2f} GB\n"
                    rel += f"    Uso: {usage.percent}%\n\n"
                except:
                    pass
            
            # Rede
            net = psutil.net_io_counters()
            rel += "[REDE]\n"
            rel += f"  Bytes Enviados: {net.bytes_sent / (1024**2):.2f} MB\n"
            rel += f"  Bytes Recebidos: {net.bytes_recv / (1024**2):.2f} MB\n"
            rel += f"  Pacotes Enviados: {net.packets_sent}\n"
            rel += f"  Pacotes Recebidos: {net.packets_recv}\n\n"
            
            # Processos
            rel += "[PROCESSOS]\n"
            rel += f"  Total: {len(psutil.pids())}\n"
            rel += f"\n  Top 10 por uso de CPU:\n"
            
            processos = []
            for proc in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    processos.append((proc.info['name'], proc.info['cpu_percent']))
                except:
                    pass
            
            processos.sort(key=lambda x: x[1], reverse=True)
            for i, (nome, cpu) in enumerate(processos[:10], 1):
                rel += f"    {i}. {nome}: {cpu}%\n"
            
        except Exception as e:
            rel += f"\n❌ Erro ao gerar relatório: {e}\n"
        
        rel += "\n" + "=" * 80 + "\n"
        rel += "Relatório gerado pelo ENIAC System Tuner Ultimate v4.0\n"
        rel += "=" * 80
        
        return rel
    
    def salvar_diagnostico(self, conteudo):
        """Salva diagnóstico/relatório"""
        try:
            # Tentar diferentes caminhos para Desktop
            desktops = [
                Path.home() / "Desktop",
                Path.home() / "OneDrive" / "Desktop",
                Path.home() / "OneDrive" / "Área de Trabalho",
                Path.home()
            ]
            
            desktop = None
            for d in desktops:
                if d.exists():
                    desktop = d
                    break
            
            if not desktop:
                desktop = Path.home()
            
            # Nome do arquivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            arquivo = desktop / f"ENIAC_Relatorio_{timestamp}.txt"
            
            # Salvar
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            
            messagebox.showinfo(
                "Relatório Salvo",
                f"✅ Relatório salvo com sucesso!\n\n{arquivo}"
            )
            
            self.status_left.config(text="● Relatório salvo", fg='#00ff88')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar relatório:\n{e}")
    
    def iniciar_monitoramento(self):
        """Atualiza informações periodicamente"""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory()
            
            status = f"CPU: {cpu:.1f}% | RAM: {ram.percent:.1f}% | "
            status += f"Admin: {'✅' if self.admin else '⚠️'}"
            
            self.status_right.config(text=status)
            
            # Atualizar info card
            self.info_label.config(text=self.get_system_info())
            
        except:
            pass
        
        # Atualizar a cada 3 segundos
        self.root.after(3000, self.iniciar_monitoramento)

def main():
    root = tk.Tk()
    app = LauncherV4(root)
    root.mainloop()

if __name__ == "__main__":
    main()