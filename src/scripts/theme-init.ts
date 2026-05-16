/**
 * Inline blocking script that resolves the active color theme before first
 * paint. Three sources, in order of precedence:
 *   1. `localStorage.theme` set explicitly by the user via the toggle.
 *   2. `prefers-color-scheme` from the OS / browser.
 *   3. Fallback to dark.
 *
 * The toggle (ThemeToggle.astro) stores one of 'light' | 'dark' | 'system'.
 * 'system' means "follow OS" → no localStorage entry is kept; the script
 * always falls back to the OS preference for this case.
 */
export const themeInitScript = `(()=>{try{var s=localStorage.getItem('theme');var t;if(s==='light'||s==='dark'){t=s;}else{t=matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';}document.documentElement.setAttribute('data-theme',t);}catch(e){document.documentElement.setAttribute('data-theme','dark');}})();`;
