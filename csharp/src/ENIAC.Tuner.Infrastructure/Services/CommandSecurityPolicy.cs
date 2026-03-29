namespace ENIAC.Tuner.Infrastructure.Services;

public static class CommandSecurityPolicy
{
    private static readonly HashSet<string> AllowedCommands = new(StringComparer.OrdinalIgnoreCase)
    {
        // Network diagnostics
        "ipconfig",
        "arp",
        "gpupdate",
        "netsh",
        
        // System configuration
        "powercfg",
        "sc",
        "reg",
        "setx",
        "bcdedit",
        "schtasks",
        "taskkill",
        "wevtutil",
        
        // PowerShell (used in FirstLogon commands)
        "powershell.exe",
        "powershell",
        "cmd.exe",
        "cmd",
        
        // WMI and management
        "wmic",
        
        // Package and feature removal (Windows 11 specific)
        "dism.exe",
        "dism",
        
        // System properties
        "wuauclt.exe",
        "wuauclt",
        "gpresult",
        "systeminfo"
    };

    private static readonly string[] ForbiddenPatterns =
    [
        "&&",
        "||",
        "|",
        ";",
        "`",
        ">",
        "<",
        "$(",  // PowerShell command substitution
        "&"    // Background job operator
    ];

    public static CommandSecurityValidationResult Validate(string fileName, string arguments)
    {
        if (!AllowedCommands.Contains(fileName))
        {
            return new CommandSecurityValidationResult(false, "Comando nao permitido pela politica de seguranca.");
        }

        if (ForbiddenPatterns.Any(arguments.Contains))
        {
            return new CommandSecurityValidationResult(false, "Padrao perigoso detectado nos argumentos.");
        }

        return new CommandSecurityValidationResult(true, string.Empty);
    }
}

public readonly record struct CommandSecurityValidationResult(bool IsAllowed, string Reason);
