// Script básico para consentimento de cookies
document.addEventListener('DOMContentLoaded', function() {
    const banner = document.getElementById('cookie-consent-banner');
    const acceptButton = document.getElementById('accept-cookies');
    const declineButton = document.getElementById('decline-cookies');
    
    // Verificar se o usuário já tomou uma decisão sobre os cookies
    const consentGiven = localStorage.getItem('cookieConsent');
    
    if (!consentGiven) {
        banner.style.display = 'block';
    }
    
    acceptButton.addEventListener('click', function() {
        localStorage.setItem('cookieConsent', 'accepted');
        banner.style.display = 'none';
    });
    
    declineButton.addEventListener('click', function() {
        localStorage.setItem('cookieConsent', 'declined');
        banner.style.display = 'none';
    });
});