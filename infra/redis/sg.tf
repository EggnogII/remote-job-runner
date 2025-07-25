# This really should belong with the application ECS definition module but I'll leave this alone for now
resource "aws_security_group" "remote-job-runner-sg" {
  name        = "remote-job-runner-sg"
  description = "Security group for app containers or EC2 instances"
  vpc_id      = data.aws_vpc.default.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "remote-job-runner-redis-sg" {
  name        = "redis-sg"
  description = "Security Group for Redis Instance, on Remote Job Runner"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description     = "Allow redis from RJR app SG"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.remote-job-runner-sg.id]
  }

}