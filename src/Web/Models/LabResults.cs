using System.Text.Json.Serialization;

namespace Web.Models
{
    public class LabResults
    {
        [JsonPropertyName("PAT_ENC_CSN_ID")]
        public int PatientEncounterCSNId { get; set; }

        [JsonPropertyName("ORD_ID")]
        public int OrderId { get; set; }

        [JsonPropertyName("CMPNT_ID")]
        public int ComponentId { get; set; }

        [JsonPropertyName("CMPNT_NM")]
        public string ComponentName { get; set; }

        [JsonPropertyName("RSLT_TSP")]
        public DateTime ResultTimestamp { get; set; }

        [JsonPropertyName("RSLT_VALUE_TXT")]
        public decimal ResultValue { get; set; }

        [JsonPropertyName("REFER_UNIT")]
        public string ReferenceUnit { get; set; }

        [JsonPropertyName("REFER_VALUE")]
        public string ReferenceValue { get; set; }
    }
}