document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submitPayment').addEventListener('click', async function (e) {
        e.preventDefault();

        const submitButton = document.getElementById('submitPayment');
        const number = document.getElementById('number').value.trim();
        const amount = document.getElementById('amount').value.trim();

        if (!number || !amount) {
            alert('Please enter a valid phone number and amount.');
            return;
        }

        submitButton.innerHTML = 'Initiating Payment... <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
        submitButton.disabled = true;
        

        const data = { number, amount };

        try {
            const response = await fetch('/buy_me_coffee/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify(data),
            });

            const responseData = await response.json();
            console.log('Response data', responseData);
            console.log('Response status', responseData.status);


            if (responseData.status === 200) {
                document.getElementById('modalTwo').style.display = 'none';
                document.getElementById('waitingModal').style.display = 'block';

                const transactionId = responseData.id;


                const checkPaymentStatus = async () => {
                let retries = 20;
                let successful = false;
                while (retries > 0) {
                    try {
                        const payResponse = await fetch(`/check_payment?user_id=${transactionId}`);
                        const payResponseData = await payResponse.json();
                        console.log('Pay Response', payResponseData);
                        
                        if (payResponseData.status === 202) {
                            console.log('Payment is pending. Retrying...');
                        } else if (payResponseData.status === 200) {
                            handlePaymentSuccess(payResponseData.message);
                            successful = true;
                            break;
                        } else {
                            handlePaymentError(payResponseData.message);
                            successful = true;
                            break;
                        }
                    } catch (error) {
                        handlePaymentError("An error occurred while checking payment status.");
                    }
                    retries--;
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }

                if (!successful) {
                    handlePaymentError("You didnt interact with the STK push within the specified time");
                }
            };

            checkPaymentStatus();

            } else {
                handlePaymentError("There was an error while initiating payment.");
            }
        } catch (error) {
            handlePaymentError("Internal server error!! An error occurred!!");
        } finally {
            resetSubmitButton(submitButton);
        }
    });

    function handlePaymentError(errorMessage) {
        document.getElementById('errorMessage').textContent = errorMessage;
        document.getElementById('modalTwo').style.display = 'none';
        document.getElementById('waitingModal').style.display = 'none';
        document.getElementById('errorModal').style.display = 'block';

        const progressBar = document.getElementById('errorProgressBar');
        let progress = 100;
        let interval = setInterval(function() {
            if (progress > 0) {
                progress--;
                $(progressBar).css('width', progress + '%');
                $(progressBar).attr('aria-valuenow', progress);
            } else {
                $(progressBar).css('width', '0%');
                $(progressBar).attr('aria-valuenow', '0');
                clearInterval(interval);
                document.getElementById('errorModal').style.display = 'none';
            }
        }, 100);
    }
    function handlePaymentSuccess(successMessage) {
        document.getElementById('successMessage').textContent = successMessage;
        document.getElementById('modalTwo').style.display = 'none';
        document.getElementById('waitingModal').style.display = 'none';
        document.getElementById('successModal').style.display = 'block';

        const successProgressBars = document.getElementById('successProgressBar');
        let successProgress = 100;
        let successInterval = setInterval(function() {
            if (successProgress > 0) {
                successProgress--;
                $(successProgressBars).css('width', successProgress + '%');
                $(successProgressBars).attr('aria-valuenow', successProgress);
            } else {
                $(successProgressBars).css('width', '0%');
                $(successProgressBars).attr('aria-valuenow', '0');
                clearInterval(successInterval);
                document.getElementById('successModal').style.display = 'none';
            }
        }, 100);
    }

    function resetSubmitButton(button) {
        button.innerHTML = 'Submit';
        button.disabled = false;
    }
});
