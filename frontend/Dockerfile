# Stage 1: Build the Vue project
FROM node:18 AS build

WORKDIR /app

# Copy the Vue project files
COPY vue-components ./vue-components

# Navigate to the Vue components folder and install dependencies
WORKDIR /app/vue-components

# Set environment variable to avoid OpenSSL issue
ENV NODE_OPTIONS=--openssl-legacy-provider

# Install dependencies and build the project
RUN npm install && npm run build

# Stage 2: Serve with NGINX
FROM nginx:alpine

# Copy built files from the build stage to NGINX
COPY --from=build /app/vue-components/dist /usr/share/nginx/html

# Expose port 80 to serve the frontend
EXPOSE 80

