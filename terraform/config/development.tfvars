environment = "dev"
team        = "bcss"
project     = "comms"
region      = "eu-west-2"

kms_arn     = "arn:aws:kms:eu-west-2:730319765130:key/25da03db-7a99-4a15-bc38-2bf757f27fca"
secrets_arn = "arn:aws:secretsmanager:eu-west-2:730319765130:secret:bcss-nonprod-notify-lambda-secrets-A8O202"

oracle_client_libraries_layer_arn = "arn:aws:lambda:eu-west-2:730319765130:layer:bcss-comms-oracleclient:2"
selected_vpc_id = "vpc-09c7c54244a87b9d9"

tags = {
  "Service" = "bcss"
}

