namespace ENIAC.Tuner.Core.Abstractions;

public interface ISystemAnalyzer
{
    string BuildSummary();

    Task<string> BuildDetailedReportAsync(CancellationToken cancellationToken);
}
