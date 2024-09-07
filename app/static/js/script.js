async function fetchText() {
    const textarea = document.getElementById('textArea');
    const text = textarea.value;

    try {
        const response = await fetch('/quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'text': text
            })
        });

        if (response.ok) {
            window.location.href = '/quiz';
        } else {
            alert('Something went wrong!');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}