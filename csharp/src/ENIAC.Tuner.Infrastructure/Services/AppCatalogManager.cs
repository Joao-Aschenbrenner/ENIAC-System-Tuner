using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using System.Diagnostics;
using System.Text.Json;

namespace ENIAC.Tuner.Infrastructure.Services;

/// <summary>
/// Gerenciador de catálogo de aplicações com integração winget
/// </summary>
public class AppCatalogManager : IAppCatalogManager
{
    private readonly IWingetService _wingetService;
    private readonly IOperationalSecurityValidator _securityValidator;
    private readonly ISystemAnalyzer _systemAnalyzer;
    
    public AppCatalogManager(
        IWingetService wingetService,
        IOperationalSecurityValidator securityValidator,
        ISystemAnalyzer systemAnalyzer)
    {
        _wingetService = wingetService;
        _securityValidator = securityValidator;
        _systemAnalyzer = systemAnalyzer;
    }
    
    public async Task<AppCatalog> LoadDefaultCatalogAsync()
    {
        var catalog = new AppCatalog();
        
        // DESENVOLVIMENTO
        catalog.Entries[AppCategory.Development] = new()
        {
            new AppEntry
            {
                WingetId = "Microsoft.VisualStudioCode",
                DisplayName = "Visual Studio Code",
                Category = AppCategory.Development,
                Description = "Editor de código moderno e leve",
                RiskLevel = RiskLevel.Safe,
                Prerequisites = []
            },
            new AppEntry
            {
                WingetId = "Microsoft.VisualStudio.Community",
                DisplayName = "Visual Studio Community",
                Category = AppCategory.Development,
                Description = "IDE completa para desenvolvimento .NET/C++",
                RiskLevel = RiskLevel.Moderate,
                Prerequisites = ["5GB space"]
            },
            new AppEntry
            {
                WingetId = "Git.Git",
                DisplayName = "Git",
                Category = AppCategory.Development,
                Description = "Controle de versão distribuído",
                RiskLevel = RiskLevel.Safe
            },
            new AppEntry
            {
                WingetId = "OpenJS.NodeJS",
                DisplayName = "Node.js",
                Category = AppCategory.Development,
                Description = "Runtime JavaScript para servidor",
                RiskLevel = RiskLevel.Safe
            },
            new AppEntry
            {
                WingetId = "Python.Python.3.12",
                DisplayName = "Python 3.12",
                Category = AppCategory.Development,
                Description = "Linguagem de programação Python",
                RiskLevel = RiskLevel.Safe
            }
        };
        
        // NAVEGADORES
        catalog.Entries[AppCategory.Browsers] = new()
        {
            new AppEntry
            {
                WingetId = "Mozilla.Firefox",
                DisplayName = "Mozilla Firefox",
                Category = AppCategory.Browsers,
                Description = "Navegador web moderno e eficiente",
                RiskLevel = RiskLevel.Safe
            },
            new AppEntry
            {
                WingetId = "Google.Chrome",
                DisplayName = "Google Chrome",
                Category = AppCategory.Browsers,
                Description = "Navegador web rápido",
                RiskLevel = RiskLevel.Moderate
            },
            new AppEntry
            {
                WingetId = "Microsoft.Edge",
                DisplayName = "Microsoft Edge",
                Category = AppCategory.Browsers,
                Description = "Navegador Chromium da Microsoft",
                RiskLevel = RiskLevel.Safe
            }
        };
        
        // PRODUTIVIDADE
        catalog.Entries[AppCategory.Productivity] = new()
        {
            new AppEntry
            {
                WingetId = "7zip.7zip",
                DisplayName = "7-Zip",
                Category = AppCategory.Productivity,
                Description = "Compressor de arquivos de código aberto",
                RiskLevel = RiskLevel.Safe
            },
            new AppEntry
            {
                WingetId = "Notion.Notion",
                DisplayName = "Notion",
                Category = AppCategory.Productivity,
                Description = "Plataforma all-in-one para notas e documentos",
                RiskLevel = RiskLevel.Safe
            },
            new AppEntry
            {
                WingetId = "Obsidian.Obsidian",
                DisplayName = "Obsidian",
                Category = AppCategory.Productivity,
                Description = "Aplicativo de notas com conexões",
                RiskLevel = RiskLevel.Safe
            }
        };
        
        // VÍDEO
        catalog.Entries[AppCategory.Video] = new()
        {
            new AppEntry
            {
                WingetId = "FFmpeg.FFmpeg",
                DisplayName = "FFmpeg",
                Category = AppCategory.Video,
                Description = "Ferramentas de processamento multimídia",
                RiskLevel = RiskLevel.Moderate
            },
            new AppEntry
            {
                WingetId = "VideoLAN.VLC",
                DisplayName = "VLC Media Player",
                Category = AppCategory.Video,
                Description = "Player multimídia versátil",
                RiskLevel = RiskLevel.Safe
            },
            new AppEntry
            {
                WingetId = "OBSProject.OBSStudio",
                DisplayName = "OBS Studio",
                Category = AppCategory.Video,
                Description = "Software de gravação e transmissão",
                RiskLevel = RiskLevel.Safe
            }
        };
        
        // GAMES
        catalog.Entries[AppCategory.Games] = new()
        {
            new AppEntry
            {
                WingetId = "Valve.Steam",
                DisplayName = "Steam",
                Category = AppCategory.Games,
                Description = "Plataforma de distribuição de jogos",
                RiskLevel = RiskLevel.Safe
            },
            new AppEntry
            {
                WingetId = "EpicGames.EpicGamesLauncher",
                DisplayName = "Epic Games Launcher",
                Category = AppCategory.Games,
                Description = "Launcher para jogos da Epic",
                RiskLevel = RiskLevel.Safe
            }
        };
        
        // UTILITÁRIOS
        catalog.Entries[AppCategory.Utilities] = new()
        {
            new AppEntry
            {
                WingetId = "Geek.Uninstaller",
                DisplayName = "Geek Uninstaller",
                Category = AppCategory.Utilities,
                Description = "Desinstalador profissional",
                RiskLevel = RiskLevel.Moderate
            },
            new AppEntry
            {
                WingetId = "WiseCleaner.WiseDiskCleaner",
                DisplayName = "Wise Disk Cleaner",
                Category = AppCategory.Utilities,
                Description = "Limpeza de disco e otimização",
                RiskLevel = RiskLevel.Moderate
            }
        };
        
        return catalog;
    }
    
