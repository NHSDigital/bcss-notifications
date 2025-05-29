resource "aws_iam_role" "message_status_handler_lambda_role" {
  name = "${var.team}-${var.project}-message-status-handler-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "message_status_handler_lambda_role_policy_attachment" {
  role       = aws_iam_role.message_status_handler_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "message_status_handler_lambda_role_vpc_access_policy_attachment" {
  role       = aws_iam_role.message_status_handler_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

data "aws_iam_policy_document" "lambda_secretsmanager_policy_document" {
  statement {
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = [
      var.secrets_arn
    ]
  }
}

data "aws_iam_policy_document" "lambda_kms_policy_document" {
  statement {
    actions = [
      "kms:Decrypt",
    ]
    resources = [
      var.kms_arn
    ]
  }
}

resource "aws_iam_policy" "message_status_handler_secretsmanager_policy" {
  name   = "${var.team}-${var.project}-message-status-handler-secretsmanager-policy-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_secretsmanager_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "message_status_handler_lambda_secretsmanager_access" {
  role       = aws_iam_role.message_status_handler_lambda_role.name
  policy_arn = aws_iam_policy.message_status_handler_secretsmanager_policy.arn
}

resource "aws_iam_policy" "message_status_handler_kms_policy" {
  name   = "${var.team}-${var.project}-message-status-handler-kms-policy-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_kms_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "message_status_handler_lambda_kms_access" {
  role       = aws_iam_role.message_status_handler_lambda_role.name
  policy_arn = aws_iam_policy.message_status_handler_kms_policy.arn
}

data "aws_iam_policy_document" "message_status_handler_sqs_policy_document" {
  statement {
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
    ]

    resources = [
      var.sqs_queue_arn,
    ]
  }
}

resource "aws_iam_policy" "message_status_handler_sqs_policy" {
  name   = "${var.team}-${var.project}-message-status-handler-sqs-policy-${var.environment}"
  policy = data.aws_iam_policy_document.message_status_handler_sqs_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "message_status_handler_lambda_sqs_access" {
  role       = aws_iam_role.message_status_handler_lambda_role.name
  policy_arn = aws_iam_policy.message_status_handler_sqs_policy.arn
}

data "aws_iam_policy_document" "message_status_handler_s3_policy_document" {
  statement {
    actions = [
      "s3:GetObject",
    ]
    resources = [
      var.notification_s3_bucket_arn
    ]
  }
}

resource "aws_iam_policy" "message_status_handler_s3_policy" {
  name   = "${var.team}-${var.project}-message-status-handler-s3-policy-${var.environment}"
  policy = data.aws_iam_policy_document.message_status_handler_s3_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "message_status_handler_lambda_s3_access" {
  role       = aws_iam_role.message_status_handler_lambda_role.name
  policy_arn = aws_iam_policy.message_status_handler_s3_policy.arn
}

resource "aws_iam_role" "batch_notification_processor_lambda_role" {
  name = "${var.team}-${var.project}-batch-notification-processor-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "batch_notification_processor_lambda_role_policy_attachment" {
  role       = aws_iam_role.batch_notification_processor_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "batch_notification_processor_lambda_role_vpc_access_policy_attachment" {
  role       = aws_iam_role.batch_notification_processor_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_policy" "batch_notification_processor_secretsmanager_policy" {
  name   = "${var.team}-${var.project}-batch-notification-processor-secretsmanager-policy-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_secretsmanager_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "batch_notification_processor_lambda_secretsmanager_access" {
  role       = aws_iam_role.batch_notification_processor_lambda_role.name
  policy_arn = aws_iam_policy.batch_notification_processor_secretsmanager_policy.arn
}

resource "aws_iam_policy" "batch_notification_processor_kms_policy" {
  name   = "${var.team}-${var.project}-batch-notification-processor-kms-policy-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_kms_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "batch_notification_processor_lambda_kms_access" {
  role       = aws_iam_role.batch_notification_processor_lambda_role.name
  policy_arn = aws_iam_policy.batch_notification_processor_kms_policy.arn
}

data "aws_iam_policy_document" "batch_notification_processor_s3_policy_document" {
  statement {
    actions = [
      "s3:PutObject",
    ]
    resources = [
      var.notification_s3_bucket_arn
    ]
  }
}

resource "aws_iam_policy" "batch_notification_processor_s3_policy" {
  name   = "${var.team}-${var.project}-batch-notification-processor-s3-policy-${var.environment}"
  policy = data.aws_iam_policy_document.batch_notification_processor_s3_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "batch_notification_processor_lambda_s3_access" {
  role       = aws_iam_role.batch_notification_processor_lambda_role.name
  policy_arn = aws_iam_policy.batch_notification_processor_s3_policy.arn
}

data "aws_iam_policy_document" "batch_notification_processor_sqs_policy_document" {
  statement {
    actions = [
      "sqs:SendMessage",
    ]

    resources = [
      var.sqs_queue_arn,
    ]
  }
}

resource "aws_iam_policy" "batch_notification_processor_sqs_policy" {
  name   = "${var.team}-${var.project}-batch-notification-processor-sqs-policy-${var.environment}"
  policy = data.aws_iam_policy_document.batch_notification_processor_sqs_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "batch_notification_processor_lambda_sqs_access" {
  role       = aws_iam_role.batch_notification_processor_lambda_role.name
  policy_arn = aws_iam_policy.batch_notification_processor_sqs_policy.arn
}

resource "aws_iam_role" "healthcheck_lambda_role" {
  name = "${var.team}-${var.project}-healthcheck-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "healthcheck_lambda_role_policy_attachment" {
  role       = aws_iam_role.healthcheck_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "healthcheck_lambda_role_vpc_access_policy_attachment" {
  role       = aws_iam_role.healthcheck_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_policy" "healthcheck_secretsmanager_policy" {
  name   = "${var.team}-${var.project}-healthcheck-secretsmanager-policy-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_secretsmanager_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "healthcheck_lambda_secretsmanager_access" {
  role       = aws_iam_role.healthcheck_lambda_role.name
  policy_arn = aws_iam_policy.healthcheck_secretsmanager_policy.arn
}

resource "aws_iam_policy" "healthcheck_kms_policy" {
  name   = "${var.team}-${var.project}-healthcheck-kms-policy-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_kms_policy_document.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "healthcheck_lambda_kms_access" {
  role       = aws_iam_role.healthcheck_lambda_role.name
  policy_arn = aws_iam_policy.healthcheck_kms_policy.arn
}
