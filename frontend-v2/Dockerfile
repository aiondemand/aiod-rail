### STAGE 1: Build ###
FROM node:lts as builder

# Install dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Build
COPY . .

ARG PROFILE
ENV PROFILE $PROFILE

RUN echo "Environment: ${PROFILE}"
RUN npm run build-${PROFILE}

### STAGE 2: Run ###
FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY nginx.conf /etc/nginx/

COPY --from=builder /app/dist /usr/share/nginx/html
