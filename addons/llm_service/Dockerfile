ARG BUILD_FROM
FROM ${BUILD_FROM}

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar Python 3 y pip
RUN apk add --no-cache python3 py3-pip

# Copiar las dependencias
COPY requirements.txt .

RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY server.py .

# Copiar el script de inicio y darle permisos
COPY run.sh .

# Asegurarse de que el script de inicio tenga permisos de ejecución
RUN chmod a+x run.sh

# Ejecutar el script de inicio
CMD [ "./run.sh" ]