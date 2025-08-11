output "python_packages_layer_arn" {
  value = aws_lambda_layer_version.python_packages.arn
}

output "oracle_client_libraries_layer_arn" {
  value = aws_lambda_layer_version.oracle_client_libraries.arn
}
