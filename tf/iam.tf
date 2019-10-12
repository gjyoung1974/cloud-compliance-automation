# Create an "Audit all the IAM things policy"
resource "aws_iam_policy" "acme_compliance_audit" {
  name        = "acme-compliance-audit"
  description = "Allow audits of security relevant resources."

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Resource": "*",
            "Action": [
                "acm:Describe*",
                "acm:List*",
                "iam:GenerateCredentialReport",
                "iam:GenerateServiceLastAccessedDetails",
                "iam:Get*",
                "iam:List*",
                "iam:ListUsers",
                "iam:ListAccessKeys",
                "iam:SimulateCustomPolicy",
                "iam:SimulatePrincipalPolicy",
                "kms:Describe*",
                "kms:Get*",
                "kms:List*"
            ]
        }
    ]
}
EOF
}

# Create a role for compliance automation jobs to assume
resource "aws_iam_role" "acme_compliance_auditor" {
  name = "acme-compliance-auditor"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com" 
      },
      "Effect": "Allow",
      "Sid": ""
    },
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "AWS": "${data.terraform_remote_state.acme_k8s.k8s_node_iam_role_prod}"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
      "AWS": "${data.terraform_remote_state.acme_k8s.k8s_node_iam_role_stage}"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# attach a policy to our IAM role
resource "aws_iam_role_policy_attachment" "acme_compliance_auditor_attach" {
  role       = "${aws_iam_role.acme_compliance_auditor.name}"
  policy_arn = "${aws_iam_policy.acme_compliance_audit.arn}"
}
