import pandas as pd


class FeatureEngineer:

    def create_features(self, health_records):

        data = []

        for record in health_records:

            row = {

                "temperature": record.temperature,

                "heart_rate": record.heart_rate,

                "spo2": record.spo2,

                "sleep_hours": record.sleep_hours,

                "pain_level": record.pain_level,

                "fatigue_level": record.fatigue_level,

                "nausea_level": record.nausea_level,

                "dizziness": int(
                    record.dizziness
                    if record.dizziness is not None
                    else False
                )

            }

            data.append(row)


        if not data:

            return pd.DataFrame()


        dataframe = pd.DataFrame(data)


        dataframe = dataframe.fillna(

            dataframe.median(numeric_only=True)

        )


        return dataframe