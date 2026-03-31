using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Microsoft.Win32;
using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using ENIAC.Tuner.Core.Services;
using ENIAC.Tuner.Core.ViewModels;
using ENIAC.Tuner.Infrastructure.Services;

namespace ENIAC.Tuner.App;

public partial class MainWindow : Window
{
    private const string LegalDisclaimer =
        "Testado no desktop pessoal do desenvolvedor. Nao ha garantia de compatibilidade universal e algumas acoes podem quebrar funcionalidades.";

    private readonly MainDashboardViewModel _viewModel;
    private readonly IAutounattendBuilder _autounattendBuilder;
    private readonly IWindowsCompatibilityAnalyzer _compatibilityAnalyzer;
    private readonly IAppCatalogManager _appCatalogManager;
    private CancellationTokenSource? _currentRunCts;
    private AppCatalog? _catalog;
    private AppCategory _selectedCategory = AppCategory.Development;

    public MainWindow()
    {
        InitializeComponent();

        IOptimizationRunner runner = new OptimizationRunner();
        ISystemAnalyzer analyzer = new WindowsSystemAnalyzerAdapter();
        ISystemSecurity security = new WindowsSecurityAdapter();

        _viewModel = new MainDashboardViewModel(runner, analyzer, security);
        _autounattendBuilder = new AutounattendBuilder(analyzer);
        _compatibilityAnalyzer = new WindowsCompatibilityAnalyzer();
        _appCatalogManager = new AppCatalogManager(new WingetService(), new OperationalSecurityValidator(), analyzer);
        DataContext = _viewModel;

        ShowCompatibilityGuardrails();
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
        if (!ConfirmHighRiskAction("EXTREMO", "desativa o servico de indexacao do Windows Search"))
        {
            return;
        }

        await RunProfileAsync(WindowsOptimizationProfiles.ExtremeProfile());
    }

    private async void PolicyMaxButton_Click(object sender, RoutedEventArgs e)
    {
        if (!ConfirmHighRiskAction("Policy-Max", "aplica politicas agressivas de privacidade/debloat"))
        {
            return;
        }

        await RunProfileAsync(WindowsOptimizationProfiles.PolicyMaxProfile());
    }

    private async void GenerateAggressiveAutounattendButton_Click(object sender, RoutedEventArgs e)
    {
        if (!ConfirmHighRiskAction("Autounattend Agressivo", "gera instalacao com preset agressivo"))
        {
            return;
        }

        await SaveAutounattendPresetAsync("aggressive");
    }

    private async void GenerateModerateAutounattendButton_Click(object sender, RoutedEventArgs e)
    {
        await SaveAutounattendPresetAsync("moderate");
    }

    private async void GenerateUnifiedAutounattendButton_Click(object sender, RoutedEventArgs e)
    {
        await EnsureCatalogLoadedAsync();

        var selectedPreset = "moderate";
        if (AutounattendPresetComboBox.SelectedItem is System.Windows.Controls.ComboBoxItem item &&
            item.Tag is string presetFromTag &&
            !string.IsNullOrWhiteSpace(presetFromTag))
        {
            selectedPreset = presetFromTag;
        }

        var config = _autounattendBuilder.LoadPreset(selectedPreset);
        var selectedApps = _catalog?.GetSelectedApps() ?? [];
        AppendSelectedAppsToAutounattend(config, selectedApps);

        await SaveAutounattendConfigurationAsync(config, selectedPreset, selectedApps.Count);
    }

    private void ValidateWindowsCompatibilityButton_Click(object sender, RoutedEventArgs e)
    {
        var (build, edition, version) = _compatibilityAnalyzer.GetWindowsInfo();
        var selectedPreset = "moderate";
        if (AutounattendPresetComboBox.SelectedItem is System.Windows.Controls.ComboBoxItem item &&
            item.Tag is string presetFromTag &&
            !string.IsNullOrWhiteSpace(presetFromTag))
        {
            selectedPreset = presetFromTag;
        }

        var config = _autounattendBuilder.LoadPreset(selectedPreset);
        var (isCompatible, warnings) = _compatibilityAnalyzer.CheckCompatibility(config, build, edition);

        var message =
            $"Windows detectado: versao={version} build={build} edicao={edition}\n\n" +
            (warnings.Count == 0
                ? "Nenhum alerta de compatibilidade encontrado."
                : "Alertas:\n - " + string.Join("\n - ", warnings));

        MessageBox.Show(
            message,
            isCompatible ? "Compatibilidade OK" : "Compatibilidade com Alertas",
            MessageBoxButton.OK,
            isCompatible ? MessageBoxImage.Information : MessageBoxImage.Warning);
    }

