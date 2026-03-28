using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using ENIAC.Tuner.Core.Services;
using ENIAC.Tuner.Core.ViewModels;

namespace ENIAC.Tuner.Tests.Core;

public sealed class MainDashboardViewModelTests
{
    public void Constructor_ShouldSetAdminText_WhenAdministrator()
    {
        var vm = CreateViewModel(isAdministrator: true);

        TestAssert.True(vm.IsAdministrator, "Flag de admin deveria ser true");
        TestAssert.Equal("Admin: sim", vm.AdminText, "AdminText incorreto para admin");
    }

    public void Constructor_ShouldSetAdminText_WhenNotAdministrator()
    {
        var vm = CreateViewModel(isAdministrator: false);

        TestAssert.False(vm.IsAdministrator, "Flag de admin deveria ser false");
        TestAssert.Equal("Admin: nao", vm.AdminText, "AdminText incorreto para nao admin");
    }

    public void AnalyzeSystem_ShouldUpdateSummaryAndStatus()
    {
        var vm = CreateViewModel();

        vm.AnalyzeSystem();

        TestAssert.Contains("CPU:", vm.SummaryText, "Summary deve conter CPU");
        TestAssert.Equal("Resumo do sistema atualizado", vm.StatusText, "Status incorreto");
    }

    public async Task ExecuteProfileAsync_WhenNotAdmin_ShouldBlockExecution()
    {
        var vm = CreateViewModel(isAdministrator: false);
        var profile = BuildAdminProfile();

        var executed = await vm.ExecuteProfileAsync(profile, CancellationToken.None);

        TestAssert.False(executed, "Execução deveria ser bloqueada sem admin");
        TestAssert.Equal("Permissão necessária", vm.StatusText, "Status deve indicar permissão");
        TestAssert.Contains("administrador", vm.LogText, "Log deve citar administrador");
    }

    public async Task ExecuteProfileAsync_ShouldUpdateProgressAndCounters()
    {
        var vm = CreateViewModel();
        var profile = new OptimizationProfile
        {
            Id = "test",
            DisplayName = "Teste",
            Operations =
            [
                new FakeOperation("Op1", true),
                new FakeOperation("Op2", false),
                new FakeOperation("Op3", true)
            ]
        };

        var executed = await vm.ExecuteProfileAsync(profile, CancellationToken.None);

        TestAssert.True(executed, "Execução deveria completar");
        TestAssert.Equal(100d, vm.ProgressValue, "Progresso final deve ser 100");
        TestAssert.Equal(2, vm.SuccessCount, "Contagem de sucesso incorreta");
        TestAssert.Equal(1, vm.FailureCount, "Contagem de falha incorreta");
        TestAssert.Contains("concluido", vm.StatusText.ToLowerInvariant(), "Status deve indicar conclusão");
    }

    public async Task DeepAnalyzeAsync_ShouldUpdateSummaryProgressAndLog()
    {
        var vm = CreateViewModel(analyzer: new StubAnalyzer("CPU: teste", "Relatorio detalhado"));

        await vm.DeepAnalyzeAsync(CancellationToken.None);

        TestAssert.Equal("Relatorio detalhado", vm.SummaryText, "Resumo detalhado incorreto");
        TestAssert.Equal(100d, vm.ProgressValue, "Progresso final do diagnostico deve ser 100");
        TestAssert.Equal("Diagnostico detalhado atualizado", vm.StatusText, "Status final incorreto");
        TestAssert.Contains("Diagnostico detalhado concluido", vm.LogText, "Log deveria registrar conclusao");
        TestAssert.False(vm.IsBusy, "ViewModel nao deveria permanecer ocupado");
    }

