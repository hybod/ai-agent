#!/bin/bash

# Configure Tomcat to use port 9090
sed -i 's/port="8080"/port="9090"/g' /usr/local/tomcat/conf/server.xml

# Start Tomcat in background to extract WAR
catalina.sh start

# Wait for WAR extraction
sleep 5

# Generate application.properties from environment variables
mkdir -p /usr/local/tomcat/webapps/shopping-cart/WEB-INF/classes/
cat > /usr/local/tomcat/webapps/shopping-cart/WEB-INF/classes/application.properties << EOF
# Database Credentials
db.driverName = com.mysql.cj.jdbc.Driver
db.connectionString = jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME}
db.username = ${DB_USERNAME}
db.password = ${DB_PASSWORD}

#Mailer Credentials
mailer.email=${MAILER_EMAIL}
mailer.password=${MAILER_PASSWORD}
EOF

# Stop Tomcat and restart in foreground
catalina.sh stop
sleep 2

# Start Tomcat in foreground
exec catalina.sh run
