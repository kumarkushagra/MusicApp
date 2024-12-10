document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('songRequestForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Form submitted');  // Log to confirm the form is submitted

        const url = document.getElementById('songUrl').value;
        console.log('URL:', url);  // Log the URL to check if it is being captured correctly

        const responseMessage = document.getElementById('responseMessage');
        
        try {
            const response = await fetch('/song-request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            if (response.ok) {
                responseMessage.textContent = 'Song requested successfully!';
                responseMessage.classList.add('success');
                responseMessage.classList.remove('error');
            } else {
                throw new Error('Failed to request song');
            }
        } catch (error) {
            console.error('Error:', error);  // Log the error to the console
            responseMessage.textContent = 'Error: ' + error.message;
            responseMessage.classList.add('error');
            responseMessage.classList.remove('success');
        }
    });
});
