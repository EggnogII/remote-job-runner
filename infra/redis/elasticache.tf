resource "aws_elasticache_cluster" "remote-job-runner-redis" {
  cluster_id           = "remote-job-runner"
  engine               = "redis"
  node_type            = "cache.t4g.small"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  engine_version       = "7.1"
  port                 = 6379

  subnet_group_name = aws_elasticache_subnet_group.redis-subnet-group.name
  security_group_ids = [aws_security_group.remote-job-runner-sg.id]


}

/*
resource "aws_elasticache_user_group" "remote-job-group" {
  user_group_id = "remoteJobgroup"
  engine        = "redis"
  user_ids      = [aws_elasticache_user.remote-job-user.user_id]
}

resource "aws_elasticache_user" "remote-job-user" {
  user_id       = "remoteJobUser"
  user_name     = "remoteJobUser"
  access_string = "on ~* +@all"
  engine        = "redis"
  passwords     = [var.redis_cluster_password]
}
*/