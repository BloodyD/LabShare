from urllib.error import URLError
from django.core.management import BaseCommand
from labshare.models import Device, GPU, GPUProcess

import urllib.request
import json


class Command(BaseCommand):
    help = "queries every connected device for updated info on GPU status"

    def handle(self, *args, **options):
        for device in Device.objects.all():
            try:
                ip_address = device.ip_address
                response = urllib.request.urlopen("http://{}:12000".format(ip_address), timeout=10).read().decode('utf-8')
                gpus = json.loads(response)
                for gpu_data in gpus:
                    gpu = GPU.objects.filter(device=device, uuid=gpu_data["uuid"])

                    gpu_in_use = gpu_data.get("in_use", "na") == "yes"
                    if gpu_data.get("in_use", "na") == "na":
                        # assume that device is in use if more than 800 MiB of video ram are in use
                        gpu_in_use = int(gpu_data["memory"]["used"].split()[0]) > 800

                    if not gpu.exists():
                        gpu = GPU(
                            device=device,
                            model_name=gpu_data["name"],
                            uuid=gpu_data["uuid"],
                            free_memory=gpu_data["memory"]["free"],
                            used_memory=gpu_data["memory"]["used"],
                            total_memory=gpu_data["memory"]["total"],
                            in_use=gpu_in_use,
                        )
                    else:
                        gpu = gpu.get()
                        memory_info = gpu_data["memory"]
                        gpu.free_memory = memory_info["free"]
                        gpu.used_memory = memory_info["used"]
                        gpu.total_memory = memory_info["total"]
                        gpu.in_use = gpu_in_use

                    gpu.save()
                    gpu.processes.all().delete()
                    for process in gpu_data.get("processes", []):
                        GPUProcess(
                            gpu = gpu,
                            process = process.get("process_name", "Unknown"),
                            pid = int(process.get("pid", "0")),
                            memory_usage = process.get("used_memory", "Unknown"),
                        ).save()
            except URLError:
                pass
            except Exception as e:
                self.stderr.write(e, ending='')
