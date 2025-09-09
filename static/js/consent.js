// Cookie Consent Script
document.addEventListener('DOMContentLoaded', function() {
    const consentBanner = document.getElementById('cookie-consent-banner');
    const acceptBtn = document.getElementById('accept-cookies');
    const declineBtn = document.getElementById('decline-cookies');

    // Check if consent already given
    if (!localStorage.getItem('cookieConsent')) {
        consentBanner.style.display = 'block';
    }

    acceptBtn.addEventListener('click', function() {
        localStorage.setItem('cookieConsent', 'accepted');
        consentBanner.style.display = 'none';
        // Enable analytics or other cookies here
    });

    declineBtn.addEventListener('click', function() {
        localStorage.setItem('cookieConsent', 'declined');
        consentBanner.style.display = 'none';
        // Disable non-essential cookies
    });
});
