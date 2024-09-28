let refreshTimeout = null;

async function refreshTokenRequest() {
    const response = await fetch('/auth/refresh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    });

    const data = await response.json();

    if (response.ok) {
        const expiresIn = data.expires_in;
        sessionStorage.setItem('expires', data.expires_in);

        setupAutoRefresh(expiresIn);
    } else {
        sessionStorage.clear();
        window.location.href = '/auth/login';
    }
}

function setupAutoRefresh(expiresIn) {
    const refreshTime = (expiresIn - 30) * 1000;

    if (refreshTimeout) {
        clearTimeout(refreshTimeout);
    }

    refreshTimeout = setTimeout(() => {
        refreshTokenRequest();
    }, refreshTime);
}

function initialize() {
    expiresIn = sessionStorage.getItem('expires');
    if (expiresIn) {
        setupAutoRefresh(Number(expiresIn));
    }
}

window.onload = initialize;


document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('logout')) {
        alert('Zostałeś wylogowany!');
    }
});
