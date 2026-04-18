# Étape 1 : Build
FROM node:20-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Étape 2 : Production avec un serveur Node léger (serve)
FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=build-stage /app/dist /app/dist

# Exposer le port (5173 par défaut ou 80)
EXPOSE 80

# Commande pour servir le dossier dist en gérant le routing SPA (-s)
CMD ["serve", "-s", "dist", "-l", "80"]
