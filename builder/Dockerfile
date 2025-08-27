FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    jq \
    zip \
    imagemagick

# Set the working directory
WORKDIR /app
VOLUME /app/build

# Copy the entire builder directory
COPY builder /app/builder

# Make the build script executable
RUN chmod +x /app/builder/build.sh

# Run the build script
CMD ["/app/builder/build.sh"]
