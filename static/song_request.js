document.getElementById('songRequestForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = document.getElementById('songUrl').value;
    const responseMessage = document.getElementById('responseMessage');

    try {
        const response = await fetch('/request-song', {
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
        responseMessage.textContent = 'Error: ' + error.message;
        responseMessage.classList.add('error');
        responseMessage.classList.remove('success');
    }
});