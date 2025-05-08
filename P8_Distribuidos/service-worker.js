// Nombre de la caché
const CACHE_NAME = 'pwa8-v1';

// Archivos a cachear
const urlsToCache = [
  './',
  './index.html',
  './CalcBinaria.php',
  './cifradocesar.php',
  './subnet.php',
  './manifest.json'
  // Agrega aquí cualquier archivo CSS, JS o imágenes que uses
];

// Instalación del Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache abierta');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activación del Service Worker
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Estrategia de caché: Cache con network fallback
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Devuelve la respuesta cacheada si está disponible
        if (response) {
          return response;
        }
        
        // Si no está en caché, hacemos un fetch a la red
        return fetch(event.request)
          .then(response => {
            // Si la respuesta no es válida, devolvemos la respuesta original
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // Clonamos la respuesta para poder ponerla en caché y devolverla
            const responseToCache = response.clone();
            
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
              
            return response;
          })
          .catch(() => {
            // Si falla el fetch, podemos devolver una página de fallback
            if (event.request.mode === 'navigate') {
              return caches.match('./offline.html');
            }
          });
      })
  );
});