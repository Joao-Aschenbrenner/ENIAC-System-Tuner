using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Core.Abstractions;

/// <summary>
/// Interface para construir e validar arquivos autounattend.xml
/// </summary>
public interface IAutounattendBuilder
{
    /// <summary>
    /// Carrega um preset padrão (agressivo, moderado, ou seguro)
    /// </summary>
    AutounattendConfiguration LoadPreset(string presetName);
    
    /// <summary>
    /// Valida a configuração para garantir integridade XML
    /// </summary>
    (bool IsValid, List<string> Errors) Validate(AutounattendConfiguration config);
    
    /// <summary>
    /// Gera o XML bruto do autounattend
    /// </summary>
    string GenerateXml(AutounattendConfiguration config);
    
    /// <summary>
    /// Salva a configuração e XML em arquivo
    /// </summary>
    Task SaveToFileAsync(AutounattendConfiguration config, string filePath);
    
    /// <summary>
    /// Carrega uma configuração salva de um arquivo XML
    /// </summary>
    Task<AutounattendConfiguration> LoadFromFileAsync(string filePath);
}

/// <summary>
/// Interface para validar segurança de scripts e URLs no autounattend
/// </summary>
public interface IAutounattendSecurityValidator
{
    /// <summary>
    /// Verifica se um comando é seguro para executar
    /// </summary>
    bool IsCommandSafe(string commandLine);
    
    /// <summary>
    /// Verifica se uma URL é confiável
    /// </summary>
    bool IsUrlTrusted(string url);
    
    /// <summary>
    /// Analisa riscos de segurança em uma configuração completa
    /// </summary>
    List<string> AnalyzeSecurityRisks(AutounattendConfiguration config);
}

/// <summary>
/// Interface para analisar compatibilidade do Windows
/// </summary>
public interface IWindowsCompatibilityAnalyzer
{
    /// <summary>
    /// Verifica se uma configuração é compatível com a edição instalada
    /// </summary>
    (bool IsCompatible, List<string> Warnings) CheckCompatibility(
        AutounattendConfiguration config,
        int buildNumber,
        string edition);
    
    /// <summary>
    /// Obtém informações sobre a versão atual do Windows
    /// </summary>
    (int BuildNumber, string Edition, string Version) GetWindowsInfo();
}
