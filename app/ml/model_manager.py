import os

import joblib


class ModelManager:

    def __init__(

        self,

        model_path="data/trained_models"

    ):

        self.model_path = model_path


        os.makedirs(

            self.model_path,

            exist_ok=True

        )


    def save_model(

        self,

        model,

        model_name

    ):


        file_path = os.path.join(

            self.model_path,

            model_name

        )


        joblib.dump(

            model,

            file_path

        )


        return file_path


    def load_model(

        self,

        model_name

    ):


        file_path = os.path.join(

            self.model_path,

            model_name

        )


        if not os.path.exists(

            file_path

        ):

            return None


        return joblib.load(

            file_path

        )