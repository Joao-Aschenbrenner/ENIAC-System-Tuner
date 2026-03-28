using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Infrastructure.Services;

/// <summary>
/// Operação de comando que armazena o comando de reversão correspondente.
/// </summary>
public sealed class RollbackableCommandOperation : ISystemOperation, IRollbackable
{
    private readonly CommandSystemOperation _executeOp;
    private readonly CommandSystemOperation _rollbackOp;

    public RollbackableCommandOperation(
        string name,
        string fileName, string arguments,
        string rollbackFileName, string rollbackArguments,
        bool requiresAdministrator = true)
    {
        Name = name;
        RequiresAdministrator = requiresAdministrator;
        _executeOp = new CommandSystemOperation(name, fileName, arguments, requiresAdministrator);
        _rollbackOp = new CommandSystemOperation($"{name} [rollback]", rollbackFileName, rollbackArguments, requiresAdministrator);
    }

    public string Name { get; }

    public bool RequiresAdministrator { get; }

    public Task<OperationResult> ExecuteAsync(CancellationToken cancellationToken)
        => _executeOp.ExecuteAsync(cancellationToken);

    public Task<OperationResult> RollbackAsync(CancellationToken cancellationToken)
        => _rollbackOp.ExecuteAsync(cancellationToken);
}
