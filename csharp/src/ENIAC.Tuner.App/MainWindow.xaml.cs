using System.Windows;
using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using ENIAC.Tuner.Core.Services;
using ENIAC.Tuner.Core.ViewModels;
using ENIAC.Tuner.Infrastructure.Services;

namespace ENIAC.Tuner.App;

public partial class MainWindow : Window
{
    private readonly MainDashboardViewModel _viewModel;
    private CancellationTokenSource? _currentRunCts;

    public MainWindow()
    {
        InitializeComponent();

        IOptimizationRunner runner = new OptimizationRunner();
        ISystemAnalyzer analyzer = new WindowsSystemAnalyzerAdapter();
        ISystemSecurity security = new WindowsSecurityAdapter();

        _viewModel = new MainDashboardViewModel(runner, analyzer, security);
        DataContext = _viewModel;
    }

    private async void SafeOptimizeButton_Click(object sender, RoutedEventArgs e)
    {
        await RunProfileAsync(WindowsOptimizationProfiles.SafeProfile());
    }

    private async void NetworkOptimizeButton_Click(object sender, RoutedEventArgs e)
    {
        await RunProfileAsync(WindowsOptimizationProfiles.NetworkProfile());
    }

    private async void HardcoreOptimizeButton_Click(object sender, RoutedEventArgs e)
    {
        var confirm = MessageBox.Show(
            "O perfil Hardcore aplica ajustes agressivos de rede e desempenho.\n\nEles podem ser revertidos via botao Reverter.\n\nDeseja continuar?",
            "Hardcore — confirmacao",
            MessageBoxButton.YesNo,
            MessageBoxImage.Warning);

        if (confirm == MessageBoxResult.Yes)
        {
            await RunProfileAsync(WindowsOptimizationProfiles.HardcoreProfile());
        }
    }

    private async void ExtremeOptimizeButton_Click(object sender, RoutedEventArgs e)
    {
        var confirm = MessageBox.Show(
            "ATENCAO: O perfil EXTREMO desativa servicos do Windows (SysMain, WSearch).\n\n" +
            "Use somente em maquinas dedicadas.\nEles podem ser revertidos via botao Reverter.\n\nDeseja continuar?",
            "EXTREMO — confirmacao",
            MessageBoxButton.YesNo,
            MessageBoxImage.Warning);

        if (confirm == MessageBoxResult.Yes)
        {
            await RunProfileAsync(WindowsOptimizationProfiles.ExtremeProfile());
        }
    }

    private async void RollbackButton_Click(object sender, RoutedEventArgs e)
    {
        var confirm = MessageBox.Show(
            $"Reverter as otimizacoes de '{_viewModel.LastProfileName}'?\n\nAs configuracoes anteriores serao restauradas.",
            "Confirmar rollback",
            MessageBoxButton.YesNo,
            MessageBoxImage.Question);

        if (confirm != MessageBoxResult.Yes) return;

        _currentRunCts = new CancellationTokenSource();
        try
        {
            await _viewModel.RollbackLastProfileAsync(_currentRunCts.Token);
        }
        catch (OperationCanceledException)
        {
            // status/log atualizados pelo ViewModel
        }
        finally
        {
            _currentRunCts?.Dispose();
            _currentRunCts = null;
        }
    }

    private void AnalyzeButton_Click(object sender, RoutedEventArgs e)
    {
        _viewModel.AnalyzeSystem();
    }

    private async void DeepAnalyzeButton_Click(object sender, RoutedEventArgs e)
    {
        _currentRunCts = new CancellationTokenSource();

        try
        {
            await _viewModel.DeepAnalyzeAsync(_currentRunCts.Token);
        }
        catch (OperationCanceledException)
        {
            // status/log atualizados pelo ViewModel
        }
    }

    private void CancelButton_Click(object sender, RoutedEventArgs e)
    {
        _currentRunCts?.Cancel();
        _viewModel.AppendLog("Cancelamento solicitado pelo usuario.");
    }

    private async Task RunProfileAsync(OptimizationProfile profile)
    {
        _currentRunCts = new CancellationTokenSource();

        try
        {
            var executed = await _viewModel.ExecuteProfileAsync(profile, _currentRunCts.Token);
            if (!executed)
            {
                MessageBox.Show(
                    "Este perfil exige privilegios de administrador.\n\nExecute o aplicativo como Administrador.",
                    "Permissao necessaria",
                    MessageBoxButton.OK,
                    MessageBoxImage.Warning);
            }
        }
        catch (OperationCanceledException)
        {
            // status/log atualizados pelo ViewModel
        }
        finally
        {
            _currentRunCts.Dispose();
            _currentRunCts = null;
        }
    }
}