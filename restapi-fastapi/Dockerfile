# set up the container.
FROM python:3.10-slim-bookworm

# set the working dir.
WORKDIR /app

# copy the app dir.
COPY app app

# install libraries.
RUN pip install --no-cache-dir fastapi uvicorn pydantic motor

# expose the port.
EXPOSE 5000

# command to run the app using uvicorn.
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","5000"]

