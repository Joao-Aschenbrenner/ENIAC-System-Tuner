"""
INSTALADOR PROFISSIONAL COM INTERFACE GRÁFICA
ENIAC SYSTEM TUNER v4.0 - Instalador Completo
CORRIGIDO - Instalação REAL com cópia de arquivos
"""

import os
import sys
import subprocess
import shutil
import winreg
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import time

# Configurar encoding CORRETAMENTE
if sys.platform == 'win32':
    try:
        if sys.stdout is not None:
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr is not None:
            sys.stderr.reconfigure(encoding='utf-8')
        os.system('chcp 65001 >nul 2>&1')
    except:
        pass

class InstaladorENIAC:
    def __init__(self, root):
        self.root = root
        self.root.title("ENIAC System Tuner - Instalador")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#0f0f0f')
        
        # Variáveis
        self.pagina_atual = 0
        self.caminho_instalacao = "C:\\Program Files\\ESTU"
        self.criar_atalho_desktop = tk.BooleanVar(value=True)
        self.criar_atalho_menu = tk.BooleanVar(value=True)
        self.instalando = False
        
        # Verificar admin
        if not self.is_admin():
            self.pedir_admin()
        
        self.criar_interface()
        self.mostrar_pagina(0)
    
    def is_admin(self):
        """Verifica se está rodando como administrador"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def pedir_admin(self):
        """Solicita privilégios de administrador"""
        try:
            import ctypes
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit(0)
        except:
            messagebox.showerror(
                "Permissão Necessária",
                "Este instalador precisa de privilégios de Administrador!\n\n"
                "Clique com botão direito e selecione 'Executar como administrador'"
            )
            sys.exit(1)
    
    def criar_interface(self):
        """Cria interface do instalador"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#1a1a1a', height=120)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Logo e título
        logo_label = tk.Label(
            header_frame,
            text="⚡",
            font=("Segoe UI", 48),
            bg='#1a1a1a',
            fg='#00ff88'
        )
        logo_label.place(x=30, y=25)
        
        titulo = tk.Label(
            header_frame,
            text="ENIAC SYSTEM TUNER",
            font=("Segoe UI", 24, "bold"),
            bg='#1a1a1a',
            fg='#00ff88'
        )
        titulo.place(x=120, y=30)
        
        subtitulo = tk.Label(
            header_frame,
            text="Ultimate Edition v4.0 - Assistente de Instalação",
            font=("Segoe UI", 11),
            bg='#1a1a1a',
            fg='#888888'
        )
        subtitulo.place(x=120, y=70)
        
        # Área de conteúdo
        self.content_frame = tk.Frame(self.root, bg='#0f0f0f')
        self.content_frame.pack(fill=tk.BOTH, expand=True, after=header_frame)
    
    def limpar_conteudo(self):
        """Limpa área de conteúdo"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def mostrar_pagina(self, pagina):
        """Mostra página do instalador"""
        self.pagina_atual = pagina
        self.limpar_conteudo()
        
        if pagina == 0:
            self.pagina_bem_vindo()
        elif pagina == 1:
            self.pagina_configuracao()
        elif pagina == 2:
            self.pagina_resumo()
        elif pagina == 3:
            self.pagina_instalacao()
        elif pagina == 4:
            self.pagina_concluido()
    
    def pagina_bem_vindo(self):
        """Página de boas-vindas com termos de licença"""
        from tkinter import scrolledtext
        
        container = tk.Frame(self.content_frame, bg='#0f0f0f')
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Título
        titulo = tk.Label(
            container,
            text="Bem-vindo ao Instalador",
            font=("Segoe UI", 18, "bold"),
            bg='#0f0f0f',
            fg='#00ff88'
        )
        titulo.pack(pady=(0, 10))
        
        # Subtítulo
        subtitulo = tk.Label(
            container,
            text="ENIAC SYSTEM TUNER ULTIMATE v4.0",
            font=("Segoe UI", 12),
            bg='#0f0f0f',
            fg='#888888'
        )
        subtitulo.pack(pady=(0, 15))
        
        # Texto de introdução
        intro = tk.Label(
            container,
            text="Por favor, leia atentamente os termos de licença antes de continuar:",
            font=("Segoe UI", 10),
            bg='#0f0f0f',
            fg='#ffffff'
        )
        intro.pack(pady=(0, 10))
        
        # Área de texto com termos de licença
        licenca_text = scrolledtext.ScrolledText(
            container,
            font=("Consolas", 9),
            bg='#1a1a1a',
            fg='#ffffff',
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0,
            height=12
        )
        licenca_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        licenca_conteudo = """TERMOS DE LICENÇA - ENIAC SYSTEM TUNER ULTIMATE v4.0

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
O software executa modificações no sistema operacional. Embora testado, não nos 
responsabilizamos por quaisquer danos diretos ou indiretos. Recomenda-se criar um 
ponto de restauração antes de usar.

