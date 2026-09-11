FROM python
WORKDIR /home/myapp
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "-u", "scheduler.py"]