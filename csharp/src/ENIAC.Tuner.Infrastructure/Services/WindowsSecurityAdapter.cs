using ENIAC.Tuner.Core.Abstractions;
using System.Runtime.Versioning;

namespace ENIAC.Tuner.Infrastructure.Services;

[SupportedOSPlatform("windows")]
public sealed class WindowsSecurityAdapter : ISystemSecurity
{
    public bool IsAdministrator() => WindowsSecurity.IsAdministrator();
}
