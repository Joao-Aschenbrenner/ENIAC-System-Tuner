namespace ENIAC.Tuner.Infrastructure.Services;

public static class CommandSecurityPolicy
{
    private static readonly HashSet<string> AllowedCommands = new(StringComparer.OrdinalIgnoreCase)
    {
        "ipconfig",
        "arp",
        "gpupdate",
        "netsh",
        "powercfg",
        "sc"
    };

    private static readonly string[] ForbiddenPatterns =
    [
        "&&",
        "||",
        "|",
        ";",
        "`",
        ">",
        "<"
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
