data "aws_vpc" "selected" {
  id = "vpc-0a409ba281f33e2e3"
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

