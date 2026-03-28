using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using ENIAC.Tuner.Core.Services;
using ENIAC.Tuner.Core.ViewModels;

namespace ENIAC.Tuner.Tests.Core;

public sealed class RollbackViewModelTests
{
    public async Task HasRollback_IsFalseBeforeAnyExecution()
    {
        var vm = CreateViewModel();

        TestAssert.False(vm.HasRollback, "HasRollback deve ser false antes de qualquer execucao");
        TestAssert.Equal(string.Empty, vm.LastProfileName, "LastProfileName deve ser vazio antes de exec");
        await Task.CompletedTask;
    }

    public async Task HasRollback_IsTrueAfterExecutingRollbackableProfile()
    {
        var vm = CreateViewModel();
        var profile = BuildRollbackableProfile();

        await vm.ExecuteProfileAsync(profile, CancellationToken.None);

        TestAssert.True(vm.HasRollback, "HasRollback deve ser true apos execucao com ops rollbackaveis");
        TestAssert.Equal("Perfil Rollbackavel", vm.LastProfileName, "LastProfileName deve refletir perfil executado");
    }

    public async Task HasRollback_IsFalseAfterRollback()
    {
        var vm = CreateViewModel();
        var profile = BuildRollbackableProfile();

        await vm.ExecuteProfileAsync(profile, CancellationToken.None);
        await vm.RollbackLastProfileAsync(CancellationToken.None);

        TestAssert.False(vm.HasRollback, "HasRollback deve ser false apos rollback concluido");
        TestAssert.Equal(string.Empty, vm.LastProfileName, "LastProfileName deve ser vazio apos rollback");
    }

    public async Task RollbackLastProfileAsync_ShouldInvokeRollbackOnReverseOrder()
    {
        var order = new List<string>();
        var vm = CreateViewModelWithTracker(order);

        var profile = new OptimizationProfile
        {
            Id = "order-test",
            DisplayName = "Ordem Rollback",
            Operations =
            [
                new TrackingRollbackOperation("A", order),
                new TrackingRollbackOperation("B", order),
                new TrackingRollbackOperation("C", order)
            ]
        };

        await vm.ExecuteProfileAsync(profile, CancellationToken.None);
        order.Clear(); // limpa rastreio de execute; mede somente rollback

        await vm.RollbackLastProfileAsync(CancellationToken.None);

        TestAssert.Equal(3, order.Count, "Rollback deve executar 3 operacoes");
        TestAssert.Equal("C-rollback", order[0], "Primeiro rollback deve ser a ultima operacao (C)");
        TestAssert.Equal("B-rollback", order[1], "Segundo rollback deve ser B");
        TestAssert.Equal("A-rollback", order[2], "Terceiro rollback deve ser A");
    }

    public async Task RollbackLastProfileAsync_ShouldUpdateProgressToHundred()
    {
        var vm = CreateViewModel();
        var profile = BuildRollbackableProfile();

        await vm.ExecuteProfileAsync(profile, CancellationToken.None);
        await vm.RollbackLastProfileAsync(CancellationToken.None);

        TestAssert.Equal(100d, vm.ProgressValue, "Progresso do rollback deve chegar a 100");
        TestAssert.Contains("rollback concluido", vm.StatusText.ToLowerInvariant(), "Status deve indicar rollback concluido");
        TestAssert.False(vm.IsBusy, "ViewModel nao deve permanecer ocupado apos rollback");
    }

    public async Task HasRollback_IsFalseForProfileWithoutRollbackableOps()
    {
        var vm = CreateViewModel();
        var profile = new OptimizationProfile
        {
            Id = "no-rollback",
            DisplayName = "Sem Rollback",
            Operations = [new FakeOperation("Op1", true)] // nao implementa IRollbackable
        };

        await vm.ExecuteProfileAsync(profile, CancellationToken.None);

        // HasRollback e true (perfil foi executado), mas rollback nao faz nada util
        TestAssert.True(vm.HasRollback, "HasRollback e true pois o perfil foi executado");

        await vm.RollbackLastProfileAsync(CancellationToken.None);

        // Apos rollback de perfil sem ops reversiveis, deve finalizar limpo
        TestAssert.False(vm.HasRollback, "HasRollback deve ser false apos rollback de perfil sem ops reversiveis");
    }

    // ─── helpers ──────────────────────────────────────────────────────────────

    private static MainDashboardViewModel CreateViewModel()
    {
        return new MainDashboardViewModel(
            new InOrderRunner(),
            new StubAnalyzer(),
            new StubSecurity());
    }

    private static MainDashboardViewModel CreateViewModelWithTracker(List<string> order)
    {
        return new MainDashboardViewModel(
            new InOrderRunner(),
            new StubAnalyzer(),
            new StubSecurity());
    }

    private static OptimizationProfile BuildRollbackableProfile()
    {
        return new OptimizationProfile
        {
            Id = "rb-test",
            DisplayName = "Perfil Rollbackavel",
            Operations =
            [
                new TrackingRollbackOperation("Op1", new List<string>()),
                new TrackingRollbackOperation("Op2", new List<string>())
            ]
        };
    }

    private sealed class InOrderRunner : IOptimizationRunner
    {
        public async IAsyncEnumerable<OperationResult> RunAsync(
            OptimizationProfile profile,
            [System.Runtime.CompilerServices.EnumeratorCancellation] CancellationToken cancellationToken = default)
        {
            foreach (var op in profile.Operations)
            {
                cancellationToken.ThrowIfCancellationRequested();
                yield return await op.ExecuteAsync(cancellationToken).ConfigureAwait(false);
            }
        }
    }

    private sealed class StubAnalyzer : ISystemAnalyzer
    {
        public string BuildSummary() => "CPU: teste";
        public Task<string> BuildDetailedReportAsync(CancellationToken cancellationToken)
            => Task.FromResult("Relatório");
    }

    private sealed class StubSecurity : ISystemSecurity
    {
        public bool IsAdministrator() => true;
    }

    private sealed class FakeOperation(string name, bool success) : ISystemOperation
    {
        public string Name { get; } = name;
        public bool RequiresAdministrator { get; } = false;
        public Task<OperationResult> ExecuteAsync(CancellationToken cancellationToken)
            => Task.FromResult(new OperationResult(success, $"{Name}: {(success ? "OK" : "Falha")}"));
    }

    /// <summary>Operação que rastreia a ordem de execute e rollback.</summary>
    private sealed class TrackingRollbackOperation(string name, List<string> order)
        : ISystemOperation, IRollbackable
    {
        public string Name { get; } = name;
        public bool RequiresAdministrator { get; } = false;

        public Task<OperationResult> ExecuteAsync(CancellationToken cancellationToken)
        {
            order.Add($"{Name}-execute");
            return Task.FromResult(new OperationResult(true, $"{Name}: OK"));
        }

        public Task<OperationResult> RollbackAsync(CancellationToken cancellationToken)
        {
            order.Add($"{Name}-rollback");
            return Task.FromResult(new OperationResult(true, $"{Name}: rollback OK"));
        }
    }
}
