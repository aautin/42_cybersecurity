FROM php:7.4-apache

# Install extensions bwapp commonly uses
RUN docker-php-ext-install mysqli pdo pdo_mysql && \
    a2enmod rewrite

# Basic hardening for container layer (app itself remains intentionally vulnerable)
RUN chown -R www-data:www-data /var/www/html

WORKDIR /var/www/html