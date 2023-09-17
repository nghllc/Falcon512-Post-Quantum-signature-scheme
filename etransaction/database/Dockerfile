FROM mysql:latest

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=transactions
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

# Copy SQL scripts to container
COPY init.sql /docker-entrypoint-initdb.d/

# Set permissions on SQL scripts
RUN chmod 755 /docker-entrypoint-initdb.d/init.sql