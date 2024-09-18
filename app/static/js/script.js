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


async function registerUser(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const userData = new URLSearchParams({
        name: name,
        email: email,
        password: password
    });

    try {
        const response = await fetch('http://localhost:8000/users', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: userData
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('message').innerHTML = `<p class="success">Rejestracja udana! Witaj, ${result.name}.</p>`;
        } else {
            document.getElementById('message').innerHTML = `<p class="error">Wystąpił błąd: ${result.detail}</p>`;
        }
    } catch (error) {
        document.getElementById('message').innerHTML = `<p class="error">Wystąpił błąd: ${error.message}</p>`;
    }
};

async function loginUser(event) {
    event.preventDefault();
    
    const username = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const userData = new URLSearchParams({
        username: username,
        password: password
    });

    try {
        const response = await fetch('http://localhost:8000/auth/login', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: userData
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('message').innerHTML = `<p class="success">Logowanie udane!</p>`;
        } else {
            document.getElementById('message').innerHTML = `<p class="error">Wystąpił błąd: ${result.detail}</p>`;
        }
    } catch (error) {
        document.getElementById('message').innerHTML = `<p class="error">Wystąpił błąd: ${error.message}</p>`;
    }
};
