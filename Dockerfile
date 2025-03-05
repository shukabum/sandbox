FROM openjdk:11

# Install required dependencies
RUN apt-get update && apt-get install -y \
    subversion \
    ant \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /sandbox

# Copy scripts into container
COPY scripts/ /sandbox/scripts/
COPY entrypoint.sh /sandbox/

# Make scripts executable
RUN chmod +x /sandbox/entrypoint.sh /sandbox/scripts/*.sh

# Run entrypoint script on container start
ENTRYPOINT ["/sandbox/entrypoint.sh"]
