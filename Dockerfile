FROM python:3.14.0-slim

WORKDIR /opt/Weather_Forecast

COPY . .
RUN pip install --upgrade pip
RUN pip install -r 'requirements.txt'

CMD [ "python3", "bot.py" ]