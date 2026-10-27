"""Entorno de ejecución para LibreOffice (soffice) en modo headless.

Versión FUSIONADA (skill ofimatica, fase F2): combina los dos helpers que
existían por separado en las skills originales:

1. De `ofimatica/scripts/office/soffice.py`: garantiza un HOME/USERPROFILE
   escribible (libreoffice necesita crear su perfil UserInstallation; en
   sandboxes/CI o perfiles temporales de Windows puede faltar o no ser
   escribible y soffice falla sin mensaje claro).
2. De `xlsx/scripts/office/soffice.py`: `SAL_USE_VCLPLUGIN=svp` (headless sin
   display) y shim LD_PRELOAD con fallback a socketpair() para entornos Linux
   donde los sockets AF_UNIX están bloqueados (VMs sandboxeadas), más el
  helper `run_soffice()`.

Uso:
    from office.soffice import get_soffice_env, run_soffice, find_soffice

    # Opción 1 – ejecutar soffice directamente
    result = run_soffice(["--headless", "--convert-to", "pdf", "input.docx"])

    # Opción 2 – obtener env para tus propios subprocess.run()
    env = get_soffice_env()
    subprocess.run([find_soffice(), ...], env=env)
"""

import os
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

# Variables que definen el directorio del perfil de usuario según la plataforma.
_HOME_VARS = ["USERPROFILE"] if sys.platform == "win32" else ["HOME"]

# El shim AF_UNIX solo aplica en Unix (Linux/macOS): en Windows socket.AF_UNIX
# no existe, así que se omite por completo (el original de xlsx craschaba con
# AttributeError al llamarlo en Windows).
_UNIX_SHIM_POSSIBLE = hasattr(socket, "AF_UNIX")

# Rutas de instalación conocidas cuando `soffice` no está en PATH (p. ej.
# Windows donde el instalador no siempre añade PATH). Misma lista que
# scripts/convert.py para mantener comportamiento consistente en la skill.
_SOFFICE_CANDIDATES = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/usr/bin/soffice",
    "/usr/local/bin/soffice",
    "/opt/libreoffice/program/soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
]


def find_soffice() -> str:
    """Resuelve el binario soffice: PATH primero, luego rutas de instalación.

    Devuelve "soffice" como último recurso para que subprocess produzca el
    error habitual (FileNotFoundError) en lugar de un camino raro inexistente.
    """
    for name in ("soffice", "soffice.exe", "libreoffice", "libreoffice.exe"):
        found = shutil.which(name)
        if found:
            return found
    for candidate in _SOFFICE_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    return "soffice"


def get_soffice_env() -> dict:
    """Copia de os.environ lista para invocar soffice: perfil escribible,
    VCL headless (svp) y shim AF_UNIX si hace falta (solo Unix)."""
    env = os.environ.copy()
    env[_HOME_VARS[0]] = _writable_home()
    env["SAL_USE_VCLPLUGIN"] = "svp"  # sin display en Linux/macOS; inocuo en Windows
    if _UNIX_SHIM_POSSIBLE and _needs_shim():
        env["LD_PRELOAD"] = str(_ensure_shim())
    return env


