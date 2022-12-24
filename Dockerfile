FROM arm32v6/python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src ./

ENV PYTHONPATH=/usr/src/app/shopping_list:/usr/src/app

EXPOSE 5000

CMD [ "python", "./shopping_list/bot.py" ]