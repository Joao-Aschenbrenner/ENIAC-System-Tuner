using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Text;
using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using ENIAC.Tuner.Core.Services;

namespace ENIAC.Tuner.Core.ViewModels;

public sealed class MainDashboardViewModel : INotifyPropertyChanged
{
    private readonly IOptimizationRunner _runner;
    private readonly ISystemAnalyzer _analyzer;
    private readonly ISystemSecurity _security;

    private readonly StringBuilder _logBuilder = new();

    private OptimizationProfile? _lastExecutedProfile;
    private readonly List<ISystemOperation> _completedOperations = [];

    private string _summaryText = "Clique em 'Analisar Sistema' para exibir dados básicos do ambiente.";
    private string _statusText = "Pronto";
    private string _adminText = "Admin: desconhecido";
    private bool _isBusy;
    private double _progressValue;
    private int _successCount;
    private int _failureCount;

    public MainDashboardViewModel(IOptimizationRunner runner, ISystemAnalyzer analyzer, ISystemSecurity security)
    {
        _runner = runner;
        _analyzer = analyzer;
        _security = security;

        IsAdministrator = _security.IsAdministrator();
        AdminText = IsAdministrator ? "Admin: sim" : "Admin: nao";
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    public bool IsAdministrator { get; }

    public string SummaryText
    {
        get => _summaryText;
        private set => SetField(ref _summaryText, value);
    }

    public string LogText => _logBuilder.ToString();

    public string StatusText
    {
        get => _statusText;
        private set => SetField(ref _statusText, value);
    }

    public string AdminText
    {
        get => _adminText;
        private set => SetField(ref _adminText, value);
    }

    public bool IsBusy
    {
        get => _isBusy;
        private set
        {
            if (SetField(ref _isBusy, value))
            {
                OnPropertyChanged(nameof(CanRunOperations));
            }
        }
    }

    public bool CanRunOperations => !IsBusy;

    public bool HasRollback => _lastExecutedProfile != null && _completedOperations.Count > 0;

    public string LastProfileName => _lastExecutedProfile?.DisplayName ?? string.Empty;

    public double ProgressValue
    {
        get => _progressValue;
        private set => SetField(ref _progressValue, value);
    }

    public int SuccessCount
    {
        get => _successCount;
        private set => SetField(ref _successCount, value);
    }

    public int FailureCount
    {
        get => _failureCount;
        private set => SetField(ref _failureCount, value);
    }

    public void AnalyzeSystem()
    {
        SummaryText = _analyzer.BuildSummary();
        StatusText = "Resumo do sistema atualizado";
    }

    public async Task DeepAnalyzeAsync(CancellationToken cancellationToken)
    {
        IsBusy = true;
        ProgressValue = 0;
        StatusText = "Gerando diagnostico detalhado...";

        try
        {
            SummaryText = await _analyzer.BuildDetailedReportAsync(cancellationToken).ConfigureAwait(false);
            ProgressValue = 100;
            StatusText = "Diagnostico detalhado atualizado";
            AppendLog("Diagnostico detalhado concluido.");
        }
        catch (OperationCanceledException)
        {
            StatusText = "Cancelado";
            AppendLog("Diagnostico detalhado cancelado.");
            throw;
        }
        finally
        {
            IsBusy = false;
        }
    }

    public async Task<bool> ExecuteProfileAsync(OptimizationProfile profile, CancellationToken cancellationToken)
    {
        if (profile.Operations.Any(o => o.RequiresAdministrator) && !IsAdministrator)
        {
            StatusText = "Permissão necessária";
            AppendLog("Operacao bloqueada: execute como administrador.");
            return false;
        }

        IsBusy = true;
        ProgressValue = 0;
        SuccessCount = 0;
        FailureCount = 0;
        _completedOperations.Clear();
        OnPropertyChanged(nameof(HasRollback));

        StatusText = $"Executando: {profile.DisplayName}";
        AppendLog($"--- Inicio {profile.DisplayName} ---");

        var total = Math.Max(1, profile.Operations.Count);
        var done = 0;

        try
        {
            await foreach (var result in _runner.RunAsync(profile, cancellationToken).ConfigureAwait(false))
            {
                AppendLog(result.Message);
                _completedOperations.Add(profile.Operations[done]);
                done++;
                ProgressValue = (double)done / total * 100;

                if (result.Success)
                {
                    SuccessCount++;
                }
                else
                {
                    FailureCount++;
                }
            }

            StatusText = FailureCount == 0 ? "Concluido" : "Concluido com falhas";
            AppendLog($"--- Fim {profile.DisplayName} | Sucesso: {SuccessCount} | Falhas: {FailureCount} ---");
            ProgressValue = 100;
            _lastExecutedProfile = profile;
            OnPropertyChanged(nameof(HasRollback));
            OnPropertyChanged(nameof(LastProfileName));
            return true;
        }
        catch (OperationCanceledException)
        {
            StatusText = "Cancelado";
            AppendLog($"--- Execucao cancelada: {profile.DisplayName} ---");
            if (_completedOperations.Count > 0)
            {
                _lastExecutedProfile = profile;
                OnPropertyChanged(nameof(HasRollback));
                OnPropertyChanged(nameof(LastProfileName));
            }
            throw;
        }
        finally
        {
            IsBusy = false;
        }
    }

    public async Task RollbackLastProfileAsync(CancellationToken cancellationToken)
    {
        if (_lastExecutedProfile == null || _completedOperations.Count == 0)
        {
            return;
        }

        var profileName = _lastExecutedProfile.DisplayName;
        var rollbackOps = _completedOperations
            .OfType<IRollbackable>()
            .Reverse()
            .ToList();

        IsBusy = true;
        ProgressValue = 0;
        StatusText = $"Revertendo: {profileName}";
        AppendLog($"--- Rollback {profileName} ---");

        var total = Math.Max(1, rollbackOps.Count);
        var done = 0;
        var successCount = 0;
        var failureCount = 0;

        _lastExecutedProfile = null;
        _completedOperations.Clear();
        OnPropertyChanged(nameof(HasRollback));
        OnPropertyChanged(nameof(LastProfileName));

        try
        {
            foreach (var op in rollbackOps)
            {
                cancellationToken.ThrowIfCancellationRequested();
                var result = await op.RollbackAsync(cancellationToken).ConfigureAwait(false);
                done++;
                ProgressValue = (double)done / total * 100;
                AppendLog(result.Message);
                if (result.Success) { successCount++; } else { failureCount++; }
            }

            ProgressValue = 100;
            StatusText = failureCount == 0 ? "Rollback concluido" : "Rollback com falhas";
            AppendLog($"--- Fim rollback | Sucesso: {successCount} | Falhas: {failureCount} ---");
        }
        catch (OperationCanceledException)
        {
            StatusText = "Rollback cancelado";
            AppendLog("--- Rollback cancelado ---");
            throw;
        }
        finally
        {
            IsBusy = false;
        }
    }

    public void AppendLog(string message)
    {
        _logBuilder.Append('[')
            .Append(DateTime.Now.ToString("HH:mm:ss"))
            .Append("] ")
            .AppendLine(message);
        OnPropertyChanged(nameof(LogText));
    }

    private bool SetField<T>(ref T storage, T value, [CallerMemberName] string? propertyName = null)
    {
        if (EqualityComparer<T>.Default.Equals(storage, value))
        {
            return false;
        }

        storage = value;
        OnPropertyChanged(propertyName);
        return true;
    }

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
