data "aws_vpc" "default" {
  id = var.vpc_id
}

data "aws_subnet" "subnet_b" {
    id = var.subnet_b_id
}

data "aws_subnet" "subnet_c" {
  id = var.subnet_c_id
}

resource "aws_elasticache_subnet_group" "redis-subnet-group" {
    name = "redis-ecache-subnet-group"
    subnet_ids = [data.aws_subnet.subnet_b.id, data.aws_subnet.subnet_c.id]
  
}