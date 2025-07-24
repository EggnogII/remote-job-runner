resource "aws_elasticache_cluster" "remote-job-runner-redis" {
    cluster_id = "remote-job-runner"
    engine = "redis"
    node_type = "cache.t4g.small"
    num_cache_nodes = 1
    parameter_group_name = "default.redis7"
    engine_version = "7.1"
    port = 6379
}

