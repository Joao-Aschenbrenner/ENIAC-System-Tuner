using System.Threading;
using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Core.Services;

public interface IOptimizationRunner
{
    IAsyncEnumerable<OperationResult> RunAsync(OptimizationProfile profile, CancellationToken cancellationToken = default);
}
