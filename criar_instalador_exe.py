"""
CRIADOR DE INSTALADOR EXECUTÁVEL COMPLETO
ENIAC SYSTEM TUNER v4.0
Cria um instalador .exe standalone completo
"""

import os
import sys
import subprocess
import shutil
import json
import time
from pathlib import Path

def print_header():
    """Cabeçalho do criador"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 80)
    print(" " * 20 + "🚀 CRIADOR DE INSTALADOR EXECUTÁVEL")
    print(" " * 23 + "ENIAC SYSTEM TUNER v4.0")
    print("=" * 80)
    print()

def verificar_arquivos_necessarios():
    """Verifica se todos os arquivos necessários existem"""
    print("[1/7] Verificando arquivos necessários...")
    print()
    
    arquivos_necessarios = [
        'instalador_gui.py',
        'launcher.py',
        'eniac_tuner.py'
    ]
    
    arquivos_encontrados = []
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"  ✅ {arquivo} encontrado")
            arquivos_encontrados.append(arquivo)
        else:
            print(f"  ❌ {arquivo} NÃO ENCONTRADO!")
    
    print()
    
    # Verificar também as imagens/ícones se existirem
    arquivos_opcionais = ['icon.ico', 'logo.png', 'background.jpg']
    for arquivo in arquivos_opcionais:
        if os.path.exists(arquivo):
            print(f"  📁 {arquivo} (opcional) encontrado")
    
    print()
    return len(arquivos_encontrados) == len(arquivos_necessarios)

def verificar_python_e_dependencias():
    """Verifica versão do Python e dependências"""
    print("[2/7] Verificando ambiente Python...")
    print()
    
    # Verificar versão do Python
    python_version = sys.version_info
    print(f"  Python: {sys.version.split()[0]}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("  ⚠️  Recomendado: Python 3.7 ou superior")
    
    # Verificar dependências
    dependencias = ['psutil', 'pyinstaller']
    
    for dep in dependencias:
        try:
            if dep == 'pyinstaller':
                import PyInstaller
                print(f"  ✅ PyInstaller disponível")
            elif dep == 'psutil':
                import psutil
                print(f"  ✅ psutil disponível")
        except ImportError:
            print(f"  ⚠️  {dep} não instalado")
    
    print()
    return True

def instalar_dependencias():
    """Instala dependências necessárias"""
    print("[3/7] Instalando/verificando dependências...")
    print()
    
    dependencias = [
        'psutil>=5.9.0',
        'pyinstaller>=5.13.0'
    ]
    
    for dep in dependencias:
        print(f"  Verificando {dep}...")
        try:
            # Extrair nome do pacote
            nome_pacote = dep.split('>=')[0] if '>=' in dep else dep
            nome_pacote = nome_pacote.split('<=')[0] if '<=' in dep else nome_pacote
            
            __import__(nome_pacote)
            print(f"    ✅ {nome_pacote} já instalado")
        except ImportError:
            print(f"    📦 Instalando {dep}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"    ✅ {dep} instalado")
            except subprocess.CalledProcessError:
                print(f"    ❌ Falha ao instalar {dep}")
                return False
    
    print()
    return True

def criar_arquivo_configuracao():
    """Cria arquivo de configuração para o instalador"""
    print("[4/7] Criando configurações do instalador...")
    print()
    
    config = {
        'nome_programa': 'ENIAC System Tuner Ultimate v4.0',
        'versao': '4.0.0',
        'empresa': 'ENIAC System Tuner',
        'copyright': 'Copyright © 2025 ENIAC System Tuner. Todos os direitos reservados.',
        'pasta_padrao': 'C:\\Program Files\\ESTU',
        'espaco_necessario_mb': 50,
        'tempo_instalacao_min': 5,
        'requer_admin': True,
        'sistemas_suportados': ['Windows 10', 'Windows 11'],
        'arquivos_principais': ['eniac_tuner.py', 'launcher.py']
    }
    
    try:
        with open('config_instalador.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print("  ✅ Arquivo de configuração criado")
    except Exception as e:
        print(f"  ⚠️  Não foi possível criar configuração: {e}")
    
    print()
    return True

def criar_arquivo_licenca_temp():
    """Cria arquivo de licença temporário"""
    print("  Criando arquivo de licença...")
    
    licenca = """ENIAC SYSTEM TUNER ULTIMATE v4.0 - TERMOS DE LICENÇA

