using ENIAC.Tuner.Core.Models;
using ENIAC.Tuner.Core.Services;
using ENIAC.Tuner.Core.Abstractions;
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
			"hardcore" => await RunProfileAsync(WindowsOptimizationProfiles.HardcoreProfile()),
			"extreme" => await RunProfileAsync(WindowsOptimizationProfiles.ExtremeProfile()),
			"policy-max" => await RunProfileAsync(WindowsOptimizationProfiles.PolicyMaxProfile()),
			"autounattend-generate" => await GenerateAutounattendAsync(args),
			"catalog-export" => await ExportCatalogAsync(args),
			"catalog-dryrun" => await RunCatalogDryRunAsync(),
			"catalog-import" => await ImportCatalogSelectionAsync(args),
			"report" => PrintReport(),
			"status" => PrintStatus(),
			_ => PrintHelp(),
		};
	}

	private static async Task<int> ImportCatalogSelectionAsync(string[] args)
	{
		if (args.Length < 2)
		{
			Console.ForegroundColor = ConsoleColor.Yellow;
			Console.WriteLine("Uso: eniac-cli catalog-import [arquivo.json] [--install] [--strict]");
			Console.WriteLine("Sem --install, executa dry-run por segurança.");
			Console.WriteLine("Com --strict, aborta no primeiro erro.");
			Console.ResetColor();
			return 2;
		}

		var inputPath = args[1];
		var install = args.Any(a => a.Equals("--install", StringComparison.OrdinalIgnoreCase));
		var dryRun = !install;
		var strict = args.Any(a => a.Equals("--strict", StringComparison.OrdinalIgnoreCase));

		ISystemAnalyzer analyzer = new WindowsSystemAnalyzerAdapter();
		IAppCatalogManager catalogManager = new AppCatalogManager(new WingetService(), new OperationalSecurityValidator(), analyzer);

		try
		{
			var catalog = await catalogManager.LoadCatalogAsync(inputPath);
			var selected = catalog.GetSelectedApps();

			if (selected.Count == 0)
			{
				Console.ForegroundColor = ConsoleColor.Yellow;
				Console.WriteLine("Nenhum app selecionado no arquivo informado.");
				Console.ResetColor();
				return 0;
			}

			Console.ForegroundColor = dryRun ? ConsoleColor.Cyan : ConsoleColor.Yellow;
			Console.WriteLine(dryRun
				? $"Executando dry-run de {selected.Count} app(s) importado(s)..."
				: $"Executando instalação real de {selected.Count} app(s) importado(s)...");
			Console.ResetColor();

			var result = await catalogManager.InstallBatchAsync(
				selected,
				dryRun: dryRun,
				continueOnError: !strict);

			Console.ForegroundColor = result.FailureCount == 0 ? ConsoleColor.Green : ConsoleColor.Red;
			Console.WriteLine($"Finalizado. Sucessos: {result.SuccessCount} | Falhas: {result.FailureCount}");
			Console.ResetColor();

			return result.FailureCount == 0 ? 0 : 1;
		}
		catch (Exception ex)
		{
			Console.ForegroundColor = ConsoleColor.Red;
			Console.WriteLine($"Falha no catalog-import: {ex.Message}");
			Console.ResetColor();
			return 1;
		}
	}

	private static async Task<int> GenerateAutounattendAsync(string[] args)
	{
		var preset = args.Length > 1 ? args[1].ToLowerInvariant() : "aggressive";
		var outputPath = args.Length > 2 ? args[2] : "autounattend.xml";

		ISystemAnalyzer analyzer = new WindowsSystemAnalyzerAdapter();
		IAutounattendBuilder builder = new AutounattendBuilder(analyzer);

		try
		{
			var config = builder.LoadPreset(preset);
			await builder.SaveToFileAsync(config, outputPath);

			Console.ForegroundColor = ConsoleColor.Green;
			Console.WriteLine($"Autounattend gerado com sucesso: {outputPath}");
			Console.ResetColor();
			return 0;
		}
		catch (Exception ex)
		{
			Console.ForegroundColor = ConsoleColor.Red;
			Console.WriteLine($"Falha ao gerar autounattend: {ex.Message}");
			Console.ResetColor();
			return 1;
		}
	}

	private static async Task<int> ExportCatalogAsync(string[] args)
	{
		var outputPath = args.Length > 1 ? args[1] : "eniac-catalogo-padrao.json";

		ISystemAnalyzer analyzer = new WindowsSystemAnalyzerAdapter();
		IAppCatalogManager catalogManager = new AppCatalogManager(new WingetService(), new OperationalSecurityValidator(), analyzer);

		try
		{
			var catalog = await catalogManager.LoadDefaultCatalogAsync();
			await catalogManager.SaveCatalogAsync(catalog, outputPath);

			Console.ForegroundColor = ConsoleColor.Green;
			Console.WriteLine($"Catalogo exportado com sucesso: {outputPath}");
			Console.WriteLine($"Total de apps: {catalog.TotalCount}");
			Console.ResetColor();
			return 0;
		}
		catch (Exception ex)
		{
			Console.ForegroundColor = ConsoleColor.Red;
			Console.WriteLine($"Falha ao exportar catalogo: {ex.Message}");
			Console.ResetColor();
			return 1;
		}
	}

	private static async Task<int> RunCatalogDryRunAsync()
	{
		ISystemAnalyzer analyzer = new WindowsSystemAnalyzerAdapter();
		IAppCatalogManager catalogManager = new AppCatalogManager(new WingetService(), new OperationalSecurityValidator(), analyzer);

		try
		{
			var catalog = await catalogManager.LoadDefaultCatalogAsync();
			var baseApps = catalog.GetAppsByCategory(AppCategory.Development)
				.Take(3)
				.Concat(catalog.GetAppsByCategory(AppCategory.Browsers).Take(1))
				.ToList();

			var result = await catalogManager.InstallBatchAsync(baseApps, dryRun: true);

			Console.ForegroundColor = ConsoleColor.Cyan;
			Console.WriteLine("Dry-run do catalogo concluido.");
			Console.WriteLine($"Apps planejados: {result.PlannedApps.Count}");
			Console.WriteLine($"Sucessos: {result.SuccessCount} | Falhas: {result.FailureCount}");
			Console.ResetColor();
			return result.FailureCount == 0 ? 0 : 1;
		}
		catch (Exception ex)
		{
			Console.ForegroundColor = ConsoleColor.Red;
			Console.WriteLine($"Falha no dry-run do catalogo: {ex.Message}");
			Console.ResetColor();
			return 1;
		}
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
		Console.WriteLine("  eniac-cli hardcore  Executa perfil hardcore");
		Console.WriteLine("  eniac-cli extreme   Executa perfil extremo");
		Console.WriteLine("  eniac-cli policy-max Executa perfil maximo de politicas");
		Console.WriteLine("  eniac-cli autounattend-generate [preset] [arquivo.xml]");
		Console.WriteLine("  eniac-cli catalog-export [arquivo.json]");
		Console.WriteLine("  eniac-cli catalog-dryrun");
		Console.WriteLine("  eniac-cli catalog-import [arquivo.json] [--install] [--strict]");
		Console.WriteLine("  eniac-cli report    Exibe diagnóstico detalhado");
		Console.WriteLine("  eniac-cli status    Exibe status básico");
		return 0;
	}
}
