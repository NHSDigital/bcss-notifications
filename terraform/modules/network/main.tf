data "aws_vpc" "selected" {
  id = "vpc-09c7c54244a87b9d9"
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }

  tags = {
    "Name" = "*private*"
  }
}

data "aws_security_group" "lambda" {
  name = "bcss-notify-lambdas"
}

