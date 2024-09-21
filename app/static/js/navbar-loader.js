function loadNavbar() {
    const navbarContainer = document.getElementById('navbar');
    
    fetch('/static/html/navbar.html')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error loading navbar.html');
            }
            return response.text();
        })
        .then(data => {
            navbarContainer.innerHTML = data;

            const isLoggedIn = checkIfLoggedIn();

            if (isLoggedIn) {
                document.getElementById('navbar-user').style.display = 'block';
            } else {
                document.getElementById('navbar-guest').style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Problem loading the navigation', error);
        });
}


function checkIfLoggedIn() {
    const accessToken = localStorage.getItem('token');
    return accessToken !== null;
}

document.addEventListener('DOMContentLoaded', loadNavbar);
