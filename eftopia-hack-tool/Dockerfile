# Use an appropriate base image with Node.js v18.x
FROM node:18

# Set the working directory inside the container
WORKDIR /eftopia-hack-tool

# Copy package.json and package-lock.json if available
COPY package.json package-lock.json /eftopia-hack-tool/

# Install dependencies
RUN npm install

# Install Angular CLI globally
RUN npm install -g @angular/cli

# Copy the rest of your frontend application files
COPY . /eftopia-hack-tool/

# Set the command to run the frontend app
CMD ["npm", "start"]
