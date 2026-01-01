"""
CRIADOR DE INSTALADOR EXECUTÁVEL
Cria um instalador .exe standalone completo para o ENIAC System Tuner
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    """Cabeçalho"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 70)
    print(" " * 15 + "🚀 CRIADOR DE INSTALADOR EXECUTÁVEL")
    print(" " * 18 + "ENIAC SYSTEM TUNER v4.0")
    print("=" * 70)
    print()

def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    print("[1/5] Verificando arquivos necessários...")
    print()
    
    arquivos_necessarios = [
        'instalador_gui.py',
        'launcher.py',
        'eniac_tuner.py'
    ]
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"  ✓ {arquivo} encontrado")
        else:
            print(f"  ✗ {arquivo} NÃO ENCONTRADO!")
            todos_ok = False
    
    print()
    return todos_ok

def instalar_pyinstaller():
    """Instala PyInstaller se necessário"""
    print("[2/5] Verificando PyInstaller...")
    print()
    
    try:
        import PyInstaller
        print("  ✓ PyInstaller já instalado")
        print()
        return True
    except ImportError:
        print("  ⏳ Instalando PyInstaller...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pyinstaller"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("  ✓ PyInstaller instalado com sucesso")
            print()
            return True
        except:
            print("  ✗ Erro ao instalar PyInstaller")
            print()
            return False

def criar_bat_bootstrap():
    """Cria arquivo .bat que será embutido no executável"""
    print("[3/5] Criando bootstrap...")
    print()
    
    bat_content = """@echo off
title ENIAC System Tuner - Instalador
color 0A

:: Verificar admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Solicitando privilegios de administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cls
echo ========================================
echo   ENIAC SYSTEM TUNER - INSTALADOR
echo ========================================
echo.
echo Iniciando instalador grafico...
echo.

:: Executar instalador Python
"%~dp0python.exe" "%~dp0instalador_gui.py"

if errorlevel 1 (
    echo.
    echo Erro ao executar instalador!
    pause
)

exit
"""
    
    try:
        with open('bootstrap.bat', 'w', encoding='utf-8') as f:
            f.write(bat_content)
        print("  ✓ Bootstrap criado")
        print()
        return True
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        print()
        return False

def compilar_instalador():
    """Compila o instalador em executável único"""
    print("[4/5] Compilando instalador executável...")
    print()
    print("  ⏳ Isso pode levar alguns minutos, aguarde...")
    print()
    
    # Limpar builds antigos
    for pasta in ['build', 'dist', '__pycache__']:
        if os.path.exists(pasta):
            shutil.rmtree(pasta, ignore_errors=True)
    
    # Comando PyInstaller
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",                    # Arquivo único
        "--noconsole",                  # Sem console
        "--name=ENIAC_Installer",       # Nome do executável
        "--icon=NONE",
        "--add-data", "launcher.py;.",  # Incluir launcher.py
        "--add-data", "eniac_tuner.py;.",  # Incluir eniac_tuner.py
        "--clean",
        "instalador_gui.py"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutos timeout
        )
        
        exe_path = Path('dist') / 'ENIAC_Installer.exe'
        
        if result.returncode == 0 and exe_path.exists():
            size = exe_path.stat().st_size / (1024*1024)
            print(f"  ✓ Instalador criado: ENIAC_Installer.exe ({size:.1f} MB)")
            print()
            return True
        else:
            print("  ✗ Erro na compilação")
            if result.stderr:
                print(f"  Erro: {result.stderr[:500]}")
            print()
            return False
            
    except subprocess.TimeoutExpired:
        print("  ✗ Timeout - compilação demorou muito")
        print()
        return False
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        print()
        return False

def criar_pacote_final():
    """Organiza arquivos finais"""
    print("[5/5] Criando pacote final...")
    print()
    
    # Criar pasta de distribuição
    dist_folder = Path('ENIAC_Installer_Package')
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    dist_folder.mkdir()
    
    # Copiar instalador
    exe_source = Path('dist') / 'ENIAC_Installer.exe'
    if exe_source.exists():
        shutil.copy2(exe_source, dist_folder / 'ENIAC_Installer.exe')
        print("  ✓ Instalador copiado")
    
    # Criar README
    readme = """
╔════════════════════════════════════════════════════════════════════╗
║                  ENIAC SYSTEM TUNER v4.0                           ║
║                   INSTALADOR EXECUTÁVEL                            ║
╚════════════════════════════════════════════════════════════════════╝

📦 COMO INSTALAR:

1. Clique direito em "ENIAC_Installer.exe"
2. Selecione "Executar como administrador"
3. Siga o assistente de instalação
4. Pronto!

⚠️ IMPORTANTE:
- Requer privilégios de administrador
- Windows 10/11 (64-bit)
- ~50 MB de espaço em disco

🎯 RECURSOS:
✓ Otimização completa do Windows
✓ Detecção automática de hardware
✓ Agendamentos automáticos
✓ Diagnóstico profundo
✓ Modo gamer
✓ Ferramentas integradas

📧 SUPORTE:
Em caso de problemas, entre em contato com o desenvolvedor.

═══════════════════════════════════════════════════════════════════

Copyright © 2025 ENIAC System Tuner. Todos os direitos reservados.
"""
    
    try:
        with open(dist_folder / 'LEIA-ME.txt', 'w', encoding='utf-8') as f:
            f.write(readme)
        print("  ✓ README criado")
    except:
        pass
    
    print()
    print(f"  📁 Pacote criado em: {dist_folder.absolute()}")
    print()
    return True

def limpar_temporarios():
    """Remove arquivos temporários"""
    print("Limpando arquivos temporários...")
    print()
    
    for item in ['build', '__pycache__', 'bootstrap.bat']:
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
            except:
                pass
    
    # Remover .spec
    for spec in Path('.').glob('*.spec'):
        try:
            spec.unlink()
        except:
            pass
    
    print("  ✓ Limpeza concluída")
    print()

def main():
    """Função principal"""
    print_header()
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("❌ Arquivos necessários não encontrados!")
        print()
        print("Certifique-se de ter os seguintes arquivos na mesma pasta:")
        print("  - instalador_gui.py")
        print("  - launcher.py")
        print("  - eniac_tuner.py")
        print()
        input("Pressione Enter para sair...")
        return
    
    # Instalar PyInstaller
    if not instalar_pyinstaller():
        print("❌ Não foi possível instalar PyInstaller!")
        input("Pressione Enter para sair...")
        return
    
    # Criar bootstrap
    criar_bat_bootstrap()
    
    # Compilar
    if not compilar_instalador():
        print("❌ Erro ao compilar instalador!")
        input("Pressione Enter para sair...")
        return
    
    # Criar pacote
    criar_pacote_final()
    
    # Limpar
    limpar_temporarios()
    
    # Sucesso!
    print("=" * 70)
    print("✅ INSTALADOR EXECUTÁVEL CRIADO COM SUCESSO!")
    print("=" * 70)
    print()
    print("📦 Seu instalador está pronto em: ENIAC_Installer_Package\\")
    print()
    print("Para distribuir:")
    print("  1. Envie a pasta 'ENIAC_Installer_Package' para os usuários")
    print("  2. OU comprima em ZIP e distribua")
    print("  3. Usuários devem executar 'ENIAC_Installer.exe' como admin")
    print()
    print("=" * 70)
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            input("\nPressione Enter para sair...")
        except:
            pass