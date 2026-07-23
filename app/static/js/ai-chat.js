document.addEventListener(
    "DOMContentLoaded",
    function () {

        const chatForm =
            document.getElementById(
                "aiChatForm"
            );


        if (!chatForm) {
            return;
        }


        chatForm.addEventListener(

            "submit",

            function (event) {

                event.preventDefault();

                console.log(
                    "AI chat module ready."
                );

            }

        );

    }
);