async function fetchText() {
    const textarea = document.getElementById('textArea');
    const text = textarea.value;
    const token = sessionStorage.getItem('actoken') || '';

    try {
        const response = await fetch('/quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`
            },
            body: new URLSearchParams({
                'text': text
            })
        });

        if (response.ok) {
            const pageContent = await response.text();
            const mainContent = document.getElementById('main-content');
            if (mainContent) {
                mainContent.innerHTML = pageContent;
            }
            loadExternalScripts();
        } else {
            alert('Something went wrong!');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


function loadExternalScripts() {
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js";
    document.head.appendChild(script);
}


async function validateForm(event) {
    event.preventDefault();

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

    const token = sessionStorage.getItem('actoken') || '';
    const form = document.getElementById('form-quiz');
    const formData = new FormData(form);

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const pageContent = await response.text();
            const mainContent = document.getElementById('main-content');
            if (mainContent) {
                mainContent.innerHTML = pageContent;
            }
            loadExternalScripts();
        } else {
            alert('Something went wrong!');
        }
    } catch (error) {
        console.error('Error:', error);
    }
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
        const response = await fetch('/users', {
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
            window.location.href = '/'
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
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: userData
        });

        const result = await response.json();

        if (response.ok) {
            sessionStorage.setItem('actoken', result.access_token);
            sessionStorage.setItem('expires', result.expires_in);
            document.getElementById('message').innerHTML = `<p class="success">Logowanie udane!</p>`;
            window.location.href = '/'
        } else {
            document.getElementById('message').innerHTML = `<p class="error">Wystąpił błąd: ${result.detail}</p>`;
        }
    } catch (error) {
        document.getElementById('message').innerHTML = `<p class="error">Wystąpił błąd: ${error.message}</p>`;
    }
};
