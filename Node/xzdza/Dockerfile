FROM node:12
RUN npm install -g nodemon
WORKDIR /app
COPY package*.json ./
RUN npm install 
COPY . .
CMD nodemon


