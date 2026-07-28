data "aws_iam_policy_document" "pipeline_access" {
  statement {
    sid     = "ReadRawTransactions"
    effect  = "Allow"
    actions = ["s3:GetObject", "s3:ListBucket"]
    resources = [
      var.raw_bucket_arn,
      "${var.raw_bucket_arn}/*",
    ]
  }

  statement {
    sid     = "WriteProcessedAssessments"
    effect  = "Allow"
    actions = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"]
    resources = [
      var.processed_bucket_arn,
      "${var.processed_bucket_arn}/*",
    ]
  }
}

resource "aws_iam_policy" "pipeline_access" {
  name        = "${var.name_prefix}-pipeline-access"
  description = "Least-privilege S3 access for the educational fraud processing job."
  policy      = data.aws_iam_policy_document.pipeline_access.json
  tags        = var.tags
}
