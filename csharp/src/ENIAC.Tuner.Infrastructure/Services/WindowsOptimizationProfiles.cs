using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Infrastructure.Services;

public static class WindowsOptimizationProfiles
{
    // GUIDs dos planos de energia do Windows
    private const string PowerPlanHighPerformance = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c";
    private const string PowerPlanBalanced = "381b4222-f694-41f0-9685-ff5bb260df2e";
    private const string CloudContentKey = @"HKLM\Software\Policies\Microsoft\Windows\CloudContent";
    private const string UserCloudContentKey = @"HKCU\Software\Policies\Microsoft\Windows\CloudContent";
    private const string DataCollectionKey = @"HKLM\Software\Policies\Microsoft\Windows\DataCollection";
    private const string DeliveryOptimizationKey = @"HKLM\Software\Policies\Microsoft\Windows\DeliveryOptimization";
    private const string OneDriveKey = @"HKLM\Software\Policies\Microsoft\Windows\OneDrive";
    private const string SettingSyncKey = @"HKLM\Software\Policies\Microsoft\Windows\SettingSync";
    private const string WindowsSearchKey = @"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search";

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
                    "Desativar Indexacao de Busca",
                    "sc", "config WSearch start= disabled",
                    "sc", "config WSearch start= auto"),
                new CommandSystemOperation("Flush DNS", "ipconfig", "/flushdns", requiresAdministrator: true)
            ]
        };
    }

    public static OptimizationProfile PolicyMaxProfile()
    {
        return new OptimizationProfile
        {
            Id = "policy-max",
            DisplayName = "Policy-Max",
            Operations =
            [
                RegistryDwordPolicy("Desativar recursos de consumidor", CloudContentKey, "DisableWindowsConsumerFeatures", 1),
                RegistryDwordPolicy("Desativar conteudo otimizado em nuvem", CloudContentKey, "DisableCloudOptimizedContent", 1),
                RegistryDwordPolicy("Desativar conteudo de conta Microsoft", CloudContentKey, "DisableConsumerAccountStateContent", 1),
                RegistryDwordPolicy("Desativar dicas do Windows", CloudContentKey, "DisableSoftLanding", 1),
                RegistryDwordPolicy("Desativar Spotlight na tela inicial", UserCloudContentKey, "DisableWindowsSpotlightFeatures", 1),
                RegistryDwordPolicy("Desativar Spotlight no Centro de Acoes", UserCloudContentKey, "DisableWindowsSpotlightOnActionCenter", 1),
                RegistryDwordPolicy("Desativar Spotlight nas Configuracoes", UserCloudContentKey, "DisableWindowsSpotlightOnSettings", 1),
                RegistryDwordPolicy("Desativar boas-vindas do Windows", UserCloudContentKey, "DisableWindowsSpotlightWindowsWelcomeExperience", 1),
                RegistryDwordPolicy("Desativar colecao Spotlight no desktop", UserCloudContentKey, "DisableSpotlightCollectionOnDesktop", 1),
                RegistryDwordPolicy("Desativar experiencias personalizadas", UserCloudContentKey, "DisableTailoredExperiencesWithDiagnosticData", 1),
                RegistryDwordPolicy("Desativar sugestoes de terceiros", UserCloudContentKey, "DisableThirdPartySuggestions", 1),
                RegistryDwordPolicy("Bloquear telemetria minima", DataCollectionKey, "AllowTelemetry", 0),
                RegistryDwordPolicy("Desativar visualizador de diagnostico", DataCollectionKey, "DisableDiagnosticDataViewer", 1),
                RegistryDwordPolicy("Ocultar pedidos de feedback", DataCollectionKey, "DoNotShowFeedbackNotifications", 1),
                RegistryDwordPolicy("Limitar coleta de logs", DataCollectionKey, "LimitDiagnosticLogCollection", 1),
                RegistryDwordPolicy("Limitar coleta de dumps", DataCollectionKey, "LimitDumpCollection", 1),
                RegistryDwordPolicy("Bloquear downloads OneSettings", DataCollectionKey, "DisableOneSettingsDownloads", 1),
                RegistryDwordPolicy("Bloquear proxy de autenticacao corporativa", DataCollectionKey, "DisableEnterpriseAuthProxy", 1),
                RegistryDwordPolicy("Desativar OneDrive", OneDriveKey, "DisableFileSyncNGSC", 1),
                RegistryDwordPolicy("Bloquear sincronizacao do navegador", SettingSyncKey, "DisableWebBrowserSettingSync", 2),
                RegistryDwordPolicy("Desativar Cortana", WindowsSearchKey, "AllowCortana", 0),
                RegistryDwordPolicy("Delivery Optimization sem peering", DeliveryOptimizationKey, "DODownloadMode", 99),
                new CommandSystemOperation("Atualizar politicas locais", "gpupdate", "/target:computer /force", requiresAdministrator: true)
            ]
        };
    }

    private static RollbackableCommandOperation RegistryDwordPolicy(string name, string keyPath, string valueName, int value)
    {
        return new RollbackableCommandOperation(
            name,
            "reg", $@"add ""{keyPath}"" /v {valueName} /t REG_DWORD /d {value} /f",
            "reg", $@"delete ""{keyPath}"" /v {valueName} /f");
    }
}