1. ACEITAÇÃO DOS TERMOS
Ao instalar e usar o ENIAC System Tuner, você concorda com estes termos.

2. LICENÇA DE USO
Concedemos uma licença pessoal, não exclusiva e intransferível para usar o software.

3. RESTRIÇÕES
Não é permitido:
- Distribuir comercialmente sem autorização
- Engenharia reversa
- Remover marcas ou créditos

4. ISENÇÃO DE GARANTIA
O software é fornecido "COMO ESTÁ", sem garantias de qualquer tipo.

5. COLETA DE DADOS
Este software NÃO coleta dados pessoais. Todas as operações são locais.

6. LIMITAÇÃO DE RESPONSABILIDADE
Não nos responsabilizamos por danos diretos ou indiretos.

7. CONTATO
Para suporte, entre em contato com o desenvolvedor.

Copyright © 2025 ENIAC System Tuner. Todos os direitos reservados.
"""
    
    try:
        with open('licenca_temp.txt', 'w', encoding='utf-8') as f:
            f.write(licenca)
        print("  ✅ Arquivo de licença criado")
    except Exception as e:
        print(f"  ⚠️  Não foi possível criar licença: {e}")
    
    return True

def compilar_com_pyinstaller():
    """Compila o instalador usando PyInstaller"""
    print("[5/7] Compilando instalador executável...")
    print()
    print("  ⏳ Esta etapa pode levar 3-10 minutos...")
    print("  🔧 Por favor, aguarde enquanto compilamos tudo em um único executável.")
    print()
    
    # Obter caminho absoluto da pasta atual
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Limpar builds anteriores
    for pasta in ['build', 'dist', '__pycache__']:
        caminho_pasta = Path(pasta)
        if caminho_pasta.exists():
            try:
                shutil.rmtree(caminho_pasta)
                print(f"  🗑️  Limpado: {pasta}")
            except Exception as e:
                print(f"  ⚠️  Não foi possível limpar {pasta}: {e}")
    
    time.sleep(1)
    
    # Preparar comando PyInstaller
    print("\n  📦 Configurando PyInstaller...")
    
    # Verificar se temos ícone
    tem_icone = os.path.exists('icon.ico')
    
    # Construir comando
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",                    # Um único arquivo executável
        "--noconsole",                  # Sem janela de console
        "--name=ENIAC_Installer",       # Nome do executável
        "--clean",                      # Limpar cache
        "--windowed",                   # Aplicação com janela
        "--noupx",                      # Desativar UPX (mais estável)
    ]
    
    # Adicionar ícone se existir
    if tem_icone:
        cmd.append("--icon=icon.ico")
        print("  🖼️  Ícone personalizado detectado")
    
    # Adicionar arquivos de dados
    arquivos_para_embutir = ['launcher.py', 'eniac_tuner.py']
    
    for arquivo in arquivos_para_embutir:
        if os.path.exists(arquivo):
            cmd.extend(["--add-data", f"{arquivo};."])
            print(f"  ➕ Embutindo: {arquivo}")
    
    # Adicionar imports ocultos necessários
    imports_ocultos = [
        'tkinter', 'psutil', 'winreg', 'json', 'pathlib',
        'datetime', 'shutil', 'threading', 'subprocess',
        'os', 'sys', 'ctypes'
    ]
    
    for import_ in imports_ocultos:
        cmd.extend(["--hidden-import", import_])
    
    # Adicionar arquivo principal
    cmd.append("instalador_gui.py")
    
    print(f"\n  🔨 Comando PyInstaller:")
    print(f"     {' '.join(cmd[:10])}...")
    print()
    
    # Executar PyInstaller
    try:
        print("  ⚙️  Iniciando compilação...")
        
        # Criar processo
        processo = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        # Mostrar progresso
        for i in range(1, 101, 10):
            if i <= 90:  # PyInstaller geralmente fica em 90% por um tempo
                print(f"  📊 Progresso: {i}%", end='\r')
                time.sleep(0.5)
        
        # Esperar conclusão
        stdout, stderr = processo.communicate(timeout=600)  # 10 minutos timeout
        
        if processo.returncode == 0:
            print("  📊 Progresso: 100%")
            print("\n  ✅ Compilação concluída com sucesso!")
            
            # Verificar se o executável foi criado
            exe_path = Path('dist') / 'ENIAC_Installer.exe'
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"  📁 Executável criado: {exe_path}")
                print(f"  📏 Tamanho: {size_mb:.1f} MB")
                return True, exe_path
            else:
                print("  ❌ Executável não foi criado!")
                return False, None
        else:
            print("  ❌ Erro na compilação!")
            if stderr:
                print(f"  Detalhes do erro:\n{stderr[:500]}")
            return False, None
            
    except subprocess.TimeoutExpired:
        print("  ⏰ Timeout - Compilação demorou muito!")
        print("  💡 Tente novamente ou use um computador mais rápido.")
        return False, None
    except Exception as e:
        print(f"  ❌ Erro inesperado: {e}")
        return False, None

def verificar_assinatura_e_seguranca(exe_path):
    """Verifica e sugere assinatura digital (opcional)"""
    print("[6/7] Verificando segurança do executável...")
    print()
    
    if not exe_path or not os.path.exists(exe_path):
        print("  ⚠️  Executável não encontrado para verificação")
        return False
    
    try:
        # Verificar se o arquivo é válido
        import hashlib
        
        with open(exe_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        
        print(f"  ✅ Executável válido")
        print(f"  📏 Tamanho: {size_mb:.1f} MB")
        print(f"  🔒 Hash SHA-256: {file_hash[:32]}...")
        print()
        
        # Aviso sobre assinatura digital
        print("  ⚠️  AVISO IMPORTANTE:")
        print("  O Windows Defender/SmartScreen pode bloquear o executável.")
        print("  Para distribuição pública, considere:")
        print("  1. Assinatura digital certificada")
        print("  2. Submeter à Microsoft para análise")
        print("  3. Usar certificado EV para confiança imediata")
        print()
        
        return True
        
    except Exception as e:
        print(f"  ⚠️  Não foi possível verificar segurança: {e}")
        return False

def criar_pacote_distribuicao(exe_path):
    """Cria pacote final para distribuição"""
    print("[7/7] Criando pacote de distribuição...")
    print()
    
    # Nome da pasta de distribuição
    nome_pacote = "ENIAC_System_Tuner_v4.0_Installer_Package"
    
    # Limpar pacote anterior se existir
    if os.path.exists(nome_pacote):
        try:
            shutil.rmtree(nome_pacote)
            print(f"  🗑️  Limpado pacote anterior")
        except:
            pass
    
    # Criar pasta
    os.makedirs(nome_pacote, exist_ok=True)
    print(f"  📁 Criada pasta: {nome_pacote}")
    
    # Copiar executável
    if exe_path and os.path.exists(exe_path):
        shutil.copy2(exe_path, os.path.join(nome_pacote, "ENIAC_Installer.exe"))
        print("  ✅ Executável copiado")
    
    # Criar arquivo README detalhado
    readme_content = """
