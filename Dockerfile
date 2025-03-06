FROM openjdk:11-jdk

# Set up Japanese locale
RUN apt-get update && apt-get install -y \
    subversion \
    ant \
    python3 \
    python3-pip \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen ja_JP.UTF-8

# Set environment variables for Japanese support
ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8

# Install required packages
RUN apt-get update && apt-get install -y \
    ant \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /sandbox

# Copy scripts
COPY scripts/ /sandbox/scripts/
COPY entrypoint.sh /sandbox/

# Make scripts executable
RUN chmod +x /sandbox/entrypoint.sh /sandbox/scripts/*.sh
RUN chmod +x /sandbox/scripts/copy_eclipse.sh

# Run entrypoint script on container start
ENTRYPOINT ["/sandbox/entrypoint.sh"]
