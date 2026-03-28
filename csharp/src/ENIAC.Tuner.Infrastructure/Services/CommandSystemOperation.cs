using System.Diagnostics;
using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Core.Models;

namespace ENIAC.Tuner.Infrastructure.Services;

public sealed class CommandSystemOperation : ISystemOperation
{
    public CommandSystemOperation(string name, string fileName, string arguments, bool requiresAdministrator = true)
    {
        Name = name;
        FileName = fileName;
        Arguments = arguments;
        RequiresAdministrator = requiresAdministrator;
    }

    public string Name { get; }

    public bool RequiresAdministrator { get; }

    private string FileName { get; }

    private string Arguments { get; }

    public async Task<OperationResult> ExecuteAsync(CancellationToken cancellationToken)
    {
        try
        {
            var validation = CommandSecurityPolicy.Validate(FileName, Arguments);
            if (!validation.IsAllowed)
            {
                return new OperationResult(false, $"{Name}: bloqueado por seguranca - {validation.Reason}");
            }

            var startInfo = new ProcessStartInfo
            {
                FileName = FileName,
                Arguments = Arguments,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = startInfo };
            process.Start();

            var outputTask = process.StandardOutput.ReadToEndAsync(cancellationToken);
            var errorTask = process.StandardError.ReadToEndAsync(cancellationToken);

            await process.WaitForExitAsync(cancellationToken).ConfigureAwait(false);

            var output = await outputTask.ConfigureAwait(false);
            var error = await errorTask.ConfigureAwait(false);

            // Aceitar exit code 0 ou 1062 para comandos sc (serviço não iniciado é considerado ok)
            if (process.ExitCode == 0 || (FileName == "sc" && process.ExitCode == 1062))
            {
                return new OperationResult(true, $"{Name}: OK");
            }

            var details = string.IsNullOrWhiteSpace(error) ? output : error;
            return new OperationResult(false, $"{Name}: falhou (exit {process.ExitCode}) - {details.Trim()}");
        }
        catch (Exception ex)
        {
            return new OperationResult(false, $"{Name}: exceção - {ex.Message}");
        }
    }
}
