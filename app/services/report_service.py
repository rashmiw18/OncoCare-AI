from datetime import datetime


class ReportService:


    @staticmethod
    def prepare_health_report(

        user,

        health_records,

        ai_insights

    ):


        report = {

            "patient_name":

                user.name,


            "patient_email":

                user.email,


            "report_generated_at":

                datetime.now(),


            "total_health_records":

                len(health_records),


            "total_ai_insights":

                len(ai_insights),


            "health_records":

                health_records,


            "ai_insights":

                ai_insights

        }


        return report