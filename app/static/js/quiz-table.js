function handleKeyPress(event, id) {
    if (event.key === 'Enter') {
        saveQuizName(id);
    }
}

function saveQuizName(id) {
    const quizNameInput = document.getElementById(`quiz_name_${id}`);
    const quizName = quizNameInput.value;

    const dataToSend = new URLSearchParams({
        id: id,
        quiz_name: quizName
    });

    fetch('/users/me/quizzes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: dataToSend
    })
    .then(response => {
        if (response.ok) {
            console.log('Quiz został zaktualizowany!');
        } else {
            console.log('Błąd podczas zapisu.');
        }
    })
    .catch(error => {
        console.error('Wystąpił błąd:', error);
    });
}

function startQuiz(id) {
    alert(`Rozpocznij test dla quizu o ID: ${id}`);
    // Tutaj możesz dodać dodatkową logikę np. przekierowanie do strony z testem
    // window.location.href = `/quiz/${id}/start`;
}