FROM python:3.12-bookworm

RUN pip install playwright==1.45.1 && \
    playwright install --with-deps

# optionally, copy test files into the image
COPY . /app

# set working directory
WORKDIR /app

# default command to run tests
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-v"]
