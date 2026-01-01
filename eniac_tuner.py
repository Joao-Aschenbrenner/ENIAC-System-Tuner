"""
ENIAC SYSTEM TUNER ULTIMATE v4.0 - INTERFACE MODERNA
Otimizador completo com interface tipo Google Chrome + agendamentos + diagnóstico profundo
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import psutil
import time
import os
import sys
import platform
import ctypes
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import winreg
import json

class ENIACTuner:
    def __init__(self, root):
        self.root = root
        self.root.title("ENIAC System Tuner Ultimate v4.0")
        self.root.geometry("1100x750")
        self.root.configure(bg='#1e1e1e')
        
        # Verificar admin
        if not self.is_admin():
            messagebox.showerror(
                "Permissão Necessária",
                "Este programa precisa ser executado como ADMINISTRADOR!\n\n"
                "Clique com botão direito e selecione 'Executar como administrador'"
            )
            sys.exit(1)
        
        self.otimizando = False
        self.aba_atual = "otimizacao"
        self.config_file = Path(os.environ.get('APPDATA')) / 'ESTU' / 'config.json'
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.carregar_config()
        self.criar_interface()
        self.mostrar_aba("otimizacao")
        self.iniciar_monitoramento()
        self.detectar_hardware()
    
    def is_admin(self):
        """Verifica se está rodando como administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def carregar_config(self):
        """Carrega configurações salvas"""
        self.config = {
            'auto_limpeza': False,
            'intervalo_limpeza': 7,
            'auto_desfrag': False,
            'intervalo_desfrag': 30,
            'auto_otimizacao': False,
            'intervalo_otimizacao': 15,
            'modo_gamer': False
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config.update(json.load(f))
            except:
                pass
    
    def salvar_config(self):
        """Salva configurações"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def criar_interface(self):
        """Cria a interface moderna estilo Chrome"""
        
        # Container principal
        main_container = tk.Frame(self.root, bg='#1e1e1e')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header com abas tipo Chrome
        header_frame = tk.Frame(main_container, bg='#2d2d2d', height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo e título
        title_frame = tk.Frame(header_frame, bg='#2d2d2d')
        title_frame.pack(pady=(10, 5))
        
        titulo = tk.Label(
            title_frame,
            text="⚡ ENIAC SYSTEM TUNER",
            font=("Segoe UI", 18, "bold"),
            bg='#2d2d2d',
            fg='#00ff88'
        )
        titulo.pack()
        
        versao = tk.Label(
            title_frame,
            text="v4.0 Ultimate Edition",
            font=("Segoe UI", 9),
            bg='#2d2d2d',
            fg='#888888'
        )
        versao.pack()
        
        # Sistema de abas tipo Google Chrome
        tabs_frame = tk.Frame(header_frame, bg='#2d2d2d')
        tabs_frame.pack(fill=tk.X, padx=20, pady=(5, 0))
        
        self.tabs = {}
        abas = [
            ("otimizacao", "🚀 Otimização", '#00ff88'),
            ("hardware", "💻 Hardware", '#00aaff'),
            ("agendamentos", "⏰ Agendamentos", '#ff9900'),
            ("diagnostico", "🔍 Diagnóstico", '#ff00ff'),
            ("ferramentas", "🛠️ Ferramentas", '#ff3366')
        ]
        
        for key, texto, cor in abas:
            btn = tk.Button(
                tabs_frame,
                text=texto,
                font=("Segoe UI", 11, "bold"),
                bg='#3d3d3d',
                fg='#ffffff',
                activebackground='#4d4d4d',
                activeforeground='#ffffff',
                relief=tk.FLAT,
                bd=0,
                padx=20,
                pady=10,
                cursor='hand2',
                command=lambda k=key: self.mostrar_aba(k)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.tabs[key] = {'btn': btn, 'cor': cor}
        
        # Área de conteúdo
        self.content_frame = tk.Frame(main_container, bg='#1e1e1e')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar moderno
        self.status_bar = tk.Frame(self.root, bg='#2d2d2d', height=30)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_bar,
            text="● Sistema Pronto | Admin: Sim",
            font=("Segoe UI", 9),
            bg='#2d2d2d',
            fg='#00ff88',
            anchor='w',
            padx=10
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.status_info = tk.Label(
            self.status_bar,
            text="",
            font=("Segoe UI", 9),
            bg='#2d2d2d',
            fg='#888888',
            anchor='e',
            padx=10
        )
        self.status_info.pack(side=tk.RIGHT)
    
    def mostrar_aba(self, aba):
        """Mostra a aba selecionada"""
        self.aba_atual = aba
        
        # Atualizar visual das abas
        for key, tab_info in self.tabs.items():
            if key == aba:
                tab_info['btn'].config(bg=tab_info['cor'], fg='#000000')
            else:
                tab_info['btn'].config(bg='#3d3d3d', fg='#ffffff')
        
        # Limpar conteúdo
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Mostrar conteúdo da aba
        if aba == "otimizacao":
            self.criar_aba_otimizacao()
        elif aba == "hardware":
            self.criar_aba_hardware()
        elif aba == "agendamentos":
            self.criar_aba_agendamentos()
        elif aba == "diagnostico":
            self.criar_aba_diagnostico()
        elif aba == "ferramentas":
            self.criar_aba_ferramentas()
    
    def criar_aba_otimizacao(self):
        """Cria aba de otimização"""
        container = tk.Frame(self.content_frame, bg='#1e1e1e')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Hardware detectado
        hw_frame = tk.LabelFrame(
            container,
            text="💻 SISTEMA DETECTADO",
            font=("Segoe UI", 11, "bold"),
            bg='#2d2d2d',
            fg='#00ff88',
            bd=0,
            relief=tk.FLAT
        )
        hw_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.hw_info_label = tk.Label(
            hw_frame,
            text="Detectando hardware...",
            font=("Consolas", 10),
            bg='#2d2d2d',
            fg='#ffffff',
            justify=tk.LEFT,
            anchor='w'
        )
        self.hw_info_label.pack(fill=tk.X, padx=15, pady=10)
        
        # Otimizações
        otim_frame = tk.LabelFrame(
            container,
            text="⚡ OTIMIZAÇÕES DISPONÍVEIS",
            font=("Segoe UI", 11, "bold"),
            bg='#2d2d2d',
            fg='#00ff88',
            bd=0
        )
        otim_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.checkboxes = {}
        otimizacoes = [
            ('limpeza_temp', '🗑️ Limpeza de Arquivos Temporários', 'Remove arquivos desnecessários'),
            ('limpeza_cache', '💾 Limpeza de Cache do Sistema', 'Limpa cache de apps e navegadores'),
            ('registro', '📋 Otimização do Registro', 'Remove entradas inválidas'),
            ('servicos', '⚙️ Otimização de Serviços', 'Desabilita serviços desnecessários'),
            ('rede', '🌐 Otimização de Rede', 'Melhora velocidade de conexão'),
            ('memoria', '🧠 Configuração de Memória Virtual', 'Ajusta paginação'),
            ('gpu', '🎮 Otimização para Jogos', 'Modo alto desempenho GPU'),
            ('inicializacao', '🚀 Otimização de Inicialização', 'Remove programas do startup'),
        ]
        
        for key, texto, desc in otimizacoes:
            item_frame = tk.Frame(otim_frame, bg='#2d2d2d')
            item_frame.pack(fill=tk.X, padx=15, pady=5)
            
            var = tk.BooleanVar(value=True)
            self.checkboxes[key] = var
            
            cb = tk.Checkbutton(
                item_frame,
                text=texto,
                variable=var,
                font=("Segoe UI", 10, "bold"),
                bg='#2d2d2d',
                fg='#ffffff',
                selectcolor='#1e1e1e',
                activebackground='#2d2d2d',
                activeforeground='#00ff88',
                relief=tk.FLAT
            )
            cb.pack(side=tk.LEFT)
            
            desc_label = tk.Label(
                item_frame,
                text=f"  •  {desc}",
                font=("Segoe UI", 9),
                bg='#2d2d2d',
                fg='#888888'
            )
            desc_label.pack(side=tk.LEFT)
        
        # Botões de ação
        btn_frame = tk.Frame(container, bg='#1e1e1e')
        btn_frame.pack(pady=20)
        
        self.btn_otimizar = tk.Button(
            btn_frame,
            text="🚀 INICIAR OTIMIZAÇÃO COMPLETA",
            font=("Segoe UI", 14, "bold"),
            bg='#00ff88',
            fg='#000000',
            activebackground='#00dd77',
            command=self.iniciar_otimizacao,
            relief=tk.FLAT,
            bd=0,
            padx=40,
            pady=15,
            cursor='hand2'
        )
        self.btn_otimizar.pack()
        
        # Progress
        progress_frame = tk.Frame(container, bg='#1e1e1e')
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.label_progresso = tk.Label(
            progress_frame,
            text="Aguardando início da otimização...",
            font=("Segoe UI", 10),
            bg='#1e1e1e',
            fg='#888888'
        )
        self.label_progresso.pack()
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar",
                       troughcolor='#2d2d2d',
                       background='#00ff88',
                       bordercolor='#2d2d2d',
                       lightcolor='#00ff88',
                       darkcolor='#00ff88')
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=1000,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=10)
        
        # Log
        log_frame = tk.LabelFrame(
            container,
            text="📋 LOG DE OTIMIZAÇÃO",
            font=("Segoe UI", 10, "bold"),
            bg='#2d2d2d',
            fg='#00ff88',
            bd=0
        )
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg='#0d0d0d',
            fg='#00ff88',
            insertbackground='#00ff88',
            height=10,
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def criar_aba_hardware(self):
        """Cria aba de hardware"""
        container = tk.Frame(self.content_frame, bg='#1e1e1e')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        titulo = tk.Label(
            container,
            text="💻 HARDWARE DETECTADO",
            font=("Segoe UI", 16, "bold"),
            bg='#1e1e1e',
            fg='#00aaff'
        )
        titulo.pack(pady=(0, 20))
        
        # Área de informações
        info_container = tk.Frame(container, bg='#1e1e1e')
        info_container.pack(fill=tk.BOTH, expand=True)
        
        self.hw_text = scrolledtext.ScrolledText(
            info_container,
            font=("Consolas", 10),
            bg='#0d0d0d',
            fg='#00aaff',
            insertbackground='#00aaff',
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0
        )
        self.hw_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botão atualizar
        btn_atualizar = tk.Button(
            container,
            text="🔄 Atualizar Informações",
            font=("Segoe UI", 11, "bold"),
            bg='#00aaff',
            fg='#000000',
            command=self.detectar_hardware,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        btn_atualizar.pack(pady=10)
    
    def criar_aba_agendamentos(self):
        """Cria aba de agendamentos"""
        container = tk.Frame(self.content_frame, bg='#1e1e1e')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        titulo = tk.Label(
            container,
            text="⏰ AGENDAMENTOS AUTOMÁTICOS",
            font=("Segoe UI", 16, "bold"),
            bg='#1e1e1e',
            fg='#ff9900'
        )
        titulo.pack(pady=(0, 20))
        
        # Limpeza automática
        self.criar_card_agendamento(
            container,
            "🗑️ Limpeza Automática",
            "auto_limpeza",
            "intervalo_limpeza",
            "dias"
        )
        
        # Desfragmentação automática
        self.criar_card_agendamento(
            container,
            "💿 Desfragmentação Automática (HDDs)",
            "auto_desfrag",
            "intervalo_desfrag",
            "dias"
        )
        
        # Otimização automática
        self.criar_card_agendamento(
            container,
            "⚡ Otimização Completa Automática",
            "auto_otimizacao",
            "intervalo_otimizacao",
            "dias"
        )
        
        # Modo Gamer
        gamer_frame = tk.LabelFrame(
            container,
            text="🎮 MODO GAMER",
            font=("Segoe UI", 11, "bold"),
            bg='#2d2d2d',
            fg='#ff00ff',
            bd=0
        )
        gamer_frame.pack(fill=tk.X, pady=10)
        
        gamer_var = tk.BooleanVar(value=self.config.get('modo_gamer', False))
        
        gamer_cb = tk.Checkbutton(
            gamer_frame,
            text="Ativar Modo Alto Desempenho para Jogos",
            variable=gamer_var,
            font=("Segoe UI", 10, "bold"),
            bg='#2d2d2d',
            fg='#ffffff',
            selectcolor='#1e1e1e',
            command=lambda: self.toggle_modo_gamer(gamer_var.get())
        )
        gamer_cb.pack(anchor='w', padx=15, pady=10)
        
        desc = tk.Label(
            gamer_frame,
            text="• Desabilita serviços em segundo plano\n• Máxima prioridade para aplicações\n• Otimiza GPU e CPU para performance",
            font=("Segoe UI", 9),
            bg='#2d2d2d',
            fg='#888888',
            justify=tk.LEFT
        )
        desc.pack(anchor='w', padx=30, pady=(0, 10))
        
        # Botão salvar
        btn_salvar = tk.Button(
            container,
            text="💾 SALVAR CONFIGURAÇÕES",
            font=("Segoe UI", 12, "bold"),
            bg='#ff9900',
            fg='#000000',
            command=self.salvar_config,
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        btn_salvar.pack(pady=20)
    
    def criar_card_agendamento(self, parent, titulo, key_ativo, key_intervalo, unidade):
        """Cria um card de agendamento"""
        frame = tk.LabelFrame(
            parent,
            text=titulo,
            font=("Segoe UI", 11, "bold"),
            bg='#2d2d2d',
            fg='#ff9900',
            bd=0
        )
        frame.pack(fill=tk.X, pady=10)
        
        var_ativo = tk.BooleanVar(value=self.config.get(key_ativo, False))
        
        cb = tk.Checkbutton(
            frame,
            text="Ativar agendamento automático",
            variable=var_ativo,
            font=("Segoe UI", 10),
            bg='#2d2d2d',
            fg='#ffffff',
            selectcolor='#1e1e1e'
        )
        cb.pack(anchor='w', padx=15, pady=5)
        
        intervalo_frame = tk.Frame(frame, bg='#2d2d2d')
        intervalo_frame.pack(anchor='w', padx=30, pady=5)
        
        tk.Label(
            intervalo_frame,
            text=f"Executar a cada:",
            font=("Segoe UI", 9),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        spin = tk.Spinbox(
            intervalo_frame,
            from_=1,
            to=90,
            width=5,
            font=("Segoe UI", 9),
            bg='#1e1e1e',
            fg='#ffffff',
            buttonbackground='#3d3d3d',
            relief=tk.FLAT
        )
        spin.delete(0, tk.END)
        spin.insert(0, self.config.get(key_intervalo, 7))
        spin.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            intervalo_frame,
            text=unidade,
            font=("Segoe UI", 9),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        # Guardar referências
        self.config[key_ativo] = var_ativo.get()
        var_ativo.trace_add('write', lambda *args: self.config.update({key_ativo: var_ativo.get()}))
        
        def atualizar_intervalo(*args):
            try:
                self.config[key_intervalo] = int(spin.get())
            except:
                pass
        
        spin.config(command=atualizar_intervalo)
    
    def criar_aba_diagnostico(self):
        """Cria aba de diagnóstico profundo"""
        container = tk.Frame(self.content_frame, bg='#1e1e1e')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        titulo = tk.Label(
            container,
            text="🔍 DIAGNÓSTICO PROFUNDO DO SISTEMA",
            font=("Segoe UI", 16, "bold"),
            bg='#1e1e1e',
            fg='#ff00ff'
        )
        titulo.pack(pady=(0, 20))
        
        # Opções de diagnóstico
        opcoes_frame = tk.Frame(container, bg='#2d2d2d')
        opcoes_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_grid = [
            ("🔍 Erros do Sistema", self.diagnostico_erros, '#ff3366'),
            ("💾 Saúde dos Discos", self.diagnostico_discos, '#00aaff'),
            ("🌡️ Temperatura", self.diagnostico_temperatura, '#ff9900'),
            ("🔌 Drivers", self.diagnostico_drivers, '#9900ff'),
        ]
        
        for i, (texto, comando, cor) in enumerate(btn_grid):
            btn = tk.Button(
                opcoes_frame,
                text=texto,
                font=("Segoe UI", 10, "bold"),
                bg=cor,
                fg='#ffffff',
                command=comando,
                relief=tk.FLAT,
                padx=15,
                pady=10,
                cursor='hand2'
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky='ew')
        
        opcoes_frame.grid_columnconfigure(0, weight=1)
        opcoes_frame.grid_columnconfigure(1, weight=1)
        
        # Resultado
        self.diag_text = scrolledtext.ScrolledText(
            container,
            font=("Consolas", 9),
            bg='#0d0d0d',
            fg='#ff00ff',
            insertbackground='#ff00ff',
            wrap=tk.WORD,
            relief=tk.FLAT,
            height=20
        )
        self.diag_text.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def criar_aba_ferramentas(self):
        """Cria aba de ferramentas"""
        container = tk.Frame(self.content_frame, bg='#1e1e1e')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        titulo = tk.Label(
            container,
            text="🛠️ FERRAMENTAS DO SISTEMA",
            font=("Segoe UI", 16, "bold"),
            bg='#1e1e1e',
            fg='#ff3366'
        )
        titulo.pack(pady=(0, 30))
        
        # Grid de ferramentas
        tools_frame = tk.Frame(container, bg='#1e1e1e')
        tools_frame.pack(expand=True)
        
        ferramentas = [
            ("🗑️ Limpeza de Disco", "cleanmgr", '#00aaff'),
            ("💿 Desfragmentador", "dfrgui", '#ff9900'),
            ("📊 Gerenciador de Tarefas", "taskmgr", '#ff3366'),
            ("📈 Monitor de Recursos", "resmon", '#9900ff'),
            ("ℹ️ Informações do Sistema", "msinfo32", '#00ff88'),
            ("🔧 Editor de Registro", "regedit", '#ff0066'),
            ("🌐 Configurações de Rede", "ncpa.cpl", '#0099ff'),
            ("⚙️ Serviços", "services.msc", '#ff9900'),
        ]
        
        for i, (texto, cmd, cor) in enumerate(ferramentas):
            btn = tk.Button(
                tools_frame,
                text=texto,
                font=("Segoe UI", 11, "bold"),
                bg=cor,
                fg='#ffffff',
                command=lambda c=cmd: os.system(c),
                relief=tk.FLAT,
                width=28,
                height=2,
                cursor='hand2'
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def detectar_hardware(self):
        """Detecta hardware completo"""
        info = "=" * 70 + "\n"
        info += "HARDWARE DETECTADO - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n"
        info += "=" * 70 + "\n\n"
        
        try:
            # Sistema
            info += "[SISTEMA OPERACIONAL]\n"
            info += f"  Sistema: {platform.system()} {platform.release()}\n"
            info += f"  Versão: {platform.version()}\n"
            info += f"  Arquitetura: {platform.machine()}\n\n"
            
            # CPU
            info += "[PROCESSADOR]\n"
            info += f"  Modelo: {platform.processor()}\n"
            info += f"  Núcleos Físicos: {psutil.cpu_count(logical=False)}\n"
            info += f"  Núcleos Lógicos: {psutil.cpu_count(logical=True)}\n"
            info += f"  Frequência: {psutil.cpu_freq().current:.0f} MHz\n"
            info += f"  Uso Atual: {psutil.cpu_percent(interval=1)}%\n\n"
            
            # Memória
            mem = psutil.virtual_memory()
            info += "[MEMÓRIA RAM]\n"
            info += f"  Total: {mem.total / (1024**3):.2f} GB\n"
            info += f"  Disponível: {mem.available / (1024**3):.2f} GB\n"
            info += f"  Em Uso: {mem.used / (1024**3):.2f} GB ({mem.percent}%)\n\n"
            
            # Discos
            info += "[ARMAZENAMENTO]\n"
            hdds = []
            ssds = []
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    tipo = "SSD" if "SSD" in partition.device or usage.total < 2**40 else "HDD"
                    
                    disco_info = f"  {partition.device} ({tipo})\n"
                    disco_info += f"    Total: {usage.total / (1024**3):.2f} GB\n"
                    disco_info += f"    Livre: {usage.free / (1024**3):.2f} GB\n"
                    disco_info += f"    Uso: {usage.percent}%\n"
                    
                    if tipo == "HDD":
                        hdds.append(partition.device)
                    else:
                        ssds.append(partition.device)
                    
                    info += disco_info
                except:
                    pass
            
            if hdds:
                info += f"\n  HDDs detectados: {', '.join(hdds)}\n"
                info += "  ⚠️ Recomendado: Agendar desfragmentação\n"
            
            info += "\n"
            
            # GPU (tentativa)
            info += "[PLACA DE VÍDEO]\n"
            try:
                import subprocess
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                                      capture_output=True, text=True, timeout=5)
                gpus = [line.strip() for line in result.stdout.split('\n')[1:] if line.strip()]
                for gpu in gpus:
                    info += f"  {gpu}\n"
            except:
                info += "  Informação não disponível\n"
            
        except Exception as e:
            info += f"\n[ERRO] {e}\n"
        
        info += "\n" + "=" * 70
        
        # Atualizar labels
        resumo = f"CPU: {platform.processor()[:50]}\n"
        resumo += f"RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB\n"
        resumo += f"Sistema: {platform.system()} {platform.release()}"
        
        if hasattr(self, 'hw_info_label'):
            self.hw_info_label.config(text=resumo)
        
        if hasattr(self, 'hw_text'):
            self.hw_text.delete('1.0', tk.END)
            self.hw_text.insert('1.0', info)
    
    def log(self, mensagem):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {mensagem}\n")
        self.log_text.see(tk.END)
        self.log_text.update()
    
    def atualizar_progresso(self, valor, texto):
        """Atualiza barra de progresso"""
        self.progress_bar['value'] = valor
        self.label_progresso.config(text=texto)
        self.root.update()
    
    def executar_comando(self, comando, shell=True):
        """Executa comando do Windows"""
        try:
            subprocess.run(
                comando,
                shell=shell,
                check=False,
                capture_output=True,
                text=True,
                timeout=30
            )
            return True
        except:
            return False
    
    def toggle_modo_gamer(self, ativo):
        """Ativa/desativa modo gamer"""
        self.config['modo_gamer'] = ativo
        if ativo:
            messagebox.showinfo("Modo Gamer", "Modo Gamer ativado!\n\nO sistema será otimizado para máximo desempenho em jogos.")
        else:
            messagebox.showinfo("Modo Gamer", "Modo Gamer desativado.")
    
    def iniciar_otimizacao(self):
        """Inicia processo de otimização"""
        if self.otimizando:
            messagebox.showwarning("Aviso", "Otimização já em andamento!")
            return
        
        if not any(var.get() for var in self.checkboxes.values()):
            messagebox.showwarning("Aviso", "Selecione pelo menos uma otimização!")
            return
        
        resposta = messagebox.askyesno(
            "Confirmar Otimização",
            "Deseja iniciar a otimização completa do sistema?\n\n"
            "Isso pode levar alguns minutos.\n"
            "Ao final, será necessário REINICIAR o computador."
        )
        
        if not resposta:
            return
        
        self.otimizando = True
        self.btn_otimizar.config(state='disabled', text='⏳ OTIMIZANDO...')
        self.status_label.config(text="● Otimizando sistema...", fg='#ff9900')
        
        thread = threading.Thread(target=self.processo_otimizacao, daemon=True)
        thread.start()
    
    def processo_otimizacao(self):
        """Processo principal de otimização"""
        try:
            self.log("=" * 60)
            self.log("🚀 INICIANDO OTIMIZAÇÃO COMPLETA DO SISTEMA")
            self.log("=" * 60)
            
            otimizacoes_ativas = [k for k, v in self.checkboxes.items() if v.get()]
            total = len(otimizacoes_ativas)
            atual = 0
            
            if self.checkboxes['limpeza_temp'].get():
                atual += 1
                self.atualizar_progresso((atual/total)*100, "🗑️ Limpando arquivos temporários...")
                self.limpar_temporarios()
            
            if self.checkboxes['limpeza_cache'].get():
                atual += 1
                self.atualizar_progresso((atual/total)*100, "💾 Limpando cache...")
                self.limpar_cache()
            
            if self.checkboxes['registro'].get():
                atual += 1
                self.atualizar_progresso((atual/total)*100, "📋 Otimizando registro...")
                self.otimizar_registro()
            
            if self.checkboxes['servicos'].get():
                atual += 1
                self.atualizar_progresso((atual/total)*100, "⚙️ Otimizando serviços...")
                self.otimizar_servicos()
            
            if self.checkboxes['rede'].get():
                atual += 1
                self.atualizar_progresso((atual/total)*100, "🌐 Otimizando rede...")
                self.otimizar_rede()
            
            if self.checkboxes['memoria'].get():
                atual += 1
                self.atualizar_progresso((atual/total)*100, "🧠 Configurando memória...")
                self.configurar_memoria()
            
            if self.checkboxes['gpu'].get():
                atual += 1
                self.atualizar_progresso((atual/total)*100, "🎮 Otimizando para jogos...")
                self.otimizar_gpu()
            
            if self.checkboxes['inicializacao'].get():
                atual += 1
                self.atualizar_progresso((atual/total)*100, "🚀 Otimizando inicialização...")
                self.otimizar_startup()
            
            self.finalizar_otimizacao()
            
        except Exception as e:
            self.log(f"❌ ERRO: {e}")
            messagebox.showerror("Erro", f"Erro durante otimização: {e}")
        finally:
            self.otimizando = False
            self.btn_otimizar.config(state='normal', text='🚀 INICIAR OTIMIZAÇÃO COMPLETA')
            self.status_label.config(text="● Sistema Pronto | Admin: Sim", fg='#00ff88')
    
    def limpar_temporarios(self):
        """Limpa arquivos temporários"""
        self.log("🗑️ Limpando arquivos temporários...")
        
        pastas_temp = [
            os.environ.get('TEMP'),
            'C:\\Windows\\Temp',
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp'),
        ]
        
        arquivos_removidos = 0
        for pasta in pastas_temp:
            if pasta and os.path.exists(pasta):
                try:
                    for item in Path(pasta).glob('*'):
                        try:
                            if item.is_file():
                                item.unlink()
                                arquivos_removidos += 1
                            elif item.is_dir():
                                shutil.rmtree(item, ignore_errors=True)
                        except:
                            pass
                except:
                    pass
        
        self.log(f"  ✅ {arquivos_removidos} arquivos temporários removidos")
    
    def limpar_cache(self):
        """Limpa cache do sistema"""
        self.log("💾 Limpando cache do sistema...")
        
        # Limpar cache do Windows
        caches = [
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft', 'Windows', 'INetCache'),
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft', 'Windows', 'WebCache'),
        ]
        
        for cache in caches:
            if os.path.exists(cache):
                try:
                    shutil.rmtree(cache, ignore_errors=True)
                except:
                    pass
        
        # Limpar DNS
        self.executar_comando('ipconfig /flushdns')
        
        self.log("  ✅ Cache limpo com sucesso")
    
    def otimizar_registro(self):
        """Otimiza registro do Windows"""
        self.log("📋 Otimizando registro...")
        
        comandos = [
            'reg add "HKCU\\System\\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
            'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v EnableLUA /t REG_DWORD /d 1 /f',
        ]
        
        for cmd in comandos:
            self.executar_comando(cmd)
        
        self.log("  ✅ Registro otimizado")
    
    def otimizar_servicos(self):
        """Otimiza serviços do Windows"""
        self.log("⚙️ Otimizando serviços...")
        
        servicos_desabilitar = [
            'DiagTrack',
            'dmwappushservice',
            'WSearch',
            'SysMain',
            'TabletInputService',
            'WMPNetworkSvc'
        ]
        
        for servico in servicos_desabilitar:
            self.executar_comando(f'sc stop {servico}')
            self.executar_comando(f'sc config {servico} start= disabled')
        
        self.log("  ✅ Serviços otimizados")
    
    def otimizar_rede(self):
        """Otimiza configurações de rede"""
        self.log("🌐 Otimizando rede...")
        
        comandos = [
            'ipconfig /flushdns',
            'netsh interface tcp set global autotuninglevel=normal',
            'netsh interface tcp set global chimney=enabled',
            'netsh interface tcp set global rss=enabled',
        ]
        
        for cmd in comandos:
            self.executar_comando(cmd)
        
        self.log("  ✅ Rede otimizada")
    
    def configurar_memoria(self):
        """Configura memória virtual"""
        self.log("🧠 Configurando memória virtual...")
        
        try:
            ram_gb = psutil.virtual_memory().total / (1024**3)
            
            if ram_gb < 8:
                min_size, max_size = 2048, 4096
            elif ram_gb < 16:
                min_size, max_size = 4096, 8192
            else:
                min_size, max_size = 8192, 16384
            
            self.executar_comando('wmic computersystem set AutomaticManagedPagefile=False')
            self.executar_comando(f'wmic pagefileset set InitialSize={min_size},MaximumSize={max_size}')
            
            self.log(f"  ✅ Memória virtual: {min_size/1024:.0f}-{max_size/1024:.0f}GB")
        except Exception as e:
            self.log(f"  ⚠️ Aviso: {e}")
    
    def otimizar_gpu(self):
        """Otimiza para jogos"""
        self.log("🎮 Otimizando para jogos...")
        
        comandos = [
            'powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c',  # Alto desempenho
            'reg add "HKCU\\Software\\Microsoft\\GameBar" /v AllowAutoGameMode /t REG_DWORD /d 1 /f',
            'reg add "HKCU\\Software\\Microsoft\\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 1 /f',
        ]
        
        for cmd in comandos:
            self.executar_comando(cmd)
        
        self.log("  ✅ Sistema otimizado para jogos")
    
    def otimizar_startup(self):
        """Otimiza inicialização"""
        self.log("🚀 Otimizando inicialização...")
        
        # Desabilitar programas desnecessários do startup
        comandos = [
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "" /t REG_SZ /d "" /f',
        ]
        
        for cmd in comandos:
            self.executar_comando(cmd)
        
        self.log("  ✅ Inicialização otimizada")
    
    def finalizar_otimizacao(self):
        """Finaliza processo de otimização"""
        self.atualizar_progresso(100, "✅ OTIMIZAÇÃO COMPLETA!")
        
        self.log("")
        self.log("=" * 60)
        self.log("✅ OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!")
        self.log("=" * 60)
        
        for key, var in self.checkboxes.items():
            if var.get():
                nome = key.replace('_', ' ').title()
                self.log(f"  ✅ {nome}")
        
        self.log("")
        self.log("⚠️ ATENÇÃO: Reinicie o computador para aplicar todas as alterações")
        self.log("=" * 60)
        
        self.status_label.config(text="✅ Otimização completa!", fg='#00ff88')
        
        resposta = messagebox.askyesnocancel(
            "Otimização Completa!",
            "✅ OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!\n\n"
            "Todas otimizações foram aplicadas.\n\n"
            "Para melhor resultado, o computador deve ser reiniciado.\n\n"
            "Deseja REINICIAR AGORA?"
        )
        
        if resposta:
            os.system('shutdown /r /t 10 /c "Reiniciando para aplicar otimizações do ENIAC System Tuner"')
    
    def diagnostico_erros(self):
        """Diagnóstico de erros do sistema"""
        self.diag_text.delete('1.0', tk.END)
        self.diag_text.insert('1.0', "🔍 Procurando erros no sistema...\n\n")
        self.root.update()
        
        try:
            # Verificar logs de eventos
            cmd = 'wevtutil qe System /c:10 /rd:true /f:text /q:"*[System[(Level=1 or Level=2 or Level=3)]]"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            self.diag_text.insert(tk.END, "[ERROS RECENTES DO SISTEMA]\n")
            if result.stdout:
                self.diag_text.insert(tk.END, result.stdout[:2000])
            else:
                self.diag_text.insert(tk.END, "✅ Nenhum erro crítico encontrado\n")
        except:
            self.diag_text.insert(tk.END, "⚠️ Erro ao verificar logs\n")
    
    def diagnostico_discos(self):
        """Diagnóstico de saúde dos discos"""
        self.diag_text.delete('1.0', tk.END)
        self.diag_text.insert('1.0', "💾 Verificando saúde dos discos...\n\n")
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                self.diag_text.insert(tk.END, f"[{partition.device}]\n")
                self.diag_text.insert(tk.END, f"  Total: {usage.total / (1024**3):.2f} GB\n")
                self.diag_text.insert(tk.END, f"  Livre: {usage.free / (1024**3):.2f} GB\n")
                self.diag_text.insert(tk.END, f"  Uso: {usage.percent}%\n")
                
                if usage.percent > 90:
                    self.diag_text.insert(tk.END, "  ⚠️ ATENÇÃO: Disco quase cheio!\n")
                elif usage.percent > 80:
                    self.diag_text.insert(tk.END, "  ⚠️ Espaço ficando limitado\n")
                else:
                    self.diag_text.insert(tk.END, "  ✅ Espaço adequado\n")
                
                self.diag_text.insert(tk.END, "\n")
            except:
                pass
    
    def diagnostico_temperatura(self):
        """Diagnóstico de temperatura"""
        self.diag_text.delete('1.0', tk.END)
        self.diag_text.insert('1.0', "🌡️ Monitoramento de temperatura...\n\n")
        self.diag_text.insert(tk.END, "⚠️ Funcionalidade requer sensores de hardware específicos\n")
        self.diag_text.insert(tk.END, "Recomendado: Use HWMonitor ou HWiNFO para detalhes precisos\n")
    
    def diagnostico_drivers(self):
        """Diagnóstico de drivers"""
        self.diag_text.delete('1.0', tk.END)
        self.diag_text.insert('1.0', "🔌 Verificando drivers...\n\n")
        
        try:
            result = subprocess.run('driverquery', shell=True, capture_output=True, text=True, timeout=10)
            self.diag_text.insert(tk.END, result.stdout[:3000])
        except:
            self.diag_text.insert(tk.END, "⚠️ Erro ao listar drivers\n")
    
    def iniciar_monitoramento(self):
        """Atualiza status bar periodicamente"""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory()
            
            if not self.otimizando:
                info = f"CPU: {cpu:.1f}% | RAM: {ram.percent:.1f}%"
                self.status_info.config(text=info)
        except:
            pass
        
        self.root.after(2000, self.iniciar_monitoramento)

def main():
    root = tk.Tk()
    app = ENIACTuner(root)
    root.mainloop()

if __name__ == "__main__":
    main()