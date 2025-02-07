variable "packet_token" {}
variable "packet_project_id" {}
variable "packet_plan" { default = "c3.small.x86" }
variable "packet_os" { default = "ubuntu_20_04" }
variable "packet_location" { default = "ams1" }

variable "use_legacy_packet" {
  description = "Set to true to use the legacy packethost/packet provider, false for equinix/metal"
  default     = false
}

provider "packet" {
  auth_token = var.packet_token
  count      = var.use_legacy_packet ? 1 : 0
}

provider "metal" {
  auth_token = var.packet_token
  count      = var.use_legacy_packet ? 0 : 1
}

# VLAN resources
resource "packet_vlan" "knb" {
  count        = var.use_legacy_packet ? 1 : 0
  description  = "knb"
  facility     = var.packet_location
  project_id   = var.packet_project_id
}

resource "metal_vlan" "knb" {
  count        = var.use_legacy_packet ? 0 : 1
  description  = "knb"
  metro        = var.packet_location
  project_id   = var.packet_project_id
}

# Device resources
resource "packet_device" "knb0" {
  count            = var.use_legacy_packet ? 1 : 0
  hostname         = "knb-0"
  plan             = var.packet_plan
  facilities       = [var.packet_location]
  operating_system = var.packet_os
  billing_cycle    = "hourly"
  project_id       = var.packet_project_id
}

resource "metal_device" "knb0" {
  count            = var.use_legacy_packet ? 0 : 1
  hostname         = "knb-0"
  plan             = var.packet_plan
  metro            = var.packet_location
  operating_system = var.packet_os
  billing_cycle    = "hourly"
  project_id       = var.packet_project_id
}

resource "packet_device" "knb1" {
  count            = var.use_legacy_packet ? 1 : 0
  hostname         = "knb-1"
  plan             = var.packet_plan
  facilities       = [var.packet_location]
  operating_system = var.packet_os
  billing_cycle    = "hourly"
  project_id       = var.packet_project_id
}

resource "metal_device" "knb1" {
  count            = var.use_legacy_packet ? 0 : 1
  hostname         = "knb-1"
  plan             = var.packet_plan
  metro            = var.packet_location
  operating_system = var.packet_os
  billing_cycle    = "hourly"
  project_id       = var.packet_project_id
}

# Network type resources
resource "packet_device_network_type" "knb0" {
  count     = var.use_legacy_packet ? 1 : 0
  device_id = packet_device.knb0.id
  type      = "hybrid"
}

resource "metal_device_network_type" "knb0" {
  count     = var.use_legacy_packet ? 0 : 1
  device_id = metal_device.knb0.id
  type      = "hybrid"
}

resource "packet_device_network_type" "knb1" {
  count     = var.use_legacy_packet ? 1 : 0
  device_id = packet_device.knb1.id
  type      = "hybrid"
}

resource "metal_device_network_type" "knb1" {
  count     = var.use_legacy_packet ? 0 : 1
  device_id = metal_device.knb1.id
  type      = "hybrid"
}

# VLAN attachment resources
resource "packet_port_vlan_attachment" "knb0" {
  count     = var.use_legacy_packet ? 1 : 0
  device_id = packet_device.knb0.id
  port_name = "eth1"
  vlan_vnid = packet_vlan.knb.vxlan
}

resource "metal_port_vlan_attachment" "knb0" {
  count     = var.use_legacy_packet ? 0 : 1
  device_id = metal_device.knb0.id
  port_name = "eth1"
  vlan_vnid = metal_vlan.knb.vxlan
}

resource "packet_port_vlan_attachment" "knb1" {
  count     = var.use_legacy_packet ? 1 : 0
  device_id = packet_device.knb1.id
  port_name = "eth1"
  vlan_vnid = packet_vlan.knb.vxlan
}

resource "metal_port_vlan_attachment" "knb1" {
  count     = var.use_legacy_packet ? 0 : 1
  device_id = metal_device.knb1.id
  port_name = "eth1"
  vlan_vnid = metal_vlan.knb.vxlan
}
