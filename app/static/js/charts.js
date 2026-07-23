document.addEventListener(

    "DOMContentLoaded",

    function () {


        const canvas =

            document.getElementById(

                "healthChart"

            );


        const selector =

            document.getElementById(

                "chartSelector"

            );


        const dataElement =

            document.getElementById(

                "health-data"

            );


        if (

            !canvas ||

            !selector ||

            !dataElement

        ) {

            console.error(

                "Chart elements not found."

            );

            return;

        }


        let data;


        try {


            data = JSON.parse(

                dataElement.textContent

            );


        } catch (error) {


            console.error(

                "Could not parse health chart data:",

                error

            );


            return;

        }


        console.log(

            "Health chart data:",

            data

        );


        const ctx =

            canvas.getContext(

                "2d"

            );


        const chartConfig = {


            heartRate: {

                label:

                    "Heart Rate (BPM)",

                data:

                    data.heartRate

            },


            spo2: {

                label:

                    "SpO₂ (%)",

                data:

                    data.spo2

            },


            temperature: {

                label:

                    "Temperature (°F)",

                data:

                    data.temperature

            },


            sleep: {

                label:

                    "Sleep (Hours)",

                data:

                    data.sleep

            },


            fatigue: {

                label:

                    "Fatigue Level",

                data:

                    data.fatigue

            },


            pain: {

                label:

                    "Pain Level",

                data:

                    data.pain

            }

        };


        let currentChart = null;


        function createChart(

            chartType

        ) {


            if (

                currentChart

            ) {


                currentChart.destroy();


            }


            const selected =

                chartConfig[

                    chartType

                ];


            if (

                !selected ||

                !selected.data ||

                selected.data.length === 0

            ) {


                console.warn(

                    "No data available for:",

                    chartType

                );


                return;

            }


            currentChart =

                new Chart(

                    ctx,

                    {


                        type:

                            "line",


                        data: {


                            labels:

                                data.labels,


                            datasets: [


                                {


                                    label:

                                        selected.label,


                                    data:

                                        selected.data,


                                    tension:

                                        0.4,


                                    borderWidth:

                                        2,


                                    pointRadius:

                                        4,


                                    pointHoverRadius:

                                        6,


                                    fill:

                                        false


                                }


                            ]

                        },


                        options: {


                            responsive:

                                true,


                            maintainAspectRatio:

                                false,


                            interaction: {


                                mode:

                                    "index",


                                intersect:

                                    false

                            },


                            plugins: {


                                legend: {


                                    display:

                                        true

                                }


                            },


                            scales: {


                                x: {


                                    ticks: {


                                        color:

                                            "#888"

                                    },


                                    grid: {


                                        color:

                                            "rgba(255,255,255,0.06)"

                                    }

                                },


                                y: {


                                    beginAtZero:

                                        false,


                                    ticks: {


                                        color:

                                            "#888"

                                    },


                                    grid: {


                                        color:

                                            "rgba(255,255,255,0.06)"

                                    }

                                }

                            }

                        }

                    }

                );

        }


        createChart(

            selector.value

        );


        selector.addEventListener(

            "change",

            function () {


                createChart(

                    this.value

                );

            }

        );

    }

);