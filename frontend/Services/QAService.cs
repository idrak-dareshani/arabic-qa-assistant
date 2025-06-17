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

    public async Task<QAAnswer> GetAnswerAsync(string query)
    {
        var encoded = Uri.EscapeDataString(query);
        var result = await _http.GetFromJsonAsync<QAAnswer>($"http://localhost:8000/qa?query={encoded}");
        if (result == null)
        {
            throw new System.Exception("Failed to retrieve QAAnswer from the service.");
        }
        return result;
    }
}
