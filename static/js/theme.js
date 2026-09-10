(() => {
  'use strict'

  const storageKey = 'theme'

  const getStoredTheme = () => localStorage.getItem(storageKey)
  const setStoredTheme = theme => localStorage.setItem(storageKey, theme)

  const autoThemeToBootstrap = () => window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
      return storedTheme
    }

    return autoThemeToBootstrap()
  }

  const setTheme = theme => {
    document.documentElement.setAttribute("data-theme", theme);
    if (theme === 'auto') {
      document.documentElement.setAttribute('data-bs-theme', autoThemeToBootstrap())
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme)
    }
  }

  const updateTheme = (theme) => {
    setStoredTheme(theme)
    setTheme(theme)
  }

  setTheme(getPreferredTheme())

  function cycleTheme() {
    const currentTheme = getStoredTheme() || "auto";
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)",
    ).matches;

    if (prefersDark) {
      // Auto (dark) -> Light -> Dark
      if (currentTheme === "auto") {
        updateTheme("light");
      } else if (currentTheme === "light") {
        updateTheme("dark");
      } else {
        updateTheme("auto");
      }
    } else {
      // Auto (light) -> Dark -> Light
      if (currentTheme === "auto") {
        updateTheme("dark");
      } else if (currentTheme === "dark") {
        updateTheme("light");
      } else {
        updateTheme("auto");
      }
    }
  }

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme()
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
      setTheme(getPreferredTheme())
    }
  })

  window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.theme-toggle')
      .forEach(
        toggle => toggle.addEventListener('click', cycleTheme)
      )
  })
})()
