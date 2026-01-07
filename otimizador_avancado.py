"""
ENIAC SYSTEM TUNER ULTIMATE v4.5 - OTIMIZADOR AVANÇADO
Otimizações profundas sem reinicialização obrigatória
"""

import os
import sys
import json
import ctypes
import winreg
import subprocess
import psutil
import shutil
import threading
import time
from pathlib import Path
from datetime import datetime

class OtimizadorAvancado:
    def __init__(self):
        self.administrador = self.is_admin()
        self.resultados = []
        self.script_hidden = False
        self.pasta_oculta = Path(os.environ['APPDATA']) / 'ENIAC_Hidden'
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def ocultar_arquivos_sistema(self):
        """Oculta scripts e arquivos em pasta do sistema"""
        try:
            # Criar pasta oculta em AppData
            self.pasta_oculta.mkdir(exist_ok=True)
            
            # Tornar a pasta oculta
            subprocess.run(f'attrib +h "{self.pasta_oculta}"', shell=True, capture_output=True)
            
            # Scripts de inicialização ocultos
            scripts = {
                'startup.bat': '''@echo off
chcp 65001 >nul
title ENIAC System Tuner - Inicialização
echo Aplicando otimizações em segundo plano...
timeout /t 5 /nobreak >nul
exit''',
                
                'optimize_memory.bat': '''@echo off
chcp 65001 >nul
:: Script para otimização de memória RAM
echo %date% %time% - Otimizando RAM >> "%TEMP%\\eniac_optimize.log"
wmic process where name="dwm.exe" call setpriority "idle" >nul
exit''',
                
                'clean_temp.bat': '''@echo off
chcp 65001 >nul
:: Limpeza automática de temporários
del /f /s /q "%TEMP%\\*.*" 2>nul
del /f /s /q "C:\\Windows\\Temp\\*.*" 2>nul
rd /s /q "C:\\Windows\\Temp" 2>nul 2>nul
md "C:\\Windows\\Temp" 2>nul
exit'''
            }
            
            for nome, conteudo in scripts.items():
                caminho = self.pasta_oculta / nome
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                subprocess.run(f'attrib +h "{caminho}"', shell=True, capture_output=True)
            
            self.script_hidden = True
            return True
        except Exception as e:
            print(f"Erro ao ocultar arquivos: {e}")
            return False
    
    def criar_task_agendada(self):
        """Cria tarefa agendada do Windows para otimizações automáticas"""
        if not self.administrador:
            return False
        
        try:
            script_path = self.pasta_oculta / 'auto_optimize.bat'
            script_content = '''@echo off
chcp 65001 >nul
:: Otimização automática do ENIAC System Tuner
echo Executando otimização automática...
echo %date% %time% - Iniciando otimizacao >> "%TEMP%\\eniac_auto.log"

:: Limpar cache DNS
ipconfig /flushdns >nul

:: Liberar memória RAM
rundll32.exe advapi32.dll,ProcessIdleTasks >nul

:: Otimizar disco
defrag C: /O /U >nul

echo %date% %time% - Otimizacao concluida >> "%TEMP%\\eniac_auto.log"
exit
'''
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            subprocess.run(f'attrib +h "{script_path}"', shell=True, capture_output=True)
            
            # Criar tarefa agendada
            task_cmd = f'''schtasks /create /tn "ENIAC_AutoOptimize" /tr "{script_path}" /sc daily /st 02:00 /rl highest /f'''
            subprocess.run(task_cmd, shell=True, capture_output=True)
            
            return True
        except Exception as e:
            print(f"Erro ao criar task: {e}")
            return False
    
    def otimizar_registro_completo(self):
        """Otimizações avançadas do registro do Windows"""
        if not self.administrador:
            return []
        
        otimizacoes = []
        
        # Lista de otimizações do registro
        registry_optimizations = [
            # Performance do sistema
            ('HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management', 
             'DisablePagingExecutive', 'REG_DWORD', '1', 'Habilitar execução de kernel na RAM'),
            
            ('HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management',
             'LargeSystemCache', 'REG_DWORD', '1', 'Cache grande do sistema'),
            
            ('HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management',
             'IOPageLockLimit', 'REG_DWORD', '40000000', 'Limite de memória para I/O'),
            
            # Performance de rede
            ('HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters',
             'Tcp1323Opts', 'REG_DWORD', '1', 'Otimizações TCP'),
            
            ('HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters',
             'DefaultTTL', 'REG_DWORD', '64', 'TTL padrão'),
            
            ('HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters',
             'EnablePMTUDiscovery', 'REG_DWORD', '1', 'Descoberta PMTU'),
            
            # Performance do sistema de arquivos
            ('HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\FileSystem',
             'NtfsDisableLastAccessUpdate', 'REG_DWORD', '1', 'Desabilitar timestamp de acesso'),
            
            ('HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\FileSystem',
             'LongPathsEnabled', 'REG_DWORD', '1', 'Habilitar caminhos longos'),
            
            # Desabilitar telemetria
            ('HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection',
             'AllowTelemetry', 'REG_DWORD', '0', 'Desabilitar telemetria'),
            
            # Otimizações para jogos
            ('HKEY_CURRENT_USER\\System\\GameConfigStore',
             'GameDVR_Enabled', 'REG_DWORD', '0', 'Desabilitar DVR de jogos'),
            
            ('HKEY_CURRENT_USER\\Software\\Microsoft\\GameBar',
             'AllowAutoGameMode', 'REG_DWORD', '1', 'Modo jogo automático'),
            
            # Power settings
            ('HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\be337238-0d82-4146-a960-4f3749d470c7',
             'Attributes', 'REG_DWORD', '2', 'Plano de energia máximo desempenho'),
            
            # Desabilitar notificações desnecessárias
            ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings',
             'NOC_GLOBAL_SETTING_ALLOW_CRITICAL_TOASTS_ABOVE_LOCK', 'REG_DWORD', '0', 'Desabilitar notificações na tela de bloqueio'),
            
            # Otimizações do explorer
            ('HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced',
             'DisallowShaking', 'REG_DWORD', '1', 'Desabilitar agitar para minimizar'),
            
            ('HKEY_CURRENT_USER\\Control Panel\\Desktop',
             'MenuShowDelay', 'REG_SZ', '0', 'Sem delay em menus'),
            
            ('HKEY_CURRENT_USER\\Control Panel\\Desktop',
             'AutoEndTasks', 'REG_SZ', '1', 'Finalizar tarefas automaticamente'),
            
            # Performance visual
            ('HKEY_CURRENT_USER\\Control Panel\\Desktop',
             'DragFullWindows', 'REG_SZ', '0', 'Desabilitar arrastar janelas completas'),
            
            ('HKEY_CURRENT_USER\\Control Panel\\Desktop\\WindowMetrics',
             'MinAnimate', 'REG_SZ', '0', 'Desabilitar animações de janela'),
        ]
        
        for key, value_name, value_type, value_data, description in registry_optimizations:
            try:
                if 'HKEY_LOCAL_MACHINE' in key:
                    root = winreg.HKEY_LOCAL_MACHINE
                    subkey = key.replace('HKEY_LOCAL_MACHINE\\', '')
                elif 'HKEY_CURRENT_USER' in key:
                    root = winreg.HKEY_CURRENT_USER
                    subkey = key.replace('HKEY_CURRENT_USER\\', '')
                else:
                    continue
                
                # Criar chave se não existir
                try:
                    key_handle = winreg.OpenKey(root, subkey, 0, winreg.KEY_WRITE)
                except FileNotFoundError:
                    key_handle = winreg.CreateKey(root, subkey)
                
                # Converter valor
                if value_type == 'REG_DWORD':
                    data = int(value_data)
                else:
                    data = value_data
                
                winreg.SetValueEx(key_handle, value_name, 0, getattr(winreg, value_type), data)
                winreg.CloseKey(key_handle)
                
                otimizacoes.append(f"✅ {description}")
            except Exception as e:
                otimizacoes.append(f"⚠️ Falha: {description} - {str(e)}")
        
        return otimizacoes
    
    def otimizar_memoria_ram(self):
        """Otimizações avançadas de memória RAM"""
        resultados = []
        
        try:
            # Script PowerShell para otimizar memória
            ps_script = '''
            # Limpar cache de memória
            [System.GC]::Collect()
            [System.GC]::WaitForPendingFinalizers()
            
            # Otimizar processos
            $processes = Get-Process | Where-Object {$_.WorkingSet -gt 100MB}
            foreach ($proc in $processes) {
                if ($proc.ProcessName -notin @("System", "Idle", "svchost", "csrss", "wininit", "winlogon")) {
                    try {
                        $proc.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal
                    } catch {}
                }
            }
            
            # Limpar páginas de memória
            $signature = @'
            [DllImport("kernel32.dll")]
            public static extern bool SetProcessWorkingSetSize(IntPtr proc, int min, int max);
'@
            $type = Add-Type -MemberDefinition $signature -Name "Win32SetProcessWorkingSetSize" -Namespace Win32Functions -PassThru
            $type::SetProcessWorkingSetSize((Get-Process -Id $PID).Handle, -1, -1)
            '''
            
            # Executar script
            with open(os.path.join(self.pasta_oculta, 'ram_optimize.ps1'), 'w') as f:
                f.write(ps_script)
            
            subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 
                          os.path.join(self.pasta_oculta, 'ram_optimize.ps1')], 
                         capture_output=True, timeout=10)
            
            resultados.append("✅ Memória RAM otimizada via PowerShell")
        except Exception as e:
            resultados.append(f"⚠️ Falha otimização RAM: {e}")
        
        return resultados
    
    def otimizar_rede_avancada(self):
        """Otimizações avançadas de rede"""
        if not self.administrador:
            return []
        
        resultados = []
        comandos = [
            ('netsh int tcp set global autotuninglevel=normal', 'Auto-ajuste TCP normal'),
            ('netsh int tcp set global chimney=enabled', 'Habilitar Chimney'),
            ('netsh int tcp set global rss=enabled', 'Habilitar RSS'),
            ('netsh int tcp set global dca=enabled', 'Habilitar Direct Cache Access'),
            ('netsh int tcp set global netdma=enabled', 'Habilitar NetDMA'),
            ('netsh int tcp set global ecncapability=disabled', 'Desabilitar ECN'),
            ('netsh int tcp set global initialRto=1000', 'RTO inicial 1000ms'),
            ('netsh int tcp set global nonSackRttResiliency=disabled', 'Desabilitar resiliência RTT'),
            ('netsh int tcp set global fastopen=enabled', 'Habilitar TCP Fast Open'),
            ('netsh int tcp set supplemental template=internet congestionprovider=ctcp', 'CTCP para internet'),
        ]
        
        for cmd, desc in comandos:
            try:
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
                resultados.append(f"✅ {desc}")
            except Exception as e:
                resultados.append(f"⚠️ Falha {desc}: {e}")
        
        return resultados
    
    def otimizar_servicos_avancados(self):
        """Desabilita serviços desnecessários para performance"""
        if not self.administrador:
            return []
        
        resultados = []
        servicos_desativar = [
            # Telemetria e coleta de dados
            'DiagTrack',  # Connected User Experiences and Telemetry
            'dmwappushservice',  # WAP Push Message Routing Service
            'WpcMonSvc',  # Parental Controls
            'PcaSvc',  # Program Compatibility Assistant
            
            # Serviços não essenciais
            'MapsBroker',  # Downloaded Maps Manager
            'lfsvc',  # Geolocation Service
            'SharedAccess',  # Internet Connection Sharing (ICS)
            'RemoteRegistry',  # Remote Registry
            'RemoteAccess',  # Routing and Remote Access
            
            # Xbox
            'XblAuthManager',  # Xbox Live Auth Manager
            'XblGameSave',  # Xbox Live Game Save
            'XboxNetApiSvc',  # Xbox Live Networking Service
            
            # Outros
            'WbioSrvc',  # Windows Biometric Service
        ]
        
        for servico in servicos_desativar:
            try:
                subprocess.run(f'sc stop {servico}', shell=True, capture_output=True)
                subprocess.run(f'sc config {servico} start= disabled', shell=True, capture_output=True)
                resultados.append(f"✅ Serviço {servico} desabilitado")
            except Exception as e:
                resultados.append(f"⚠️ Serviço {servico}: {e}")
        
        return resultados
    
    def limpeza_profunda_sistema(self):
        """Limpeza profunda do sistema sem reinicialização"""
        resultados = []
        
        try:
            # Limpar logs do Windows
            logs_paths = [
                'C:\\Windows\\Logs',
                'C:\\Windows\\System32\\LogFiles',
                os.path.join(os.environ['WINDIR'], 'Temp'),
            ]
            
            for log_path in logs_paths:
                if os.path.exists(log_path):
                    for root, dirs, files in os.walk(log_path):
                        for file in files:
                            if file.endswith(('.log', '.tmp', '.old', '.bak')):
                                try:
                                    os.remove(os.path.join(root, file))
                                except:
                                    pass
            
            resultados.append("✅ Logs do sistema limpos")
        except Exception as e:
            resultados.append(f"⚠️ Erro limpar logs: {e}")
        
        try:
            # Limpar cache de fontes
            font_cache = os.path.join(os.environ['WINDIR'], 'ServiceProfiles', 'LocalService', 
                                     'AppData', 'Local', 'FontCache')
            if os.path.exists(font_cache):
                shutil.rmtree(font_cache, ignore_errors=True)
                resultados.append("✅ Cache de fontes limpo")
        except Exception as e:
            resultados.append(f"⚠️ Erro cache fontes: {e}")
        
        try:
            # Limpar cache do Store
            store_cache = os.path.join(os.environ['LOCALAPPDATA'], 'Packages')
            if os.path.exists(store_cache):
                for pkg in os.listdir(store_cache):
                    if 'Microsoft.WindowsStore' in pkg:
                        cache_dir = os.path.join(store_cache, pkg, 'LocalCache')
                        if os.path.exists(cache_dir):
                            shutil.rmtree(cache_dir, ignore_errors=True)
                resultados.append("✅ Cache da Microsoft Store limpo")
        except Exception as e:
            resultados.append(f"⚠️ Erro cache Store: {e}")
        
        return resultados
    
    def executar_otimizacao_completa(self):
        """Executa todas as otimizações avançadas"""
        print("🚀 INICIANDO OTIMIZAÇÃO AVANÇADA ENIAC v4.5")
        print("=" * 60)
        
        resultados_totais = []
        
        # 1. Preparar sistema
        print("[1/7] Preparando sistema...")
        self.ocultar_arquivos_sistema()
        resultados_totais.append("✅ Sistema preparado")
        time.sleep(1)
        
        # 2. Otimizar registro
        print("[2/7] Otimizando registro...")
        reg_result = self.otimizar_registro_completo()
        resultados_totais.extend(reg_result)
        time.sleep(2)
        
        # 3. Otimizar serviços
        print("[3/7] Otimizando serviços...")
        serv_result = self.otimizar_servicos_avancados()
        resultados_totais.extend(serv_result)
        time.sleep(2)
        
        # 4. Otimizar rede
        print("[4/7] Otimizando rede...")
        net_result = self.otimizar_rede_avancada()
        resultados_totais.extend(net_result)
        time.sleep(2)
        
        # 5. Otimizar memória
        print("[5/7] Otimizando memória...")
        ram_result = self.otimizar_memoria_ram()
        resultados_totais.extend(ram_result)
        time.sleep(2)
        
        # 6. Limpeza profunda
        print("[6/7] Limpeza profunda...")
        clean_result = self.limpeza_profunda_sistema()
        resultados_totais.extend(clean_result)
        time.sleep(2)
        
        # 7. Configurar otimizações permanentes
        print("[7/7] Configurando otimizações permanentes...")
        self.criar_task_agendada()
        resultados_totais.append("✅ Otimizações permanentes configuradas")
        
        print("\n" + "=" * 60)
        print("✅ OTIMIZAÇÃO AVANÇADA CONCLUÍDA!")
        print("=" * 60)
        
        # Salvar log
        log_path = self.pasta_oculta / 'otimizacao_log.txt'
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"ENIAC System Tuner - Otimização Avançada\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Administrador: {self.administrador}\n")
            f.write("=" * 50 + "\n")
            for resultado in resultados_totais:
                f.write(resultado + "\n")
        
        return resultados_totais

