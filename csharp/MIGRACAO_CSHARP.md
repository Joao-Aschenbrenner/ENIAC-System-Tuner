# Migracao para C# (Windows)

## Objetivo
Levar o ENIAC System Tuner para uma base Windows-native em C#, com melhor manutencao, UI mais estavel e fluxo seguro para alteracoes de sistema.

## Estrutura criada
- ENIAC.SystemTuner.slnx
- csharp/src/ENIAC.Tuner.Core
- csharp/src/ENIAC.Tuner.Infrastructure
- csharp/src/ENIAC.Tuner.App (WPF)
- csharp/src/ENIAC.Tuner.Cli
- csharp/src/ENIAC.Tuner.Installer (WPF)

## Fase 1 - Fundacao (concluida)
- Solution e projetos separados por responsabilidades.
- Runner de operacoes com retorno estruturado de sucesso/falha.
- Execucao de comandos Windows com captura de erro.
- UI WPF inicial com:
  - Analise de sistema
  - Diagnostico detalhado (CPU, memoria, discos e top processos)
  - Perfil seguro
  - Perfil de rede
  - Log e status em tempo real

## Fase 2 - Paridade funcional (proxima)
- Migrar modulo de limpeza temporaria para Infrastructure.
- Migrar diagnostico de hardware/rede para Core + Infrastructure.
- Adicionar perfil "agressivo" com opt-in explicito e validacoes.
- Incluir verificacao de privilegios admin e elevacao UAC.

## Fase 3 - Confiabilidade e rollback
- Persistir backup de configuracoes alteradas (registro, servicos, rede).
- Implementar botao de rollback completo.
- Telemetria local de operacoes (arquivo de auditoria).

## Fase 4 - Distribuicao
- Publicacao self-contained para Windows x64.
- Instalador MSI/EXE com assinatura de codigo.
- Estrategia de update incremental.

## Comandos uteis
- Build: dotnet build ENIAC.SystemTuner.slnx
- Run app WPF: dotnet run --project csharp/src/ENIAC.Tuner.App/ENIAC.Tuner.App.csproj
- Run CLI: dotnet run --project csharp/src/ENIAC.Tuner.Cli/ENIAC.Tuner.Cli.csproj -- status
- Run Installer: dotnet run --project csharp/src/ENIAC.Tuner.Installer/ENIAC.Tuner.Installer.csproj

## Observacao
Transicao para C# concluida. O repositorio nao depende mais de stack legada para build/execucao.
