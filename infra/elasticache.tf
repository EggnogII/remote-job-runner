resource "aws_elasticache_cluster" "remote-job-runner-redis" {
    cluster_id = "remote-job-runner"
    engine = "redis"
    node_type = "cache.t4g.small"
    num_cache_nodes = 1
    parameter_group_name = "default.redis7"
    engine_version = "7.1"
    port = 6379

    
}

resource "aws_elasticache_user_group" "remote-job-group"{
    user_group_id = "remoteJobgroup"
    engine = "REDIS"
    user_ids = [aws_elasticache_user.remote-job-user.user_id]
}

resource "aws_elasticache_user" "remote-job-user" {
    user_id = "remoteJobUser"
    user_name = "remoteJobUser"
    access_string = "on ~* +@all"
    engine = "REDIS"
    passwords = [var.redis_cluster_password]
}