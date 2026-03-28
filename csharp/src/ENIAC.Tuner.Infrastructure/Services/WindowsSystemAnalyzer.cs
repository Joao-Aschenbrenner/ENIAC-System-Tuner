using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Text;

namespace ENIAC.Tuner.Infrastructure.Services;

public static class WindowsSystemAnalyzer
{
    public static string BuildSummary()
    {
        var processRamMb = Environment.WorkingSet / 1024d / 1024d;

        return
            $"SO: {RuntimeInformation.OSDescription}\n" +
            $"Arquitetura: {RuntimeInformation.OSArchitecture}\n" +
            $"Runtime: {RuntimeInformation.FrameworkDescription}\n" +
            $"RAM do processo atual: {processRamMb:F0} MB";
    }

    public static string BuildDetailedReport()
    {
        var sb = new StringBuilder();
        sb.AppendLine("============================================================");
        sb.AppendLine("DIAGNOSTICO DETALHADO - ENIAC SYSTEM TUNER (C#)");
        sb.AppendLine($"Data/Hora: {DateTime.Now:dd/MM/yyyy HH:mm:ss}");
        sb.AppendLine("============================================================");
        sb.AppendLine();

        AppendSystemSection(sb);
        AppendMemorySection(sb);
        AppendDiskSection(sb);
        AppendTopProcessesSection(sb);

        return sb.ToString();
    }

    private static void AppendSystemSection(StringBuilder sb)
    {
        sb.AppendLine("[SISTEMA]");
        sb.AppendLine($"SO: {RuntimeInformation.OSDescription}");
        sb.AppendLine($"Arquitetura SO: {RuntimeInformation.OSArchitecture}");
        sb.AppendLine($"Arquitetura Processo: {RuntimeInformation.ProcessArchitecture}");
        sb.AppendLine($"Runtime: {RuntimeInformation.FrameworkDescription}");
        sb.AppendLine($"Maquina: {Environment.MachineName}");
        sb.AppendLine($"Processadores logicos: {Environment.ProcessorCount}");
        sb.AppendLine();
    }

    private static void AppendMemorySection(StringBuilder sb)
    {
        sb.AppendLine("[MEMORIA]");
        var gcInfo = GC.GetGCMemoryInfo();
        var totalAvailableMb = gcInfo.TotalAvailableMemoryBytes / 1024d / 1024d;
        var heapMb = GC.GetTotalMemory(forceFullCollection: false) / 1024d / 1024d;
        var workingSetMb = Environment.WorkingSet / 1024d / 1024d;

        sb.AppendLine($"Memoria disponivel para GC: {totalAvailableMb:F0} MB");
        sb.AppendLine($"Heap gerenciado atual: {heapMb:F0} MB");
        sb.AppendLine($"Working set do processo: {workingSetMb:F0} MB");
        sb.AppendLine();
    }

    private static void AppendDiskSection(StringBuilder sb)
    {
        sb.AppendLine("[DISCOS]");

        var drives = DriveInfo.GetDrives()
            .Where(d => d.IsReady)
            .OrderBy(d => d.Name);

        foreach (var drive in drives)
        {
            var totalGb = drive.TotalSize / 1024d / 1024d / 1024d;
            var freeGb = drive.AvailableFreeSpace / 1024d / 1024d / 1024d;
            var usedPercent = totalGb <= 0 ? 0 : ((totalGb - freeGb) / totalGb) * 100;

            sb.AppendLine($"{drive.Name} ({drive.DriveFormat})");
            sb.AppendLine($"  Total: {totalGb:F1} GB");
            sb.AppendLine($"  Livre: {freeGb:F1} GB");
            sb.AppendLine($"  Uso: {usedPercent:F1}%");

            if (usedPercent >= 90)
            {
                sb.AppendLine("  ALERTA: Disco quase cheio");
            }
            else if (usedPercent >= 80)
            {
                sb.AppendLine("  ATENCAO: Espaco em disco limitado");
            }

            sb.AppendLine();
        }
    }

    private static void AppendTopProcessesSection(StringBuilder sb)
    {
        sb.AppendLine("[TOP PROCESSOS POR MEMORIA]");

        var processData = new List<(string Name, double WorkingSetMb)>();
        foreach (var process in Process.GetProcesses())
        {
            try
            {
                var memoryMb = process.WorkingSet64 / 1024d / 1024d;
                processData.Add((process.ProcessName, memoryMb));
            }
            catch
            {
                // Processo pode encerrar ou negar acesso durante leitura.
            }
            finally
            {
                process.Dispose();
            }
        }

        foreach (var item in processData
            .OrderByDescending(p => p.WorkingSetMb)
            .Take(10)
            .Select((p, index) => new { Index = index + 1, p.Name, p.WorkingSetMb }))
        {
            sb.AppendLine($"{item.Index}. {item.Name} - {item.WorkingSetMb:F0} MB");
        }

        sb.AppendLine();
    }
}
