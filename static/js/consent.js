// Script aprimorado para consentimento de cookies
document.addEventListener('DOMContentLoaded', function() {
    const banner = document.getElementById('cookie-consent-banner');
    const acceptButton = document.getElementById('accept-cookies');
    const declineButton = document.getElementById('decline-cookies');
    
    // Verificar se o usuário já tomou uma decisão sobre os cookies
    const consentGiven = localStorage.getItem('cookieConsent');
    
    if (consentGiven) {
        banner.style.display = 'none';
        // Se aceitou, habilitar tracking
        if (consentGiven === 'accepted') {
            enableTracking();
        }
    } else {
        banner.style.display = 'block';
    }
    
    if (acceptButton) {
        acceptButton.addEventListener('click', function() {
            localStorage.setItem('cookieConsent', 'accepted');
            banner.style.display = 'none';
            enableTracking();
        });
    }
    
    if (declineButton) {
        declineButton.addEventListener('click', function() {
            localStorage.setItem('cookieConsent', 'declined');
            banner.style.display = 'none';
            disableTracking();
        });
    }
    
    function enableTracking() {
        // Aqui você pode habilitar scripts de tracking adicionais
        console.log('Tracking habilitado');
        
        // Registrar consentimento no backend (opcional)
        if (typeof visitId !== 'undefined' && visitId !== null) {
            // Você pode enviar uma requisição para registrar o consentimento
        }
    }
    
    function disableTracking() {
        // Desabilitar tracking (remover listeners, etc.)
        console.log('Tracking desabilitado');
        
        // Limpar dados de tracking se necessário
        // Note que isso deve ser feito de acordo com as leis de privacidade aplicáveis
    }
});

// Função para verificar se o consentimento foi dado
function hasConsent() {
    return localStorage.getItem('cookieConsent') === 'accepted';
}

// Função para solicitar consentimento (se necessário)
function requestConsent() {
    const banner = document.getElementById('cookie-consent-banner');
    if (banner) {
        banner.style.display = 'block';
    }
}