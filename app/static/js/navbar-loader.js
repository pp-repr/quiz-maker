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

            fetch('/users/me', {
                method: 'GET',
                credentials: 'include'
            })
            .then(response => {
                if (response.ok) {
                    document.getElementById('navbar-user').style.display = 'block';
                } else if (response.status === 401) {
                    document.getElementById('navbar-guest').style.display = 'block';
                } else {
                    throw new Error('Unexpected response status: ' + response.status);
                }
            })
            .catch(error => {
                console.error('Error checking login status:', error);
                document.getElementById('navbar-guest').style.display = 'block';
            });
        })
        .catch(error => {
            console.error('Problem loading the navigation', error);
        });
}

document.addEventListener('DOMContentLoaded', loadNavbar);
