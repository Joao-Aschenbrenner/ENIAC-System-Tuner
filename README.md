# ENIAC System Tuner v5.0 - Release Final

Versão final C# da solução ENIAC com suporte completo a Windows 10/11.

## 🎯 Artefatos de Release

Os arquivos executáveis estão em `artifacts/release/`:

- **ENIAC.Tuner.App.exe** - Aplicação WPF com UI interativa
- **ENIAC.Tuner.Cli.exe** - Interface de linha de comando para automação
- **ENIAC.Tuner.Installer.exe** - Ferramenta instaladora

## 📋 Requisitos

- Windows 10 ou superior (64-bit)
- .NET Runtime 10.0+ ([baixar](https://dotnet.microsoft.com/download/dotnet))

## 🚀 Como Usar

### Aplicação GUI

```bash
ENIAC.Tuner.App.exe
```

Funcionalidades:
- Análise detalhada de sistema
- Diagnóstico avançado em tempo real
- Perfis: Safe, Network, Hardcore e Extreme
- Rollback do último perfil aplicado
- Cancelamento de operações
- Log completo de atividades

### CLI

```bash
ENIAC.Tuner.Cli.exe safe        # Otimização segura
ENIAC.Tuner.Cli.exe network     # Otimização de rede
ENIAC.Tuner.Cli.exe hardcore    # Otimização agressiva
ENIAC.Tuner.Cli.exe extreme     # Otimização extrema
ENIAC.Tuner.Cli.exe report      # Relatório de diagnóstico
ENIAC.Tuner.Cli.exe status      # Status do sistema
```

*Requer privilégios administrativos*

### Instalador

```bash
ENIAC.Tuner.Installer.exe
```

- Seleção visual de pasta de destino
- Cópia automática de binários
- Criação de atalhos

## 🏗️ Arquitetura

- **Core**: Modelos e abstrações (ISystemOperation, OptimizationRunner)
- **Infrastructure**: Implementações Windows (CommandSystemOperation, WindowsOptimizationProfiles)
- **App**: UI WPF com análise, diagnóstico e perfis
- **Cli**: Interface de automação
- **Installer**: Setup WPF

## 🔐 Segurança

- Verificação UAC antes de operações
- Execução assíncrona com timeout
- Tratar de erros de forma robusta
- Cancelamento em tempo real

## 📦 Stack

- **.NET 10** (C#, 100% Windows-native)
- **WPF** para desktop
- **Async/Await** para operações assíncronas
- **Windows Process API** para execução de comandos

##  Desenvolvimento

```powershell
# Build
dotnet build ENIAC.SystemTuner.slnx

# Publicar release
cd csharp && powershell -ExecutionPolicy Bypass -File publish_release.ps1

# Executar componentes localmente
dotnet run --project csharp/src/ENIAC.Tuner.App/ENIAC.Tuner.App.csproj
dotnet run --project csharp/src/ENIAC.Tuner.Cli/ENIAC.Tuner.Cli.csproj -- safe
dotnet run --project csharp/src/ENIAC.Tuner.Installer/ENIAC.Tuner.Installer.csproj
```

## 📝 Changelog

**v5.0** (Final)
- Migração 100% Python → C#
- Remoção de todo legado Python
- Nova arquitetura DDD
- WPF UI moderna com cancelamento
- CLI para automação
- Instalador standalone

**v4.5 - v4.0**: Python (descontinuado)

---

**Status**: ✅ Production Ready  
**Licença**: [Adicionar]

