# Configuration Gunicorn optimisée pour Render
import multiprocessing
import os

# Nombre de workers (1 pour le plan gratuit de Render)
workers = 1

# Nombre de threads par worker
threads = 2

# Timeout en secondes (5 minutes)
timeout = 300

# Nombre maximum de requêtes par worker avant redémarrage
max_requests = 1000
max_requests_jitter = 100

# Précharger l'application
preload_app = True

# Bind sur le port spécifié par Render
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# Logs
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Worker class
worker_class = "sync"

# Worker connections
worker_connections = 1000

# Keep alive
keepalive = 2

# Graceful timeout
graceful_timeout = 30

# Max requests jitter
max_requests_jitter = 100

# Worker tmp directory
worker_tmp_dir = "/dev/shm"

# Hook pour nettoyer la mémoire
def worker_exit(server, worker):
    import gc
    gc.collect()

def on_starting(server):
    print("🚀 Démarrage du serveur Gunicorn...")

def on_reload(server):
    print("🔄 Rechargement du serveur...")

def worker_int(worker):
    print("⚠️  Worker interrompu")

def pre_fork(server, worker):
    print(f"🔄 Préparation du worker {worker.pid}")

def post_fork(server, worker):
    print(f"✅ Worker {worker.pid} démarré")

def post_worker_init(worker):
    print(f"🔧 Initialisation du worker {worker.pid}")

def worker_abort(worker):
    print(f"❌ Worker {worker.pid} interrompu")
