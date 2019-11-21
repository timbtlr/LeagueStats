[uwsgi]
processes = {{ UWSGI_PROCESSES | default(4, true) }}
http-socket = :{{ PORT | default(80, true) }} 
module = app.config.wsgi
single-interpreter = true
vacuum = 1
master = 1
thunder-lock = 1