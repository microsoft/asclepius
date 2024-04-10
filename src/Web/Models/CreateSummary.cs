namespace Web.Models;

using System.Text.Json.Serialization;

public class CreateSummary
{
    [JsonPropertyName("lab_results")]
    public List<LabResults> LabResults { get; set; }

    [JsonPropertyName("visit_note")]
    public string VisitNote { get; set; }
}