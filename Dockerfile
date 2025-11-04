
# FROM python:3.13-alpine AS requirement

# WORKDIR /app

# RUN pip3 install poetry
# RUN pip3 install poetry-plugin-export
# COPY ./pyproject.toml ./poetry.lock ./
# RUN poetry export --only main --output requirements.txt



# FROM alpine:3 AS models
# ENV DETECTION_MODEL=model_weights/fabric_defect_detection_yolo11l.pt
# WORKDIR /app


# COPY ./model_weights ./model_weights



# FROM ultralytics/ultralytics:8.0.188-python

# ENV PORT=8002
# ENV WORKERS=1
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV DETECTION_MODEL=model_weights/fabric_defect_detection_yolo11l.pt

# WORKDIR /fabric_defect_detetion_app

# RUN pip3 install -U pip
# COPY --from=requirement /app/requirements.txt ./requirements.txt
# RUN pip3 install -r requirements.txt

# COPY . .
# COPY --from=models /app/model_weights ./model_weights

# EXPOSE ${PORT}
# CMD ["/bin/sh", "-c", "uvicorn application:app --workers ${WORKERS} --host 0.0.0.0 --port ${PORT}"]


# 1) Build requirements with Poetry
FROM python:3.13-slim

ENV PORT=8002
ENV WORKERS=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DETECTION_MODEL=model_weights/fabric_defect_detection_yolo11l.pt

WORKDIR /app

# Install poetry & export requirements
RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry export --only main --output requirements.txt
RUN pip install -r requirements.txt

# Copy all source code
COPY . .

# Copy model weights
COPY ./model_weights ./model_weights

EXPOSE ${PORT}

CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8002"]
