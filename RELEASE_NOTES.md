# ENIAC System Tuner v5.0 - Release Notes

## 🎉 Lançamento da Versão Final (C# 100%)

### Qual é o novo?

**Migração Completa Python → C#**
- Remoção de todo código Python
- 5 projetos .NET 10 bem estruturados
- Arquitetura DDD (Domain-Driven Design)
- Zero resíduos legados

**Interface WPF Moderna**
- Análise de sistema em tempo real
- Diagnóstico detalhado com formatação de memória/disco
- Perfis de otimização (Safe/Network)
- Cancelamento de operações assíncrono
- Log persistente de atividades

**CLI para Automação**
- Comandos: `safe`, `network`, `report`, `status`
- Verificação UAC automática
- Saída estruturada para parsing
- Ideal para scripts e CI/CD

**Instalador Standalone**
- Seleção visual de pasta
- Cópia automática
- Criação de atalhos PowerShell
- Interface progress bar

### Arquivos de Release

```
artifacts/release/
├── app/
│   ├── ENIAC.Tuner.App.exe         (WPF UI)
│   ├── ENIAC.Tuner.App.dll
│   ├── ENIAC.Tuner.Core.dll
│   ├── ENIAC.Tuner.Infrastructure.dll
│   ├── ENIAC.Tuner.App.deps.json   (dependências .NET)
│   ├── ENIAC.Tuner.App.runtimeconfig.json
│   └── *.pdb                       (símbolos de debug)
│
├── cli/
│   ├── ENIAC.Tuner.Cli.exe         (CLI)
│   ├── ENIAC.Tuner.Cli.dll
│   └── [mesmas dependências]
│
└── installer/
    ├── ENIAC.Tuner.Installer.exe   (Setup)
    ├── ENIAC.Tuner.Installer.dll
    └── [mesmas dependências]
```

### Requisitos de Execução

- **Windows**: 10 (versão 22H2) ou 11
- **.NET Runtime**: 10.0.x ou superior
- **Permissões**: UAC (Admin) para perfis de otimização
- **Armazenamento**: ~50 MB (com runtimes)

### Como Começar

1. **Download dos binários**: [artifacts/release/](./artifacts/release/)
2. **Instalação do .NET** (se não estiver instalado):
   ```
   winget install Microsoft.DotNet.Runtime.10
   ```
3. **Execução**:
   ```
   ENIAC.Tuner.App.exe           # Interface visual
   # ou
   ENIAC.Tuner.Cli.exe safe      # CLI automação
   # ou
   ENIAC.Tuner.Installer.exe     # Instalador
   ```

### Mudanças desde v4.5

| Aspecto | v4.5 (Python) | v5.0 (C#) |
|---------|---------------|----------|
| Linguagem | Python 3.10 | C# + .NET 10 |
| UI | Tkinter | WPF |
| Performance | Lenta (bytecode) | Rápida (IL/JIT) |
| Build | py2exe (~80 MB) | dotnet publish (~50 MB) |
| Segurança | Básica | UAC + Async safe |
| Cancelamento | Não | ✅ Sim |

### Problemas Corrigidos

- ✅ Thread-safety de UI (eliminado GIL Python)
- ✅ Lentidão no startup (JIT vs bytecode)
- ✅ Falta de cancelamento de operações
- ✅ Segurança fraca de caminho (validação strict)
- ✅ Erro de retorno de comando (captura completa)
- ✅ Backup seguro vs deleção perigosa

### Testing

```powershell
# Build
dotnet build ENIAC.SystemTuner.slnx -c Release

# Publicar release
cd csharp
powershell -ExecutionPolicy Bypass -File publish_release.ps1

# Testar App
.\artifacts\release\app\ENIAC.Tuner.App.exe

# Testar CLI  
.\artifacts\release\cli\ENIAC.Tuner.Cli.exe status

# Testar Installer
.\artifacts\release\installer\ENIAC.Tuner.Installer.exe
```

### Roadmap

- [ ] Testes unitários (xUnit)
- [ ] Integração CI/CD (GitHub Actions)
- [ ] Documentação de API
- [ ] Web dashboard (Blazor)
- [ ] Mobile companion (MAUI)

### Suporte

Para issues, entre em contato via GitHub Issues ou discussions.

---

**Release Date**: Março 2026  
**Status**: ✅ Production Ready  
**Próxima**: Manutenção + Features (TBD)
