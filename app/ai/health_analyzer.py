from app.ai.risk_engine import RiskEngine


class HealthAnalyzer:

    def __init__(self):

        self.risk_engine = RiskEngine()


    def analyze_health_record(
        self,
        health_record
    ):


        risk_result = self.risk_engine.analyze(

            health_record

        )


        health_data = {

            "temperature": health_record.temperature,

            "heart_rate": health_record.heart_rate,

            "spo2": health_record.spo2,

            "sleep_hours": health_record.sleep_hours,

            "pain_level": health_record.pain_level,

            "fatigue_level": health_record.fatigue_level,

            "nausea_level": health_record.nausea_level,

            "dizziness": health_record.dizziness,

            "notes": health_record.notes

        }


        return {

            "health_data": health_data,

            "risk_level": risk_result["risk_level"],

            "risk_score": risk_result["risk_score"],

            "risk_factors": risk_result["risk_factors"]

        }