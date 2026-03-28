using System.Runtime.CompilerServices;
using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Core.Services;

public sealed class OptimizationRunner : IOptimizationRunner
{
    public async IAsyncEnumerable<OperationResult> RunAsync(
        OptimizationProfile profile,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        foreach (var operation in profile.Operations)
        {
            cancellationToken.ThrowIfCancellationRequested();
            yield return await operation.ExecuteAsync(cancellationToken).ConfigureAwait(false);
        }
    }
}