COLETA DE DADOS:
Este software NÃO coleta dados pessoais ou telemetria.
Todas as operações são executadas localmente.

RECURSOS INCLUÍDOS:
⚡ Otimização completa do Windows
💻 Detecção automática de hardware
⏰ Agendamentos automáticos
🔍 Diagnóstico profundo do sistema
🎮 Modo gamer para alto desempenho
🛠️ Ferramentas integradas

Ao continuar com a instalação, você concorda com estes termos."""
        
        licenca_text.insert('1.0', licenca_conteudo)
        licenca_text.config(state='disabled')
        
        # Frame para checkbox e botão
        bottom_frame = tk.Frame(container, bg='#0f0f0f')
        bottom_frame.pack(pady=20, fill=tk.X)
        
        # Checkbox de aceitação
        self.aceitar_licenca = tk.BooleanVar(value=False)
        
        cb = tk.Checkbutton(
            bottom_frame,
            text="✓ Eu li e aceito os termos de licença",
            variable=self.aceitar_licenca,
            font=("Segoe UI", 12, "bold"),
            bg='#0f0f0f',
            fg='#00ff88',
            selectcolor='#1a1a1a',
            activebackground='#0f0f0f',
            activeforeground='#00ff88',
            command=self.atualizar_botao_continuar_welcome
        )
        cb.pack(pady=(0, 20))
        
        # BOTÃO CONTINUAR
        self.btn_continuar_welcome = tk.Button(
            bottom_frame,
            text="CONTINUAR ▶",
            font=("Segoe UI", 14, "bold"),
            bg='#00ff88',
            fg='#000000',
            activebackground='#00dd77',
            command=self.ir_para_configuracao,
            relief=tk.FLAT,
            bd=0,
            padx=50,
            pady=15,
            cursor='hand2',
            state='disabled'
        )
        self.btn_continuar_welcome.pack()
        
        # Botão cancelar
        footer_btns = tk.Frame(container, bg='#0f0f0f')
        footer_btns.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        tk.Button(
            footer_btns,
            text="✕ Cancelar",
            font=("Segoe UI", 10),
            bg='#ff3366',
            fg='#ffffff',
            command=self.cancelar,
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2'
        ).pack(side=tk.LEFT)
    
    def atualizar_botao_continuar_welcome(self):
        """Atualiza estado do botão continuar"""
        if hasattr(self, 'btn_continuar_welcome'):
            if self.aceitar_licenca.get():
                self.btn_continuar_welcome.config(state='normal', bg='#00ff88')
            else:
                self.btn_continuar_welcome.config(state='disabled', bg='#666666')
    
    def ir_para_configuracao(self):
        """Vai para página de configuração"""
        self.mostrar_pagina(1)
    
    def pagina_configuracao(self):
        """Página de configuração"""
        container = tk.Frame(self.content_frame, bg='#0f0f0f')
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        content_area = tk.Frame(container, bg='#0f0f0f')
        content_area.pack(fill=tk.BOTH, expand=True)
        
        titulo = tk.Label(
            content_area,
            text="Configurar Instalação",
            font=("Segoe UI", 16, "bold"),
            bg='#0f0f0f',
            fg='#00ff88'
        )
        titulo.pack(pady=(0, 20))
        
        # Local de instalação
        local_frame = tk.LabelFrame(
            content_area,
            text="📁 Local de Instalação",
            font=("Segoe UI", 12, "bold"),
            bg='#1a1a1a',
            fg='#00ff88',
            bd=0
        )
        local_frame.pack(fill=tk.X, pady=(0, 15))
        
        path_frame = tk.Frame(local_frame, bg='#1a1a1a')
        path_frame.pack(fill=tk.X, padx=15, pady=15)
        
        self.entry_caminho = tk.Entry(
            path_frame,
            font=("Consolas", 11),
            bg='#0f0f0f',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            bd=0
        )
        self.entry_caminho.insert(0, self.caminho_instalacao)
        self.entry_caminho.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        
        btn_procurar = tk.Button(
            path_frame,
            text="📂 Procurar",
            font=("Segoe UI", 10, "bold"),
            bg='#00aaff',
            fg='#ffffff',
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.procurar_pasta
        )
        btn_procurar.pack(side=tk.RIGHT)
        
        espaco_label = tk.Label(
            local_frame,
            text="💾 Espaço necessário: ~50 MB",
            font=("Segoe UI", 9),
            bg='#1a1a1a',
            fg='#888888'
        )
        espaco_label.pack(anchor='w', padx=15, pady=(0, 10))
        
        # Opções adicionais
        opcoes_frame = tk.LabelFrame(
            content_area,
            text="⚙️ Opções Adicionais",
            font=("Segoe UI", 12, "bold"),
            bg='#1a1a1a',
            fg='#00ff88',
            bd=0
        )
        opcoes_frame.pack(fill=tk.X, pady=(0, 15))
        
        cb1 = tk.Checkbutton(
            opcoes_frame,
            text="✓ Criar atalho na Área de Trabalho",
            variable=self.criar_atalho_desktop,
            font=("Segoe UI", 11),
            bg='#1a1a1a',
            fg='#ffffff',
            selectcolor='#0f0f0f',
            activebackground='#1a1a1a',
            activeforeground='#00ff88'
        )
        cb1.pack(anchor='w', padx=15, pady=8)
        
        cb2 = tk.Checkbutton(
            opcoes_frame,
            text="✓ Criar atalho no Menu Iniciar",
            variable=self.criar_atalho_menu,
            font=("Segoe UI", 11),
            bg='#1a1a1a',
            fg='#ffffff',
            selectcolor='#0f0f0f',
            activebackground='#1a1a1a',
            activeforeground='#00ff88'
        )
        cb2.pack(anchor='w', padx=15, pady=8)
        
        info_label = tk.Label(
            content_area,
            text="ℹ️ A instalação levará aproximadamente 2-5 minutos",
            font=("Segoe UI", 10),
            bg='#0f0f0f',
            fg='#888888'
        )
        info_label.pack(pady=(15, 10))
        
        # Botões fixos no rodapé
        btn_container = tk.Frame(container, bg='#0f0f0f')
        btn_container.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        btn_frame = tk.Frame(btn_container, bg='#0f0f0f')
        btn_frame.pack(fill=tk.X)
        
        tk.Button(
            btn_frame,
            text="◀ Voltar",
            font=("Segoe UI", 11, "bold"),
            bg='#3d3d3d',
            fg='#ffffff',
            command=lambda: self.mostrar_pagina(0),
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            btn_frame,
            text="✕ Cancelar",
            font=("Segoe UI", 11, "bold"),
            bg='#ff3366',
            fg='#ffffff',
            command=self.cancelar,
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        ).pack(side=tk.LEFT)
        
        tk.Button(
            btn_frame,
            text="PRÓXIMO ▶",
            font=("Segoe UI", 16, "bold"),
            bg='#00ff88',
            fg='#000000',
            command=lambda: self.mostrar_pagina(2),
            relief=tk.FLAT,
            padx=60,
            pady=18,
            cursor='hand2'
        ).pack(side=tk.RIGHT)
    
    def pagina_resumo(self):
        """Página de resumo"""
        container = tk.Frame(self.content_frame, bg='#0f0f0f')
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Container para o conteúdo com scroll
        canvas = tk.Canvas(container, bg='#0f0f0f', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        content_area = tk.Frame(canvas, bg='#0f0f0f')
        
        content_area.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_area, anchor="nw", width=700)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        titulo = tk.Label(
            content_area,
            text="Pronto para Instalar",
            font=("Segoe UI", 16, "bold"),
            bg='#0f0f0f',
            fg='#00ff88'
        )
        titulo.pack(pady=(0, 20))
        
        # Atualizar caminho de instalação
        if hasattr(self, 'entry_caminho'):
            self.caminho_instalacao = self.entry_caminho.get()
        
        # Frame do resumo
        resumo_frame = tk.LabelFrame(
            content_area,
            text="📦 RESUMO DA INSTALAÇÃO",
            font=("Segoe UI", 12, "bold"),
            bg='#1a1a1a',
            fg='#00ff88',
            bd=0
        )
        resumo_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Informações do programa
        info_programa = tk.Label(
            resumo_frame,
            text="Programa:  ENIAC System Tuner Ultimate v4.0",
            font=("Segoe UI", 10, "bold"),
            bg='#1a1a1a',
            fg='#ffffff',
            anchor='w'
        )
        info_programa.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        # Local de instalação
        info_local = tk.Label(
            resumo_frame,
            text=f"Local:  {self.caminho_instalacao}",
            font=("Consolas", 9),
            bg='#1a1a1a',
            fg='#00aaff',
            anchor='w'
        )
        info_local.pack(fill=tk.X, padx=20, pady=5)
        
        # Espaço necessário
        info_espaco = tk.Label(
            resumo_frame,
            text="Espaço:  ~50 MB",
            font=("Segoe UI", 10),
            bg='#1a1a1a',
            fg='#ffffff',
            anchor='w'
        )
        info_espaco.pack(fill=tk.X, padx=20, pady=5)
        
        # Separador
        sep = tk.Frame(resumo_frame, bg='#333333', height=1)
        sep.pack(fill=tk.X, padx=20, pady=10)
        
        # Opções
        tk.Label(
            resumo_frame,
            text="Opções selecionadas:",
            font=("Segoe UI", 10, "bold"),
            bg='#1a1a1a',
            fg='#ffffff',
            anchor='w'
        ).pack(fill=tk.X, padx=20, pady=(5, 10))
        
        if self.criar_atalho_desktop.get():
            tk.Label(
                resumo_frame,
                text="  ✓ Criar atalho na Área de Trabalho",
                font=("Segoe UI", 9),
                bg='#1a1a1a',
                fg='#00ff88',
                anchor='w'
            ).pack(fill=tk.X, padx=30, pady=2)
        else:
            tk.Label(
                resumo_frame,
                text="  ✗ Atalho na Área de Trabalho",
                font=("Segoe UI", 9),
                bg='#1a1a1a',
                fg='#666666',
                anchor='w'
            ).pack(fill=tk.X, padx=30, pady=2)
        
        if self.criar_atalho_menu.get():
            tk.Label(
                resumo_frame,
                text="  ✓ Criar atalho no Menu Iniciar",
                font=("Segoe UI", 9),
                bg='#1a1a1a',
                fg='#00ff88',
                anchor='w'
            ).pack(fill=tk.X, padx=30, pady=2)
        else:
            tk.Label(
                resumo_frame,
                text="  ✗ Atalho no Menu Iniciar",
                font=("Segoe UI", 9),
                bg='#1a1a1a',
                fg='#666666',
                anchor='w'
            ).pack(fill=tk.X, padx=30, pady=2)
        
        # Espaçamento final
        tk.Label(resumo_frame, text="", bg='#1a1a1a').pack(pady=5)
        
        # Mensagem informativa
        msg_label = tk.Label(
            content_area,
            text="ℹ️ Clique em 'INSTALAR AGORA' para iniciar a instalação",
            font=("Segoe UI", 11),
            bg='#0f0f0f',
            fg='#888888'
        )
        msg_label.pack(pady=(10, 20))
        
        # Empacotar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Área de botões fixa no rodapé
        btn_container = tk.Frame(self.content_frame, bg='#0f0f0f')
        btn_container.pack(side=tk.BOTTOM, fill=tk.X, padx=40, pady=(10, 20))
        
        btn_frame = tk.Frame(btn_container, bg='#0f0f0f')
        btn_frame.pack(fill=tk.X)
        
        # Botão Voltar
        tk.Button(
            btn_frame,
            text="◀ Voltar",
            font=("Segoe UI", 11, "bold"),
            bg='#3d3d3d',
            fg='#ffffff',
            command=lambda: self.mostrar_pagina(1),
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão Cancelar
        tk.Button(
            btn_frame,
            text="✕ Cancelar",
            font=("Segoe UI", 11, "bold"),
            bg='#ff3366',
            fg='#ffffff',
            command=self.cancelar,
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        ).pack(side=tk.LEFT)
        
        # Botão INSTALAR AGORA
        btn_instalar = tk.Button(
            btn_frame,
            text="🚀 INSTALAR AGORA",
            font=("Segoe UI", 16, "bold"),
            bg='#00ff88',
            fg='#000000',
            activebackground='#00dd77',
            command=lambda: self.iniciar_instalacao_real(),
            relief=tk.FLAT,
            bd=0,
            padx=60,
            pady=18,
            cursor='hand2'
        )
        btn_instalar.pack(side=tk.RIGHT)
    
    def iniciar_instalacao_real(self):
        """Inicia o processo de instalação"""
        self.root.update()
        self.mostrar_pagina(3)
    
    def pagina_instalacao(self):
        """Página de instalação com progresso"""
        from tkinter import scrolledtext
        
        container = tk.Frame(self.content_frame, bg='#0f0f0f')
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        titulo = tk.Label(
            container,
            text="Instalando...",
            font=("Segoe UI", 16, "bold"),
            bg='#0f0f0f',
            fg='#00ff88'
        )
        titulo.pack(pady=(0, 30))
        
        # Status
        self.status_label = tk.Label(
            container,
            text="Preparando instalação...",
            font=("Segoe UI", 12),
            bg='#0f0f0f',
            fg='#ffffff'
        )
        self.status_label.pack(pady=(0, 20))
        
        # Barra de progresso
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Install.Horizontal.TProgressbar",
                       troughcolor='#1a1a1a',
                       background='#00ff88',
                       bordercolor='#1a1a1a',
                       lightcolor='#00ff88',
                       darkcolor='#00ff88',
                       thickness=30)
        
        self.progress = ttk.Progressbar(
            container,
            length=700,
            mode='determinate',
            style="Install.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=(0, 20))
        
        # Porcentagem
        self.percent_label = tk.Label(
            container,
            text="0%",
            font=("Segoe UI", 14, "bold"),
            bg='#0f0f0f',
            fg='#00ff88'
        )
        self.percent_label.pack(pady=(0, 30))
        
        # Log
        log_frame = tk.LabelFrame(
            container,
            text="📋 Detalhes",
            font=("Segoe UI", 10, "bold"),
            bg='#1a1a1a',
            fg='#00ff88',
            bd=0
        )
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg='#0d0d0d',
            fg='#00ff88',
            wrap=tk.WORD,
            relief=tk.FLAT,
            height=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Iniciar instalação
        self.instalando = True
        thread = threading.Thread(target=self.executar_instalacao, daemon=True)
        thread.start()
    
    def pagina_concluido(self):
        """Página de conclusão"""
        container = tk.Frame(self.content_frame, bg='#0f0f0f')
        container.pack(fill=tk.BOTH, expand=True)
        
        center_frame = tk.Frame(container, bg='#0f0f0f')
        center_frame.place(relx=0.5, rely=0.45, anchor='center')
        
        # Ícone de sucesso
        check_label = tk.Label(
            center_frame,
            text="✓",
            font=("Segoe UI", 72, "bold"),
            bg='#0f0f0f',
            fg='#00ff88'
        )
        check_label.pack(pady=(0, 20))
        
        titulo = tk.Label(
            center_frame,
            text="Instalação Concluída!",
            font=("Segoe UI", 20, "bold"),
            bg='#0f0f0f',
            fg='#00ff88'
        )
        titulo.pack(pady=(0, 20))
        
        texto = f"""
        O ENIAC System Tuner foi instalado com sucesso!
        
        Local: {self.caminho_instalacao}
        
        Você pode iniciar o programa de três formas:
        
        {"✓ Atalho na Área de Trabalho" if self.criar_atalho_desktop.get() else ""}
        {"✓ Menu Iniciar > ENIAC System Tuner" if self.criar_atalho_menu.get() else ""}
        ✓ Executável em: {self.caminho_instalacao}
        
        Lembre-se: Execute sempre como Administrador!
        """
        
        label_texto = tk.Label(
            center_frame,
            text=texto,
            font=("Segoe UI", 11),
            bg='#0f0f0f',
            fg='#ffffff',
            justify=tk.CENTER
        )
        label_texto.pack(pady=(0, 20))
        
        # Checkbox para executar
        self.executar_agora = tk.BooleanVar(value=True)
        
        cb = tk.Checkbutton(
            center_frame,
            text="🚀 Executar ENIAC System Tuner agora",
            variable=self.executar_agora,
            font=("Segoe UI", 11, "bold"),
            bg='#0f0f0f',
            fg='#00ff88',
            selectcolor='#1a1a1a'
        )
        cb.pack(pady=(0, 30))
        
        # BOTÃO CONCLUIR
        tk.Button(
            center_frame,
            text="CONCLUIR ✓",
            font=("Segoe UI", 14, "bold"),
            bg='#00ff88',
            fg='#000000',
            command=self.concluir,
            relief=tk.FLAT,
            padx=50,
            pady=15,
            cursor='hand2'
        ).pack()
    
    def procurar_pasta(self):
        """Abre diálogo para escolher pasta"""
        pasta = filedialog.askdirectory(
            title="Escolher Local de Instalação",
            initialdir="C:\\Program Files"
        )
        if pasta:
            self.caminho_instalacao = os.path.join(pasta, "ESTU")
            self.entry_caminho.delete(0, tk.END)
            self.entry_caminho.insert(0, self.caminho_instalacao)
    
    def cancelar(self):
        """Cancela instalação"""
        if self.instalando:
            return
        
        resposta = messagebox.askyesno(
            "Cancelar Instalação",
            "Deseja realmente cancelar a instalação?"
        )
        if resposta:
            self.root.quit()
    
    def concluir(self):
        """Conclui instalação"""
        if self.executar_agora.get():
            launcher_path = os.path.join(self.caminho_instalacao, "ENIAC_Launcher.exe")
            if os.path.exists(launcher_path):
                try:
                    subprocess.Popen([launcher_path])
                except:
                    pass
        
        self.root.quit()
    
    def log(self, mensagem):
        """Adiciona mensagem ao log"""
        try:
            self.log_text.insert(tk.END, f"{mensagem}\n")
            self.log_text.see(tk.END)
            self.root.update()
        except:
            pass
    
    def atualizar_progresso(self, valor, status):
        """Atualiza barra de progresso"""
        try:
            self.progress['value'] = valor
            self.percent_label.config(text=f"{int(valor)}%")
            self.status_label.config(text=status)
            self.root.update()
        except:
            pass
    
    def executar_instalacao(self):
        """Executa processo de instalação REAL"""
        try:
            # 1. Verificar dependências e arquivos
            self.atualizar_progresso(5, "Verificando arquivos...")
            self.log("[5%] Verificando arquivos necessários...")
            
            arquivos_necessarios = ['eniac_tuner.py', 'launcher.py']
            pasta_atual = Path(__file__).parent
            
            arquivos_encontrados = []
            for arquivo in arquivos_necessarios:
                caminho = pasta_atual / arquivo
                if caminho.exists():
                    self.log(f"  ✓ {arquivo} encontrado")
                    arquivos_encontrados.append(caminho)
                else:
                    self.log(f"  ✗ {arquivo} NÃO ENCONTRADO!")
            
            if len(arquivos_encontrados) < len(arquivos_necessarios):
                raise Exception("Arquivos necessários não encontrados na pasta do instalador")
            
            time.sleep(0.5)
            
            # 2. Criar diretório de instalação
            self.atualizar_progresso(15, "Criando diretório de instalação...")
            self.log("[15%] Criando diretório de instalação...")
            
            pasta_destino = Path(self.caminho_instalacao)
            if pasta_destino.exists():
                self.log("  ⚠ Diretório já existe, será substituído")
                try:
                    shutil.rmtree(pasta_destino)
                except:
                    pass
            
            pasta_destino.mkdir(parents=True, exist_ok=True)
            self.log(f"  ✓ Diretório criado: {pasta_destino}")
            time.sleep(0.5)
            
            # 3. Copiar arquivos
            self.atualizar_progresso(30, "Copiando arquivos do programa...")
            self.log("[30%] Copiando arquivos...")
            
            for arquivo_origem in arquivos_encontrados:
                arquivo_destino = pasta_destino / arquivo_origem.name
                shutil.copy2(arquivo_origem, arquivo_destino)
                self.log(f"  ✓ Copiado: {arquivo_origem.name}")
                time.sleep(0.3)
            
            # 4. Criar arquivo batch de inicialização
            self.atualizar_progresso(50, "Configurando sistema...")
            self.log("[50%] Criando launcher...")
            
            batch_content = f"""@echo off
