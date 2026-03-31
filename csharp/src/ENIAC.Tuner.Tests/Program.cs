using ENIAC.Tuner.Tests.Core;
using ENIAC.Tuner.Tests.Infrastructure;

var suites = new List<(string Name, Func<Task> Run)>
{
    ("MainDashboardViewModelTests", async () =>
    {
        var t = new MainDashboardViewModelTests();
        t.Constructor_ShouldSetAdminText_WhenAdministrator();
        t.Constructor_ShouldSetAdminText_WhenNotAdministrator();
        t.AnalyzeSystem_ShouldUpdateSummaryAndStatus();
        await t.ExecuteProfileAsync_WhenNotAdmin_ShouldBlockExecution();
        await t.ExecuteProfileAsync_ShouldUpdateProgressAndCounters();
        await t.DeepAnalyzeAsync_ShouldUpdateSummaryProgressAndLog();
        await t.DeepAnalyzeAsync_WhenCanceled_ShouldSetStatusAndRethrow();
        await t.ExecuteProfileAsync_WhenCanceled_ShouldSetStatusAndRethrow();
    }),
    ("CommandSecurityPolicyTests", () =>
    {
        var t = new CommandSecurityPolicyTests();
        t.Validate_ShouldAllowWhitelistedCommands();
        t.Validate_ShouldRejectNonWhitelistedCommand();
        t.Validate_ShouldRejectCommandInjectionPatterns();
        t.Validate_ShouldAllowExtendedCommands();
        return Task.CompletedTask;
    }),
    ("WindowsOptimizationProfilesTests", () =>
    {
        var t = new WindowsOptimizationProfilesTests();
        t.ExtremeProfile_ShouldNotContainSysMainOperation();
        t.PolicyMaxProfile_ShouldExposeExpectedPolicyOperations();
        return Task.CompletedTask;
    }),
    ("AppCatalogManagerTests", async () =>
    {
        var t = new AppCatalogManagerTests();
        await t.InstallBatchAsync_ShouldStopOnFirstFailure_WhenStrictMode();
        await t.InstallBatchAsync_ShouldContinue_WhenContinueOnErrorTrue();
    }),
    ("AutounattendBuilderTests", async () =>
    {
        var t = new AutounattendBuilderTests();
        t.GenerateXml_ShouldUseUnattendNamespaceAndWcmAction();
        await t.SaveToFileAsync_ShouldPersistValidXml();
    }),
    ("RollbackViewModelTests", async () =>
    {
        var t = new RollbackViewModelTests();
        await t.HasRollback_IsFalseBeforeAnyExecution();
        await t.HasRollback_IsTrueAfterExecutingRollbackableProfile();
        await t.HasRollback_IsFalseAfterRollback();
        await t.RollbackLastProfileAsync_ShouldInvokeRollbackOnReverseOrder();
        await t.RollbackLastProfileAsync_ShouldUpdateProgressToHundred();
        await t.HasRollback_IsFalseForProfileWithoutRollbackableOps();
    })
};

var failures = new List<string>();

foreach (var suite in suites)
{
    try
    {
        await suite.Run().ConfigureAwait(false);
        Console.WriteLine($"[PASS] {suite.Name}");
    }
    catch (Exception ex)
    {
        failures.Add($"{suite.Name}: {ex.Message}");
        Console.WriteLine($"[FAIL] {suite.Name}: {ex.Message}");
    }
}

if (failures.Count > 0)
{
    Console.Error.WriteLine("\nFalhas encontradas:");
    foreach (var failure in failures)
    {
        Console.Error.WriteLine($" - {failure}");
    }

    Environment.ExitCode = 1;
}
else
{
    Console.WriteLine("\nTodos os testes passaram.");
}
