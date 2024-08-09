FROM node:18

WORKDIR /Users/akintundemayokun/Desktop/Personalised Resume/Dev/backend

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]
