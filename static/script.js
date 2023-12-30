document.addEventListener('DOMContentLoaded', function() {
    // Function to disable the button and start the 5-minute timer
    function startTimer() {
        var btnNext = document.querySelector('.btn-next');
        btnNext.disabled = true;

        //var timer = 5 * 60; // 5 minutes in seconds
        var timer = 10; // 10 seconds

        var intervalId = setInterval(function() {
            timer--;

            //var minutes = Math.floor(timer / 60);
            //var seconds = timer % 60;
            var seconds = timer;

            // Update the button text with the remaining time
            //btnNext.innerHTML = 'Guess Next Picture (' + minutes + ':' + (seconds < 10 ? '0' : '') + seconds + ')';
            btnNext.innerHTML = 'Guess Next Picture (' + seconds + 's)';


            if (timer <= 0) {
                // Enable the button and reset the text after the timer runs out
                btnNext.disabled = false;
                btnNext.innerHTML = 'Guess Next Picture';
                clearInterval(intervalId);
            }
        }, 1000);
    }

    // Check if guess_result is not null (user has guessed)
    var guessResult = '{{ guess_result }}';
    if (guessResult !== null && guessResult !== '') {
        startTimer(); // Start the timer after the user has guessed
    }
});
