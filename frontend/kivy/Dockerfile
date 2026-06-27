FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Kivy needs some dependencies for graphical output
# For simplicity, we'll use the SDL2 video driver
ENV KIVY_WINDOW=sdl2

CMD ["python", "main.py"]