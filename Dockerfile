FROM python:3.7

# assuming we're running in the root dir
ADD ./src .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