    public async Task SaveCatalogAsync(AppCatalog catalog, string filePath)
    {
        var json = JsonSerializer.Serialize(catalog, new JsonSerializerOptions { WriteIndented = true });
        await File.WriteAllTextAsync(filePath, json);
    }
    
    public async Task<AppCatalog> LoadCatalogAsync(string filePath)
    {
        if (!File.Exists(filePath))
            throw new FileNotFoundException($"Catálogo não encontrado: {filePath}");
        
        var json = await File.ReadAllTextAsync(filePath);
        var catalog = JsonSerializer.Deserialize<AppCatalog>(json) ?? new AppCatalog();
        
        return catalog;
    }
    
    public async Task<BatchInstallationSession> InstallBatchAsync(
        List<AppEntry> apps,
        bool dryRun = false,
        bool continueOnError = true,
        CancellationToken cancellationToken = default)
    {
        var session = new BatchInstallationSession
        {
            PlannedApps = apps,
            IsDryRun = dryRun,
            ContinueOnError = continueOnError
        };
        
        // Validação de segurança
        var (isSecure, issues) = _securityValidator.ValidateSession(session);
        if (!isSecure)
        {
            foreach (var issue in issues)
            {
                var result = new AppInstallationResult
                {
                    Success = false,
                    Error = issue,
                    InstalledAt = DateTime.Now
                };
                session.Results.Add(result);
            }
            session.CompletedAt = DateTime.Now;
            return session;
        }
        
        // Instala cada app
        var order = 1;
        foreach (var app in apps)
        {
            if (cancellationToken.IsCancellationRequested)
                break;
            
            try
            {
                var stopwatch = Stopwatch.StartNew();
                var success = await _wingetService.InstallPackageAsync(app.WingetId, dryRun);
                stopwatch.Stop();
                
                var result = new AppInstallationResult
                {
                    WingetId = app.WingetId,
                    DisplayName = app.DisplayName,
                    Success = success,
                    Duration = stopwatch.Elapsed,
                    InstalledAt = DateTime.Now
                };
                
                session.Results.Add(result);
            }
            catch (Exception ex)
            {
                session.Results.Add(new AppInstallationResult
                {
                    WingetId = app.WingetId,
                    DisplayName = app.DisplayName,
                    Success = false,
                    Error = ex.Message,
                    InstalledAt = DateTime.Now
                });
                
                if (!session.ContinueOnError)
                    break;
            }
            
            order++;
        }
        
        session.CompletedAt = DateTime.Now;
        return session;
    }
    
