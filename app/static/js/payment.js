document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submitPayment').addEventListener('click', async function (e) {
        e.preventDefault();

        const submitButton = document.getElementById('submitPayment');
        const number = document.getElementById('number').value;
        const amount = document.getElementById('amount').value;

        if (!number || !amount) {
            alert('Please enter valid phone number and amount.');
            return;
        }

        submitButton.innerHTML = 'Initiating Payment....... <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
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
            console.log('Payment response', responseData.id)
            const transactionId = responseData.id;



            if (response.status_code == 200 && response.json().get('response', {}).get('ResponseCode') == '0') {
                document.getElementById('modalTwo').style.display = 'none';
                document.getElementById('waitingModal').style.display = 'block';

                const checkPaymentStatus = async () => {
                    try {
                        const payResponse = await fetch(`/check_payment_status?user_id=${transactionId}`);
                        const payResponseData = await payResponse.json();

                        console.log('Payment status response:', payResponseData);

                        if (payResponse.status === 200 && payResponseData.data === "Paid") {
                            document.getElementById('waitingModal').style.display = 'none';
                            const successModal = document.getElementById('successModal');
                            successModal.style.display = 'block';
                        } else {
                            setTimeout(checkPaymentStatus, 2000);
                        }
                    } catch (error) {
                        console.error('Error while checking payment status:', error);
                        document.getElementById('waitingModal').style.display = 'none';
                        const errorModal = document.getElementById('errorModal');
                        errorModal.style.display = 'block';
                    }
                };

                checkPaymentStatus();
            } 
            else {
                document.getElementById('errorMessage').textContent = responseData.message || "There was an issue with your payment.";
                document.getElementById('errorModal').style.display = 'block';
                document.getElementById('modalTwo').style.display = 'none';

                const progressBar = document.getElementById('errorProgressBar');
                let progress = 100;
                const interval = 50;
                const totalDuration = 5000;
                const decrement = 100 / (totalDuration / interval);

                progressBar.style.width = progress + '%';
                progressBar.setAttribute('aria-valuenow', progress);

                const progressInterval = setInterval(() => {
                    progress -= decrement;
                    progressBar.style.width = Math.max(progress, 0) + '%';
                    progressBar.setAttribute('aria-valuenow', Math.max(progress, 0));

                    if (progress <= 0) {
                        clearInterval(progressInterval);
                        document.getElementById('errorModal').style.display = 'none';
                    }
                }, interval);

            }

        } catch (error) {
            console.error('Error processing payment:', error);
            document.getElementById('errorMessage').textContent = "An error occurred while processing your payment.";
            document.getElementById('errorModal').style.display = 'block';
            document.getElementById('modalTwo').style.display = 'none';
        } finally {
            submitButton.innerHTML = 'Submit';
        }
    });
});