namespace Web.Models;

using System.Text.Json.Serialization;

/// <summary>
/// Represents a visit note.
/// NOTE_ID,LINE,PAT_ENC_CSN_ID,NOTE_TEXT
/// </summary>
public class VisitNote
{
    [JsonPropertyName("NOTE_ID")]
    public int NoteId { get; set; }

    [JsonPropertyName("LINE")]
    public int Line { get; set; }

    [JsonPropertyName("PAT_ENC_CSN_ID")]
    public int VisitId { get; set; }

    [JsonPropertyName("NOTE_TEXT")]
    public string NoteText { get; set; }

}