using System.Threading;
using System.Threading.Tasks;
using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Core.Abstractions;

public interface ISystemOperation
{
    string Name { get; }

    bool RequiresAdministrator { get; }

    Task<OperationResult> ExecuteAsync(CancellationToken cancellationToken);
}
