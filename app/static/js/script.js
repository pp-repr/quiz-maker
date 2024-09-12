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


function validateForm() {
    const questions = document.querySelectorAll('.section input[type="radio"]');
    const answeredQuestions = new Set();
    const totalQuestions = new Set([...questions].map(q => q.name)).size;
    
    questions.forEach((radio) => {
        if (radio.checked) {
            answeredQuestions.add(radio.name);
        }
    });
    if (answeredQuestions.size < totalQuestions) {
        alert("Proszę odpowiedzieć na wszystkie pytania przed wysłaniem.");
        return false;
    }
    return true;
}


function toggleDetails(key) {
    var details = document.getElementById('details-' + key);
    if (details.classList.contains('show')) {
        details.classList.remove('show');
    } else {
        details.classList.add('show');
    }
}