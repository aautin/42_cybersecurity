FROM alpine:latest

RUN apk add --no-cache vsftpd

RUN adduser -D -s /bin/sh ftpuser && \
    echo "ftpuser:1234" | chpasswd

COPY files /home/ftp/
RUN chmod -R 755 /home/ftp
RUN chown -R ftpuser:ftpuser /home/ftp

COPY vsftpd.conf /etc/vsftpd/vsftpd.conf

CMD ["vsftpd", "/etc/vsftpd/vsftpd.conf"]