title ENIAC System Tuner
cd /d "{pasta_destino}"

:: Verificar admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Solicitando privilegios de administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Executar programa principal
python launcher.py
if errorlevel 1 (
    python eniac_tuner.py
)

exit
"""
            
            launcher_bat = pasta_destino / "ENIAC_Launcher.bat"
            with open(launcher_bat, 'w', encoding='utf-8') as f:
                f.write(batch_content)
            self.log("  ✓ Launcher criado")
            time.sleep(0.5)
            
            # 5. Criar atalhos
            self.atualizar_progresso(70, "Criando atalhos...")
            self.log("[70%] Criando atalhos...")
            
            if self.criar_atalho_desktop.get():
                try:
                    self.criar_atalho_windows(
                        nome="ENIAC System Tuner",
                        destino=str(launcher_bat),
                        local="Desktop"
                    )
                    self.log("  ✓ Atalho na Área de Trabalho criado")
                except Exception as e:
                    self.log(f"  ⚠ Atalho Desktop: {e}")
            
            if self.criar_atalho_menu.get():
                try:
                    self.criar_atalho_windows(
                        nome="ENIAC System Tuner",
                        destino=str(launcher_bat),
                        local="StartMenu"
                    )
                    self.log("  ✓ Atalho no Menu Iniciar criado")
                except Exception as e:
                    self.log(f"  ⚠ Atalho Menu Iniciar: {e}")
            
            time.sleep(0.5)
            
            # 6. Registrar no sistema
            self.atualizar_progresso(85, "Registrando aplicação...")
            self.log("[85%] Registrando no sistema...")
            
            try:
                self.registrar_app()
                self.log("  ✓ Aplicação registrada")
            except Exception as e:
                self.log(f"  ⚠ Registro: {e}")
            
            time.sleep(0.5)
            
            # 7. Finalizar
            self.atualizar_progresso(100, "✓ Instalação concluída!")
            self.log("[100%] ✓ INSTALAÇÃO CONCLUÍDA!")
            self.log("")
            self.log("=" * 60)
            self.log("✓ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
            self.log("=" * 60)
            self.log(f"Local: {pasta_destino}")
            self.log("")
            
            time.sleep(1)
            self.instalando = False
            self.mostrar_pagina(4)
            
        except Exception as e:
            self.log(f"\n✗ ERRO: {e}")
            messagebox.showerror("Erro na Instalação", f"Ocorreu um erro:\n\n{e}")
            self.instalando = False
    
    def criar_atalho_windows(self, nome, destino, local="Desktop"):
        """Cria atalho no Windows"""
        try:
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            
            if local == "Desktop":
                pasta_atalhos = shell.SpecialFolders("Desktop")
            elif local == "StartMenu":
                pasta_atalhos = shell.SpecialFolders("Programs")
            else:
                pasta_atalhos = local
            
            caminho_atalho = os.path.join(pasta_atalhos, f"{nome}.lnk")
            atalho = shell.CreateShortCut(caminho_atalho)
            atalho.Targetpath = destino
            atalho.WorkingDirectory = os.path.dirname(destino)
            atalho.IconLocation = destino
            atalho.save()
            
        except ImportError:
            # Se win32com não estiver disponível, criar manualmente com PowerShell
            if local == "Desktop":
                pasta_atalhos = str(Path.home() / "Desktop")
            elif local == "StartMenu":
                pasta_atalhos = str(Path(os.environ['APPDATA']) / "Microsoft" / "Windows" / "Start Menu" / "Programs")
            else:
                pasta_atalhos = local
            
            caminho_atalho = os.path.join(pasta_atalhos, f"{nome}.lnk")
            
            ps_script = f"""
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{caminho_atalho}")
$Shortcut.TargetPath = "{destino}"
$Shortcut.WorkingDirectory = "{os.path.dirname(destino)}"
$Shortcut.Save()
"""
            
            subprocess.run(["powershell", "-Command", ps_script], check=True, capture_output=True)
    
    def registrar_app(self):
        """Registra aplicação no Windows"""
        try:
            # Registrar no registro do Windows
            chave = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Uninstall\ENIACSystemTuner"
            )
            
            winreg.SetValueEx(chave, "DisplayName", 0, winreg.REG_SZ, "ENIAC System Tuner v4.0")
            winreg.SetValueEx(chave, "DisplayVersion", 0, winreg.REG_SZ, "4.0")
            winreg.SetValueEx(chave, "Publisher", 0, winreg.REG_SZ, "ENIAC System Tuner")
            winreg.SetValueEx(chave, "InstallLocation", 0, winreg.REG_SZ, self.caminho_instalacao)
            winreg.SetValueEx(chave, "UninstallString", 0, winreg.REG_SZ, 
                            f'cmd /c rmdir /s /q "{self.caminho_instalacao}"')
            
            winreg.CloseKey(chave)
        except:
            pass

def main():
    root = tk.Tk()
    app = InstaladorENIAC(root)
    root.mainloop()

if __name__ == "__main__":
    main()