    public async Task DeepAnalyzeAsync_WhenCanceled_ShouldSetStatusAndRethrow()
    {
        var vm = CreateViewModel(analyzer: new CancelingAnalyzer());

        var canceled = false;
        try
        {
            await vm.DeepAnalyzeAsync(new CancellationToken(canceled: true));
        }
        catch (OperationCanceledException)
        {
            canceled = true;
        }

        TestAssert.True(canceled, "Deveria propagar OperationCanceledException");
        TestAssert.Equal("Cancelado", vm.StatusText, "Status deveria indicar cancelamento");
        TestAssert.Contains("cancelado", vm.LogText, "Log deveria registrar cancelamento");
        TestAssert.False(vm.IsBusy, "ViewModel nao deveria permanecer ocupado apos cancelamento");
    }

    public async Task ExecuteProfileAsync_WhenCanceled_ShouldSetStatusAndRethrow()
    {
        var vm = CreateViewModel();
        var profile = new OptimizationProfile
        {
            Id = "cancel",
            DisplayName = "Cancelavel",
            Operations = [new FakeOperation("Op1", true)]
        };

        var canceled = false;
        try
        {
            await vm.ExecuteProfileAsync(profile, new CancellationToken(canceled: true));
        }
        catch (OperationCanceledException)
        {
            canceled = true;
        }

        TestAssert.True(canceled, "Deveria propagar OperationCanceledException");
        TestAssert.Equal("Cancelado", vm.StatusText, "Status deveria indicar cancelamento");
        TestAssert.Contains("Execucao cancelada", vm.LogText, "Log deveria registrar cancelamento");
        TestAssert.False(vm.IsBusy, "ViewModel nao deveria permanecer ocupado apos cancelamento");
    }

    private static MainDashboardViewModel CreateViewModel(bool isAdministrator = true, ISystemAnalyzer? analyzer = null, IOptimizationRunner? runner = null)
    {
        analyzer ??= new StubAnalyzer();
        var security = new StubSecurity(isAdministrator);
        runner ??= new StubRunner();
        return new MainDashboardViewModel(runner, analyzer, security);
    }

    private static OptimizationProfile BuildAdminProfile()
    {
        return new OptimizationProfile
        {
            Id = "safe",
            DisplayName = "Seguro",
            Operations = [new FakeOperation("Op1", true, requiresAdministrator: true)]
        };
    }

    private sealed class StubAnalyzer(string summary = "CPU: teste", string detailedReport = "Relatório") : ISystemAnalyzer
    {
        public string BuildSummary() => summary;

        public Task<string> BuildDetailedReportAsync(CancellationToken cancellationToken)
            => Task.FromResult(detailedReport);
    }

    private sealed class CancelingAnalyzer : ISystemAnalyzer
    {
        public string BuildSummary() => "CPU: teste";

        public Task<string> BuildDetailedReportAsync(CancellationToken cancellationToken)
        {
            cancellationToken.ThrowIfCancellationRequested();
            return Task.FromResult("Nao deveria chegar aqui");
        }
    }

    private sealed class StubSecurity(bool isAdministrator) : ISystemSecurity
    {
        public bool IsAdministrator() => isAdministrator;
    }

    private sealed class StubRunner : IOptimizationRunner
    {
        public async IAsyncEnumerable<OperationResult> RunAsync(OptimizationProfile profile, [System.Runtime.CompilerServices.EnumeratorCancellation] CancellationToken cancellationToken = default)
        {
            foreach (var operation in profile.Operations)
            {
                cancellationToken.ThrowIfCancellationRequested();
                yield return await operation.ExecuteAsync(cancellationToken).ConfigureAwait(false);
            }
        }
    }

    private sealed class FakeOperation(string name, bool success, bool requiresAdministrator = false) : ISystemOperation
    {
        public string Name { get; } = name;

        public bool RequiresAdministrator { get; } = requiresAdministrator;

        public Task<OperationResult> ExecuteAsync(CancellationToken cancellationToken)
        {
            var result = new OperationResult(success, $"{Name}: {(success ? "OK" : "Falha")}");
            return Task.FromResult(result);
        }
    }
}
