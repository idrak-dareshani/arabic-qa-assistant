using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

public class QAService
{
    private readonly HttpClient _http;

    public QAService(HttpClient http)
    {
        _http = http;
    }

    public async Task<QAAnswer> GetAnswerAsync(string query, string? level = null, string? section = null)
    {
        var encoded = Uri.EscapeDataString(query);

        var url = $"http://localhost:8000/qa?query={Uri.EscapeDataString(encoded)}";
        if (!string.IsNullOrWhiteSpace(level))
            url += $"&level={Uri.EscapeDataString(level)}";
        if (!string.IsNullOrWhiteSpace(section))
            url += $"&section={Uri.EscapeDataString(section)}";

        var result = await _http.GetFromJsonAsync<QAAnswer>(url) ?? throw new System.Exception("Failed to retrieve QAAnswer from the service.");
        return result;
    }
}
