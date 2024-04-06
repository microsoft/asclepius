from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel_pydantic import KernelBaseModel

class ParseNotesPlugin(KernelBaseModel):
    @kernel_function(name='GetChiefComplaint')
    def get_chief_complaint(self, input: str) -> str:
        start_index = input.find('Chief Complaint\n')
        end_index = input.find('ROS\n')
        return input[start_index:end_index]
    
    @kernel_function(name='GetROS')
    def get_ros(self, input: str) -> str:
        start_index = input.find('ROS\n')
        end_index = input.find('Past Medical History\n')
        return input[start_index:end_index]
    
    @kernel_function(name='GetAssessment')
    def get_assessment(self, input: str) -> str:
        start_index = input.find('ASSESSMENT and PLAN:')
        end_index = input.find('Revision History\n')
        return input[start_index:end_index]