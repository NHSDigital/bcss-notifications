locals {
  runtime = "python3.13"
}

data "archive_file" "placeholder_zip" {
  type        = "zip"
  output_path = "${path.module}/placeholder.zip"

  source {
    content  = "placeholder"
    filename = "placeholder.txt"
  }
}

resource "aws_lambda_layer_version" "python_packages" {
  layer_name          = "${var.team}-${var.project}-python-packages-${var.environment}"
  compatible_runtimes = [local.runtime]
  filename            = "${path.module}/placeholder.zip"
}

resource "aws_lambda_layer_version" "oracle_client_libraries" {
  layer_name          = "${var.team}-${var.project}-oracleclient-${var.environment}"
  compatible_runtimes = [local.runtime]
  filename            = "${path.module}/placeholder.zip"
}
