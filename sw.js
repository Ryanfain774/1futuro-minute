// Service worker: deja la página usable sin conexión después de la primera carga.
// Estrategia "red primero": si hay internet trae la versión nueva y la guarda;
// si no hay, sirve la última copia guardada.
const CACHE = "minute-launcher-v1";
const PRECACHE = ["./", "./index.html"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  // Solo cacheamos la página y las fuentes; el resto pasa directo.
  const isPage = url.origin === location.origin;
  const isFont = url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com";
  if (!isPage && !isFont) return;
  // La página se guarda sin la query (?t=...) para que cualquier configuración funcione sin conexión.
  const key = isPage && (url.pathname.endsWith("/") || url.pathname.endsWith("/index.html")) ? new Request(url.origin + url.pathname) : req;
  e.respondWith(
    fetch(req).then(res => {
      if (res && res.ok) caches.open(CACHE).then(c => c.put(key, res.clone()));
      return res;
    }).catch(() => caches.match(key).then(hit => hit || caches.match("./index.html")))
  );
});
