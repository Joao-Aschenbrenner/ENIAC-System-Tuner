using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using System.Text;
using System.Xml.Linq;

namespace ENIAC.Tuner.Infrastructure.Services;

/// <summary>
/// Implementação do construtor de autounattend.xml com suporte a presets
/// </summary>
public class AutounattendBuilder : IAutounattendBuilder
{
    private readonly ISystemAnalyzer _systemAnalyzer;
    
    public AutounattendBuilder(ISystemAnalyzer systemAnalyzer)
    {
        _systemAnalyzer = systemAnalyzer;
    }
    
    public AutounattendConfiguration LoadPreset(string presetName)
    {
        return presetName.ToLowerInvariant() switch
        {
            "aggressive" => BuildAggressivePreset(),
            "moderate" => BuildModeratePreset(),
            "safe" => BuildSafePreset(),
            _ => BuildModeratePreset()
        };
    }
    
    public (bool IsValid, List<string> Errors) Validate(AutounattendConfiguration config)
    {
        var errors = new List<string>();
        
        if (string.IsNullOrWhiteSpace(config.ComputerName))
            errors.Add("Nome do computador não pode estar vazio");
        
        if (config.ComputerName.Length > 15)
            errors.Add("Nome do computador não pode exceder 15 caracteres");
        
        if (config.FirstLogonCommands.Count > 0)
        {
            var invalidCommands = config.FirstLogonCommands
                .Where(cmd => string.IsNullOrWhiteSpace(cmd.CommandLine))
                .ToList();
            
            if (invalidCommands.Any())
                errors.Add($"{invalidCommands.Count} comandos FirstLogon estão vazios");
        }
        
        return (errors.Count == 0, errors);
    }
    
    public string GenerateXml(AutounattendConfiguration config)
    {
        var doc = new XDocument(
            new XDeclaration("1.0", "utf-8", "yes"),
            new XElement("unattend",
                BuildWindowsPESettings(config),
                BuildSpecializeSettings(config),
                BuildOobeSystemSettings(config)
            )
        );
        
        return doc.ToString(SaveOptions.None);
    }
    
    public async Task SaveToFileAsync(AutounattendConfiguration config, string filePath)
    {
        var validation = Validate(config);
        if (!validation.IsValid)
            throw new InvalidOperationException($"Configuração inválida: {string.Join("; ", validation.Errors)}");
        
        var xml = GenerateXml(config);
        await File.WriteAllTextAsync(filePath, xml, Encoding.UTF8);
    }
    
    public async Task<AutounattendConfiguration> LoadFromFileAsync(string filePath)
    {
        if (!File.Exists(filePath))
            throw new FileNotFoundException($"Arquivo não encontrado: {filePath}");
        
        var xmlContent = await File.ReadAllTextAsync(filePath, Encoding.UTF8);
        var doc = XDocument.Parse(xmlContent);
        
        // Parse básico - em produção seria muito mais robusto
        var config = new AutounattendConfiguration
        {
            PresetName = "Imported",
            IsAggressive = false,
            Verification = new ProductionVerification
            {
                AppliedAt = DateTime.Now,
                Environment = "Windows 11"
            }
        };
        
        return config;
    }
    
    #region Private Methods
    
    private AutounattendConfiguration BuildAggressivePreset()
    {
        return new AutounattendConfiguration
        {
            PresetName = "Aggressive",
            IsAggressive = true,
            OverallRiskLevel = RiskLevel.High,
            ComputerName = "ENIAC-PC",
            UILanguage = "pt-BR",
            SystemLocale = "pt-BR",
            UserLocale = "pt-BR",
            KeyboardLayout = "Portuguese (Brazilian)",
            
            WindowsPESettings =
            [
                new AutounattendComponentConfig
                {
                    ComponentName = "Microsoft-Windows-Setup",
                    Description = "Configurações principais de setup",
                    RiskLevel = RiskLevel.Safe
                }
            ],
            
            SpecializeSettings =
            [
                new AutounattendComponentConfig
                {
                    ComponentName = "RemovePackages",
                    Description = "Remove pacotes e recursos desnecessários",
                    RiskLevel = RiskLevel.High,
                    Items = new()
                    {
                        "Microsoft.BingSearch",
                        "Microsoft.GamingApp",
                        "Microsoft.MixedReality.Portal",
                        "Microsoft.OneDrive",
                        "Clipchamp.Clipchamp",
                        "MicrosoftCorporationII.QuickAssist",
                        "Microsoft.ZuneMusic",
                        "Microsoft.ZuneVideo"
                    }
                },
                new AutounattendComponentConfig
                {
                    ComponentName = "RemoveFeatures",
                    Description = "Desabilita recursos não essenciais",
                    RiskLevel = RiskLevel.Moderate,
                    Items = new()
                    {
                        "MediaPlayer",
                        "ActiveDirectory-LDAP",
                        "IIS-WebServer",
                        "Internet-Explorer-Optional-amd64"
                    }
                }
            ],
            
            OobeSystemSettings =
            [
                new AutounattendComponentConfig
                {
                    ComponentName = "NetworkLocation",
                    Description = "Configura localização da rede",
                    Settings = new() { { "Type", "Work" } },
                    RiskLevel = RiskLevel.Safe
                }
            ],
            
            FirstLogonCommands =
            [
                new AutounattendCommand
                {
                    Order = 1,
                    Description = "Desabilita telemetria de diagnósticos",
                    CommandLine = "powershell.exe -Command \"Set-Service DiagTrack -StartupType Disabled\"",
                    RiskLevel = RiskLevel.Moderate
                },
                new AutounattendCommand
                {
                    Order = 2,
                    Description = "Desabilita serviço de experiência conectada",
                    CommandLine = "powershell.exe -Command \"Set-Service dmwappushservice -StartupType Disabled\"",
                    RiskLevel = RiskLevel.Moderate
                },
                new AutounattendCommand
                {
                    Order = 3,
                    Description = "Limpa tarefas agendadas desnecessárias",
                    CommandLine = "powershell.exe -Command \"Get-ScheduledTask -TaskPath \\\\Microsoft\\\\Windows\\\\Application\\ Experience\\\\* | Disable-ScheduledTask -Confirm:$false\"",
                    RiskLevel = RiskLevel.High
                }
            ],
            
            Verification = new ProductionVerification
            {
                AppliedAt = DateTime.Now,
                Environment = "Windows 11",
                RiskLevel = RiskLevel.High,
                IsProduction = false
            }
        };
    }
    
