data "aws_vpc" "selected" {
  id = var.selected_vpc_id
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
