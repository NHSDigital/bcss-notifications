locals {
  runtime = "python3.13"
  secrets = var.secrets
}

data "archive_file" "placeholder_zip" {
  type        = "zip"
  output_path = "${path.module}/placeholder.zip"

  source {
    content  = "placeholder"
    filename = "placeholder.txt"
  }
}

resource "aws_lambda_function" "batch_notification_processor" {
  filename      = data.archive_file.placeholder_zip.output_path
  function_name = "${var.team}-${var.project}-batch-notification-processor-${var.environment}"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  role          = var.batch_notification_processor_lambda_role_arn
  runtime       = local.runtime
  timeout       = 300

  logging_config {
    application_log_level = "INFO"
    log_format            = "JSON"
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [var.security_group]
  }

  layers = [
    var.parameters_and_secrets_lambda_extension_arn,
    var.python_packages_layer_arn
  ]

  environment {
    variables = {
      DATABASE_PORT       = local.secrets["database_port"]
      ENVIRONMENT         = var.environment
      NOTIFY_API_BASE_URL = local.secrets["notify_api_base_url"]
      OAUTH_TOKEN_URL     = local.secrets["oauth_token_url"]
      REGION_NAME         = var.region
      SECRET_ARN          = var.secrets_arn

      LAMBDA_STATUS_CHECK_ARN      = aws_lambda_function.message_status_handler.arn
      LAMBDA_STATUS_CHECK_ROLE_ARN = var.message_status_handler_lambda_role_arn

      PARAMETERS_SECRETS_EXTENSION_CACHE_ENABLED = "true"
      PARAMETERS_SECRETS_EXTENSION_LOG_LEVEL     = "debug"
    }
  }

  tags = var.tags
}

resource "aws_lambda_function" "message_status_handler" {
  filename      = data.archive_file.placeholder_zip.output_path
  function_name = "${var.team}-${var.project}-message-status-handler-${var.environment}"
  handler       = "callback_lambda_function.lambda_handler"
  memory_size   = 128
  role          = var.message_status_handler_lambda_role_arn
  runtime       = local.runtime
  timeout       = 300

  logging_config {
    application_log_level = "INFO"
    log_format            = "JSON"
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [var.security_group]
  }

  layers = [
    var.parameters_and_secrets_lambda_extension_arn,
    var.python_packages_layer_arn
  ]

  environment {
    variables = {
      DATABASE_PORT       = local.secrets["database_port"]
      ENVIRONMENT         = var.environment
      NOTIFY_API_BASE_URL = local.secrets["notify_api_base_url"]
      REGION_NAME         = var.region
      SECRET_ARN          = var.secrets_arn

      PARAMETERS_SECRETS_EXTENSION_CACHE_ENABLED = "true"
      PARAMETERS_SECRETS_EXTENSION_LOG_LEVEL     = "debug"
    }
  }

  tags = var.tags
}

resource "aws_lambda_function_url" "message_status_handler_url" {
  function_name      = aws_lambda_function.message_status_handler.function_name
  authorization_type = "NONE"
  cors {
    allow_origins = ["https://int.api.service.nhs.uk"]
    allow_methods = ["POST"]
  }
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = var.sqs_queue_arn
  function_name    = aws_lambda_function.message_status_handler.function_name
  batch_size       = 10 # Adjust as needed
}

resource "aws_lambda_permission" "allow_sqs_to_call_lambda" {
  statement_id  = "AllowSQSInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.message_status_handler.function_name
  principal     = "sqs.amazonaws.com"
  source_arn    = var.sqs_queue_arn
}

resource "aws_lambda_function" "healthcheck" {
  filename      = data.archive_file.placeholder_zip.output_path
  function_name = "${var.team}-${var.project}-healthcheck-${var.environment}"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  role          = var.healthcheck_lambda_role_arn
  runtime       = local.runtime
  timeout       = 300

  logging_config {
    application_log_level = "INFO"
    log_format            = "JSON"
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [var.security_group]
  }

  layers = [
    var.parameters_and_secrets_lambda_extension_arn,
    var.python_packages_layer_arn
  ]

  environment {
    variables = {
      DATABASE_PORT       = local.secrets["database_port"]
      ENVIRONMENT         = var.environment
      NOTIFY_API_BASE_URL = local.secrets["notify_api_base_url"]
      OAUTH_TOKEN_URL     = local.secrets["oauth_token_url"]
      REGION_NAME         = var.region
      SECRET_ARN          = var.secrets_arn

      PARAMETERS_SECRETS_EXTENSION_CACHE_ENABLED = "true"
      PARAMETERS_SECRETS_EXTENSION_LOG_LEVEL     = "debug"
    }
  }

  tags = var.tags
}

resource "aws_lambda_function" "callback_simulator" {
  filename      = data.archive_file.placeholder_zip.output_path
  function_name = "${var.team}-${var.project}-callback-simulator-${var.environment}"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  role          = var.callback_simulator_lambda_role_arn
  runtime       = local.runtime
  timeout       = 300

  logging_config {
    application_log_level = "INFO"
    log_format            = "JSON"
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [var.security_group]
  }

  layers = [
    var.parameters_and_secrets_lambda_extension_arn,
    var.python_packages_layer_arn
  ]

  environment {
    variables = {
      DATABASE_PORT = local.secrets["database_port"]
      ENVIRONMENT   = var.environment
      REGION_NAME   = var.region
      SECRET_ARN    = var.secrets_arn

      MESSAGE_STATUS_HANDLER_LAMBDA_URL = aws_lambda_function_url.message_status_handler_url.function_url

      PARAMETERS_SECRETS_EXTENSION_CACHE_ENABLED = "true"
      PARAMETERS_SECRETS_EXTENSION_LOG_LEVEL     = "info"
    }
  }

  tags = var.tags
}
