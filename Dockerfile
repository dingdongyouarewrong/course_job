FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

# устанавливаем параметры сборки
RUN apt-get update && \
	apt-get install -y gcc make apt-transport-https ca-certificates build-essential

# задаем рабочую директорию для контейнера
WORKDIR  /usr/src/recommendation

# устанавливаем зависимости python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем все файлы из корня проекта в рабочую директорию
COPY src/ /src/
RUN ls -la /src/*
EXPOSE  5000
# запускаем приложение Python
CMD ["python3", "/webserver.py"]