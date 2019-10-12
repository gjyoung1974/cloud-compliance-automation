# Source some varibles from remote states
data "terraform_remote_state" "tf" {
  # output variables from https://github.com/Acme/tf
  backend = "s3"

  config {
    bucket         = "com.Acme.tf-state.tfrepo"
    key            = "tf"
    dynamodb_table = "tfrepo-terraform-state-lock"
    region         = "us-west-1"
  }
}

data "terraform_remote_state" "tf-gcp" {
  # output variables from gcp subfolder of https://github.com/Acme/tf/gcp
  backend = "s3"

  config {
    bucket = "com.Acme.tf-state.tf-gcp"
    key    = "tf-gcp"
    region = "us-west-1"
  }
}

data "terraform_remote_state" "acme-k8s" {
  # output variables from https://github.com/Acme/acme-k8s/tree/master/tf
  backend = "s3"

  config {
    bucket = "com.Acme.tf-state.k8stf"
    key    = "k8stf"
    region = "us-west-1"
  }
}

data "terraform_remote_state" "k8stf" {
  # output variables from https://github.com/Acme/acme-k8s/tree/master/tf
  backend = "s3"

  config {
    bucket         = "com.Acme.tf-state.k8stf"
    key            = "k8stf"
    dynamodb_table = "k8stf-terraform-state-lock"
    region         = "us-west-1"
  }
}
