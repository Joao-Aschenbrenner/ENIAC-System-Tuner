using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using Microsoft.Win32;
using System.Runtime.Versioning;

namespace ENIAC.Tuner.Infrastructure.Services;

/// <summary>
/// Analisa compatibilidade de configuração com a versão instalada do Windows
/// </summary>
public class WindowsCompatibilityAnalyzer : IWindowsCompatibilityAnalyzer
{
    [SupportedOSPlatform("windows")]
    public (int BuildNumber, string Edition, string Version) GetWindowsInfo()
    {
        if (!OperatingSystem.IsWindows())
        {
            return (0, "Unknown", "Unknown");
        }

        try
        {
            using var key = Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Microsoft\Windows NT\CurrentVersion");
            
            var buildNumber = int.TryParse(
                key?.GetValue("CurrentBuildNumber")?.ToString() ?? "0", 
                out var build) ? build : 0;
            
            var edition = key?.GetValue("EditionID")?.ToString() ?? "Unknown";
            var version = key?.GetValue("CurrentVersion")?.ToString() ?? "Unknown";
            
            return (buildNumber, edition, version);
        }
        catch
        {
            return (0, "Unknown", "Unknown");
        }
    }
    
    public (bool IsCompatible, List<string> Warnings) CheckCompatibility(
        AutounattendConfiguration config,
        int buildNumber,
        string edition)
    {
        var warnings = new List<string>();
        var isWin11 = buildNumber >= 22000;
        
        if (!isWin11 && config.SpecializeSettings.Any(s => s.ComponentName == "RemovePackages"))
        {
            warnings.Add("⚠️ Remoção de pacotes (AppX) funciona melhor no Windows 11");
        }
        
        // Verifica se é edição Home (tem limitações)
        if (edition.Contains("Home", StringComparison.OrdinalIgnoreCase))
        {
            warnings.Add("⚠️ Detectada edição Home - alguns recursos de Diretiva de Grupo podem não disponíveis");
        }
        
        // Verifica compatibilidade por build específico
        if (buildNumber < 22621)
        {
            warnings.Add("⚠️ Windows 11 com build < 22621 detectado - algumas otimizações podem não funcionar");
        }
        
        // Valida risco no contexto
        if (config.OverallRiskLevel >= RiskLevel.High)
        {
            if (edition.Contains("Home", StringComparison.OrdinalIgnoreCase))
            {
                warnings.Add("⚠️ CAUTELA: Configuração de risco ALTO em Windows Home");
            }
        }
        
        var isCompatible = warnings.Count <= 2; // Permite warnings, mas não bloqueios críticos
        
        return (isCompatible, warnings);
    }
}

/// <summary>
/// Valida segurança de comandos e URLs em autounattend
/// </summary>
public class AutounattendSecurityValidator : IAutounattendSecurityValidator
{
    private static readonly HashSet<string> DangerousPatterns = new(StringComparer.OrdinalIgnoreCase)
    {
        "format",
        "diskpart",
        "cipher",
        "cipher /w",
        "file_delete",
        "\\registry",
        "regedit",
        "takeown",
        "icacls /reset",
        "secedit /configure",
        "gpupdate /force /boot"
    };
    
    private static readonly HashSet<string> SafeCommands = new(StringComparer.OrdinalIgnoreCase)
    {
        "powershell",
        "cmd",
        "schtasks",
        "reg",
        "setx",
        "bcdedit",
        "wmic",
        "net"
    };
    
    public bool IsCommandSafe(string commandLine)
    {
        if (string.IsNullOrWhiteSpace(commandLine))
            return true;
        
        var lowerCmd = commandLine.ToLowerInvariant();
        
        // Verifica padrões perigosos
        if (DangerousPatterns.Any(pattern => lowerCmd.Contains(pattern)))
            return false;
        
        // Verifica se começa com comando conhecido
        var firstCmd = lowerCmd.Split(' ', StringSplitOptions.RemoveEmptyEntries).FirstOrDefault() ?? "";
        if (!SafeCommands.Any(safe => firstCmd.Contains(safe)))
            return false;
        
        return true;
    }
    
    public bool IsUrlTrusted(string url)
    {
        if (string.IsNullOrWhiteSpace(url))
            return true;
        
        var lowerUrl = url.ToLowerInvariant();
        
        // Aceita drives locais
        if (lowerUrl.StartsWith("c:\\") || lowerUrl.StartsWith("d:\\") || lowerUrl.StartsWith("\\\\"))
            return true;
        
        // Rejeita URLs suspeitas
        if (lowerUrl.Contains("bit.ly") || lowerUrl.Contains("tinyurl") || lowerUrl.Contains("short.link"))
            return false;
        
        // Aceita dominios conhecidos (microsoft, github, etc)
        var trustedDomains = new[] 
        { 
            "microsoft.com", "github.com", "winget.run", 
            "sourceforge.net", "download.nvidia.com"
        };
        
        return trustedDomains.Any(domain => lowerUrl.Contains(domain));
    }
    
    public List<string> AnalyzeSecurityRisks(AutounattendConfiguration config)
    {
        var risks = new List<string>();
        
        // Analisa comandos FirstLogon
        foreach (var cmd in config.FirstLogonCommands)
        {
            if (!IsCommandSafe(cmd.CommandLine))
                risks.Add($"❌ Comando perigoso em posição {cmd.Order}: {cmd.Description}");
            
            if (cmd.RiskLevel >= RiskLevel.High)
                risks.Add($"⚠️ Comando de risco alto: {cmd.Description}");
        }
        
        // Verifica quantidade de remoções de pacotes (pode quebrar o SO)
        var packageRemoval = config.SpecializeSettings
            .FirstOrDefault(s => s.ComponentName == "RemovePackages");
        
        if (packageRemoval?.Items.Count > 10)
            risks.Add($"⚠️ Remoção agressiva de {packageRemoval.Items.Count} pacotes - pode deixar o SO instável");
        
        // Valida nome do computador (não deve conter caracteres especiais)
        if (!System.Text.RegularExpressions.Regex.IsMatch(config.ComputerName, @"^[a-zA-Z0-9\-]{1,15}$"))
            risks.Add("⚠️ Nome de computador contém caracteres inválidos ou comprimento incorreto");
        
        // Aviso sobre preset agressivo
        if (config.IsAggressive && config.OverallRiskLevel >= RiskLevel.High)
            risks.Add("⚠️ CAUTELA: Preset AGRESSIVO com risco ALTO - revise todas as mudanças antes de aplicar");
        
        return risks;
    }
}