    private AutounattendConfiguration BuildModeratePreset()
    {
        var preset = BuildAggressivePreset();
        preset.PresetName = "Moderate";
        preset.IsAggressive = false;
        preset.OverallRiskLevel = RiskLevel.Moderate;
        
        // Remove comandos de risco muito alto
        preset.FirstLogonCommands = preset.FirstLogonCommands
            .Where(cmd => cmd.RiskLevel < RiskLevel.High)
            .ToList();
        
        return preset;
    }
    
    private AutounattendConfiguration BuildSafePreset()
    {
        return new AutounattendConfiguration
        {
            PresetName = "Safe",
            IsAggressive = false,
            OverallRiskLevel = RiskLevel.Safe,
            ComputerName = "ENIAC-PC",
            UILanguage = "pt-BR",
            SystemLocale = "pt-BR",
            UserLocale = "pt-BR",
            KeyboardLayout = "Portuguese (Brazilian)",
            
            Verification = new ProductionVerification
            {
                AppliedAt = DateTime.Now,
                Environment = "Windows 11",
                RiskLevel = RiskLevel.Safe,
                IsProduction = true
            }
        };
    }
    
    private XElement BuildWindowsPESettings(AutounattendConfiguration config)
    {
        return new XElement("settings",
            new XAttribute("pass", "windowsPE"),
            new XElement("component",
                new XAttribute("name", "Microsoft-Windows-Setup"),
                new XAttribute("publicKeyToken", "31bf3856ad364e35"),
                new XAttribute("language", config.UILanguage),
                new XAttribute("versionScope", "nonSxS")
            )
        );
    }
    
    private XElement BuildSpecializeSettings(AutounattendConfiguration config)
    {
        var components = new List<XElement>
        {
            new XElement("component",
                new XAttribute("name", "Microsoft-Windows-Shell-Setup"),
                new XAttribute("publicKeyToken", "31bf3856ad364e35"),
                new XAttribute("language", config.UILanguage),
                new XAttribute("versionScope", "nonSxS"),
                new XElement("ComputerName", config.ComputerName)
            )
        };
        
        // Adiciona configurações de remoção de pacotes se existirem
        foreach (var setting in config.SpecializeSettings)
        {
            if (setting.Items.Any())
            {
                var itemElements = setting.Items
                    .Select((item, idx) => new XElement(setting.ComponentName == "RemovePackages" ? "Package" : "Feature",
                        new XAttribute("name", item)
                    ))
                    .Cast<object>()
                    .ToList();
                
                components.Add(new XElement("component",
                    itemElements.ToArray()
                ));
            }
        }
        
        return new XElement("settings",
            new XAttribute("pass", "specialize"),
            components.ToArray()
        );
    }
    
    private XElement BuildOobeSystemSettings(AutounattendConfiguration config)
    {
        XNamespace wcm = "http://schemas.microsoft.com/WMIConfig/2002/State";
        var elements = new List<XElement>();
        
        // Componentes OOBE
        foreach (var setting in config.OobeSystemSettings)
        {
            elements.Add(new XElement("component",
                new XAttribute("name", setting.ComponentName),
                new XAttribute("publicKeyToken", "31bf3856ad364e35"),
                new XAttribute("language", config.UILanguage),
                new XAttribute("versionScope", "nonSxS"),
                setting.Settings.Select(kvp => new XElement(kvp.Key, kvp.Value)).ToArray()
            ));
        }
        
        // FirstLogonCommands se houver
        if (config.FirstLogonCommands.Any())
        {
            var commands = config.FirstLogonCommands
                .OrderBy(cmd => cmd.Order)
                .Select(cmd => new XElement("SynchronousCommand",
                    new XAttribute(XNamespace.Xmlns + "wcm", wcm),
                    new XAttribute(wcm + "action", "add"),
                    new XElement("Order", cmd.Order.ToString()),
                    new XElement("Description", cmd.Description),
                    new XElement("CommandLine", cmd.CommandLine)
                ))
                .Cast<object>()
                .ToList();
            
            elements.Add(new XElement("component",
                new XAttribute("name", "Microsoft-Windows-Shell-Setup"),
                new XAttribute("publicKeyToken", "31bf3856ad364e35"),
                new XAttribute("language", config.UILanguage),
                new XAttribute("versionScope", "nonSxS"),
                new XElement("FirstLogonCommands",
                    commands.ToArray()
                )
            ));
        }
        
        return new XElement("settings",
            new XAttribute("pass", "oobeSystem"),
            elements.ToArray()
        );
    }
    
    #endregion
}