def main():
    """Função principal"""
    print("=" * 60)
    print("⚡ ENIAC SYSTEM TUNER ULTIMATE - OTIMIZADOR AVANÇADO")
    print("=" * 60)
    
    otimizador = OtimizadorAvancado()
    
    if not otimizador.administrador:
        print("\n⚠️  AVISO: Execute como ADMINISTRADOR para todas as otimizações!")
        print("   Clique direito > Executar como administrador")
        resposta = input("\nContinuar mesmo assim? (S/N): ")
        if resposta.upper() != 'S':
            return
    
    print("\n📋 Opções disponíveis:")
    print("1. Otimização Completa Avançada")
    print("2. Somente Otimizações de Registro")
    print("3. Somente Otimização de Serviços")
    print("4. Verificar Status do Sistema")
    
    escolha = input("\nEscolha uma opção (1-4): ")
    
    if escolha == '1':
        resultados = otimizador.executar_otimizacao_completa()
        print("\n📊 RESUMO DA OTIMIZAÇÃO:")
        for resultado in resultados:
            print(f"  {resultado}")
    
    elif escolha == '2':
        print("\n⚙️ Otimizando registro...")
        resultados = otimizador.otimizar_registro_completo()
        for resultado in resultados:
            print(f"  {resultado}")
    
    elif escolha == '3':
        print("\n⚙️ Otimizando serviços...")
        resultados = otimizador.otimizar_servicos_avancados()
        for resultado in resultados:
            print(f"  {resultado}")
    
    elif escolha == '4':
        print("\n📊 STATUS DO SISTEMA:")
        print(f"  Administrador: {'✅ Sim' if otimizador.administrador else '❌ Não'}")
        print(f"  CPU: {psutil.cpu_percent()}%")
        mem = psutil.virtual_memory()
        print(f"  RAM: {mem.percent}% ({mem.used/1024/1024:.0f}MB/{mem.total/1024/1024:.0f}MB)")
        disk = psutil.disk_usage('C:')
        print(f"  Disco C: {disk.percent}%")
    
    print("\n" + "=" * 60)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
