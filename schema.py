# The purpose of this file is to validate the output schema from the LLM

from pydantic import BaseModel, Field, model_validator
from typing import Literal

class Patient(BaseModel):
    name: str = Field(min_length=1)
    age_value: float | None = None
    age_unit: Literal["year(s)", "month(s)", "week(s)", "day(s)"] | None = None
    sex: Literal["Male", "Female"] | None = None
    
    @model_validator(mode="after")
    def validate_age_format(self):
        if self.age is not None and self.age_unit is not None:
            if self.age_unit == "years" and self.age % 1 != 0:
                raise ValueError(
                    "Age in years must be a whole number"
                )
        return self
    
class Diagnosis(BaseModel):
    condition: str
    certainty: str | None = None # example: likely, possible, confirmed
    status: str | None = None # example: improving, stable, controlled, etc

class Medication(BaseModel):
    medicine_name: str
    dosage: float | None = Field(default=None, gt=0)
    unit: str | None = None
    frequency: str | None = None
    duration: str | None = None
    additional_notes: str | None = None # example: before/after meal
    
class FollowUp(BaseModel):
    timeframe: str | None = None
    instructions: str | None = None
    
class Consultation(BaseModel):
    consultation_id: str = Field(pattern=r"^(TM-\d{4}-\d{4})$")
    date: str | None = None
    patient: Patient
    patient_history: str | None = None
    consultation_reason: str | None = None
    diagnoses: list[Diagnosis] = Field(default_factory=list) # to avoid mutability
    medications: list[Medication] = Field(default_factory=list) # to avoid mutability
    treatment_plan: list[str] = Field(default_factory=list) # to avoid mutability
    provider: str | None = None
    clinical_observations: str | None = None
    follow_up_instructions: FollowUp | None = None
    
    
    
    