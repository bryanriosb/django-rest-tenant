FROM postgres:14.6

COPY ./compose/pro/postgres/maintenance /usr/dev/bin/maintenance
RUN chmod +x /usr/dev/bin/maintenance/*
RUN mv /usr/dev/bin/maintenance/* /usr/dev/bin \
    && rmdir /usr/dev/bin/maintenance
