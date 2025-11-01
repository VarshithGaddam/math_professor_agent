FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY public/ ./public/
COPY src/ ./src/

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