    // ─── Aba 3: Catálogo de Apps ─────────────────────────────────────────────

    private async Task EnsureCatalogLoadedAsync()
    {
        if (_catalog is not null) return;
        _catalog = await _appCatalogManager.LoadDefaultCatalogAsync();
    }

    private async void MainTabControl_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
    {
        // Processa apenas a troca real de aba do controle principal.
        // SelectionChanged de controles filhos (ListBox/ComboBox) tambem borbulha aqui.
        if (!ReferenceEquals(e.OriginalSource, MainTabControl))
        {
            return;
        }

        if (MainTabControl.SelectedIndex != 1) return;
        await EnsureCatalogLoadedAsync();
        PopulateCategoryList();
    }

    private void PopulateCategoryList()
    {
        if (_catalog is null) return;

        var orderedCategories = _catalog.Entries.Keys
            .OrderBy(c => c.ToString())
            .ToList();

        CatalogCategoryListBox.ItemsSource = orderedCategories;

        if (CatalogCategoryListBox.SelectedItem is AppCategory selectedCategory &&
            orderedCategories.Contains(selectedCategory))
        {
            return;
        }

        if (orderedCategories.Contains(_selectedCategory))
        {
            CatalogCategoryListBox.SelectedItem = _selectedCategory;
            return;
        }

        CatalogCategoryListBox.SelectedIndex = orderedCategories.Count > 0 ? 0 : -1;
    }

    private void CatalogCategoryListBox_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
    {
        if (CatalogCategoryListBox.SelectedItem is not AppCategory category) return;
        _selectedCategory = category;
        CatalogCategoryTitleText.Text = category.ToString();
        CatalogAppsListBox.ItemsSource = _catalog?.GetAppsByCategory(category);
        RefreshCatalogSummary();
    }

    private void SelectAllCategoryButton_Click(object sender, RoutedEventArgs e)
    {
        if (_catalog is null) return;
        foreach (var app in _catalog.GetAppsByCategory(_selectedCategory))
            app.IsSelected = true;
        RefreshCatalogView();
    }

    private void ClearCategoryButton_Click(object sender, RoutedEventArgs e)
    {
        if (_catalog is null) return;
        foreach (var app in _catalog.GetAppsByCategory(_selectedCategory))
            app.IsSelected = false;
        RefreshCatalogView();
    }

    private void CatalogAppSelectionChanged(object sender, RoutedEventArgs e)
    {
        RefreshCatalogSummary();
    }

    private void CatalogAppRow_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
    {
        if (_catalog is null)
        {
            return;
        }

        // Evita alternar duas vezes quando o clique foi diretamente no CheckBox.
        if (e.OriginalSource is DependencyObject original && FindVisualParent<CheckBox>(original) is not null)
        {
            return;
        }

        if (sender is FrameworkElement element && element.DataContext is AppEntry app)
        {
            app.IsSelected = !app.IsSelected;
            RefreshCatalogView();
            e.Handled = true;
        }
    }

    private void CatalogAppsListBox_MouseDoubleClick(object sender, MouseButtonEventArgs e)
    {
        if (_catalog is null)
        {
            return;
        }

        if (CatalogAppsListBox.SelectedItem is AppEntry app)
        {
            app.IsSelected = !app.IsSelected;
            RefreshCatalogView();
            e.Handled = true;
        }
    }

