packer {
  required_plugins {
    proxmox = {
      version = ">= 1.1.8"
      source  = "github.com/hashicorp/proxmox"
    }
  }
}

variable "proxmox_host" {
    type = string
}

variable "proxmox_node" {
    type = string
}

variable "iso_file" {
    type = string
}

variable "proxmox_user" {
    type = string
}

variable "proxmox_token" {
    type = string
}

variable "cpu_type" {
    type = string
}

variable "cores" {
    type = number
}

variable "sockets" {
    type = number
}

variable "memory" {
    type = number
}

variable "disk_size" {
    type = string
}

variable "storage_pool" {
    type = string
}

variable "disk_type" {
    type = string
}

variable "network_bridge" {
    type = string
}

variable "vm_name" {
    type = string
}

variable "ssh_user" {
    type = string
}

variable "ssh_pass" {
    type = string
}

source "proxmox-iso" "rhel-tpl" {

    proxmox_url = var.proxmox_host
    insecure_skip_tls_verify = true
    node = var.proxmox_node
    iso_file = var.iso_file
    vm_name = var.vm_name
    username = var.proxmox_user
    token = var.proxmox_token
    cpu_type = var.cpu_type
    cores = var.cores 
    sockets = var.sockets
    memory = var.memory
    disks {
        disk_size         = var.disk_size 
        storage_pool      = var.storage_pool
        type              = var.disk_type 
    }
    network_adapters {
        bridge = var.network_bridge
    }
    ssh_username = var.ssh_user
    ssh_password = var.ssh_pass
    ssh_timeout = "30m"
    ssh_handshake_attempts = "100"
    boot_command = ["<esc><wait>", "vmlinuz initrd=initrd.img ", "inst.ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/ks.cfg", "<enter>"]
    http_directory = "http"   
}

build {
    sources = ["source.proxmox-iso.rhel-tpl"]
}