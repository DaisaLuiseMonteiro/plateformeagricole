# Utiliser Node pour le build et le service local
FROM node:20-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build-only

# Étape finale avec serve pour le test local (Vercel gérera la prod indépendamment)
FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=build-stage /app/dist /app/dist
EXPOSE 80
CMD ["serve", "-s", "dist", "-l", "80"]
