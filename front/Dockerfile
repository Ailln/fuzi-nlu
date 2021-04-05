FROM node:16.13.0-alpine as builder

WORKDIR /app/

COPY package*.json /app/

RUN npm install --registry=https://registry.npmmirror.com

COPY ./ /app/

RUN npm run build


FROM nginx:1.21.4-alpine as runner

WORKDIR /usr/share/nginx/html/

COPY --from=builder /app/dist  /usr/share/nginx/html/

CMD ["nginx", "-g", "daemon off;"]