╔════════════════════════════════════════════════════════════════════╗
║                ENIAC SYSTEM TUNER ULTIMATE v4.0                   ║
║                PACOTE DE INSTALAÇÃO OFICIAL                       ║
╚════════════════════════════════════════════════════════════════════╝

📦 INFORMAÇÕES DO PROGRAMA:
• Nome: ENIAC System Tuner Ultimate Edition
• Versão: 4.0.0
• Desenvolvedor: ENIAC System Tuner
• Data: """ + time.strftime("%d/%m/%Y") + """
• Tamanho: ~50 MB (após instalação)

🎯 RECURSOS PRINCIPAIS:
⚡ Otimização Completa do Windows
💻 Detecção Automática de Hardware
⏰ Agendamentos Automáticos
🔍 Diagnóstico Profundo do Sistema
🎮 Modo Gamer para Alto Desempenho
🛠️ Ferramentas Integradas do Windows

🚀 COMO INSTALAR:

1. ANTES DE INSTALAR:
   • Crie um ponto de restauração do sistema
   • Feche todos os programas abertos
   • Conecte o computador à energia (para notebooks)

2. PROCESSO DE INSTALAÇÃO:
   a) Clique com botão direito em 'ENIAC_Installer.exe'
   b) Selecione 'Executar como administrador'
   c) Siga o assistente de instalação
   d) Reinicie o computador após a instalação

