FROM python:3.6

# The ARG instruction defines a variable 
# that users can pass at build-time to the builder with the 
# docker build command using the --build-arg <varname>=<value> flag.
# e.g. docker build --build-arg discord_token=mytoken -t durkabot .
ARG discord_token

ENV DISCORD_TOKEN=$discord_token

# assuming we're running in the root dir
ADD ./src .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
