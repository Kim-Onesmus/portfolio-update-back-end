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

            if (response.ok && responseData.response?.ResponseCode === '0') {
                document.getElementById('modalTwo').style.display = 'none';
                document.getElementById('waitingModal').style.display = 'block';

                const transactionId = responseData.id;

                const checkPaymentStatus = async () => {
                    try {
                        const payResponse = await fetch(`/check_payment_status?user_id=${transactionId}`);
                        const payResponseData = await payResponse.json();

                        if (payResponse.ok && payResponseData.data === "Paid") {
                            document.getElementById('waitingModal').style.display = 'none';
                            document.getElementById('successModal').style.display = 'block';
                        } else if (payResponse.ok && payResponseData.data !== "Paid") {
                            setTimeout(checkPaymentStatus, 2000);
                        } else {
                            throw new Error("Payment status check failed");
                        }
                    } catch (error) {
                        console.error('Error while checking payment status:', error);
                        document.getElementById('waitingModal').style.display = 'none';
                        document.getElementById('errorModal').style.display = 'block';
                    }
                };

                checkPaymentStatus();
            } else {
                handlePaymentError(responseData.message || "There was an issue with your payment.");
            }
        } catch (error) {
            console.error('Error processing payment:', error);
            handlePaymentError("An error occurred while processing your payment.");
        } finally {
            resetSubmitButton(submitButton);
        }
    });

    function handlePaymentError(errorMessage) {
        document.getElementById('errorMessage').textContent = errorMessage;
        document.getElementById('modalTwo').style.display = 'none';
        document.getElementById('errorModal').style.display = 'block';

        const progressBar = document.getElementById('errorProgressBar');
        let progress = 100;
        const interval = 50;
        const totalDuration = 5000;
        const decrement = 100 / (totalDuration / interval);

        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);

        const progressInterval = setInterval(() => {
            progress -= decrement;
            progressBar.style.width = `${Math.max(progress, 0)}%`;
            progressBar.setAttribute('aria-valuenow', Math.max(progress, 0));

            if (progress <= 0) {
                clearInterval(progressInterval);
                document.getElementById('errorModal').style.display = 'none';
            }
        }, interval);
    }

    function resetSubmitButton(button) {
        button.innerHTML = 'Submit';
        button.disabled = false;
    }
});