3. APÓS INSTALAÇÃO:
   • Execute sempre como administrador
   • Use o atalho na Área de Trabalho
   • Ou: Menu Iniciar > ENIAC System Tuner

⚠️ IMPORTANTE:

• REQUER: Windows 10/11 (64-bit)
• REQUER: Privilégios de administrador
• RECOMENDADO: 2 GB RAM, 50 MB espaço livre
• AVISO: Alguns antivírus podem detectar como falso positivo

🔧 SOLUÇÃO DE PROBLEMAS:

1. Se o instalador não abrir:
   • Execute como administrador
   • Desative temporariamente o antivírus
   • Verifique se o Windows está atualizado

2. Se o programa não funcionar:
   • Execute como administrador
   • Verifique se tem Python 3.7+ instalado
   • Reinstale o programa

3. Otimização não funciona completamente:
   • Execute como administrador
   • Reinicie o computador após otimização

📞 SUPORTE:

Para suporte técnico, entre em contato com o desenvolvedor.

• Email: suporte@eniacsystemtuner.com
• Site: www.eniacsystemtuner.com
• Documentação: Incluída no programa

⚖️ INFORMAÇÕES LEGAIS:

Copyright © 2025 ENIAC System Tuner. Todos os direitos reservados.
Este software é fornecido "como está", sem garantias de qualquer tipo.

════════════════════════════════════════════════════════════════════

Gerado automaticamente pelo Criador de Instalador ENIAC v1.0
"""
    
    try:
        with open(os.path.join(nome_pacote, "LEIA-ME.txt"), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("  ✅ Arquivo LEIA-ME criado")
    except Exception as e:
        print(f"  ⚠️  Não foi possível criar LEIA-ME: {e}")
    
    # Criar arquivo de desinstalação
    desinstalador_content = f"""@echo off
chcp 65001 >nul
title Desinstalador ENIAC System Tuner v4.0
echo ========================================
echo    DESINSTALADOR ENIAC SYSTEM TUNER
echo ========================================
echo.
echo AVISO: Isso removerá completamente o ENIAC System Tuner.
echo.
set /p confirm="Digite 'S' para confirmar desinstalação: "
if /i "%confirm%" neq "S" (
    echo.
    echo Desinstalação cancelada.
    pause
    exit /b
)

echo.
echo Parando processos do ENIAC...
taskkill /f /im python.exe /t 2>nul
timeout /t 2 /nobreak >nul

echo Removendo arquivos...
rmdir /s /q "C:\\Program Files\\ESTU" 2>nul

echo Removendo atalhos...
del "%USERPROFILE%\\Desktop\\ENIAC System Tuner.lnk" 2>nul
del "%USERPROFILE%\\Desktop\\ENIAC System Tuner.url" 2>nul

echo Removendo do registro...
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ENIACSystemTuner" /f 2>nul

echo.
echo ========================================
echo    DESINSTALAÇÃO CONCLUÍDA!
echo ========================================
echo.
echo O ENIAC System Tuner foi removido do sistema.
echo.
pause
"""
    
    try:
        with open(os.path.join(nome_pacote, "Desinstalar.bat"), 'w', encoding='utf-8') as f:
            f.write(desinstalador_content)
        print("  ✅ Script de desinstalação criado")
    except Exception as e:
        print(f"  ⚠️  Não foi possível criar desinstalador: {e}")
    
    # Criar arquivo de verificação
    verificar_content = """@echo off
