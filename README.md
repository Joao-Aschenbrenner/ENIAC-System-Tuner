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
- Perfis: Safe (seguro) e Network (rede)
- Cancelamento de operações
- Log completo de atividades

### CLI

```bash
ENIAC.Tuner.Cli.exe safe        # Otimização segura
ENIAC.Tuner.Cli.exe network     # Otimização de rede
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

## 🔐 Proteções do Repositório

Este repositório é **público** e toda alteração de código deve passar por um **Pull Request** — push direto para `main` é bloqueado.

### Regras aplicadas ao branch `main`

| Proteção | Configuração |
|---|---|
| Pull Request obrigatório | ✅ Mínimo de 1 aprovação |
| Revisão de code owner obrigatória | ✅ (`@Joao-Aschenbrenner`) |
| Status check obrigatório | ✅ `Build & Test` (CI deve passar) |
| Descarte de aprovações em novos commits | ✅ |
| Resolução de conversas obrigatória | ✅ |
| Aplica regras ao administrador | ✅ |
| Force push bloqueado | ✅ |
| Deleção do branch bloqueada | ✅ |

### Ativar proteções (primeira configuração)

1. Vá em **Settings → Secrets and variables → Actions** e crie um segredo chamado `PROTECTION_TOKEN` com um [Personal Access Token](https://github.com/settings/tokens) com o escopo `repo` (necessário para gerenciar proteções de branch).
2. Execute o workflow **"Setup Branch Protection"** em **Actions → Setup Branch Protection → Run workflow**.
3. Confirme em **Settings → Branches** que as regras foram aplicadas ao branch `main`.

---

## 🔧 Desenvolvimento

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

