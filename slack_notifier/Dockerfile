FROM public.ecr.aws/lambda/python:3.13

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]
