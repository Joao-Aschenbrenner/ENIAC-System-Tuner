namespace ENIAC.Tuner.Tests;

public static class TestAssert
{
    public static void True(bool condition, string message)
    {
        if (!condition)
        {
            throw new InvalidOperationException(message);
        }
    }

    public static void False(bool condition, string message)
    {
        if (condition)
        {
            throw new InvalidOperationException(message);
        }
    }

    public static void Equal<T>(T expected, T actual, string message)
    {
        if (!EqualityComparer<T>.Default.Equals(expected, actual))
        {
            throw new InvalidOperationException($"{message}. Esperado: {expected}; Atual: {actual}");
        }
    }

    public static void Contains(string expectedSubstring, string actual, string message)
    {
        if (actual is null || !actual.Contains(expectedSubstring, StringComparison.OrdinalIgnoreCase))
        {
            throw new InvalidOperationException($"{message}. Substring esperada: {expectedSubstring}");
        }
    }
}
