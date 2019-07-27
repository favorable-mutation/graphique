FROM 3.7.4-alpine

WORKDIR /app

RUN pip install bs4

COPY ./* /app

CMD ["./src/parse_html.py", "./test/fixtures/the-winters-tale.html"]
