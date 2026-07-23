document.addEventListener(
    "DOMContentLoaded",
    function () {

        const cards =
            document.querySelectorAll(
                ".vital-card"
            );


        cards.forEach(

            function (card, index) {

                card.style.animationDelay =
                    `${index * 0.1}s`;

            }

        );

    }
);