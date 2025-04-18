# Usar la imagen oficial de Node.js
FROM node:23

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY package.json ./
COPY . .

# Instalar las dependencias necesarias
# RUN npm install

# Instalar node-fetch junto con las dependencias de la aplicación
RUN npm install node-fetch@2 && npm install

# Instalar dependencias necesarias para Chromium
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrender1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgtk-3-0 \
    libgbm1 \
    fonts-liberation \
    xdg-utils \
    wget \
    ca-certificates

# Limpiar la caché de apt para reducir el tamaño de la imagen
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Ejecutar el script principal
CMD ["node", "index.js"]