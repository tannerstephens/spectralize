FROM python:3.10 as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
ENV FLASK_APP=lyra:create_app

RUN useradd --create-home appuser
RUN mkdir /var/database
RUN chown -R appuser:appuser /var/database
WORKDIR /home/appuser
USER appuser

COPY . .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "4", "spectralize:app"]
