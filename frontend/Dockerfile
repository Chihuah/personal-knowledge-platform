# Build stage
FROM node:22-alpine AS builder
WORKDIR /app/frontend

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install all dependencies (including devDependencies needed for build)
RUN npm ci && npm cache clean --force

# Copy source code
COPY frontend ./

# Accept build-time environment variable
ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL

# Build the application
RUN npm run build

# Production stage
FROM node:22-alpine AS runner
WORKDIR /app/frontend

ENV NODE_ENV=production

# Copy built application from builder
COPY --from=builder /app/frontend/.next/standalone ./
COPY --from=builder /app/frontend/.next/static ./.next/static
COPY --from=builder /app/frontend/public ./public

EXPOSE 3000

CMD ["node", "server.js"]
