FROM --platform=linux/amd64 tomcat:11.0-jdk11

# Remove default webapps
RUN rm -rf /usr/local/tomcat/webapps/*

# Copy WAR file
COPY target/shopping-cart-0.0.1-SNAPSHOT.war /usr/local/tomcat/webapps/shopping-cart.war

# Environment variables with defaults
ENV DB_HOST=localhost \
    DB_PORT=3306 \
    DB_NAME=shopping-cart \
    DB_USERNAME=root \
    DB_PASSWORD=root123 \
    MAILER_EMAIL=your_email \
    MAILER_PASSWORD=your_app_password

# Copy startup script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 9090

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
