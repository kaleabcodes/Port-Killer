import psutil
import threading
from gi.repository import GLib

def get_active_ports():
    """
    Returns a list of dicts representing active listening ports.
    """
    try:
        connections = psutil.net_connections(kind="inet")
    except psutil.AccessDenied:
        raise PermissionError("Run with elevated privileges to see all ports")

    ports = []
    seen = set()
    for conn in connections:
        if conn.status != "LISTEN" or conn.pid is None:
            continue
        key = (conn.pid, conn.laddr.port)
        if key in seen:
            continue
        seen.add(key)
        
        try:
            name = psutil.Process(conn.pid).name()
        except Exception:
            name = "Unknown"
            
        ports.append({
            "pid": conn.pid,
            "name": name,
            "ip": conn.laddr.ip,
            "port": conn.laddr.port,
            "status": conn.status
        })
    return ports

def kill_process(pid, success_cb, already_dead_cb, error_cb):
    """
    Kills a process by PID. Calls the appropriate callback on GLib idle.
    """
    def _kill():
        try:
            p = psutil.Process(pid)
            p.terminate()
            try:
                p.wait(timeout=3)
            except psutil.TimeoutExpired:
                p.kill()
            GLib.idle_add(success_cb)
        except psutil.NoSuchProcess:
            GLib.idle_add(already_dead_cb)
        except Exception as e:
            GLib.idle_add(error_cb, str(e))

    threading.Thread(target=_kill, daemon=True).start()
