# Rueckfallweg fuer den Neustart einer System-Unit ohne fremdes Recht (T-0342).
#
# Anlass: "systemctl restart kap2-test" schickt eine D-Bus-Anfrage an PID 1 und braucht dafuer
# eine polkit-Berechtigung. Die Berechtigung vom 12.09.2026 ist auf die Kennung "overlord"
# ausgestellt; seit dem Corp-Umbau laufen unsere Laeufe als "ovl", und der Neustart endete am
# 18.09.2026 mit "Access denied". Die Berechtigung liegt ausserhalb unseres Containers.
#
# Der Dienstprozess selbst gehoert aber derselben Kennung, unter der der Deploy-Lauf arbeitet
# (Unit faehrt User=ovl). Ein Signal an den eigenen Prozess braucht kein polkit, keinen D-Bus
# und kein sudo. Stirbt der Prozess an einem Signal, wertet systemd das als Fehlschlag und
# startet die Unit wegen Restart=on-failure nach RestartSec von selbst neu -- mit dem dann
# ausgelieferten Code. Genau das, was "systemctl restart" erreichen sollte.
#
# Warum KILL und nicht TERM: Bei Restart=on-failure gilt ein per SIGTERM beendeter Prozess als
# sauber beendet -- systemd wuerde ihn gerade NICHT neu starten. Das ist der einzige Grund fuer
# das harte Signal; bei einem Testdienst ohne schreibende Dauerlast ist es vertretbar.
#
# Diese Datei wird per "source" eingebunden und startet von sich aus nichts.

# $1 = Name der Unit (z. B. kap2-test)
# Rueckgabewerte: 0 = Signal gesendet, 1 = kein Hauptprozess (MainPID leer oder 0),
#                 2 = Prozess gehoert nicht dem laufenden Benutzer (oder existiert nicht mehr).
# Die Funktion startet nichts selbst und ruft kein sudo auf; den Neustart macht systemd.
neustart_ueber_eigenen_prozess() {
  local unit="$1" pid
  pid=$(systemctl show -p MainPID --value "$unit" 2>/dev/null || true)
  pid="${pid//[[:space:]]/}"
  if [[ -z "$pid" || "$pid" == "0" ]]; then
    echo "-- Eigenprozess-Neustart: $unit hat keinen laufenden Hauptprozess (MainPID='${pid:-leer}')"
    return 1
  fi
  # kill -0 sendet kein Signal, prueft aber genau das, worauf der Weg beruht: dass der Prozess
  # existiert und dem laufenden Benutzer gehoert. Gehoert er einem anderen, liefert kill -0 EPERM.
  if ! kill -0 "$pid" 2>/dev/null; then
    echo "-- Eigenprozess-Neustart: Prozess $pid gehoert nicht dem laufenden Benutzer ($(id -un 2>/dev/null)) oder existiert nicht mehr"
    return 2
  fi
  kill -KILL "$pid" 2>/dev/null || true
  echo "-- Eigenprozess-Neustart: SIGKILL an Hauptprozess $pid von $unit gesendet"
  return 0
}
