/**
 * Open all external links in new tabs.
 * Works with MkDocs Material instant navigation.
 */
(function () {
  function openExternalLinksInNewTab() {
    document.querySelectorAll("a[href]").forEach(function (link) {
      if (
        link.hostname &&
        link.hostname !== window.location.hostname &&
        !link.hasAttribute("target")
      ) {
        link.setAttribute("target", "_blank");
        link.setAttribute("rel", "noopener");
      }
    });
  }

  // Initial page load
  document.addEventListener("DOMContentLoaded", openExternalLinksInNewTab);

  // MkDocs Material instant navigation
  if (typeof document$ !== "undefined") {
    document$.subscribe(openExternalLinksInNewTab);
  }
})();
