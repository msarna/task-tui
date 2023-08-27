data "archive_file" "lambda" {
  type        = "zip"
  source_file = "../lambda_function.py"
  output_path = "../lambda_function_payload.zip"
}

resource "aws_lambda_function" "lambda_ebssess" {
  filename      = "../lambda_function_payload.zip"
  function_name = "list-instances-ebsses"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"

  timeout = "30"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.11"
}

resource "aws_iam_role" "lambda_role" {
  name = "list-instances-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lamdab-role-ec2ro-attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}

resource "aws_iam_policy" "cloudwatch_lambda_policy" {
  name        = "cloudwatch-lmabda-policy"
  description = "Cloudwatch for Lambdas allowing to write to cw"
  policy      = file("data/cloudwatch-policy.json")
}

resource "aws_iam_role_policy_attachment" "lamdab-role-cw-attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.cloudwatch_lambda_policy.arn
}