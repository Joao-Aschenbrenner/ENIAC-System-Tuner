using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using ENIAC.Tuner.Infrastructure.Services;

namespace ENIAC.Tuner.Tests.Infrastructure;

public sealed class AppCatalogManagerTests
{
    public async Task InstallBatchAsync_ShouldStopOnFirstFailure_WhenStrictMode()
    {
        var winget = new FakeWingetService(shouldFailAtCall: 1);
        var validator = new FakeOperationalSecurityValidator();
        var analyzer = new FakeSystemAnalyzer();
        var manager = new AppCatalogManager(winget, validator, analyzer);

        var apps = new List<AppEntry>
        {
            new() { WingetId = "App.One", DisplayName = "App One" },
            new() { WingetId = "App.Two", DisplayName = "App Two" },
            new() { WingetId = "App.Three", DisplayName = "App Three" }
        };

        var session = await manager.InstallBatchAsync(apps, dryRun: true, continueOnError: false);

        TestAssert.Equal(1, winget.Calls, "Modo estrito deve parar no primeiro erro.");
        TestAssert.Equal(1, session.Results.Count, "Sessao deve conter apenas o primeiro resultado em modo estrito.");
        TestAssert.False(session.Results[0].Success, "Primeiro resultado deve ser falha.");
    }

    public async Task InstallBatchAsync_ShouldContinue_WhenContinueOnErrorTrue()
    {
        var winget = new FakeWingetService(shouldFailAtCall: 2);
        var validator = new FakeOperationalSecurityValidator();
        var analyzer = new FakeSystemAnalyzer();
        var manager = new AppCatalogManager(winget, validator, analyzer);

        var apps = new List<AppEntry>
        {
            new() { WingetId = "App.One", DisplayName = "App One" },
            new() { WingetId = "App.Two", DisplayName = "App Two" },
            new() { WingetId = "App.Three", DisplayName = "App Three" }
        };

        var session = await manager.InstallBatchAsync(apps, dryRun: true, continueOnError: true);

        TestAssert.Equal(3, winget.Calls, "Modo padrao deve tentar todos os apps.");
        TestAssert.Equal(3, session.Results.Count, "Sessao deve conter todos os resultados quando continua em erro.");
        TestAssert.Equal(2, session.SuccessCount, "Devem existir 2 sucessos no cenario configurado.");
        TestAssert.Equal(1, session.FailureCount, "Deve existir 1 falha no cenario configurado.");
    }

    private sealed class FakeWingetService : IWingetService
    {
        private readonly int _shouldFailAtCall;
        public int Calls { get; private set; }

        public FakeWingetService(int shouldFailAtCall)
        {
            _shouldFailAtCall = shouldFailAtCall;
        }

        public Task<bool> InstallPackageAsync(string wingetId, bool dryRun = false)
        {
            Calls++;
            if (Calls == _shouldFailAtCall)
            {
                throw new InvalidOperationException("Falha simulada de instalacao");
            }

            return Task.FromResult(true);
        }

        public Task<List<string>> SearchPackagesAsync(string query)
            => Task.FromResult(new List<string>());

        public Task<string> ExportInstalledAsync(string filePath)
            => Task.FromResult(filePath);

        public Task InstallFromFileAsync(string filePath)
            => Task.CompletedTask;

        public Task<WingetPackageInfo?> GetPackageInfoAsync(string wingetId)
            => Task.FromResult<WingetPackageInfo?>(null);
    }

    private sealed class FakeOperationalSecurityValidator : IOperationalSecurityValidator
    {
        public (bool IsSecure, List<string> Issues) ValidateSession(BatchInstallationSession session)
            => (true, new List<string>());

        public bool IsAppTrusted(string wingetId)
            => true;
    }

    private sealed class FakeSystemAnalyzer : ISystemAnalyzer
    {
        public string BuildSummary() => "ok";

        public Task<string> BuildDetailedReportAsync(CancellationToken cancellationToken)
            => Task.FromResult("ok");
    }
}
