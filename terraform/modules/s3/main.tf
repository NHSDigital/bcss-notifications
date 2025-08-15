resource "aws_s3_bucket" "s3_bucket" {
  count  = var.environment != "prod" ? 1 : 0
  bucket = "${var.team}-${var.project}-s3-${var.environment}"
  tags   = var.tags
}