    private void CatalogAppsListBox_PreviewKeyDown(object sender, KeyEventArgs e)
    {
        if (_catalog is null)
        {
            return;
        }

        if (e.Key == Key.Space && CatalogAppsListBox.SelectedItem is AppEntry app)
        {
            app.IsSelected = !app.IsSelected;
            RefreshCatalogView();
            e.Handled = true;
        }
    }

    private void RefreshCatalogView()
    {
        CatalogAppsListBox.Items.Refresh();
        RefreshCatalogSummary();
    }

    private void RefreshCatalogSummary()
    {
        var count = _catalog?.SelectedCount ?? 0;
        CatalogSummaryText.Text = $"Selecionados: {count}";
        UpdateCatalogActionState(count > 0);
    }

    private void UpdateCatalogActionState(bool hasSelection)
    {
        GenerateUnifiedAutounattendBottomButton.IsEnabled = hasSelection;

        if (!hasSelection && CatalogStatusText.Text.StartsWith("Pronto", StringComparison.OrdinalIgnoreCase) == false)
        {
            CatalogStatusText.Text = "Pronto para selecionar apps.";
        }
    }

    private static T? FindVisualParent<T>(DependencyObject child) where T : DependencyObject
    {
        var current = child;
        while (current is not null)
        {
            if (current is T typed)
            {
                return typed;
            }

            current = System.Windows.Media.VisualTreeHelper.GetParent(current);
        }

        return null;
    }

    private AppCatalog BuildSelectedCatalog(AppCatalog source)
    {
        var filtered = new AppCatalog
        {
            Version = source.Version,
            LastUpdated = DateTime.Now
        };

        foreach (var (category, apps) in source.Entries)
        {
            var selectedApps = apps
                .Where(app => app.IsSelected)
                .Select(app => new AppEntry
                {
                    WingetId = app.WingetId,
                    DisplayName = app.DisplayName,
                    Category = app.Category,
                    Description = app.Description,
                    RiskLevel = app.RiskLevel,
                    Prerequisites = [.. app.Prerequisites],
                    IsSelected = true,
                    InstalledVersion = app.InstalledVersion,
                    InfoUrl = app.InfoUrl
                })
                .ToList();

            if (selectedApps.Count > 0)
            {
                filtered.Entries[category] = selectedApps;
            }
        }

        return filtered;
    }

    private async void ExportCatalogSelectionButton_Click(object sender, RoutedEventArgs e)
    {
        await EnsureCatalogLoadedAsync();
        var selected = _catalog!.GetSelectedApps();
        if (selected.Count == 0)
        {
            MessageBox.Show("Nenhum app selecionado.", "Exportar", MessageBoxButton.OK, MessageBoxImage.Information);
            return;
        }

        var saveDialog = new SaveFileDialog
        {
            Title = "Exportar selecao",
            Filter = "JSON (*.json)|*.json|Todos os arquivos (*.*)|*.*",
            FileName = "eniac-catalogo-selecao.json"
        };

        if (saveDialog.ShowDialog() != true) return;

        var selectedCatalog = BuildSelectedCatalog(_catalog!);
        await _appCatalogManager.SaveCatalogAsync(selectedCatalog, saveDialog.FileName);
        CatalogStatusText.Text = $"Selecao exportada: {selected.Count} app(s).";
        MessageBox.Show($"{selected.Count} apps exportados.", "Exportar", MessageBoxButton.OK, MessageBoxImage.Information);
    }

