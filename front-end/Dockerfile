# Base image with Node.js and npm
FROM node:18-alpine

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (for better caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the full source code into the container
COPY . .

# Expose the port (React uses 3000 by default)
EXPOSE 3000

# Run the React app in development mode
CMD ["npm", "start"]