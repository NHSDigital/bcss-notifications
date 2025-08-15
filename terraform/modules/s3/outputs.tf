output "bucket_name" {
  value = aws_s3_bucket[0].s3_bucket.id
}

output "bucket_arn" {
  value = aws_s3_bucket[0].s3_bucket.arn
}