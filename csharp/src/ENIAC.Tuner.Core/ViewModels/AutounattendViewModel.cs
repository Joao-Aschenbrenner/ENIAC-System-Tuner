using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace ENIAC.Tuner.Core.ViewModels;

/// <summary>
/// ViewModel para geração e gerenciamento de autounattend.xml
/// </summary>
public class AutounattendViewModel : INotifyPropertyChanged
{
    private readonly IAutounattendBuilder _builder;
    private readonly IAutounattendSecurityValidator _securityValidator;
    private readonly IWindowsCompatibilityAnalyzer _compatibilityAnalyzer;
    
    private string _presetName = "Aggressive";
    private string _previewXml = "";
    private string _riskWarnings = "";
    private string _generatedFilePath = "";
    private bool _isGenerating = false;
    private AutounattendConfiguration _currentConfig;
    private string _computerName = "ENIAC-PC";
    
    public AutounattendViewModel(
        IAutounattendBuilder builder,
        IAutounattendSecurityValidator securityValidator,
        IWindowsCompatibilityAnalyzer compatibilityAnalyzer)
    {
        _builder = builder;
        _securityValidator = securityValidator;
        _compatibilityAnalyzer = compatibilityAnalyzer;
        _currentConfig = _builder.LoadPreset(_presetName);
    }
    
    public string PresetName
    {
        get => _presetName;
        set
        {
            if (_presetName != value)
            {
                _presetName = value;
                LoadPreset(value);
                OnPropertyChanged();
            }
        }
    }
    
    public string ComputerName
    {
        get => _computerName;
        set
        {
            if (_computerName != value)
            {
                _computerName = value;
                if (_currentConfig != null)
                    _currentConfig.ComputerName = value;
                OnPropertyChanged();
            }
        }
    }
    
    public string PreviewXml
    {
        get => _previewXml;
        private set
        {
            if (_previewXml != value)
            {
                _previewXml = value;
                OnPropertyChanged();
            }
        }
    }
    
    public string RiskWarnings
    {
        get => _riskWarnings;
        private set
        {
            if (_riskWarnings != value)
            {
                _riskWarnings = value;
                OnPropertyChanged();
            }
        }
    }
    
    public string GeneratedFilePath
    {
        get => _generatedFilePath;
        private set
        {
            if (_generatedFilePath != value)
            {
                _generatedFilePath = value;
                OnPropertyChanged();
            }
        }
    }
    
    public bool IsGenerating
    {
        get => _isGenerating;
        private set
        {
            if (_isGenerating != value)
            {
                _isGenerating = value;
                OnPropertyChanged();
            }
        }
    }
    
    /// <summary>
    /// Carrega o preset selecionado
    /// </summary>
    public void LoadPreset(string presetName)
    {
        try
        {
            _currentConfig = _builder.LoadPreset(presetName);
            _computerName = _currentConfig.ComputerName;
            
            GeneratePreview();
            ValidateAndShowWarnings();
        }
        catch (Exception ex)
        {
            RiskWarnings = $"❌ Erro ao carregar preset: {ex.Message}";
        }
    }
    
    /// <summary>
    /// Gera preview do XML baseado na configuração atual
    /// </summary>
    public void GeneratePreview()
    {
        if (_currentConfig == null)
            return;
        
        try
        {
            var xml = _builder.GenerateXml(_currentConfig);
            PreviewXml = xml;
        }
        catch (Exception ex)
        {
            PreviewXml = $"Erro ao gerar XML: {ex.Message}";
        }
    }
    
    /// <summary>
    /// Valida a configuração e mostra warnings
    /// </summary>
    public void ValidateAndShowWarnings()
    {
        if (_currentConfig == null)
            return;
        
        var warnings = new List<string>();
        
        // Validação de configuração
        var (isValid, errors) = _builder.Validate(_currentConfig);
        if (!isValid)
        {
            warnings.AddRange(errors.Select(e => $"❌ {e}"));
        }
        
        // Análise de segurança
        var securityRisks = _securityValidator.AnalyzeSecurityRisks(_currentConfig);
        warnings.AddRange(securityRisks);
        
        // Compatibilidade com Windows
        var (buildNumber, edition, _) = _compatibilityAnalyzer.GetWindowsInfo();
        var (isCompatible, compatWarnings) = _compatibilityAnalyzer.CheckCompatibility(
            _currentConfig, buildNumber, edition);
        
        if (!isCompatible)
            warnings.Insert(0, "⚠️ Compatibilidade reduzida com sua versão do Windows");
        
        warnings.AddRange(compatWarnings);
        
        RiskWarnings = warnings.Any() 
            ? string.Join("\n", warnings)
            : "✅ Configuração validada com sucesso!";
    }
    
    /// <summary>
    /// Salva o autounattend em arquivo
    /// </summary>
    public async Task SaveToFileAsync(string filePath)
    {
        try
        {
            IsGenerating = true;
            await _builder.SaveToFileAsync(_currentConfig, filePath);
            GeneratedFilePath = filePath;
        }
        catch (Exception ex)
        {
            RiskWarnings = $"❌ Erro ao salvar arquivo: {ex.Message}";
        }
        finally
        {
            IsGenerating = false;
        }
    }
    
    /// <summary>
    /// Alterna entre presets agressivos e moderados
    /// </summary>
    public void ToggleRiskLevel()
    {
        var newPreset = _currentConfig.IsAggressive ? "Moderate" : "Aggressive";
        LoadPreset(newPreset);
        OnPropertyChanged(nameof(PresetName));
    }
    
    public event PropertyChangedEventHandler? PropertyChanged;
    
    protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