    public void ClearSelections(AppCatalog catalog)
    {
        foreach (var category in catalog.Entries.Values)
        {
            foreach (var app in category)
            {
                app.IsSelected = false;
            }
        }
    }
}

/// <summary>
/// Serviço winget usando Process para execução
/// </summary>
public class WingetService : IWingetService
{
    public async Task<bool> InstallPackageAsync(string wingetId, bool dryRun = false)
    {
        var args = dryRun ? $"install {wingetId} --dry-run" : $"install {wingetId}";
        
        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = "winget",
                Arguments = args,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };
            
            using var process = Process.Start(psi);
            if (process == null)
                return false;
            
            await process.WaitForExitAsync();
            return process.ExitCode == 0;
        }
        catch
        {
            return false;
        }
    }
    
    public async Task<List<string>> SearchPackagesAsync(string query)
    {
        var results = new List<string>();
        
        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = "winget",
                Arguments = $"search {query}",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true
            };
            
            using var process = Process.Start(psi);
            if (process == null)
                return results;
            
            var output = await process.StandardOutput.ReadToEndAsync();
            results = output.Split('\n', StringSplitOptions.RemoveEmptyEntries)
                .Skip(1) // Skip header
                .Select(line => line.Split(' ').FirstOrDefault() ?? "")
                .Where(id => !string.IsNullOrEmpty(id))
                .ToList();
        }
        catch { }
        
        return results;
    }
    
    public async Task<string> ExportInstalledAsync(string filePath)
    {
        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = "winget",
                Arguments = $"export -o {filePath}",
                UseShellExecute = false,
                CreateNoWindow = true
            };
            
            using var process = Process.Start(psi);
            if (process != null)
                await process.WaitForExitAsync();
        }
        catch { }
        
        return filePath;
    }
    
    public async Task InstallFromFileAsync(string filePath)
    {
        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = "winget",
                Arguments = $"import -i {filePath}",
                UseShellExecute = false,
                CreateNoWindow = true
            };
            
            using var process = Process.Start(psi);
            if (process != null)
                await process.WaitForExitAsync();
        }
        catch { }
    }
    
    public async Task<WingetPackageInfo?> GetPackageInfoAsync(string wingetId)
    {
        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = "winget",
                Arguments = $"show {wingetId}",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true
            };
            
            using var process = Process.Start(psi);
            if (process == null)
                return null;
            
            var output = await process.StandardOutput.ReadToEndAsync();
            
            // Parse muito básico - em produção seria muito mais robusto
            return new WingetPackageInfo(
                Id: wingetId,
                Name: wingetId,
                Version: "1.0",
                Publisher: "Unknown",
                Description: "App from catalog",
                Moniker: null,
                Installer: null
            );
        }
        catch
        {
            return null;
        }
    }
}

/// <summary>
/// Validador de segurança operacional
/// </summary>
public class OperationalSecurityValidator : IOperationalSecurityValidator
{
    private static readonly HashSet<string> TrustedPublishers = new(StringComparer.OrdinalIgnoreCase)
    {
        "Microsoft",
        "Mozilla",
        "Git",
        "OpenJS",
        "Python",
        "VideoLAN",
        "Valve",
        "Epic Games",
        "Google"
    };
    
    public (bool IsSecure, List<string> Issues) ValidateSession(BatchInstallationSession session)
    {
        var issues = new List<string>();
        
        if (session.PlannedApps.Count > 20)
            issues.Add("⚠️ Mais de 20 apps para instalar - processo será longo");
        
        var highRiskApps = session.PlannedApps
            .Where(app => app.RiskLevel >= RiskLevel.High)
            .ToList();
        
        if (highRiskApps.Any())
            issues.Add($"⚠️ {highRiskApps.Count} app(s) com risco alto detectado(s)");
        
        var unsafeApps = session.PlannedApps
            .Where(app => !IsAppTrusted(app.WingetId))
            .ToList();
        
        if (unsafeApps.Any())
            issues.Add($"⚠️ {unsafeApps.Count} app(s) de editor desconhecido");
        
        return (issues.Count == 0, issues);
    }
    
    public bool IsAppTrusted(string wingetId)
    {
        // Extrai o publicador do ID (formato: Publisher.AppName)
        var parts = wingetId.Split('.', StringSplitOptions.RemoveEmptyEntries);
        if (parts.Length == 0)
            return false;
        
        var publisher = parts[0];
        return TrustedPublishers.Contains(publisher);
    }
}
