FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn scikit-learn

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
