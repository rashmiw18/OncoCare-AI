class RiskEngine:

    def __init__(self):

        self.risk_score = 0

        self.risk_factors = []


    def analyze(self, health_data):

        self.risk_score = 0

        self.risk_factors = []


        # =====================================
        # TEMPERATURE
        # =====================================

        if health_data.temperature is not None:

            if health_data.temperature >= 100.4:

                self.risk_score += 3

                self.risk_factors.append(
                    "Elevated temperature detected"
                )


        # =====================================
        # HEART RATE
        # =====================================

        if health_data.heart_rate is not None:

            if health_data.heart_rate > 100:

                self.risk_score += 2

                self.risk_factors.append(
                    "Elevated heart rate detected"
                )


            elif health_data.heart_rate < 50:

                self.risk_score += 2

                self.risk_factors.append(
                    "Low heart rate detected"
                )


        # =====================================
        # SPO2
        # =====================================

        if health_data.spo2 is not None:

            if health_data.spo2 < 94:

                self.risk_score += 3

                self.risk_factors.append(
                    "Lower-than-usual blood oxygen level detected"
                )


        # =====================================
        # PAIN
        # =====================================

        if health_data.pain_level is not None:

            if health_data.pain_level >= 7:

                self.risk_score += 2

                self.risk_factors.append(
                    "High pain level reported"
                )


        # =====================================
        # FATIGUE
        # =====================================

        if health_data.fatigue_level is not None:

            if health_data.fatigue_level >= 8:

                self.risk_score += 2

                self.risk_factors.append(
                    "High fatigue level reported"
                )


        # =====================================
        # NAUSEA
        # =====================================

        if health_data.nausea_level is not None:

            if health_data.nausea_level >= 8:

                self.risk_score += 2

                self.risk_factors.append(
                    "High nausea level reported"
                )


        # =====================================
        # RISK CLASSIFICATION
        # =====================================

        if self.risk_score >= 6:

            risk_level = "High"

        elif self.risk_score >= 3:

            risk_level = "Medium"

        else:

            risk_level = "Low"


        return {

            "risk_score": self.risk_score,

            "risk_level": risk_level,

            "risk_factors": self.risk_factors

        }