data "aws_secretsmanager_secret_version" "lambda_secrets" {
  secret_id = var.secrets_arn
}

module "lambda_layer" {
  source      = "./modules/lambda_layer"
  team        = var.team
  project     = var.project
  environment = var.environment
  region      = var.region
}

module "lambdas" {
  source      = "./modules/lambdas"
  team        = var.team
  project     = var.project
  environment = var.environment
  region      = var.region
  tags        = var.tags

  subnet_ids     = module.network.private_subnet_ids
  security_group = module.network.security_group
  secrets        = jsondecode(data.aws_secretsmanager_secret_version.lambda_secrets.secret_string)
  secrets_arn    = var.secrets_arn
  sqs_queue_arn  = module.sqs.sqs_queue_arn

  batch_notification_processor_lambda_role_arn = module.iam.batch_notification_processor_lambda_role_arn
  message_status_handler_lambda_role_arn       = module.iam.message_status_handler_lambda_role_arn
  healthcheck_lambda_role_arn                  = module.iam.healthcheck_lambda_role_arn
  callback_simulator_lambda_role_arn           = module.iam.callback_simulator_lambda_role_arn
  python_packages_layer_arn                    = module.lambda_layer.python_packages_layer_arn
  oracle_client_libraries_layer_arn            = var.oracle_client_libraries_layer_arn
}

module "s3" {
  source      = "./modules/s3"
  team        = var.team
  project     = var.project
  environment = var.environment
  tags        = var.tags
}

module "sqs" {
  source      = "./modules/sqs"
  team        = var.team
  project     = var.project
  environment = var.environment
  tags        = var.tags
}

module "eventbridge" {
  source      = "./modules/eventbridge"
  team        = var.team
  project     = var.project
  environment = var.environment

  batch_notification_processor_lambda_arn  = module.lambdas.batch_notification_processor_arn
  batch_notification_processor_lambda_name = module.lambdas.batch_notification_processor_name
}

module "iam" {
  source                     = "./modules/iam"
  team                       = var.team
  project                    = var.project
  environment                = var.environment
  kms_arn                    = var.kms_arn
  secrets_arn                = var.secrets_arn
  sqs_queue_arn              = module.sqs.sqs_queue_arn
  notification_s3_bucket_arn = module.s3.bucket_arn
  tags                       = var.tags
}

module "network" {
  source          = "./modules/network"
  selected_vpc_id = var.selected_vpc_id
}

module "slack_notifier" {
  source      = "./modules/slack_notifier"
  team        = var.team
  project     = var.project
  environment = var.environment
  tags        = var.tags

  slack_webhook_url              = var.slack_webhook_url
  slack_notifier_lambda_role_arn = module.iam.slack_notifier_lambda_role_arn
}

module "cloudwatch_alarms" {
  source      = "./modules/cloudwatch_alarms"
  team        = var.team
  project     = var.project
  environment = var.environment
  tags        = var.tags

  lambda_functions = {
    "batch-notification-processor" = module.lambdas.batch_notification_processor_name
    "message-status-handler"       = module.lambdas.message_status_handler_name
    "slack-notifier"               = module.slack_notifier.slack_notifier_lambda_name
  }

  lambda_alerts_sns_topic_arn = module.slack_notifier.lambda_alerts_sns_topic_arn
}

