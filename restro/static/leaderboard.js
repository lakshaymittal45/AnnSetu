
        function showWeekly() {
            document.getElementById("weekly-leaderboard").style.display = "block";
            document.getElementById("monthly-leaderboard").style.display = "none";

            document.querySelector(".tab-button.active").classList.remove("active");
            document.querySelectorAll(".tab-button")[0].classList.add("active");
        }

        function showMonthly() {
            document.getElementById("weekly-leaderboard").style.display = "none";
            document.getElementById("monthly-leaderboard").style.display = "block";

            document.querySelector(".tab-button.active").classList.remove("active");
            document.querySelectorAll(".tab-button")[1].classList.add("active");
        }
   