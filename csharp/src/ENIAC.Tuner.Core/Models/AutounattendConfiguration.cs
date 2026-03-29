namespace ENIAC.Tuner.Core.Models;

/// <summary>
/// Representa os diferentes passes do arquivo autounattend.xml
/// </summary>
public enum AutounattendPass
{
    /// <summary>
    /// Pass windowsPE - Executa durante o pré-setup do Windows
    /// </summary>
    WindowsPE,
    
    /// <summary>
    /// Pass offlineServicing - Executa entre a cópia de arquivos e a primeira reinicialização
    /// </summary>
    OfflineServicing,
    
    /// <summary>
    /// Pass generalize - Executa quando o usuário executa sysprep /generalize
    /// </summary>
    Generalize,
    
    /// <summary>
    /// Pass specialize - Executa após a primeira reinicialização, antes de ir para OOBE
    /// </summary>
    Specialize,
    
    /// <summary>
    /// Pass oobeSystem - Executa durante a experiência de primeiro uso (OOBE)
    /// </summary>
    OobeSystem,
    
    /// <summary>
    /// Pass oobeUser - Executa após o usuário criar uma conta durante OOBE
    /// </summary>
    OobeUser
}

/// <summary>
/// Nível de risco para configurações e otimizações
/// </summary>
public enum RiskLevel
{
    /// <summary>
    /// Seguro - Sem riscos conhecidos
    /// </summary>
    Safe = 0,
    
    /// <summary>
    /// Moderado - Alguns aplicativos podem não funcionar corretamente
    /// </summary>
    Moderate = 1,
    
    /// <summary>
    /// Alto - Pode quebrar funcionalidades importantes
    /// </summary>
    High = 2,
    
    /// <summary>
    /// Não testado - Funcionalidade desconhecida
    /// </summary>
    Untested = 3,
    
    /// <summary>
    /// Perigoso - Alto risco de provocar problemas
    /// </summary>
    Dangerous = 4
}

/// <summary>
///  Auditoria para rastrear quando e quem aplicou configurações
/// </summary>
public class ProductionVerification
{
    public DateTime AppliedAt { get; set; }
    public string AppliedBy { get; set; } = "System";
    public string Environment { get; set; } = "Unknown";  // Versão do Windows
    public string BuildNumber { get; set; } = "";
    public RiskLevel RiskLevel { get; set; } = RiskLevel.Safe;
    public bool IsProduction { get; set; } = false;
}

/// <summary>
/// Configuração de componente aninhada (ex: RemovePackages, Features)
/// </summary>
public class AutounattendComponentConfig
{
    public string ComponentName { get; set; } = "";
    public Dictionary<string, string> Settings { get; set; } = [];
    public List<string> Items { get; set; } = [];  // Packages, Features, etc.
    public RiskLevel RiskLevel { get; set; } = RiskLevel.Safe;
    public string? Description { get; set; }
}

/// <summary>
/// Definição de um comando a executar em FirstLogonCommands (pós-instalação)
/// </summary>
public class AutounattendCommand
{
    public int Order { get; set; }
    public string Description { get; set; } = "";
    public string CommandLine { get; set; } = "";
    public bool RequiresReboot { get; set; } = false;
    public RiskLevel RiskLevel { get; set; } = RiskLevel.Safe;
}

/// <summary>
/// Configuração principal do autounattend com todas as passagens
/// </summary>
public class AutounattendConfiguration
{
    public string ComputerName { get; set; } = "ENIAC-PC";
    public string UILanguage { get; set; } = "pt-BR";
    public string SystemLocale { get; set; } = "pt-BR";
    public string UserLocale { get; set; } = "pt-BR";
    public string KeyboardLayout { get; set; } = "Portuguese (Brazilian)";
    
    // Configurações por pass
    public List<AutounattendComponentConfig> WindowsPESettings { get; set; } = [];
    public List<AutounattendComponentConfig> SpecializeSettings { get; set; } = [];
    public List<AutounattendComponentConfig> OobeSystemSettings { get; set; } = [];
    
    // Comandos pós-instalação
    public List<AutounattendCommand> FirstLogonCommands { get; set; } = [];
    
    // Metadados
    public ProductionVerification Verification { get; set; } = new();
    public RiskLevel OverallRiskLevel { get; set; } = RiskLevel.Safe;
    public string PresetName { get; set; } = "Custom";
    public bool IsAggressive { get; set; } = true;
    public string? Notes { get; set; }
}
