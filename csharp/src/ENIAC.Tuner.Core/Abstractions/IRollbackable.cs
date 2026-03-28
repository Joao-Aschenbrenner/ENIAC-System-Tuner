using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Core.Abstractions;

/// <summary>
/// Operação que suporta reversão das mudanças realizadas.
/// </summary>
public interface IRollbackable
{
    Task<OperationResult> RollbackAsync(CancellationToken cancellationToken);
}
