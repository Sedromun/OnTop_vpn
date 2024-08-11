FROM python

RUN apt-get update


WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/bin/bash", "-c", "python backend.py"]
CMD ["/bin/bash", "-c", "python main.py"]
