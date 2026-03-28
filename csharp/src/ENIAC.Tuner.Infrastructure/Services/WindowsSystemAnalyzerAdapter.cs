using ENIAC.Tuner.Core.Abstractions;

namespace ENIAC.Tuner.Infrastructure.Services;

public sealed class WindowsSystemAnalyzerAdapter : ISystemAnalyzer
{
    public string BuildSummary() => WindowsSystemAnalyzer.BuildSummary();

    public Task<string> BuildDetailedReportAsync(CancellationToken cancellationToken)
    {
        return Task.Run(WindowsSystemAnalyzer.BuildDetailedReport, cancellationToken);
    }
}
