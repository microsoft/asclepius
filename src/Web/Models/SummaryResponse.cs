namespace Web.Models;

using System.Text.Json.Serialization;

public class SummaryResponse
{
    [JsonPropertyName("summary")]
    public string Summary { get; set; }

    [JsonPropertyName("total_tokens")]
    public int TotalTokens { get; set; }
}