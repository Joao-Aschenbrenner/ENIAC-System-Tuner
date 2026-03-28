using ENIAC.Tuner.Core.Abstractions;

namespace ENIAC.Tuner.Core.Models;

public sealed class OptimizationProfile
{
    public required string Id { get; init; }

    public required string DisplayName { get; init; }

    public required IReadOnlyList<ISystemOperation> Operations { get; init; }
}