    private async void ImportCatalogSelectionButton_Click(object sender, RoutedEventArgs e)
    {
        await EnsureCatalogLoadedAsync();

        var openDialog = new OpenFileDialog
        {
            Title = "Importar selecao de apps",
            Filter = "JSON (*.json)|*.json|Todos os arquivos (*.*)|*.*"
        };

        if (openDialog.ShowDialog() != true)
        {
            return;
        }

        try
        {
            var imported = await _appCatalogManager.LoadCatalogAsync(openDialog.FileName);
            _appCatalogManager.ClearSelections(_catalog!);

            var selectedIds = imported.GetSelectedApps()
                .Select(app => app.WingetId)
                .Where(id => !string.IsNullOrWhiteSpace(id))
                .Distinct(StringComparer.OrdinalIgnoreCase)
                .ToHashSet(StringComparer.OrdinalIgnoreCase);

            var allLocalApps = _catalog!.Entries.Values.SelectMany(list => list).ToList();
            var matched = 0;

            foreach (var app in allLocalApps)
            {
                if (selectedIds.Contains(app.WingetId))
                {
                    app.IsSelected = true;
                    matched++;
                }
            }

            var notFound = selectedIds.Count - matched;
            RefreshCatalogView();

            CatalogStatusText.Text =
                notFound > 0
                    ? $"Importado: {matched} app(s). Nao encontrados: {notFound}."
                    : $"Importado: {matched} app(s).";

            MessageBox.Show(
                notFound > 0
                    ? $"Selecao importada com sucesso.\nEncontrados: {matched}\nNao encontrados no catalogo atual: {notFound}"
                    : $"Selecao importada com sucesso.\nApps encontrados: {matched}",
                "Importar Selecao",
                MessageBoxButton.OK,
                notFound > 0 ? MessageBoxImage.Warning : MessageBoxImage.Information);
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                $"Falha ao importar selecao:\n{ex.Message}",
                "Importar Selecao",
                MessageBoxButton.OK,
                MessageBoxImage.Error);
        }
    }

    private async void DryRunSelectedAppsButton_Click(object sender, RoutedEventArgs e)
    {
        await EnsureCatalogLoadedAsync();
        var selected = _catalog!.GetSelectedApps();
        if (selected.Count == 0)
        {
            MessageBox.Show("Nenhum app selecionado.", "Dry-run", MessageBoxButton.OK, MessageBoxImage.Information);
            return;
        }

        CatalogStatusText.Text = "Executando dry-run…";
        var session = await _appCatalogManager.InstallBatchAsync(selected, dryRun: true);
        CatalogStatusText.Text = $"Dry-run concluido: {session.SuccessCount} ok, {session.FailureCount} falhas.";

        var details = session.Results.Count > 0
            ? "\n\nDetalhes:\n" + string.Join("\n", session.Results.Select(r => $"  [{(r.Success ? "OK" : "FAIL")}] {r.WingetId}"))
            : string.Empty;

        MessageBox.Show(
            $"Dry-run finalizado.\nApps: {session.PlannedApps.Count}\nSucesso: {session.SuccessCount}\nFalhas: {session.FailureCount}{details}",
            "Dry-run Winget",
            MessageBoxButton.OK,
            MessageBoxImage.Information);
    }

    private async void InstallSelectedAppsButton_Click(object sender, RoutedEventArgs e)
    {
        await EnsureCatalogLoadedAsync();
        var selected = _catalog!.GetSelectedApps();
        if (selected.Count == 0)
        {
            MessageBox.Show("Nenhum app selecionado.", "Instalar", MessageBoxButton.OK, MessageBoxImage.Information);
            return;
        }

        if (!ConfirmHighRiskAction("Instalacao em lote", $"instala {selected.Count} apps via winget"))
            return;

        CatalogStatusText.Text = "Instalando…";
        var session = await _appCatalogManager.InstallBatchAsync(selected, dryRun: false);
        CatalogStatusText.Text = $"Instalacao concluida: {session.SuccessCount} ok, {session.FailureCount} falhas.";

        MessageBox.Show(
            $"Instalacao finalizada.\nSucesso: {session.SuccessCount}\nFalhas: {session.FailureCount}",
            "Instalar Apps",
            MessageBoxButton.OK,
            session.FailureCount == 0 ? MessageBoxImage.Information : MessageBoxImage.Warning);
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

    private bool ConfirmHighRiskAction(string actionName, string actionDescription)
    {
        var confirm = MessageBox.Show(
            $"ATENCAO: {actionName} {actionDescription}.\n\n" +
            $"{LegalDisclaimer}\n\n" +
            "Deseja continuar?",
            $"{actionName} - alto risco",
            MessageBoxButton.YesNo,
            MessageBoxImage.Warning);

        if (confirm != MessageBoxResult.Yes)
        {
            return false;
        }

        var secondConfirm = MessageBox.Show(
            "Confirmacao final obrigatoria: esta acao pode exigir recuperacao manual do sistema. Prosseguir?",
            "Confirmacao final",
            MessageBoxButton.YesNo,
            MessageBoxImage.Warning);

        return secondConfirm == MessageBoxResult.Yes;
    }

    private async Task SaveAutounattendPresetAsync(string presetName)
    {
        var saveDialog = new SaveFileDialog
        {
            Title = "Salvar autounattend.xml",
            Filter = "XML (*.xml)|*.xml|Todos os arquivos (*.*)|*.*",
            FileName = "autounattend.xml"
        };

        if (saveDialog.ShowDialog() != true)
        {
            return;
        }

        var config = _autounattendBuilder.LoadPreset(presetName);
        await _autounattendBuilder.SaveToFileAsync(config, saveDialog.FileName);

        MessageBox.Show(
            $"Arquivo gerado com sucesso em:\n{saveDialog.FileName}",
            "Autounattend",
            MessageBoxButton.OK,
            MessageBoxImage.Information);
    }

    private void AppendSelectedAppsToAutounattend(AutounattendConfiguration config, List<AppEntry> selectedApps)
    {
        if (selectedApps.Count == 0)
        {
            return;
        }

        var nextOrder = config.FirstLogonCommands.Count == 0
            ? 1
            : config.FirstLogonCommands.Max(c => c.Order) + 1;

        foreach (var app in selectedApps)
        {
            var wingetCommand =
                $"powershell.exe -ExecutionPolicy Bypass -Command \"winget install --id {app.WingetId} --exact --silent --accept-package-agreements --accept-source-agreements\"";

            config.FirstLogonCommands.Add(new AutounattendCommand
            {
                Order = nextOrder++,
                Description = $"Instalar app selecionado: {app.DisplayName}",
                CommandLine = wingetCommand,
                RiskLevel = app.RiskLevel,
                RequiresReboot = false
            });
        }

        config.Notes = selectedApps.Count > 0
            ? $"Gerado com {selectedApps.Count} app(s) selecionado(s) no catalogo."
            : config.Notes;
    }

    private async Task SaveAutounattendConfigurationAsync(AutounattendConfiguration config, string presetName, int selectedAppsCount)
    {
        var saveDialog = new SaveFileDialog
        {
            Title = "Salvar autounattend.xml",
            Filter = "XML (*.xml)|*.xml|Todos os arquivos (*.*)|*.*",
            FileName = "autounattend.xml"
        };

        if (saveDialog.ShowDialog() != true)
        {
            return;
        }

        await _autounattendBuilder.SaveToFileAsync(config, saveDialog.FileName);

        var appsInfo = selectedAppsCount > 0
            ? $"\nApps incorporados ao FirstLogon: {selectedAppsCount}"
            : "\nNenhum app selecionado no catalogo.";

        MessageBox.Show(
            $"Arquivo gerado com sucesso em:\n{saveDialog.FileName}\nPreset: {presetName}{appsInfo}",
            "Autounattend unificado",
            MessageBoxButton.OK,
            MessageBoxImage.Information);
    }

    private void ShowCompatibilityGuardrails()
    {
        var (build, edition, version) = _compatibilityAnalyzer.GetWindowsInfo();
        if (build <= 0)
        {
            return;
        }

        if (build < 22000)
        {
            MessageBox.Show(
                $"Sistema detectado: versao={version} build={build} ({edition}).\n\n" +
                "Este app foi otimizado para Windows 11. Alguns recursos podem nao funcionar como esperado.",
                "Guardrail de compatibilidade",
                MessageBoxButton.OK,
                MessageBoxImage.Warning);
        }
        else if (edition.Contains("Home", StringComparison.OrdinalIgnoreCase))
        {
            MessageBox.Show(
                $"Sistema detectado: versao={version} build={build} ({edition}).\n\n" +
                "A edicao Home tem limitacoes para algumas politicas corporativas.",
                "Guardrail de edicao",
                MessageBoxButton.OK,
                MessageBoxImage.Information);
        }
    }
}