# Run from California
provider "aws" {
  region = "us-west-1"
}

# Store TF state in the acme-compliance-jobs bucket.
terraform {
  backend "s3" {
    bucket         = "com.Acme.tf-state.acme-compliance-jobs"
    key            = "acme-compliance-jobs"
    kms_key_id     = "arn:aws:kms:us-west-1:293993587779:key/3c89e612-0067-4b3f-b2e1-0196de8eb1c9"
    encrypt        = true
    dynamodb_table = "acme-compliance-jobs-terraform-state-lock"
    region         = "us-west-1"
  }
}
