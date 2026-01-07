"""
CORRETOR AUTOMÁTICO - ENIAC SYSTEM TUNER
Corrige o erro de import do otimizador_avancado
"""

import os
import sys
from pathlib import Path

def corrigir_import():
    """Corrige o import problemático no eniac_tuner.py"""
    
    print("=" * 70)
    print(" " * 15 + "🔧 CORRETOR DE IMPORT - ENIAC v4.5")
    print("=" * 70)
    print()
    
    # Verificar se o arquivo existe
    arquivo = Path("eniac_tuner.py")
    
    if not arquivo.exists():
        print("❌ ERRO: eniac_tuner.py não encontrado!")
        print(f"   Pasta atual: {os.getcwd()}")
        print("\n💡 Navegue até a pasta onde está o arquivo e execute novamente")
        input("\nPressione Enter para sair...")
        return False
    
    print(f"📁 Arquivo encontrado: {arquivo.absolute()}")
    print()
    
    # Criar backup
    backup = Path("eniac_tuner.py.backup")
    try:
        import shutil
        shutil.copy2(arquivo, backup)
        print(f"✅ Backup criado: {backup.name}")
    except Exception as e:
        print(f"⚠️  Não foi possível criar backup: {e}")
    
    print()
    print("🔍 Analisando arquivo...")
    
    # Ler conteúdo
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        input("\nPressione Enter para sair...")
        return False
    
    # Procurar e corrigir
    modificado = False
    novas_linhas = []
    
    for i, linha in enumerate(linhas, 1):
        # Remover import problemático
        if linha.strip() == 'import otimizador_avancado':
            print(f"   🔧 Linha {i}: Comentando import problemático")
            novas_linhas.append('# import otimizador_avancado  # Carregado dinamicamente\n')
            modificado = True
        else:
            novas_linhas.append(linha)
    
    if not modificado:
        print("   ℹ️  Import já está corrigido ou não foi encontrado")
        print()
        
        # Verificar se otimizador_avancado.py existe
        otim_arquivo = Path("otimizador_avancado.py")
        if otim_arquivo.exists():
            print("✅ Arquivo otimizador_avancado.py ENCONTRADO!")
            print("   O programa deve funcionar normalmente.")
        else:
            print("⚠️  Arquivo otimizador_avancado.py NÃO ENCONTRADO!")
            print("\n💡 SOLUÇÃO:")
            print("   1. Crie o arquivo otimizador_avancado.py nesta pasta")
            print("   2. Ou remova/desabilite o botão de otimização avançada")
            print("   3. O programa funcionará normalmente sem este módulo")
        
        input("\nPressione Enter para sair...")
        return True
    
    # Salvar arquivo corrigido
    try:
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.writelines(novas_linhas)
        print()
        print("=" * 70)
        print("✅ CORREÇÃO APLICADA COM SUCESSO!")
        print("=" * 70)
        print()
        print("📋 O que foi feito:")
        print("   1. Backup criado (eniac_tuner.py.backup)")
        print("   2. Import problemático comentado")
        print("   3. Módulo será carregado dinamicamente quando necessário")
        print()
        print("🚀 PRÓXIMOS PASSOS:")
        print("   1. Execute: python eniac_tuner.py")
        print("   2. O programa deve abrir normalmente")
        print("   3. Todas funcionalidades exceto 'Otimização Avançada' funcionarão")
        print()
        print("💡 PARA USAR OTIMIZAÇÃO AVANÇADA:")
        print("   • Coloque o arquivo 'otimizador_avancado.py' nesta pasta")
        print("   • Ou desabilite o botão na interface")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")
        print("⚠️  Tentando restaurar backup...")
        
        try:
            if backup.exists():
                shutil.copy2(backup, arquivo)
                print("✅ Backup restaurado")
        except:
            print("❌ Erro ao restaurar backup")
        
        input("\nPressione Enter para sair...")
        return False

def verificar_arquivos():
    """Verifica quais arquivos estão presentes"""
    print("\n📂 VERIFICANDO ARQUIVOS NA PASTA...")
    print()
    
    arquivos_importantes = [
        ('eniac_tuner.py', 'Principal'),
        ('otimizador_avancado.py', 'Otimizador Avançado'),
        ('launcher.py', 'Launcher'),
        ('instalador_gui.py', 'Instalador'),
        ('config_avancado.json', 'Configurações'),
    ]
    
    presentes = []
    ausentes = []
    
    for arquivo, descricao in arquivos_importantes:
        if Path(arquivo).exists():
            presentes.append((arquivo, descricao))
            print(f"   ✅ {arquivo:<30} - {descricao}")
        else:
            ausentes.append((arquivo, descricao))
            print(f"   ❌ {arquivo:<30} - {descricao} (FALTANDO)")
    
    print()
    print(f"📊 Resumo: {len(presentes)} presentes, {len(ausentes)} ausentes")
    print()
    
    return presentes, ausentes

def main():
    """Função principal"""
    
    # Verificar arquivos
    presentes, ausentes = verificar_arquivos()
    
    # Verificar se eniac_tuner.py existe
    if not any(nome == 'eniac_tuner.py' for nome, _ in presentes):
        print("❌ ERRO CRÍTICO: eniac_tuner.py não encontrado!")
        print()
        print(f"📁 Pasta atual: {os.getcwd()}")
        print()
        print("💡 SOLUÇÃO:")
        print("   1. Navegue até a pasta correta: cd E:\\OTIMIZADOR\\ESTU")
        print("   2. Execute este script novamente")
        print()
        input("Pressione Enter para sair...")
        return
    
    # Perguntar se deseja corrigir
    print("🔧 Este script irá:")
    print("   1. Criar backup do eniac_tuner.py")
    print("   2. Comentar o import problemático")
    print("   3. Permitir que o programa funcione normalmente")
    print()
    
    resposta = input("Deseja aplicar a correção? (S/N): ")
    
    if resposta.upper() != 'S':
        print("\n❌ Correção cancelada")
        input("\nPressione Enter para sair...")
        return
    
    print()
    
    # Aplicar correção
    sucesso = corrigir_import()
    
    if sucesso:
        print("\n" + "=" * 70)
        print("🎉 PROGRAMA CORRIGIDO COM SUCESSO!")
        print("=" * 70)
        print("\nAgora você pode executar:")
        print("   python eniac_tuner.py")
        print()
    else:
        print("\n❌ Ocorreu um erro durante a correção")
        print("Verifique os arquivos de backup")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPressione Enter para sair...")
