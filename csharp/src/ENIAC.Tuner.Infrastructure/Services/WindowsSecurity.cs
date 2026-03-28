using System.Security.Principal;
using System.Runtime.Versioning;

namespace ENIAC.Tuner.Infrastructure.Services;

[SupportedOSPlatform("windows")]
public static class WindowsSecurity
{
    public static bool IsAdministrator()
    {
        try
        {
            using var identity = WindowsIdentity.GetCurrent();
            var principal = new WindowsPrincipal(identity);
            return principal.IsInRole(WindowsBuiltInRole.Administrator);
        }
        catch
        {
            return false;
        }
    }
}