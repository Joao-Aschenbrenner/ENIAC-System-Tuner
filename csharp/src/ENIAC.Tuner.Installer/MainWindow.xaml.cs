using System.Diagnostics;
using System.IO;
using System.Windows;
using Microsoft.Win32;

namespace ENIAC.Tuner.Installer;

public partial class MainWindow : Window
{
    private const string AppExeName = "ENIAC.Tuner.App.exe";
    private const string CliExeName = "ENIAC.Tuner.Cli.exe";

    public MainWindow()
    {
        InitializeComponent();
        InstallPathBox.Text = @"C:\Program Files\ENIAC";
        AppendLog("Instalador carregado.");
    }

    private void BrowseButton_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new OpenFolderDialog
        {
            InitialDirectory = InstallPathBox.Text,
            Title = "Selecione pasta de instalação"
        };

        if (dialog.ShowDialog() == true)
        {
            InstallPathBox.Text = dialog.FolderName;
        }
    }

    private async void InstallButton_Click(object sender, RoutedEventArgs e)
    {
        InstallButton.IsEnabled = false;
        UpdateProgress(0);

        try
        {
            var destination = InstallPathBox.Text.Trim();
            if (string.IsNullOrWhiteSpace(destination))
            {
                MessageBox.Show("Informe uma pasta de instalação válida.", "Erro", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            if (!Path.IsPathRooted(destination))
            {
                MessageBox.Show("Use um caminho absoluto para a instalação.", "Erro", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            await InstallAsync(destination);
            MessageBox.Show("Instalação concluída com sucesso.", "ENIAC Installer", MessageBoxButton.OK, MessageBoxImage.Information);
        }
        catch (Exception ex)
        {
            AppendLog($"Erro: {ex.Message}");
            MessageBox.Show(ex.Message, "Falha na instalação", MessageBoxButton.OK, MessageBoxImage.Error);
        }
        finally
        {
            InstallButton.IsEnabled = true;
        }
    }

    private void CloseButton_Click(object sender, RoutedEventArgs e)
    {
        Close();
    }

    private async Task InstallAsync(string destination)
    {
        var sourceDir = ResolveSourceDirectory();
        AppendLog($"Origem detectada: {sourceDir}");

        Directory.CreateDirectory(destination);
        UpdateProgress(10);

        await CopyRequiredBinaryAsync(sourceDir, destination, AppExeName);
        UpdateProgress(60);

        var cliCopied = await TryCopyOptionalBinaryAsync(sourceDir, destination, CliExeName);
        if (cliCopied)
        {
            AppendLog("CLI detectado e copiado.");
        }
        else
        {
            AppendLog("CLI não encontrado; instalação seguirá apenas com o app principal.");
        }

        UpdateProgress(75);

        if (DesktopShortcutCheck.IsChecked == true)
        {
            var desktop = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
            CreateShortcut(desktop, "ENIAC System Tuner", Path.Combine(destination, AppExeName));
            AppendLog("Atalho desktop criado.");
        }

        if (StartMenuShortcutCheck.IsChecked == true)
        {
            var startMenu = Environment.GetFolderPath(Environment.SpecialFolder.Programs);
            CreateShortcut(startMenu, "ENIAC System Tuner", Path.Combine(destination, AppExeName));
            AppendLog("Atalho menu iniciar criado.");
        }

        UpdateProgress(100);
        AppendLog("Instalação finalizada.");
    }

    private static string ResolveSourceDirectory()
    {
        var baseDir = AppContext.BaseDirectory;
        var cwd = Environment.CurrentDirectory;

        var candidates = new List<string>
        {
            baseDir,
            cwd
        };

        IEnumerable<string> ExpandSearchRoots(string root)
        {
            if (string.IsNullOrWhiteSpace(root))
            {
                yield break;
            }

            var dir = new DirectoryInfo(root);
            while (dir is not null)
            {
                yield return dir.FullName;
                yield return Path.Combine(dir.FullName, "artifacts", "release");
                yield return Path.Combine(dir.FullName, "csharp", "artifacts", "release");
                yield return Path.Combine(dir.FullName, "src", "artifacts", "release");
                yield return Path.Combine(dir.FullName, "src", "ENIAC.Tuner.App", "bin", "Release", "net10.0-windows");
                yield return Path.Combine(dir.FullName, "src", "ENIAC.Tuner.App", "bin", "Debug", "net10.0-windows");
                dir = dir.Parent;
            }
        }

        candidates.AddRange(ExpandSearchRoots(baseDir));
        candidates.AddRange(ExpandSearchRoots(cwd));

        foreach (var path in candidates.Distinct())
        {
            if (Directory.Exists(path) && FindFile(path, AppExeName) is not null)
            {
                return path;
            }
        }

        throw new InvalidOperationException("Não foi possível localizar a pasta de origem do ENIAC.Tuner.App.exe.");
    }

    private async Task CopyRequiredBinaryAsync(string sourceDir, string destinationDir, string fileName)
    {
        var file = FindFile(sourceDir, fileName);
        if (file is null)
        {
            throw new FileNotFoundException($"Arquivo necessário não encontrado: {fileName}");
        }

        var dest = Path.Combine(destinationDir, fileName);
        await using var source = File.OpenRead(file);
        await using var target = File.Create(dest);
        await source.CopyToAsync(target);
        AppendLog($"Copiado: {fileName}");
    }

    private async Task<bool> TryCopyOptionalBinaryAsync(string sourceDir, string destinationDir, string fileName)
    {
        var file = FindFile(sourceDir, fileName);
        if (file is null)
        {
            return false;
        }

        var dest = Path.Combine(destinationDir, fileName);
        await using var source = File.OpenRead(file);
        await using var target = File.Create(dest);
        await source.CopyToAsync(target);
        AppendLog($"Copiado: {fileName}");
        return true;
    }

    private static string? FindFile(string root, string name)
    {
        try
        {
            return Directory
                .EnumerateFiles(root, name, SearchOption.AllDirectories)
                .FirstOrDefault();
        }
        catch
        {
            return null;
        }
    }

    private static void CreateShortcut(string targetFolder, string shortcutName, string targetPath)
    {
        var shortcutPath = Path.Combine(targetFolder, $"{shortcutName}.lnk");
        var script =
            "$WshShell = New-Object -ComObject WScript.Shell; " +
            $"$Shortcut = $WshShell.CreateShortcut('{shortcutPath}'); " +
            $"$Shortcut.TargetPath = '{targetPath}'; " +
            $"$Shortcut.WorkingDirectory = '{Path.GetDirectoryName(targetPath)}'; " +
            "$Shortcut.Save();";

        var psi = new ProcessStartInfo
        {
            FileName = "powershell",
            Arguments = $"-NoProfile -ExecutionPolicy Bypass -Command \"{script}\"",
            CreateNoWindow = true,
            UseShellExecute = false
        };

        using var process = Process.Start(psi);
        process?.WaitForExit();
    }

    private void AppendLog(string message)
    {
        LogBox.AppendText($"[{DateTime.Now:HH:mm:ss}] {message}{Environment.NewLine}");
        LogBox.ScrollToEnd();
    }

    private void UpdateProgress(double value)
    {
        InstallProgress.Value = value;
        ProgressText.Text = $"{value:F0}%";
    }
}