chcp 65001 >nul
title Verificador de Sistema ENIAC
echo ========================================
echo    VERIFICADOR DE SISTEMA
echo    ENIAC SYSTEM TUNER v4.0
echo ========================================
echo.
echo Verificando requisitos do sistema...
echo.

:: Verificar Windows
ver | find "Windows 10" >nul
if %errorlevel% equ 0 (
    echo ✅ Windows 10 detectado
) else (
    ver | find "Windows 11" >nul
    if %errorlevel% equ 0 (
        echo ✅ Windows 11 detectado
    ) else (
        echo ⚠️  Versão do Windows não suportada
    )
)

:: Verificar arquitetura
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo ✅ Sistema 64-bit
) else (
    echo ❌ Sistema 32-bit não suportado
)

:: Verificar Python
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Python instalado
) else (
    echo ⚠️  Python não encontrado
)

:: Verificar permissões
net session >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Executando como administrador
) else (
    echo ❌ Execute como administrador!
)

echo.
echo ========================================
echo Verificação concluída!
echo.
pause
"""
    
    try:
        with open(os.path.join(nome_pacote, "Verificar_Sistema.bat"), 'w', encoding='utf-8') as f:
            f.write(verificar_content)
        print("  ✅ Verificador de sistema criado")
    except Exception as e:
        print(f"  ⚠️  Não foi possível criar verificador: {e}")
    
    # Copiar licença
    if os.path.exists('licenca_temp.txt'):
        try:
            shutil.copy2('licenca_temp.txt', os.path.join(nome_pacote, "LICENCA.txt"))
            print("  ✅ Licença copiada")
        except:
            pass
    
    print(f"\n  📦 Pacote completo criado em: {nome_pacote}")
    print(f"  📁 Conteúdo:")
    for item in os.listdir(nome_pacote):
        item_path = os.path.join(nome_pacote, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path) / 1024
            print(f"     • {item} ({size:.1f} KB)")
    
    return nome_pacote

def limpar_arquivos_temporarios():
    """Limpa arquivos temporários criados durante o processo"""
    print("\n🧹 Limpando arquivos temporários...")
    
    arquivos_para_remover = [
        'config_instalador.json',
        'licenca_temp.txt',
        'bootstrap.bat'
    ]
    
    pastas_para_remover = ['__pycache__']
    
    # Remover arquivos
    for arquivo in arquivos_para_remover:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"  🗑️  Removido: {arquivo}")
            except:
                pass
    
    # Remover pastas
    for pasta in pastas_para_remover:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"  🗑️  Removido: {pasta}")
            except:
                pass
    
    # Remover arquivos .spec
    for spec in Path('.').glob('*.spec'):
        try:
            spec.unlink()
            print(f"  🗑️  Removido: {spec.name}")
        except:
            pass
    
    print("  ✅ Limpeza concluída")
    print()

def mostrar_resumo_final(pacote_nome, sucesso):
    """Mostra resumo final do processo"""
    print("\n" + "=" * 80)
    
    if sucesso:
        print("🎉 INSTALADOR CRIADO COM SUCESSO!")
        print("=" * 80)
        print()
        print("📦 SEU INSTALADOR ESTÁ PRONTO!")
        print()
        print(f"📍 Local: {pacote_nome}\\")
        print()
        print("📁 Conteúdo do pacote:")
        print("   • ENIAC_Installer.exe - Instalador principal")
        print("   • LEIA-ME.txt - Instruções detalhadas")
        print("   • Desinstalar.bat - Script de desinstalação")
        print("   • Verificar_Sistema.bat - Verificador de requisitos")
        print("   • LICENCA.txt - Termos de licença")
        print()
        print("🚀 PARA DISTRIBUIR:")
        print(f"   1. Comprima a pasta em ZIP: {pacote_nome}.zip")
        print("   2. Envie o ZIP para seus usuários")
        print("   3. Ou copie a pasta para um pendrive/CD")
        print()
        print("⚡ PARA INSTALAR:")
        print("   1. Execute 'ENIAC_Installer.exe' como ADMINISTRADOR")
        print("   2. Siga o assistente de instalação")
        print("   3. Reinicie o computador após instalação")
        print()
        print("⚠️  IMPORTANTE:")
        print("   • Windows Defender pode bloquear inicialmente")
        print("   • Sempre execute como administrador")
        print("   • Crie ponto de restauração antes de usar")
    else:
        print("❌ FALHA AO CRIAR INSTALADOR")
        print("=" * 80)
        print()
        print("😞 Ocorreu um erro durante a criação do instalador.")
        print()
        print("🔧 SOLUÇÕES POSSÍVEIS:")
        print("   1. Execute como administrador")
        print("   2. Verifique se tem todos os arquivos na pasta:")
        print("      - instalador_gui.py")
        print("      - eniac_tuner.py")
        print("      - launcher.py")
        print("   3. Atualize o PyInstaller:")
        print("      pip install --upgrade pyinstaller")
        print("   4. Tente em outro computador")
        print()
        print("📞 Se o problema persistir, contate o desenvolvedor.")
    
    print("=" * 80)
    print()

def main():
    """Função principal"""
    try:
        # Mostrar cabeçalho
        print_header()
        
        # Verificar se está sendo executado como administrador (recomendado)
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("⚠️  AVISO: Execute como administrador para melhores resultados")
                print("   (Clique direito > Executar como administrador)")
                print()
        except:
            pass
        
        # Passo 1: Verificar arquivos
        if not verificar_arquivos_necessarios():
            print("❌ Arquivos necessários não encontrados!")
            print("\nCertifique-se de ter na mesma pasta:")
            print("  • instalador_gui.py")
            print("  • eniac_tuner.py")
            print("  • launcher.py")
            input("\nPressione Enter para sair...")
            return
        
        # Passo 2: Verificar Python
        verificar_python_e_dependencias()
        
        # Passo 3: Instalar dependências
        if not instalar_dependencias():
            print("⚠️  Algumas dependências não puderam ser instaladas")
            resposta = input("Deseja continuar mesmo assim? (S/N): ")
            if resposta.upper() != 'S':
                return
        
        # Passo 4: Criar configurações
        criar_arquivo_configuracao()
        criar_arquivo_licenca_temp()
        
        # Passo 5: Compilar
        sucesso_compilacao, exe_path = compilar_com_pyinstaller()
        
        if not sucesso_compilacao:
            print("\n❌ Falha na compilação do instalador!")
            print("Tente as seguintes soluções:")
            print("1. Execute como administrador")
            print("2. pip install --upgrade pyinstaller")
            print("3. pip install pyinstaller-hooks-contrib")
            print("4. Tente em outro computador")
            input("\nPressione Enter para sair...")
            return
        
        # Passo 6: Verificar segurança
        verificar_assinatura_e_seguranca(exe_path)
        
        # Passo 7: Criar pacote
        pacote_nome = criar_pacote_distribuicao(exe_path)
        
        # Limpar temporários
        limpar_arquivos_temporarios()
        
        # Mostrar resumo
        mostrar_resumo_final(pacote_nome, True)
        
        # Perguntar se quer testar
        print("\n🧪 DESEJA TESTAR O INSTALADOR AGORA?")
        print("   (Recomendado para verificar se funciona)")
        resposta = input("\nExecutar instalador agora? (S/N): ")
        
        if resposta.upper() == 'S' and exe_path and os.path.exists(exe_path):
            print("\n🚀 Executando instalador...")
            try:
                # Tentar executar
                subprocess.Popen([str(exe_path)])
                print("  ✅ Instalador iniciado!")
                print("  ℹ️  Lembre-se: Para instalar corretamente, execute como ADMINISTRADOR")
            except Exception as e:
                print(f"⚠️  Não foi possível executar: {e}")
                print("  💡 Tente executar manualmente como Administrador")
        
        input("\n🎯 Processo concluído! Pressione Enter para sair...")
        
    except KeyboardInterrupt:
        print("\n\n❌ Processo cancelado pelo usuário")
        input("\nPressione Enter para sair...")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()