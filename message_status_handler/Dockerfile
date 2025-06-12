FROM public.ecr.aws/lambda/python:3.13

COPY --from=root_dir pyproject.toml ${LAMBDA_TASK_ROOT}
COPY --from=root_dir poetry.lock ${LAMBDA_TASK_ROOT}
COPY --from=root_dir shared/*.py ${LAMBDA_TASK_ROOT}
COPY *.py ${LAMBDA_TASK_ROOT}

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

CMD [ "callback_lambda_function.lambda_handler" ]
