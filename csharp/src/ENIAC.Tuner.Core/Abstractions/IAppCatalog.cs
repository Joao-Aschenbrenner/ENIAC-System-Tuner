using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Core.Abstractions;

/// <summary>
/// Interface para integração com winget package manager
/// </summary>
public interface IWingetService
{
    /// <summary>
    /// Executa instalação de um pacote via winget
    /// </summary>
    Task<bool> InstallPackageAsync(string wingetId, bool dryRun = false);
    
    /// <summary>
    /// Lista aplicativos disponíveis (filtra ou busca)
    /// </summary>
    Task<List<string>> SearchPackagesAsync(string query);
    
    /// <summary>
    /// Exporta lista de apps instalados
    /// </summary>
    Task<string> ExportInstalledAsync(string filePath);
    
    /// <summary>
    /// Importa e instala apps de um arquivo de exportação
    /// </summary>
    Task InstallFromFileAsync(string filePath);
    
    /// <summary>
    /// Obtém informações de um pacote específico
    /// </summary>
    Task<WingetPackageInfo?> GetPackageInfoAsync(string wingetId);
}

/// <summary>
/// Informações sobre um pacote no winget
/// </summary>
public record WingetPackageInfo(
    string Id,
    string Name,
    string Version,
    string Publisher,
    string Description,
    string? Moniker,
    string? Installer
);

/// <summary>
/// Interface para gerenciar catálogo de aplicações
/// </summary>
public interface IAppCatalogManager
{
    /// <summary>
    /// Carrega o catálogo padrão
    /// </summary>
    Task<AppCatalog> LoadDefaultCatalogAsync();
    
    /// <summary>
    /// Salva o catálogo em arquivo (para persistência de seleções)
    /// </summary>
    Task SaveCatalogAsync(AppCatalog catalog, string filePath);
    
    /// <summary>
    /// Carrega catálogo salvo
    /// </summary>
    Task<AppCatalog> LoadCatalogAsync(string filePath);
    
    /// <summary>
    /// Executa instalação em lote
    /// </summary>
    Task<BatchInstallationSession> InstallBatchAsync(
        List<AppEntry> apps,
        bool dryRun = false,
        bool continueOnError = true,
        CancellationToken cancellationToken = default);
    
    /// <summary>
    /// Zera todas as seleções
    /// </summary>
    void ClearSelections(AppCatalog catalog);
}

/// <summary>
/// Interface para validação de segurança operacional
/// </summary>
public interface IOperationalSecurityValidator
{
    /// <summary>
    /// Valida segurança operacional de uma sessão de instalação
    /// </summary>
    (bool IsSecure, List<string> Issues) ValidateSession(BatchInstallationSession session);
    
    /// <summary>
    /// Verifica se um app é conhecido e confiável
    /// </summary>
    bool IsAppTrusted(string wingetId);
}
