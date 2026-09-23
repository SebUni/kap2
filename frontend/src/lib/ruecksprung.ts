// Prüft ein Rücksprungziel nach der Anmeldung: nur interne, einfache Pfade werden akzeptiert.
// Siehe T-0560 (Anschluss an T-0502): RequireAuth.tsx gibt location.pathname als state.from an
// die Anmeldeseite; LoginPage.tsx darf diesen Wert nicht ungeprüft an navigate() weitergeben.
export const RUECKSPRUNG_MUSTER = /^\/(?![\/\\])[^\\\u0000-\u001f]*$/

export function sicheresRuecksprungziel(ziel: unknown): string | null {
  if (typeof ziel !== 'string') return null
  return RUECKSPRUNG_MUSTER.test(ziel) ? ziel : null
}
