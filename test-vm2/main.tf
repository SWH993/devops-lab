terraform {
  required_providers {
    proxmox = {
      source = "telmate/proxmox"
      version = "2.9.11"
    }
  }
}

provider "proxmox" {
  pm_api_url            = "https://192.168.1.250:8006/api2/json"
  pm_api_token_id       = ""
  pm_api_token_secret   = ""
  pm_tls_insecure       = true
}

/*MASZYNA test-vm*/
resource "proxmox_vm_qemu" "test-vm2" {
  vmid        = 202
  name        = "test-vm2"
  target_node = "lab"
  agent       = 1
  scsihw      = "virtio-scsi-pci"

  boot    = "order=ide2;scsi0"
  
  bios    = "seabios"
  cores   = 2
  sockets = 1
  memory  = 2048
  cpu     = "host"

  disk {
    slot    = 0
    size    = "15G"
    type    = "scsi"
    storage = "local-lvm"
  }

  network {
    model  = "virtio"
    bridge = "vmbr0"
  }

  iso = "local:iso/debian-13.4.0-amd64-netinst.iso"
}