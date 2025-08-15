output "bucket_name" {
  value = aws_s3_bucket.s3_bucket[0].id
}

output "bucket_arn" {
  value = aws_s3_bucket.s3_bucket[0].arn
}