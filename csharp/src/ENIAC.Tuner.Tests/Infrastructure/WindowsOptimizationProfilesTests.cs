using ENIAC.Tuner.Core.Abstractions;
using ENIAC.Tuner.Infrastructure.Services;

namespace ENIAC.Tuner.Tests.Infrastructure;

public sealed class WindowsOptimizationProfilesTests
{
    public void ExtremeProfile_ShouldNotContainSysMainOperation()
    {
        var profile = WindowsOptimizationProfiles.ExtremeProfile();

        TestAssert.False(
            profile.Operations.Any(operation => operation.Name.Contains("SysMain", StringComparison.OrdinalIgnoreCase)),
            "Perfil extremo nao deve mais conter SysMain.");
    }

    public void PolicyMaxProfile_ShouldExposeExpectedPolicyOperations()
    {
        var profile = WindowsOptimizationProfiles.PolicyMaxProfile();

        TestAssert.Equal("policy-max", profile.Id, "Id do perfil deve ser policy-max.");
        TestAssert.Equal("Policy-Max", profile.DisplayName, "Nome do perfil deve ser Policy-Max.");
        TestAssert.True(profile.Operations.Count >= 10, "Policy-Max deve incluir um conjunto amplo de politicas.");
        TestAssert.True(
            profile.Operations.Any(operation => operation.Name.Contains("OneDrive", StringComparison.OrdinalIgnoreCase)),
            "Policy-Max deve bloquear OneDrive.");
        TestAssert.True(
            profile.Operations.Any(operation => operation.Name.Contains("Cortana", StringComparison.OrdinalIgnoreCase)),
            "Policy-Max deve desativar Cortana.");
        TestAssert.True(
            profile.Operations.Any(operation => operation.Name.Contains("Spotlight", StringComparison.OrdinalIgnoreCase)),
            "Policy-Max deve cortar recursos do Spotlight.");
        TestAssert.True(
            profile.Operations.Count(operation => operation is IRollbackable) >= 15,
            "Policy-Max deve permitir rollback da maior parte das politicas.");
    }
}