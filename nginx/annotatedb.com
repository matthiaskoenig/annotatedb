# -----------------------------
# AnnotateDB (proxy config)
#-----------------------------

access_log /var/www/logs/annotatedb.com_access.log;
error_log /var/www/logs/annotatedb.com_error.log;


# redirect non-https traffic to https correct domain
server {
    listen 80;
    listen [::]:80;

    server_name annotatedb.com www.annotatedb.com;
    return 301 https://annotatedb.com$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name www.annotatedb.com;
    ssl_certificate     /etc/letsencrypt/live/annotatedb.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/annotatedb.com/privkey.pem;

    return 301 https://annotatedb.com$request_uri;
}

# https
server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;

        server_name annotatedb.com;

        ssl_certificate     /etc/letsencrypt/live/annotatedb.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/annotatedb.com/privkey.pem;
        include /etc/nginx/snippets/ssl.conf;

        client_max_body_size 100m;
        location / {
                # return 200 "ssl on proxy";
                proxy_pass http://172.107.0.100:8889;
                proxy_set_header HOST $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-for $remote_addr;
                proxy_set_header X-Forwarded-Proto https;
                port_in_redirect off;
        }
}
