FROM node:14
WORKDIR /frontend
ENV PATH /frontend/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY ./src ./src
COPY ./public ./public
CMD ["npm", "start"]
