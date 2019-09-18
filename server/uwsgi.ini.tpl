[uwsgi]
processes = {{ UWSGI_PROCESSES | default(4, true) }}

module = app.config.wsgi
single-interpreter = true
vacuum = 1
master = 1
thunder-lock = 1
http-socket = :80
http-keepalive = 75
http-timeout = 75
http-enable-proxy-protocol = 1
http-auto-chunked = true
add-header = Connection: Keep-Alive
route-run = chunked:
route-run = last:
buffer-size = 65535
chdir = /code/

stats = :5050
memory-report

lazy-apps = 0
die-on-term = true
need-app = true

# Harakiri
harakiri = 120
harakiri-verbose = true
post-buffering = 4096
max-requests = 2000

# Avoid errors on aborted client connections
ignore-sigpipe = true
ignore-write-errors = true
disable-write-exception = true
