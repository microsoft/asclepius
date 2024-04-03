using System.Text.Json.Serialization;

namespace Mercy.LabSummarization.Web.Models;

// Create patient model class with following fields
// PAT_ID,PAT_MRN_ID,PAT_NAME,PAT_FIRST_NAME,PAT_LAST_NAME,HOME_PHONE,BIRTH_DATE,
// CURRENT_AGE,GENDER,ETHNCTY,RACE,
// ADD_LINE_1,ADD_LINE_2,CITY,STATE_NAME,STATE_ABBR,ZIP_5,LANGUAGE_NAME,MYCHART_ACTIVE_YN

public class Patient
{
    [JsonPropertyName("PAT_ID")]
    public string PatientId { get; set; }
    
    [JsonPropertyName("PAT_MRN_ID")]
    public string PatientMRNId { get; set; }
    
    [JsonPropertyName("PAT_NAME")]
    public string PatientName { get; set; }
    
    [JsonPropertyName("PAT_FIRST_NAME")]
    public string PatientFirstName { get; set; }
    
    [JsonPropertyName("PAT_LAST_NAME")]
    public string PatientLastName { get; set; }
    
    [JsonPropertyName("HOME_PHONE")]
    public string HomePhone { get; set; }
    
    [JsonPropertyName("BIRTH_DATE")]
    public DateTime BirthDate { get; set; }
    
    [JsonPropertyName("CURRENT_AGE")]
    public int CurrentAge { get; set; }
    
    [JsonPropertyName("GENDER")]
    public string Gender { get; set; }
    
    [JsonPropertyName("ETHNCTY")]
    public string Ethnicity { get; set; }
    
    [JsonPropertyName("RACE")]
    public string Race { get; set; }
    
    [JsonPropertyName("ADD_LINE_1")]
    public string AddressLine1 { get; set; }
    
    [JsonPropertyName("CITY")]
    public string City { get; set; }
    
    [JsonPropertyName("STATE_NAME")]
    public string StateName { get; set; }
    
    [JsonPropertyName("STATE_ABBR")]
    public string StateAbbreviation { get; set; }
    
    [JsonPropertyName("ZIP_5")]
    public int ZipCode { get; set; }
    
    [JsonPropertyName("LANGUAGE_NAME")]
    public string Language { get; set; }
    
    [JsonPropertyName("MYCHART_ACTIVE_YN")]
    public string MyChartActive { get; set; }
}