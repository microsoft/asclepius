using System.Text.Json.Serialization;

namespace Web.Models;

// create a lab result model class with the following properties
// PAT_ID,ORDER_PROC_ID,PAT_ENC_CSN_ID,ORDER_INST,REMARKS_HNO_ID,
// DESCRIPTION,PROC_ID,PROC_NAME,PROC_CODE,PROC_CAT_ID,
// PROC_CAT_NAME,CONTACT_TYPE_C,CONTACT_TYPE,ABNORMAL_YN,
// ORDER_STATUS_C,ORDER_STATUS,LAB_STATUS_C,LAB_STATUS,ORDER_TYPE_C,
// ORDER_TYPE,AUTHRZING_PROV_ID,AUTHRZING_PROV_NAME,ORDER_TIME,
// REVIEW_TIME,RESULT_TIME,RESULT_LAB_ID,RESULT_LAB_NAME,SPECIMEN_TYPE_C,
// SPECIMEN_TYPE,COMMENT_RESULTS
public class LabOrderResults
{
    [JsonPropertyName("PAT_ID")]
    public string PatientId { get; set; }
    
    [JsonPropertyName("ORDER_PROC_ID")]
    public int OrderProcedureId { get; set; }
    
    [JsonPropertyName("PAT_ENC_CSN_ID")]
    public int PatientEncounterCsnId { get; set; }
    
    [JsonPropertyName("ORDER_INST")]
    public string OrderInstitution { get; set; }
    
    [JsonPropertyName("REMARKS_HNO_ID")]
    public int RemarksHnoId { get; set; }
    
    [JsonPropertyName("DESCRIPTION")]
    public string Description { get; set; }
    
    [JsonPropertyName("PROC_ID")]
    public int ProcedureId { get; set; }
    
    [JsonPropertyName("PROC_NAME")]
    public string ProcedureName { get; set; }
    
    [JsonPropertyName("PROC_CODE")]
    public string ProcedureCode { get; set; }
        
    [JsonPropertyName("PROC_CAT_NAME")]
    public string ProcedureCategoryName { get; set; }
    
    [JsonPropertyName("CONTACT_TYPE")]
    public string ContactType { get; set; }
    
    [JsonPropertyName("ABNORMAL_YN")]
    public string AbnormalYn { get; set; }
        
    [JsonPropertyName("ORDER_STATUS")]
    public string OrderStatus { get; set; }
    
    [JsonPropertyName("LAB_STATUS")]
    public string LabStatus { get; set; }
    
    [JsonPropertyName("ORDER_TYPE")]
    public string OrderType { get; set; }
    
    [JsonPropertyName("AUTHRZING_PROV_ID")]
    public int AuthorizingProviderId { get; set; }
    
    [JsonPropertyName("AUTHRZING_PROV_NAME")]
    public string AuthorizingProviderName { get; set; }
    
    [JsonPropertyName("ORDER_TIME")]
    public DateTime OrderTime { get; set; }

    [JsonPropertyName("REVIEW_TIME")]
    public DateTime ReviewTime { get; set; }

    [JsonPropertyName("RESULT_TIME")]
    public DateTime ResultTime { get; set; }

    [JsonPropertyName("RESULT_LAB_NAME")]
    public string ResultLabName { get; set; }

    [JsonPropertyName("SPECIMEN_TYPE")]
    public string SpecimenType { get; set; }

    [JsonPropertyName("COMMENT_RESULTS")]
    public string CommentResults { get; set; }

}