# modules/cloudwatch/main.tf

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 7
}

# 1. URLs Shortened Per Hour - Custom Metric Filter
resource "aws_cloudwatch_log_metric_filter" "urls_shortened" {
  name           = "urls-shortened-rate"
  log_group_name = aws_cloudwatch_log_group.lambda_logs.name
  pattern        = "URL_SHORTENED"
  
  metric_transformation {
    name      = "URLsShortenedCount"
    namespace = "URLShortener/Business"
    value     = "1"
    unit      = "Count"
  }
}

# 2. Redirect Success Rate - Success Count
resource "aws_cloudwatch_log_metric_filter" "redirect_success" {
  name           = "redirect-success-rate"
  log_group_name = aws_cloudwatch_log_group.lambda_logs.name
  pattern        = "REDIRECT_SUCCESS"
  
  metric_transformation {
    name      = "RedirectSuccessCount"
    namespace = "URLShortener/Business"
    value     = "1"
    unit      = "Count"
  }
}

# 2. Redirect Success Rate - Failed Count
resource "aws_cloudwatch_log_metric_filter" "redirect_failed" {
  name           = "redirect-failed-rate"
  log_group_name = aws_cloudwatch_log_group.lambda_logs.name
  pattern        = "REDIRECT_FAILED"
  
  metric_transformation {
    name      = "RedirectFailedCount"
    namespace = "URLShortener/Business"
    value     = "1"
    unit      = "Count"
  }
}

# 6. End-to-End Latency - Custom Metric Filter
resource "aws_cloudwatch_log_metric_filter" "request_latency" {
  name           = "request-latency"
  log_group_name = aws_cloudwatch_log_group.lambda_logs.name
  pattern        = "REQUEST_LATENCY"
  
  metric_transformation {
    name      = "RequestLatency"
    namespace = "URLShortener/Performance"
    value     = "1"
    unit      = "Count"
  }
}