data "aws_vpc" "selected" {
  id = var.selected_vpc_id
}

# Important note:
# The DB requires connection only from private-a subnet.
# This is because the DB is only available in AZ 2a
data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }

  tags = {
    "Name" = "*private-a*"
  }
}

data "aws_security_group" "lambda" {
  name = "bcss-notify-lambdas"
}
