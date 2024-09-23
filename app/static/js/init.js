async function refreshTokenRequest() {
    refreshToken = sessionStorage.getItem('retoken');
    const response = await fetch('/auth/refresh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'refresh-token': refreshToken
        },
        body: JSON.stringify({})
    });

    const data = await response.json();

    if (response.ok) {
        sessionStorage.setItem('actoken', data.access_token);
        sessionStorage.setItem('retoken', data.refresh_token);
        sessionStorage.setItem('expires', data.expires_in);

        setupAutoRefresh(expiresIn);
    } else {
        sessionStorage.clear();
        window.location.href = '/auth/login';
    }
}

function setupAutoRefresh(expiresIn) {
    const refreshTime = (expiresIn - 30) * 1000;

    setTimeout(() => {
        refreshTokenRequest();
    }, refreshTime);
}

function initialize() {
    accessToken = sessionStorage.getItem('actoken');
    refreshToken = sessionStorage.getItem('retoken');
    expiresIn = sessionStorage.getItem('expires');

    if (accessToken && refreshToken && expiresIn) {
        setupAutoRefresh(expiresIn);
    } else {
        document.getElementById('status').innerText = "Token status: Not logged in";
        window.location.href = '/auth/login';
    }
}

window.onload = initialize;