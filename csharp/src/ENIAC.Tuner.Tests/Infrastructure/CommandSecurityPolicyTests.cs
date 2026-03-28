using ENIAC.Tuner.Infrastructure.Services;

namespace ENIAC.Tuner.Tests.Infrastructure;

public sealed class CommandSecurityPolicyTests
{
    public void Validate_ShouldAllowWhitelistedCommands()
    {
        var allowed = new[] { "ipconfig", "netsh", "gpupdate", "arp" };
        foreach (var fileName in allowed)
        {
            var result = CommandSecurityPolicy.Validate(fileName, "test");
            TestAssert.True(result.IsAllowed, $"Comando {fileName} deveria ser permitido");
        }
    }

    public void Validate_ShouldRejectNonWhitelistedCommand()
    {
        var result = CommandSecurityPolicy.Validate("cmd", "/c whoami");
        TestAssert.False(result.IsAllowed, "Comando fora da whitelist deveria ser bloqueado");
        TestAssert.Contains("nao permitido", result.Reason.ToLowerInvariant(), "Motivo deve indicar bloqueio");
    }

    public void Validate_ShouldRejectCommandInjectionPatterns()
    {
        var dangerousArgs = new[] { "/flushdns; calc", "/flushdns && whoami", "/flushdns | whoami" };
        foreach (var args in dangerousArgs)
        {
            var result = CommandSecurityPolicy.Validate("ipconfig", args);
            TestAssert.False(result.IsAllowed, $"Argumento perigoso deveria ser bloqueado: {args}");
        }
    }

    public void Validate_ShouldAllowExtendedCommands()
    {
        var extended = new[] { "powercfg", "sc" };
        foreach (var fileName in extended)
        {
            var result = CommandSecurityPolicy.Validate(fileName, "test");
            TestAssert.True(result.IsAllowed, $"Comando {fileName} deveria ser permitido na allowlist expandida");
        }
    }
}
