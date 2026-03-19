// Reset the announcement dismiss state once per browser session.
// MkDocs Material stores dismiss in localStorage (permanent).
// We clear it on the first page load of each session so the
// disclaimer reappears when the user returns after closing the browser,
// but stays dismissed for the rest of the current session.
(function () {
  if (!sessionStorage.getItem("_announce_seen")) {
    localStorage.removeItem("__md_announce");
    sessionStorage.setItem("_announce_seen", "1");
  }
})();