def run_soffice(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Ejecuta soffice (binario resuelto con find_soffice()) con get_soffice_env()."""
    env = get_soffice_env()
    return subprocess.run([find_soffice()] + args, env=env, **kwargs)


def _writable_home() -> str:
    for var in _HOME_VARS:
        value = os.environ.get(var)
        if value and _is_writable_dir(value):
            return value
    fallback = Path(tempfile.gettempdir()) / "soffice-home"
    fallback.mkdir(parents=True, exist_ok=True)
    return str(fallback)


def _is_writable_dir(path: str) -> bool:
    try:
        return Path(path).is_dir() and os.access(path, os.W_OK)
    except OSError:
        return False


_SHIM_SO = Path(tempfile.gettempdir()) / "lo_socket_shim.so"


def _needs_shim() -> bool:
    if not _UNIX_SHIM_POSSIBLE:
        return False
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.close()
        return False
    except OSError:
        return True


def _ensure_shim() -> Path:
    if _SHIM_SO.exists():
        return _SHIM_SO

    src = Path(tempfile.gettempdir()) / "lo_socket_shim.c"
    src.write_text(_SHIM_SOURCE)
    subprocess.run(
        ["gcc", "-shared", "-fPIC", "-o", str(_SHIM_SO), str(src), "-ldl"],
        check=True,
        capture_output=True,
    )
    src.unlink()
    return _SHIM_SO


# Shim C: intercepta socket(AF_UNIX)/listen/accept/close y los emula con
# socketpair()+pipes. LibreOffice usa un socket AF_UNIX de solo un hilo para
# su protocolo singleton; en sandboxes donde socket(AF_UNIX) es EPERM, este
# shim permite que la conversión headless termine sin colgarse.
_SHIM_SOURCE = r"""
#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

static int (*real_socket)(int, int, int);
static int (*real_socketpair)(int, int, int, int[2]);
static int (*real_listen)(int, int);
static int (*real_accept)(int, struct sockaddr *, socklen_t *);
static int (*real_close)(int);
static int (*real_read)(int, void *, size_t);

/* Per-FD bookkeeping (FDs >= 1024 are passed through unshimmed). */
static int is_shimmed[1024];
static int peer_of[1024];
static int wake_r[1024];            /* accept() blocks reading this */
static int wake_w[1024];            /* close()  writes to this      */
static int listener_fd = -1;        /* FD that received listen()    */

__attribute__((constructor))
static void init(void) {
    real_socket     = dlsym(RTLD_NEXT, "socket");
    real_socketpair = dlsym(RTLD_NEXT, "socketpair");
    real_listen     = dlsym(RTLD_NEXT, "listen");
    real_accept     = dlsym(RTLD_NEXT, "accept");
    real_close      = dlsym(RTLD_NEXT, "close");
    real_read       = dlsym(RTLD_NEXT, "read");
    for (int i = 0; i < 1024; i++) {
        peer_of[i] = -1;
        wake_r[i]  = -1;
        wake_w[i]  = -1;
    }
}

/* ---- socket ---------------------------------------------------------- */
int socket(int domain, int type, int protocol) {
    if (domain == AF_UNIX) {
        int fd = real_socket(domain, type, protocol);
        if (fd >= 0) return fd;
        /* socket(AF_UNIX) blocked – fall back to socketpair(). */
        int sv[2];
        if (real_socketpair(domain, type, protocol, sv) == 0) {
            if (sv[0] >= 0 && sv[0] < 1024) {
                is_shimmed[sv[0]] = 1;
                peer_of[sv[0]]    = sv[1];
                int wp[2];
                if (pipe(wp) == 0) {
                    wake_r[sv[0]] = wp[0];
                    wake_w[sv[0]] = wp[1];
                }
            }
            return sv[0];
        }
        errno = EPERM;
        return -1;
    }
    return real_socket(domain, type, protocol);
}

/* ---- listen ---------------------------------------------------------- */
int listen(int sockfd, int backlog) {
    if (sockfd >= 0 && sockfd < 1024 && is_shimmed[sockfd]) {
        listener_fd = sockfd;
        return 0;
    }
    return real_listen(sockfd, backlog);
}

/* ---- accept ---------------------------------------------------------- */
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen) {
    if (sockfd >= 0 && sockfd < 1024 && is_shimmed[sockfd]) {
        /* Block until close() writes to the wake pipe. */
        if (wake_r[sockfd] >= 0) {
            char buf;
            real_read(wake_r[sockfd], &buf, 1);
        }
        errno = ECONNABORTED;
        return -1;
    }
    return real_accept(sockfd, addr, addrlen);
}

/* ---- close ----------------------------------------------------------- */
int close(int fd) {
    if (fd >= 0 && fd < 1024 && is_shimmed[fd]) {
        int was_listener = (fd == listener_fd);
        is_shimmed[fd] = 0;

        if (wake_w[fd] >= 0) {              /* unblock accept() */
            char c = 0;
            write(wake_w[fd], &c, 1);
            real_close(wake_w[fd]);
            wake_w[fd] = -1;
        }
        if (wake_r[fd] >= 0) { real_close(wake_r[fd]); wake_r[fd]  = -1; }
        if (peer_of[fd] >= 0) { real_close(peer_of[fd]); peer_of[fd] = -1; }

        if (was_listener)
            _exit(0);                        /* conversion done – exit */
    }
    return real_close(fd);
}
"""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = run_soffice(sys.argv[1:])
        sys.exit(result.returncode)
    env = get_soffice_env()
    print(f"soffice env ready: bin={find_soffice()} {_HOME_VARS[0]}={env[_HOME_VARS[0]]}")
