FROM oraclelinux:8
USER root
ENV TZ=America/New_York

ADD files4docker/ /var/www/cgi-bin
ADD misc/ /misc
ADD htmlfiles/ /var/www/html
RUN update-ca-trust && \
    dnf update -y  && \
    unset http_proxy && \
    dnf install -y sudo python3 httpd && \
    pip3 install requests && \
    rm -rf /var/cache/dnf && \
    useradd -m -u 3000 notroot && \
    python3 /misc/checkjson.py && \
    echo "notroot ALL=SETENV:NOPASSWD:/misc/startup.sh" > /etc/sudoers.d/notroot && \
    chmod ugo+x /var/www/cgi-bin/* && \
    chmod -R ugo+rwx /var/www/ && \
    touch /misc/statuscheck.log && \
    chown notroot: /misc/statuscheck.log && \
    chown -R apache: /var/www/
USER notroot
CMD sudo /misc/startup.sh
HEALTHCHECK --start-period=5s --interval=5m --timeout=7s \
  CMD /misc/health.sh || exit 1
