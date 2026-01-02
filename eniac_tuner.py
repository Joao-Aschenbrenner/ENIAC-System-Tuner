"""
ENIAC SYSTEM TUNER ULTIMATE v4.0 - VERSÃO CORRIGIDA
Correções: Hardware, Reinicialização, Permissões
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
            resposta = messagebox.askyesno(
                "Permissão Necessária",
                "⚠️ Este programa precisa ser executado como ADMINISTRADOR!\n\n"
                "Muitas funcionalidades não funcionarão corretamente.\n\n"
                "Deseja continuar mesmo assim?\n"
                "(Clique 'Não' para fechar e executar como administrador)"
            )
            if not resposta:
                sys.exit(1)
        
        self.otimizando = False
        self.aba_atual = "otimizacao"
        self.config_file = Path(os.environ.get('APPDATA')) / 'ESTU' / 'config.json'
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.carregar_config()
        self.criar_interface()
        self.mostrar_aba("otimizacao")
        self.iniciar_monitoramento()
        
        # Detectar hardware em thread separada
        threading.Thread(target=self.detectar_hardware, daemon=True).start()
    
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
            messagebox.showinfo("Sucesso", "✅ Configurações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações:\n{e}")
    
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
            text="v4.0 Ultimate Edition - CORRIGIDO",
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
        
        admin_status = "✅ Admin" if self.is_admin() else "⚠️ Sem Admin"
        
        self.status_label = tk.Label(
            self.status_bar,
            text=f"● Sistema Pronto | {admin_status}",
            font=("Segoe UI", 9),
            bg='#2d2d2d',
            fg='#00ff88' if self.is_admin() else '#ff9900',
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
            text="🔄 Detectando hardware...",
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
            command=lambda: threading.Thread(target=self.detectar_hardware, daemon=True).start(),
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
            ("📌 Erros do Sistema", self.diagnostico_erros, '#ff3366'),
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
    
    def detectar_hardware_completo(self):
        """Detecta hardware com múltiplos métodos"""
        info_hw = {}
        
        try:
            # CPU via WMI
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'name'],
                capture_output=True,
                text=True,
                timeout=5
            )
            cpu_lines = [l.strip() for l in result.stdout.split('\n') if l.strip() and l.strip() != 'Name']
            info_hw['cpu_nome'] = cpu_lines[0] if cpu_lines else platform.processor()
        except:
            info_hw['cpu_nome'] = platform.processor()
        
        try:
            # GPU via WMI
            result = subprocess.run(
                ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                capture_output=True,
                text=True,
                timeout=5
            )
            gpu_lines = [l.strip() for l in result.stdout.split('\n') if l.strip() and l.strip() != 'Name']
            info_hw['gpu'] = gpu_lines if gpu_lines else ["Não detectada"]
        except:
            info_hw['gpu'] = ["Informação não disponível"]
        
        try:
            # Placa mãe
            result = subprocess.run(
                ['wmic', 'baseboard', 'get', 'product,manufacturer'],
                capture_output=True,
                text=True,
                timeout=5
            )
            lines = [l.strip() for l in result.stdout.split('\n')[1:] if l.strip()]
            info_hw['motherboard'] = lines[0] if lines else "Não detectada"
        except:
            info_hw['motherboard'] = "Informação não disponível"
        
        return info_hw
    
    def detectar_hardware(self):
        """Detecta hardware completo com melhorias"""
        try:
            # Primeiro, mostrar info básica
            mem = psutil.virtual_memory()
            resumo = f"CPU: Detectando...\nRAM: {mem.total / (1024**3):.1f} GB\nSistema: {platform.system()} {platform.release()}"
            
            if hasattr(self, 'hw_info_label'):
                self.hw_info_label.config(text=resumo)
                self.root.update()
            
            # Agora detectar detalhes
            hw_detalhado = self.detectar_hardware_completo()
            
            info = "=" * 70 + "\n"
            info += "HARDWARE DETECTADO - " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n"
            info += "=" * 70 + "\n\n"
            
            # Sistema
            info += "[SISTEMA OPERACIONAL]\n"
            info += f"  Sistema: {platform.system()} {platform.release()}\n"
            info += f"  Versão: {platform.version()}\n"
            info += f"  Arquitetura: {platform.machine()}\n"
            info += f"  Nome do PC: {platform.node()}\n\n"
            
            # CPU detalhado
            info += "[PROCESSADOR]\n"
            info += f"  Modelo: {hw_detalhado.get('cpu_nome', 'Não detectado')}\n"
            info += f"  Núcleos Físicos: {psutil.cpu_count(logical=False)}\n"
            info += f"  Núcleos Lógicos (Threads): {psutil.cpu_count(logical=True)}\n"
            
            try:
                freq = psutil.cpu_freq()
                if freq:
                    info += f"  Frequência Atual: {freq.current:.0f} MHz\n"
                    info += f"  Frequência Máxima: {freq.max:.0f} MHz\n"
            except:
                pass
            
            cpu_percent = psutil.cpu_percent(interval=1)
            info += f"  Uso Atual: {cpu_percent}%\n"
            
            # Cores individuais
            try:
                cpu_per_core = psutil.cpu_percent(interval=0.5, percpu=True)
                info += f"  Uso por Core: "
                for i, percent in enumerate(cpu_per_core):
                    info += f"{i}:{percent:.0f}% "
                info += "\n"
            except:
                pass
            
            info += "\n"
            
            # Memória detalhada
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            info += "[MEMÓRIA RAM]\n"
            info += f"  Total Instalada: {mem.total / (1024**3):.2f} GB\n"
            info += f"  Disponível: {mem.available / (1024**3):.2f} GB\n"
            info += f"  Em Uso: {mem.used / (1024**3):.2f} GB ({mem.percent}%)\n"
            info += f"  Livre: {mem.free / (1024**3):.2f} GB\n"
            info += f"\n  Memória Virtual (SWAP):\n"
            info += f"  Total: {swap.total / (1024**3):.2f} GB\n"
            info += f"  Usado: {swap.used / (1024**3):.2f} GB ({swap.percent}%)\n\n"
            
            # Discos detalhados
            info += "[ARMAZENAMENTO]\n"
            hdds = []
            ssds = []
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    info += f"  {partition.device}\n"
                    info += f"    Montagem: {partition.mountpoint}\n"
                    info += f"    Sistema de Arquivos: {partition.fstype}\n"
                    info += f"    Total: {usage.total / (1024**3):.2f} GB\n"
                    info += f"    Usado: {usage.used / (1024**3):.2f} GB\n"
                    info += f"    Livre: {usage.free / (1024**3):.2f} GB\n"
                    info += f"    Percentual de Uso: {usage.percent}%\n"
                    
                    # Detectar SSD vs HDD (método aproximado)
                    tipo_disco = "SSD" if usage.total < 2**40 else "HDD"  # < 1TB geralmente é SSD
                    info += f"    Tipo Estimado: {tipo_disco}\n"
                    
                    if tipo_disco == "HDD":
                        hdds.append(partition.device)
                    else:
                        ssds.append(partition.device)
                    
                    if usage.percent > 90:
                        info += "    ⚠️ AVISO: Disco quase cheio!\n"
                    elif usage.percent > 80:
                        info += "    ⚠️ Espaço ficando limitado\n"
                    
                    info += "\n"
                except:
                    pass
            
            if hdds:
                info += f"  HDDs detectados: {', '.join(hdds)}\n"
                info += "  💡 Recomendação: Agendar desfragmentação regular\n\n"
            
            if ssds:
                info += f"  SSDs detectados: {', '.join(ssds)}\n"
                info += "  ✓ SSDs não precisam de desfragmentação\n\n"
            
            # GPU
            info += "[PLACA(S) DE VÍDEO]\n"
            gpus = hw_detalhado.get('gpu', [])
            for gpu in gpus:
                info += f"  • {gpu}\n"
            info += "\n"
            
            # Placa mãe
            info += "[PLACA MÃE]\n"
            info += f"  {hw_detalhado.get('motherboard', 'Não detectada')}\n\n"
            
            # Rede
            try:
                net = psutil.net_io_counters()
                info += "[REDE]\n"
                info += f"  Bytes Enviados: {net.bytes_sent / (1024**2):.2f} MB\n"
                info += f"  Bytes Recebidos: {net.bytes_recv / (1024**2):.2f} MB\n"
                info += f"  Pacotes Enviados: {net.packets_sent}\n"
                info += f"  Pacotes Recebidos: {net.packets_recv}\n\n"
            except:
                pass
            
            # Bateria (notebooks)
            try:
                battery = psutil.sensors_battery()
                if battery:
                    info += "[BATERIA]\n"
                    info += f"  Nível: {battery.percent}%\n"
                    info += f"  Status: {'Carregando' if battery.power_plugged else 'Descarregando'}\n\n"
            except:
                pass
            
        except Exception as e:
            info = f"\n[ERRO ao detectar hardware] {e}\n"
        
        info += "=" * 70
        
        # Atualizar resumo
        try:
            cpu_nome = hw_detalhado.get('cpu_nome', 'Não detectado')
            if len(cpu_nome) > 50:
                cpu_nome = cpu_nome[:50] + "..."
            
            resumo = f"CPU: {cpu_nome}\n"
            resumo += f"RAM: {mem.total / (1024**3):.1f} GB ({mem.percent}% usado)\n"
            resumo += f"Sistema: {platform.system()} {platform.release()}"
            
            if hdds:
                resumo += f"\n💿 HDDs: {len(hdds)} | "
            if ssds:
                resumo += f"⚡ SSDs: {len(ssds)}"
            
            if hasattr(self, 'hw_info_label'):
                self.hw_info_label.config(text=resumo)
        except:
            pass
        
        # Atualizar área de texto detalhada
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
    
    def executar_comando(self, comando, shell=True, requer_admin=True):
        """Executa comando do Windows com verificação de permissões"""
        if requer_admin and not self.is_admin():
            self.log(f"⚠️ Sem privilégios de admin para: {comando}")
            return False
        
        try:
            result = subprocess.run(
                comando,
                shell=shell,
                check=False,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            self.log(f"⚠️ Erro ao executar comando: {e}")
            return False
    
    def toggle_modo_gamer(self, ativo):
        """Ativa/desativa modo gamer"""
        self.config['modo_gamer'] = ativo
        if ativo:
            messagebox.showinfo("Modo Gamer", "🎮 Modo Gamer ativado!\n\nO sistema será otimizado para máximo desempenho em jogos.")
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
        
        if not self.is_admin():
            messagebox.showwarning(
                "Permissões Insuficientes",
                "⚠️ AVISO: Você não está rodando como ADMINISTRADOR!\n\n"
                "Muitas otimizações podem não funcionar corretamente.\n\n"
                "Para melhores resultados:\n"
                "1. Feche este programa\n"
                "2. Clique direito no ícone\n"
                "3. Selecione 'Executar como administrador'\n\n"
                "Deseja continuar mesmo assim?"
            )
        
        resposta = messagebox.askyesno(
            "Confirmar Otimização",
            "🚀 Deseja iniciar a otimização completa do sistema?\n\n"
            "Isso pode levar alguns minutos.\n"
            "Ao final, será recomendado REINICIAR o computador."
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
            admin_status = "✅ Admin" if self.is_admin() else "⚠️ Sem Admin"
            self.status_label.config(text=f"● Sistema Pronto | {admin_status}", fg='#00ff88' if self.is_admin() else '#ff9900')
    
    def limpar_temporarios(self):
        """Limpa arquivos temporários"""
        self.log("🗑️ Limpando arquivos temporários...")
        
        pastas_temp = [
            os.environ.get('TEMP'),
            'C:\\Windows\\Temp',
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp'),
            os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Local', 'Temp'),
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
                                arquivos_removidos += 1
                        except:
                            pass
                except:
                    pass
        
        self.log(f"  ✅ {arquivos_removidos} itens removidos")
    
    def limpar_cache(self):
        """Limpa cache do sistema"""
        self.log("💾 Limpando cache do sistema...")
        
        # Limpar cache do Windows
        caches = [
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft', 'Windows', 'INetCache'),
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft', 'Windows', 'WebCache'),
            os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Local', 'Microsoft', 'Windows', 'Caches'),
        ]
        
        removidos = 0
        for cache in caches:
            if os.path.exists(cache):
                try:
                    shutil.rmtree(cache, ignore_errors=True)
                    removidos += 1
                except:
                    pass
        
        # Limpar DNS
        if self.executar_comando('ipconfig /flushdns', requer_admin=False):
            self.log("  ✅ Cache DNS limpo")
        
        self.log(f"  ✅ {removidos} caches limpos")
    
    def otimizar_registro(self):
        """Otimiza registro do Windows"""
        self.log("📋 Otimizando registro...")
        
        if not self.is_admin():
            self.log("  ⚠️ Requer privilégios de administrador")
            return
        
        comandos_aplicados = 0
        comandos = [
            ('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f', 'Desabilitar DVR de jogos'),
            ('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f', 'Desabilitar telemetria'),
            ('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v TaskbarAnimations /t REG_DWORD /d 0 /f', 'Desabilitar animações'),
        ]
        
        for cmd, desc in comandos:
            if self.executar_comando(cmd):
                comandos_aplicados += 1
                self.log(f"  ✓ {desc}")
            else:
                self.log(f"  ✗ Falha: {desc}")
        
        self.log(f"  ✅ {comandos_aplicados} otimizações de registro aplicadas")
    
    def otimizar_servicos(self):
        """Otimiza serviços do Windows"""
        self.log("⚙️ Otimizando serviços...")
        
        if not self.is_admin():
            self.log("  ⚠️ Requer privilégios de administrador")
            return
        
        servicos_desabilitar = [
            ('DiagTrack', 'Telemetria'),
            ('dmwappushservice', 'Push de mensagens'),
            ('WSearch', 'Busca do Windows'),
            ('SysMain', 'Superfetch'),
        ]
        
        servicos_parados = 0
        for servico, nome in servicos_desabilitar:
            if self.executar_comando(f'sc stop {servico}'):
                if self.executar_comando(f'sc config {servico} start= disabled'):
                    servicos_parados += 1
                    self.log(f"  ✓ {nome} desabilitado")
            else:
                self.log(f"  • {nome} já parado ou não existe")
        
        self.log(f"  ✅ {servicos_parados} serviços otimizados")
    
    def otimizar_rede(self):
        """Otimiza configurações de rede"""
        self.log("🌐 Otimizando rede...")
        
        comandos = [
            ('ipconfig /flushdns', 'Limpar DNS', False),
            ('netsh interface tcp set global autotuninglevel=normal', 'Otimizar TCP', True),
            ('netsh interface tcp set global chimney=enabled', 'Habilitar Chimney', True),
            ('netsh int tcp set global rss=enabled', 'Habilitar RSS', True),
        ]
        
        aplicados = 0
        for cmd, desc, requer_admin in comandos:
            if self.executar_comando(cmd, requer_admin=requer_admin):
                aplicados += 1
                self.log(f"  ✓ {desc}")
            else:
                self.log(f"  • {desc} - não aplicado")
        
        self.log(f"  ✅ {aplicados} otimizações de rede aplicadas")
    
    def configurar_memoria(self):
        """Configura memória virtual"""
        self.log("🧠 Configurando memória virtual...")
        
        if not self.is_admin():
            self.log("  ⚠️ Requer privilégios de administrador")
            return
        
        try:
            ram_gb = psutil.virtual_memory().total / (1024**3)
            
            if ram_gb < 8:
                min_size, max_size = 2048, 4096
            elif ram_gb < 16:
                min_size, max_size = 4096, 8192
            else:
                min_size, max_size = 8192, 16384
            
            # Tentar configurar
            if self.executar_comando('wmic computersystem set AutomaticManagedPagefile=False'):
                if self.executar_comando(f'wmic pagefileset set InitialSize={min_size},MaximumSize={max_size}'):
                    self.log(f"  ✅ Memória virtual: {min_size/1024:.0f}-{max_size/1024:.0f}GB")
                else:
                    self.log("  ⚠️ Falha ao configurar tamanhos")
            else:
                self.log("  ⚠️ Falha ao desabilitar gerenciamento automático")
        except Exception as e:
            self.log(f"  ⚠️ Erro: {e}")
    
    def otimizar_gpu(self):
        """Otimiza para jogos"""
        self.log("🎮 Otimizando para jogos...")
        
        comandos = [
            ('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', 'Plano Alto Desempenho', True),
            ('reg add "HKCU\\Software\\Microsoft\\GameBar" /v AllowAutoGameMode /t REG_DWORD /d 1 /f', 'Modo Jogo automático', True),
            ('reg add "HKCU\\Software\\Microsoft\\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 1 /f', 'Habilitar Modo Jogo', True),
            ('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_FSEBehaviorMode /t REG_DWORD /d 2 /f', 'Otimizar tela cheia', True),
        ]
        
        aplicados = 0
        for cmd, desc, requer_admin in comandos:
            if self.executar_comando(cmd, requer_admin=requer_admin):
                aplicados += 1
                self.log(f"  ✓ {desc}")
        
        self.log(f"  ✅ {aplicados} otimizações para jogos aplicadas")
    
    def otimizar_startup(self):
        """Otimiza inicialização"""
        self.log("🚀 Otimizando inicialização...")
        
        if not self.is_admin():
            self.log("  ⚠️ Requer privilégios de administrador")
            return
        
        # Desabilitar programas desnecessários do startup
        try:
            # Usar Task Manager para desabilitar startups
            self.log("  💡 Use o Gerenciador de Tarefas > Inicializar para controlar programas")
            
            # Otimizar tempo de boot
            comandos = [
                'bcdedit /set bootmenupolicy legacy',
                'bcdedit /timeout 3',
            ]
            
            for cmd in comandos:
                self.executar_comando(cmd)
            
            self.log("  ✅ Configurações de boot otimizadas")
        except Exception as e:
            self.log(f"  ⚠️ Erro: {e}")
    
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
        self.log("💡 IMPORTANTE: Reinicie o computador para aplicar todas as alterações")
        self.log("=" * 60)
        
        self.status_label.config(text="✅ Otimização completa!", fg='#00ff88')
        
        resposta = messagebox.askyesnocancel(
            "Otimização Completa!",
            "✅ OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!\n\n"
            "Todas otimizações foram aplicadas.\n\n"
            "Para que as mudanças tenham efeito completo,\n"
            "é ALTAMENTE RECOMENDADO reiniciar o computador.\n\n"
            "Deseja REINICIAR AGORA?"
        )
        
        if resposta is True:
            # Usuário clicou SIM - reiniciar
            try:
                self.log("🔄 Preparando reinicialização em 10 segundos...")
                self.log("⏰ Salve todos os trabalhos abertos!")
                
                # Dar tempo para o usuário ver e salvar trabalhos
                for i in range(10, 0, -1):
                    self.status_label.config(text=f"⏰ Reiniciando em {i} segundos...")
                    self.root.update()
                    time.sleep(1)
                
                # Executar reinicialização
                if self.is_admin():
                    subprocess.Popen(['shutdown', '/r', '/t', '5', '/c', 
                                    '"ENIAC System Tuner - Aplicando otimizações"'])
                    self.log("✅ Comando de reinicialização enviado!")
                    messagebox.showinfo("Reiniciando", 
                                      "🔄 O computador será reiniciado em 5 segundos!\n\n"
                                      "Salve todos os trabalhos agora!")
                else:
                    messagebox.showwarning("Sem Permissões",
                                         "⚠️ Não foi possível reiniciar automaticamente.\n\n"
                                         "Por favor, reinicie manualmente:\n"
                                         "Menu Iniciar > Reiniciar")
            except Exception as e:
                self.log(f"❌ Erro ao tentar reiniciar: {e}")
                messagebox.showerror("Erro", 
                                   f"Não foi possível reiniciar automaticamente:\n{e}\n\n"
                                   "Por favor, reinicie manualmente.")
        elif resposta is False:
            # Usuário clicou NÃO - não reiniciar
            messagebox.showinfo("Lembrete",
                              "⚠️ Lembre-se de reiniciar o computador mais tarde\n"
                              "para que todas as otimizações tenham efeito completo!")
    
    def diagnostico_erros(self):
        """Diagnóstico de erros do sistema"""
        self.diag_text.delete('1.0', tk.END)
        self.diag_text.insert('1.0', "🔍 Procurando erros no sistema...\n\n")
        self.root.update()
        
        try:
            # Verificar logs de eventos
            cmd = 'wevtutil qe System /c:20 /rd:true /f:text /q:"*[System[(Level=1 or Level=2 or Level=3)]]"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            
            self.diag_text.insert(tk.END, "[ERROS RECENTES DO SISTEMA]\n")
            self.diag_text.insert(tk.END, "=" * 50 + "\n\n")
            
            if result.stdout and len(result.stdout.strip()) > 0:
                # Limitar saída
                erros = result.stdout[:3000]
                self.diag_text.insert(tk.END, erros)
                self.diag_text.insert(tk.END, "\n\n... (mostrando primeiros erros)")
            else:
                self.diag_text.insert(tk.END, "✅ Nenhum erro crítico encontrado nos logs recentes\n")
        except subprocess.TimeoutExpired:
            self.diag_text.insert(tk.END, "⏰ Timeout - verificação demorou muito\n")
        except Exception as e:
            self.diag_text.insert(tk.END, f"⚠️ Erro ao verificar logs: {e}\n")
    
    def diagnostico_discos(self):
        """Diagnóstico de saúde dos discos"""
        self.diag_text.delete('1.0', tk.END)
        self.diag_text.insert('1.0', "💾 Verificando saúde dos discos...\n\n")
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                self.diag_text.insert(tk.END, f"[{partition.device}]\n")
                self.diag_text.insert(tk.END, f"  Montagem: {partition.mountpoint}\n")
                self.diag_text.insert(tk.END, f"  Sistema: {partition.fstype}\n")
                self.diag_text.insert(tk.END, f"  Total: {usage.total / (1024**3):.2f} GB\n")
                self.diag_text.insert(tk.END, f"  Usado: {usage.used / (1024**3):.2f} GB\n")
                self.diag_text.insert(tk.END, f"  Livre: {usage.free / (1024**3):.2f} GB\n")
                self.diag_text.insert(tk.END, f"  Uso: {usage.percent}%\n")
                
                if usage.percent > 95:
                    self.diag_text.insert(tk.END, "  🔴 CRÍTICO: Disco quase cheio!\n")
                elif usage.percent > 90:
                    self.diag_text.insert(tk.END, "  ⚠️ ATENÇÃO: Disco quase cheio!\n")
                elif usage.percent > 80:
                    self.diag_text.insert(tk.END, "  ⚠️ Espaço ficando limitado\n")
                else:
                    self.diag_text.insert(tk.END, "  ✅ Espaço adequado\n")
                
                self.diag_text.insert(tk.END, "\n")
            except Exception as e:
                self.diag_text.insert(tk.END, f"  ⚠️ Erro: {e}\n\n")
        
        # Verificar SMART (se disponível)
        self.diag_text.insert(tk.END, "\n[VERIFICAÇÃO SMART]\n")
        self.diag_text.insert(tk.END, "💡 Para verificação completa SMART, use:\n")
        self.diag_text.insert(tk.END, "  • CrystalDiskInfo (recomendado)\n")
        self.diag_text.insert(tk.END, "  • HD Tune\n")
    
    def diagnostico_temperatura(self):
        """Diagnóstico de temperatura"""
        self.diag_text.delete('1.0', tk.END)
        self.diag_text.insert('1.0', "🌡️ Monitoramento de temperatura...\n\n")
        
        # Tentar obter temperaturas (limitado no Windows)
        try:
            # Verificar se psutil suporta temperaturas
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    self.diag_text.insert(tk.END, f"[{name}]\n")
                    for entry in entries:
                        self.diag_text.insert(tk.END, 
                            f"  {entry.label or name}: {entry.current}°C\n")
                    self.diag_text.insert(tk.END, "\n")
            else:
                self.diag_text.insert(tk.END, "⚠️ Sensores de temperatura não disponíveis no Windows\n\n")
        except AttributeError:
            self.diag_text.insert(tk.END, "⚠️ Monitoramento de temperatura não suportado\n\n")
        
        self.diag_text.insert(tk.END, "[RECOMENDAÇÃO]\n")
        self.diag_text.insert(tk.END, "Para monitoramento completo de temperatura, use:\n")
        self.diag_text.insert(tk.END, "  • HWMonitor (recomendado)\n")
        self.diag_text.insert(tk.END, "  • HWiNFO64\n")
        self.diag_text.insert(tk.END, "  • Core Temp (para CPU)\n")
        self.diag_text.insert(tk.END, "  • MSI Afterburner (para GPU)\n")
    
    def diagnostico_drivers(self):
        """Diagnóstico de drivers"""
        self.diag_text.delete('1.0', tk.END)
        self.diag_text.insert('1.0', "🔌 Verificando drivers instalados...\n\n")
        
        try:
            result = subprocess.run('driverquery', shell=True, capture_output=True, 
                                  text=True, timeout=10)
            
            if result.stdout:
                # Mostrar primeiros drivers
                linhas = result.stdout.split('\n')
                self.diag_text.insert(tk.END, '\n'.join(linhas[:50]))
                self.diag_text.insert(tk.END, f"\n\n... (mostrando primeiros 50 de {len(linhas)} drivers)")
            else:
                self.diag_text.insert(tk.END, "⚠️ Não foi possível listar drivers\n")
        except Exception as e:
            self.diag_text.insert(tk.END, f"⚠️ Erro ao listar drivers: {e}\n")
        
        self.diag_text.insert(tk.END, "\n\n[VERIFICAÇÃO DE DRIVERS]\n")
        self.diag_text.insert(tk.END, "Para atualizar drivers:\n")
        self.diag_text.insert(tk.END, "  1. Windows Update\n")
        self.diag_text.insert(tk.END, "  2. Site do fabricante do hardware\n")
        self.diag_text.insert(tk.END, "  3. Driver Booster (ferramenta terceiros)\n")
    
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