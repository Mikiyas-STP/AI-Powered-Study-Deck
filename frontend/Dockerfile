FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# For development/simple portfolio deployment:
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]