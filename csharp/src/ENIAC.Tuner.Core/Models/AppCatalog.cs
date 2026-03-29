using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Core.Models;

/// <summary>
/// Categorias de aplicações para o catálogo
/// </summary>
public enum AppCategory
{
    Development,
    Productivity,
    Games,
    Browsers,
    Video,
    Audio,
    Graphics,
    Drivers,
    Utilities
}

/// <summary>
/// Representa uma entrada no catálogo de aplicações
/// </summary>
public class AppEntry
{
    /// <summary>
    /// Identificador único winget (ex: "Microsoft.VisualStudioCode")
    /// </summary>
    public string WingetId { get; set; } = "";
    
    /// <summary>
    /// Nome do aplicativo para exibição
    /// </summary>
    public string DisplayName { get; set; } = "";
    
    /// <summary>
    /// Categoria do aplicativo
    /// </summary>
    public AppCategory Category { get; set; }
    
    /// <summary>
    /// Descrição breve
    /// </summary>
    public string Description { get; set; } = "";
    
    /// <summary>
    /// Nível de risco para instalação
    /// </summary>
    public RiskLevel RiskLevel { get; set; } = RiskLevel.Safe;
    
    /// <summary>
    /// Pré-requisitos ou dependências (ex: ".NET Runtime")
    /// </summary>
    public List<string> Prerequisites { get; set; } = [];
    
    /// <summary>
    /// Indica se é selecionado para instalação
    /// </summary>
    public bool IsSelected { get; set; } = false;
    
    /// <summary>
    /// Versão da última atualização do catálogo
    /// </summary>
    public string? InstalledVersion { get; set; }
    
    /// <summary>
    /// URL para mais informações
    /// </summary>
    public string? InfoUrl { get; set; }
}

/// <summary>
/// Catálogo completo de aplicações organizadas por categoria
/// </summary>
public class AppCatalog
{
    public string Version { get; set; } = "1.0";
    public DateTime LastUpdated { get; set; } = DateTime.Now;
    
    /// <summary>
    /// Aplicações organizadas por categoria
    /// </summary>
    public Dictionary<AppCategory, List<AppEntry>> Entries { get; set; } = new();
    
    /// <summary>
    /// Total de apps disponíveis
    /// </summary>
    public int TotalCount => Entries.Values.Sum(list => list.Count);
    
    /// <summary>
    /// Total de apps selecionados para instalação
    /// </summary>
    public int SelectedCount => Entries.Values.Sum(list => list.Count(app => app.IsSelected));
    
    /// <summary>
    /// Retorna todas as entradas selecionadas
    /// </summary>
    public List<AppEntry> GetSelectedApps()
    {
        return Entries.Values
            .SelectMany(list => list)
            .Where(app => app.IsSelected)
            .ToList();
    }
    
    /// <summary>
    /// Retorna apps de uma categoria específica
    /// </summary>
    public List<AppEntry> GetAppsByCategory(AppCategory category)
    {
        return Entries.TryGetValue(category, out var apps) ? apps : [];
    }
}

/// <summary>
/// Resultado da instalação de um aplicativo
/// </summary>
public class AppInstallationResult
{
    public string WingetId { get; set; } = "";
    public string DisplayName { get; set; } = "";
    public bool Success { get; set; } = false;
    public string? Error { get; set; }
    public TimeSpan Duration { get; set; }
    public DateTime InstalledAt { get; set; } = DateTime.Now;
    public string? InstalledVersion { get; set; }
}

/// <summary>
/// Sessão de instalação em lote
/// </summary>
public class BatchInstallationSession
{
    public Guid SessionId { get; set; } = Guid.NewGuid();
    public DateTime StartedAt { get; set; } = DateTime.Now;
    public DateTime? CompletedAt { get; set; }
    
    /// <summary>
    /// Apps que serão instalados
    /// </summary>
    public List<AppEntry> PlannedApps { get; set; } = [];
    
    /// <summary>
    /// Resultados de instalação
    /// </summary>
    public List<AppInstallationResult> Results { get; set; } = [];
    
    /// <summary>
    /// Modo simulação (dry-run)
    /// </summary>
    public bool IsDryRun { get; set; } = false;
    
    /// <summary>
    /// Continuar mesmo em caso de falha
    /// </summary>
    public bool ContinueOnError { get; set; } = true;
    
    public int SuccessCount => Results.Count(r => r.Success);
    public int FailureCount => Results.Count(r => !r.Success);
    public TimeSpan TotalDuration => (CompletedAt ?? DateTime.Now) - StartedAt;
}
