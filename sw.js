// Service Worker para Push Notifications
// =====================================

const CACHE_NAME = 'trendhunter-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/push-notifications.js'
];

// Instala o Service Worker
self.addEventListener('install', event => {
    console.log('🔧 Service Worker instalando...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('📦 Cache aberto');
                return cache.addAll(urlsToCache);
            })
    );
});

// Ativa o Service Worker
self.addEventListener('activate', event => {
    console.log('✅ Service Worker ativado');
    
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('🗑️ Removendo cache antigo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Intercepta requisições (cache)
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Retorna do cache se encontrar
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }
        )
    );
});

// Recebe Push Notifications
self.addEventListener('push', event => {
    console.log('🔔 Push recebido');
    
    let data = {
        title: '🔥 TrendHunter',
        body: 'Nova tendência identificada!',
        icon: '/icon-192.png',
        badge: '/badge-72.png',
        tag: 'trend-alert',
        data: {
            url: '/'
        }
    };
    
    // Parse dos dados se enviados
    if (event.data) {
        try {
            const pushData = event.data.json();
            data = { ...data, ...pushData };
        } catch (e) {
            console.log('Dados de push em formato texto:', event.data.text());
            data.body = event.data.text();
        }
    }
    
    const options = {
        body: data.body,
        icon: data.icon,
        badge: data.badge,
        tag: data.tag,
        data: data.data,
        actions: [
            {
                action: 'open',
                title: '📈 Ver Tendência'
            },
            {
                action: 'close',
                title: '❌ Fechar'
            }
        ],
        requireInteraction: true
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// Clique na notificação
self.addEventListener('notificationclick', event => {
    console.log('👆 Notificação clicada:', event);
    
    event.notification.close();
    
    const action = event.action;
    const data = event.notification.data;
    
    if (action === 'open' || !action) {
        // Abre ou foca na aba do TrendHunter
        event.waitUntil(
            clients.matchAll({ type: 'window' }).then(clientList => {
                // Procura por uma aba já aberta
                for (let client of clientList) {
                    if (client.url.includes('trendhunter') && 'focus' in client) {
                        return client.focus();
                    }
                }
                
                // Se não encontrou, abre nova aba
                if (clients.openWindow) {
                    return clients.openWindow(data?.url || '/');
                }
            })
        );
    }
    
    // Analytics de clique (opcional)
    if ('gtag' in self) {
        gtag('event', 'notification_click', {
            'notification_tag': event.notification.tag,
            'action': action || 'open'
        });
    }
});

// Fecha notificação
self.addEventListener('notificationclose', event => {
    console.log('❌ Notificação fechada:', event);
    
    // Analytics de fechamento (opcional)
    if ('gtag' in self) {
        gtag('event', 'notification_close', {
            'notification_tag': event.notification.tag
        });
    }
});