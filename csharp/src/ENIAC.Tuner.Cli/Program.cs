using ENIAC.Tuner.Core.Models;
using ENIAC.Tuner.Core.Services;
using ENIAC.Tuner.Infrastructure.Services;

namespace ENIAC.Tuner.Cli;

internal static class Program
{
	private static readonly IOptimizationRunner Runner = new OptimizationRunner();

	private static async Task<int> Main(string[] args)
	{
		var command = args.FirstOrDefault()?.ToLowerInvariant() ?? "help";

		return command switch
		{
			"safe" => await RunProfileAsync(WindowsOptimizationProfiles.SafeProfile()),
			"network" => await RunProfileAsync(WindowsOptimizationProfiles.NetworkProfile()),
			"report" => PrintReport(),
			"status" => PrintStatus(),
			_ => PrintHelp(),
		};
	}

	private static async Task<int> RunProfileAsync(OptimizationProfile profile)
	{
		var isAdmin = WindowsSecurity.IsAdministrator();
		if (profile.Operations.Any(x => x.RequiresAdministrator) && !isAdmin)
		{
			Console.ForegroundColor = ConsoleColor.Yellow;
			Console.WriteLine("Este perfil exige privilégios de administrador.");
			Console.WriteLine("Reabra o terminal como Administrador.");
			Console.ResetColor();
			return 2;
		}

		Console.WriteLine($"Iniciando perfil: {profile.DisplayName}");
		var ok = 0;
		var fail = 0;

		await foreach (var result in Runner.RunAsync(profile))
		{
			if (result.Success)
			{
				Console.ForegroundColor = ConsoleColor.Green;
				ok++;
			}
			else
			{
				Console.ForegroundColor = ConsoleColor.Red;
				fail++;
			}

			Console.WriteLine(result.Message);
			Console.ResetColor();
		}

		Console.WriteLine();
		Console.WriteLine($"Resumo: sucesso={ok} falhas={fail}");
		return fail == 0 ? 0 : 1;
	}

	private static int PrintReport()
	{
		Console.WriteLine(WindowsSystemAnalyzer.BuildDetailedReport());
		return 0;
	}

	private static int PrintStatus()
	{
		Console.WriteLine("ENIAC Tuner CLI");
		Console.WriteLine($"Admin: {(WindowsSecurity.IsAdministrator() ? "sim" : "nao")}");
		Console.WriteLine($"Sistema: {Environment.OSVersion}");
		return 0;
	}

	private static int PrintHelp()
	{
		Console.WriteLine("ENIAC Tuner CLI (C#)");
		Console.WriteLine();
		Console.WriteLine("Uso:");
		Console.WriteLine("  eniac-cli safe      Executa perfil seguro de otimização");
		Console.WriteLine("  eniac-cli network   Executa perfil de rede");
		Console.WriteLine("  eniac-cli report    Exibe diagnóstico detalhado");
		Console.WriteLine("  eniac-cli status    Exibe status básico");
		return 0;
	}
}
