document.addEventListener('DOMContentLoaded', function() {
    const billForm = document.getElementById('billForm');
    const amountUsdInput = document.getElementById('amountUsd');
    const paymentTokenSelect = document.getElementById('paymentToken');
    const errorMessageDiv = document.getElementById('errorMessage');
    const submitBillBtn = document.getElementById('submitBillBtn');
    const payBillBtn = document.getElementById('payBillBtn');
    const darkModeToggle = document.getElementById('darkModeToggle');
    const checkApiKeyBtn = document.getElementById('checkApiKeyBtn');
    const apiKeyStatusText = document.getElementById('apiKeyStatusText');
    const apiKeyStatusDiv = document.getElementById('apiKeyStatus');

    let csrfToken = '';

    console.log('Initializing application');

    // Fetch CSRF token
    fetch('/api/get_csrf_token')
        .then(response => response.json())
        .then(data => {
            csrfToken = data.csrf_token;
            console.log('CSRF token fetched successfully');
        })
        .catch(error => {
            console.error('Error fetching CSRF token:', error);
            displayErrorMessage('Failed to initialize application. Please refresh the page.');
        });

    // Dark mode toggle
    darkModeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        console.log('Dark mode toggled');
    });

    // Check API Key
    checkApiKeyBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/check_api_key');
            const data = await response.json();
            apiKeyStatusText.textContent = data.status;
            apiKeyStatusDiv.className = `mb-4 p-4 rounded-lg ${data.status === 'valid' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`;
            alert(data.message);
        } catch (error) {
            console.error('Error checking API key:', error);
            displayErrorMessage('Failed to check API key status. Please try again.');
        }
    });

    // Form validation
    const formInputs = billForm.querySelectorAll('input, select');
    formInputs.forEach(input => {
        input.addEventListener('input', validateInput);
    });

    function validateInput(event) {
        const input = event.target;
        if (input.validity.valid) {
            input.classList.remove('border-red-500');
            input.classList.add('border-green-500');
        } else {
            input.classList.remove('border-green-500');
            input.classList.add('border-red-500');
        }
    }

    // Add event listeners
    submitBillBtn.addEventListener('click', submitBill);
    payBillBtn.addEventListener('click', payBill);

    // Fetch analytics data
    fetchAnalytics();

    async function submitBill() {
        console.log('Submit bill button clicked');
        if (!billForm.checkValidity()) {
            billForm.reportValidity();
            console.log('Form validation failed');
            return;
        }

        const formData = {
            patientId: document.getElementById('patientId').value,
            date: document.getElementById('date').value,
            visitType: document.getElementById('visitType').value,
            diagnosis: document.getElementById('diagnosis').value,
            amountUsd: amountUsdInput.value,
            paymentToken: paymentTokenSelect.value
        };

        console.log('Submitting bill:', formData);
        showLoading(submitBillBtn);

        try {
            console.log('Sending POST request to /api/submit_bill');
            const response = await fetch('/api/submit_bill', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(formData),
            });

            console.log('Received response from /api/submit_bill');
            const result = await response.json();

            if (response.ok) {
                console.log('Bill submitted successfully:', result);
                alert('Bill submitted successfully! Redirecting to payment page.');
                window.location.href = result.charge_url;
            } else {
                console.error('Error submitting bill:', result);
                displayErrorMessage(`Error submitting bill: ${result.error}`);
            }
        } catch (error) {
            console.error('Error submitting bill:', error);
            displayErrorMessage('Error submitting bill. Please try again.');
        } finally {
            hideLoading(submitBillBtn);
        }
    }

    function payBill() {
        console.log('Pay bill function called');
        // Implement pay bill functionality
    }

    function fetchAnalytics() {
        console.log('Fetching analytics');
        // Implement analytics fetching
    }

    function displayErrorMessage(message) {
        console.error('Displaying error message:', message);
        errorMessageDiv.textContent = message;
        errorMessageDiv.classList.remove('hidden');
    }

    function clearErrorMessage() {
        console.log('Clearing error message');
        errorMessageDiv.textContent = '';
        errorMessageDiv.classList.add('hidden');
    }

    function showLoading(element) {
        console.log('Showing loading state for element:', element);
        element.classList.add('opacity-50', 'cursor-not-allowed');
        element.disabled = true;
    }

    function hideLoading(element) {
        console.log('Hiding loading state for element:', element);
        element.classList.remove('opacity-50', 'cursor-not-allowed');
        element.disabled = false;
    }
});
