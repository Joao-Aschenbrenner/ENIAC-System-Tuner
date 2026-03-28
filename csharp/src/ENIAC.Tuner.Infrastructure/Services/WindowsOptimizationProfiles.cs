using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Infrastructure.Services;

public static class WindowsOptimizationProfiles
{
    // GUIDs dos planos de energia do Windows
    private const string PowerPlanHighPerformance = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c";
    private const string PowerPlanBalanced = "381b4222-f694-41f0-9685-ff5bb260df2e";

    public static OptimizationProfile SafeProfile()
    {
        return new OptimizationProfile
        {
            Id = "safe",
            DisplayName = "Perfil Seguro",
            Operations =
            [
                new CommandSystemOperation("Flush DNS", "ipconfig", "/flushdns", requiresAdministrator: true),
                new CommandSystemOperation("Limpar lista ARP", "arp", "-d *", requiresAdministrator: true),
                new CommandSystemOperation("Atualizar políticas locais", "gpupdate", "/target:computer /force", requiresAdministrator: true)
            ]
        };
    }

    public static OptimizationProfile NetworkProfile()
    {
        return new OptimizationProfile
        {
            Id = "network",
            DisplayName = "Perfil Rede",
            Operations =
            [
                new CommandSystemOperation("TCP autotuning normal", "netsh", "int tcp set global autotuninglevel=normal", requiresAdministrator: true),
                new CommandSystemOperation("RSS enabled", "netsh", "int tcp set global rss=enabled", requiresAdministrator: true),
                new CommandSystemOperation("Flush DNS", "ipconfig", "/flushdns", requiresAdministrator: true)
            ]
        };
    }

    public static OptimizationProfile HardcoreProfile()
    {
        return new OptimizationProfile
        {
            Id = "hardcore",
            DisplayName = "Perfil Hardcore",
            Operations =
            [
                new RollbackableCommandOperation(
                    "TCP Autotuning Restrito",
                    "netsh", "int tcp set global autotuninglevel=highlyrestricted",
                    "netsh", "int tcp set global autotuninglevel=normal"),
                new RollbackableCommandOperation(
                    "TCP Timestamps Desativado",
                    "netsh", "int tcp set global timestamps=disabled",
                    "netsh", "int tcp set global timestamps=enabled"),
                new RollbackableCommandOperation(
                    "TCP ECN Ativado",
                    "netsh", "int tcp set global ecncapability=enabled",
                    "netsh", "int tcp set global ecncapability=disabled"),
                new RollbackableCommandOperation(
                    "Plano Alto Desempenho",
                    "powercfg", $"/setactive {PowerPlanHighPerformance}",
                    "powercfg", $"/setactive {PowerPlanBalanced}"),
                new CommandSystemOperation("Flush DNS", "ipconfig", "/flushdns", requiresAdministrator: true)
            ]
        };
    }

    public static OptimizationProfile ExtremeProfile()
    {
        return new OptimizationProfile
        {
            Id = "extreme",
            DisplayName = "Perfil Extremo",
            Operations =
            [
                new RollbackableCommandOperation(
                    "TCP Autotuning Desativado",
                    "netsh", "int tcp set global autotuninglevel=disabled",
                    "netsh", "int tcp set global autotuninglevel=normal"),
                new RollbackableCommandOperation(
                    "TCP Timestamps Desativado",
                    "netsh", "int tcp set global timestamps=disabled",
                    "netsh", "int tcp set global timestamps=enabled"),
                new RollbackableCommandOperation(
                    "TCP ECN Ativado",
                    "netsh", "int tcp set global ecncapability=enabled",
                    "netsh", "int tcp set global ecncapability=disabled"),
                new RollbackableCommandOperation(
                    "Plano Alto Desempenho",
                    "powercfg", $"/setactive {PowerPlanHighPerformance}",
                    "powercfg", $"/setactive {PowerPlanBalanced}"),
                new RollbackableCommandOperation(
                    "Desativar SysMain",
                    "sc", "config SysMain start= disabled",
                    "sc", "config SysMain start= auto"),
                new RollbackableCommandOperation(
                    "Desativar Indexacao de Busca",
                    "sc", "config WSearch start= disabled",
                    "sc", "config WSearch start= auto"),
                new CommandSystemOperation("Flush DNS", "ipconfig", "/flushdns", requiresAdministrator: true)
            ]
        };
    }
}
