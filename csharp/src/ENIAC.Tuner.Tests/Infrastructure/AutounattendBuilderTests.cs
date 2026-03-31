using System.Xml.Linq;
using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Infrastructure.Services;

namespace ENIAC.Tuner.Tests.Infrastructure;

public sealed class AutounattendBuilderTests
{
    public void GenerateXml_ShouldUseUnattendNamespaceAndWcmAction()
    {
        var builder = new AutounattendBuilder(new FakeSystemAnalyzer());
        var config = builder.LoadPreset("aggressive");

        var xml = builder.GenerateXml(config);
        var doc = XDocument.Parse(xml);

        TestAssert.Equal("unattend", doc.Root?.Name.LocalName, "Raiz do XML deve ser unattend.");
        TestAssert.Equal("urn:schemas-microsoft-com:unattend", doc.Root?.Name.NamespaceName, "Namespace padrão do unattend deve estar presente.");
        TestAssert.Contains("wcm:action", xml, "Comandos devem conter atributo wcm:action.");
        TestAssert.True(!xml.Contains("name=\"RemovePackages\"", StringComparison.Ordinal), "Não deve gerar componente custom RemovePackages.");
        TestAssert.True(!xml.Contains("name=\"RemoveFeatures\"", StringComparison.Ordinal), "Não deve gerar componente custom RemoveFeatures.");
        TestAssert.Contains("<OOBE>", xml, "Configuração OOBE deve existir no componente Shell-Setup.");
        TestAssert.Contains("<NetworkLocation>", xml, "NetworkLocation deve ficar dentro de OOBE.");
    }

    public async Task SaveToFileAsync_ShouldPersistValidXml()
    {
        var builder = new AutounattendBuilder(new FakeSystemAnalyzer());
        var config = builder.LoadPreset("moderate");
        var filePath = Path.Combine(Path.GetTempPath(), $"autounattend-test-{Guid.NewGuid():N}.xml");

        try
        {
            await builder.SaveToFileAsync(config, filePath);
            TestAssert.True(File.Exists(filePath), "Arquivo XML deve ser salvo.");

            var xml = await File.ReadAllTextAsync(filePath);
            var doc = XDocument.Parse(xml);
            TestAssert.Equal("unattend", doc.Root?.Name.LocalName, "Arquivo salvo deve ter raiz unattend.");
        }
        finally
        {
            if (File.Exists(filePath))
            {
                File.Delete(filePath);
            }
        }
    }

    private sealed class FakeSystemAnalyzer : ISystemAnalyzer
    {
        public string BuildSummary() => "ok";

        public Task<string> BuildDetailedReportAsync(CancellationToken cancellationToken)
            => Task.FromResult("ok");
    }
}
