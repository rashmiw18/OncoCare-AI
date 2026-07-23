from sklearn.ensemble import IsolationForest

from app.ml.feature_engineering import (
    FeatureEngineer
)


class AnomalyDetector:

    def __init__(self):

        self.feature_engineer = FeatureEngineer()

        self.model = IsolationForest(

            contamination=0.15,

            random_state=42

        )


    def detect_anomalies(self, health_records):

        if not health_records:

            return {

                "status": "insufficient_data",

                "message": (
                    "Not enough health records "
                    "for anomaly detection."
                ),

                "anomalies": []

            }


        dataframe = (

            self.feature_engineer
            .create_features(
                health_records
            )

        )


        if len(dataframe) < 3:

            return {

                "status": "insufficient_data",

                "message": (
                    "At least 3 health records "
                    "are recommended."
                ),

                "anomalies": []

            }


        predictions = self.model.fit_predict(

            dataframe

        )


        anomaly_scores = self.model.decision_function(

            dataframe

        )


        anomalies = []


        for index, prediction in enumerate(

            predictions

        ):


            if prediction == -1:

                anomalies.append({

                    "record_index": index,

                    "anomaly_score": float(

                        anomaly_scores[index]

                    ),

                    "health_data":
                        dataframe.iloc[
                            index
                        ].to_dict()

                })


        return {

            "status": "success",

            "total_records": len(

                health_records

            ),

            "anomaly_count": len(

                anomalies

            ),

            "anomalies": anomalies

        }