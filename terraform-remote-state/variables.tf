variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name prefix for resources"
  type        = string
  default     = "devops-task6"
}

variable "instance_types" {
  description = "Instance size for each workspace"
  type        = map(string)
  default = {
    dev  = "t3.micro"
    prod = "t3.small"
  }
}
