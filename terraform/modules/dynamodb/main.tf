resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = "PAYPERREQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}
