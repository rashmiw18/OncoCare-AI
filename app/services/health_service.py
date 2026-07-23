from app.ml.anomaly_detector import (
    AnomalyDetector
)

from app.ai.health_analyzer import (
    HealthAnalyzer
)

from app.ai.gemini_service import (
    GeminiService
)


class HealthService:


    def __init__(self):

        self.anomaly_detector = (

            AnomalyDetector()

        )


        self.health_analyzer = (

            HealthAnalyzer()

        )


        self.gemini_service = (

            GeminiService()

        )


    def analyze_patient_health(

        self,

        health_records

    ):


        # =====================================
        # STEP 1: ML ANOMALY DETECTION
        # =====================================

        anomaly_result = (

            self.anomaly_detector

            .detect_anomalies(

                health_records

            )

        )


        # =====================================
        # STEP 2: CHECK DATA
        # =====================================

        if not health_records:

            return {

                "status": "insufficient_data",

                "message":

                    "No health records available."

            }


        # =====================================
        # STEP 3: LATEST RECORD
        # =====================================

        latest_record = (

            health_records[-1]

        )


        risk_result = (

            self.health_analyzer

            .analyze_health_record(

                latest_record

            )

        )


        # =====================================
        # STEP 4: ANOMALY FACTORS
        # =====================================

        anomaly_factors = []


        if (

            anomaly_result.get(

                "status"

            )

            == "success"

        ):


            if (

                anomaly_result.get(

                    "anomaly_count",

                    0

                )

                > 0

            ):


                anomaly_factors.append(

                    "Unusual health pattern detected "
                    "by machine learning analysis."

                )


        all_risk_factors = (

            risk_result.get(

                "risk_factors",

                []

            )

            + anomaly_factors

        )


        # =====================================
        # STEP 5: PREPARE AI DATA
        # =====================================

        analysis_data = {

            "health_data":

                risk_result.get(

                    "health_data",

                    {}

                ),


            "risk_level":

                risk_result.get(

                    "risk_level",

                    "Unknown"

                ),


            "risk_factors":

                all_risk_factors

        }


        # =====================================
        # STEP 6: GEMINI ANALYSIS
        # =====================================

        ai_insight = (

            self.gemini_service

            .generate_health_insight(

                analysis_data

            )

        )


        # =====================================
        # FINAL RESULT
        # =====================================

        return {

            "status": "success",


            "risk_level":

                risk_result.get(

                    "risk_level",

                    "Unknown"

                ),


            "risk_score":

                risk_result.get(

                    "risk_score",

                    0

                ),


            "risk_factors":

                all_risk_factors,


            "anomaly_result":

                anomaly_result,


            "ai_insight":

                ai_insight

        }