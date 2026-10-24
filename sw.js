// Destination Atlas — Lightweight Offline Cache Service Worker
const CACHE_NAME = "destination-atlas-v2026-10";
const CORE_ASSETS = [
  "./",
  "./index.html",
  "./beaches.html",
  "./aquariums.html",
  "./zoos.html",
  "./museums.html",
  "./themeparks.html",
  "./ski.html",
  "./shows.html",
  "./shared_widgets.js",
  "./data.js",
  "./data_part2.js",
  "./data_aquariums_zoos_museums.js",
  "./data_themeparks.js",
  "./data_ski.js",
  "./data_shows.js",
  "./geo.js",
  "./cities.js"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request)
      .then((res) => {
        if (res && res.status === 200 && event.request.url.startsWith(self.location.origin)) {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return res;
      })
      .catch(() => caches.match(event.request))
  );
});
