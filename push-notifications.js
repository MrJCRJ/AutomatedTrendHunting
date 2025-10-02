// TrendHunter Push Notifications
// ===============================

class TrendHunterNotifications {
  constructor() {
    this.publicKey = 'YOUR_VAPID_PUBLIC_KEY_HERE';
    this.isSupported = 'serviceWorker' in navigator && 'PushManager' in window;
    this.isSubscribed = false;

    console.log('🔔 TrendHunter Notifications inicializadas');

    if (this.isSupported) {
      this.init();
    }
  }

  async init() {
    try {
      // Registra Service Worker
      const registration = await navigator.serviceWorker.register('/sw.js');
      console.log('✅ Service Worker registrado');

      // Verifica se já está inscrito
      const subscription = await registration.pushManager.getSubscription();
      this.isSubscribed = !(subscription === null);

      this.updateUI();

    } catch (error) {
      console.error('❌ Erro ao inicializar notificações:', error);
    }
  }

  async subscribe() {
    try {
      const registration = await navigator.serviceWorker.ready;

      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlBase64ToUint8Array(this.publicKey)
      });

      console.log('✅ Usuário inscrito para notificações');
      this.isSubscribed = true;

      // Envia subscription para o servidor
      await this.sendSubscriptionToServer(subscription);

      this.updateUI();
      this.showWelcomeNotification();

      return subscription;

    } catch (error) {
      console.error('❌ Erro ao inscrever:', error);

      if (Notification.permission === 'denied') {
        alert('❌ Notificações bloqueadas. Ative nas configurações do navegador.');
      }
    }
  }

  async unsubscribe() {
    try {
      const registration = await navigator.serviceWorker.ready;
      const subscription = await registration.pushManager.getSubscription();

      if (subscription) {
        await subscription.unsubscribe();
        console.log('✅ Usuário desinscrito');
        this.isSubscribed = false;
        this.updateUI();

        // Remove do servidor
        await this.removeSubscriptionFromServer(subscription);
      }

    } catch (error) {
      console.error('❌ Erro ao desinscrever:', error);
    }
  }

  async sendSubscriptionToServer(subscription) {
    // Envia subscription para seu backend
    try {
      const response = await fetch('/api/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          subscription: subscription,
          timestamp: new Date().toISOString(),
          source: 'trendhunter'
        })
      });

      if (response.ok) {
        console.log('✅ Subscription enviada para servidor');
      }

    } catch (error) {
      console.log('⚠️ Servidor offline, salvando localmente');
      // Salva localmente se servidor estiver offline
      localStorage.setItem('pendingSubscription', JSON.stringify({
        subscription: subscription,
        timestamp: new Date().toISOString()
      }));
    }
  }

  async removeSubscriptionFromServer(subscription) {
    try {
      await fetch('/api/unsubscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          subscription: subscription
        })
      });

    } catch (error) {
      console.log('⚠️ Erro ao remover do servidor:', error);
    }
  }

  updateUI() {
    const button = document.getElementById('notification-button');
    const status = document.getElementById('notification-status');

    if (!button) return;

    if (!this.isSupported) {
      button.textContent = 'Notificações não suportadas';
      button.disabled = true;
      return;
    }

    if (this.isSubscribed) {
      button.textContent = '🔕 Desativar Alertas';
      button.onclick = () => this.unsubscribe();
      if (status) status.textContent = '✅ Alertas ativados';
    } else {
      button.textContent = '🔔 Ativar Alertas';
      button.onclick = () => this.subscribe();
      if (status) status.textContent = '🔕 Alertas desativados';
    }
  }

  showWelcomeNotification() {
    if (Notification.permission === 'granted') {
      navigator.serviceWorker.ready.then(registration => {
        registration.showNotification('🔥 TrendHunter', {
          body: 'Alertas ativados! Você receberá as tendências mais quentes.',
          icon: '/icon-192.png',
          badge: '/badge-72.png',
          tag: 'welcome',
          actions: [
            {
              action: 'open',
              title: 'Ver Tendências'
            }
          ]
        });
      });
    }
  }

  // Função utilitária para converter chave VAPID
  urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  // Método para testar notificação
  async testNotification() {
    if (Notification.permission === 'granted') {
      navigator.serviceWorker.ready.then(registration => {
        registration.showNotification('🧪 Teste TrendHunter', {
          body: 'Esta é uma notificação de teste. Sistema funcionando! 🚀',
          icon: '/icon-192.png',
          tag: 'test'
        });
      });
    }
  }
}

// Inicializa quando a página carrega
document.addEventListener('DOMContentLoaded', () => {
  window.trendHunterNotifications = new TrendHunterNotifications();
});

// Exporta para uso global
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TrendHunterNotifications;
}