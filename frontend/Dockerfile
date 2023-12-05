FROM node:lts as build-env

# Install dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Build
COPY . .
RUN npm run build-prod-flat

# ========
# Stage 2
# ========
FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY nginx.conf /etc/nginx/

COPY --from=build-env /app/dist /usr/share/nginx/html
