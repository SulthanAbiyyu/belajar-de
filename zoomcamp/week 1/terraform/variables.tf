variable "credentials" {
  description = "value of credentials"
  default     = "./cred.json"
}

variable "project_id" {
  description = "my project id"
  default     = "taxi-rides-ny-413704"
}

variable "region" {
  description = "my region"
  default     = "asia-southeast2"
}

variable "location" {
  description = "my location"
  default     = "ASIA-SOUTHEAST2"
}

variable "bq_dataset_name" {
  description = "my data"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "my bucket name"
  default     = "demo-taxi-rides-ny-413704"

}

variable "gcs_storage_class" {
  description = "my bucket class"
  default     = "STANDARD"
}