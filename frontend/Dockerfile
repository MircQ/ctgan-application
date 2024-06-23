FROM node:alpine

WORKDIR /usr/src/app

# Copy project files into the container
COPY . /usr/src/app

# Installing Angular cli
RUN npm install -g @angular/cli

# Installing packages
RUN npm install

# Serving the application
CMD ["ng", "serve", "--host", "0.0.0.0"]