import subprocess
import xml.etree.ElementTree as ET
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class DeviceQueryHandler(BaseHTTPRequestHandler):

    def __parse_memory(self, memory_usage):
        return {
            "total": memory_usage.find("total").text,
            "used": memory_usage.find("used").text,
            "free": memory_usage.find("free").text,
        }

    def __parse_processes(self, procs):
        processes = []
        if procs.text == "N/A":
            return "na", processes

        in_use = "no"
        for process in procs.iter("process_info"):
            if process.find('type').text.lower() == "c":
                in_use = "yes"
                processes.append({
                    "pid": process.find("pid").text,
                    "process_name": process.find("process_name").text,
                    "used_memory": process.find("used_memory").text,
                })
        return in_use, processes

    def parse_nvidia_xml(self, xml):
        gpu_data = []
        root = ET.fromstring(xml)
        for gpu in root.iter('gpu'):
            in_use, processes = self.__parse_processes(gpu.find("processes"))
            gpu_data.append({
                "name": gpu.find("product_name").text,
                "uuid": gpu.find("uuid").text,
                "memory": self.__parse_memory(gpu.find("fb_memory_usage")),
                "processes": processes,
                "in_use": in_use,
            })
        return gpu_data

    def cpu_util(self, n_frames=2):
        output = subprocess.check_output("top -b -n{}".format(n_frames).split()).decode('utf-8')
        lines = [l.replace(",", ".").split() for l in output.split("\n") if "Cpu(s)" in l]
        lines = [float(l[1]) + float(l[3]) for l in lines]
        return sum(lines) / n_frames


    def do_GET(self):
        try:
            raw_gpu_data = subprocess.check_output(["nvidia-smi", "-x", "-q"]).decode('utf-8')
            gpu_data = self.parse_nvidia_xml(raw_gpu_data)
            cpu_util = self.cpu_util()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(dict(gpus=gpu_data, cpu_util=cpu_util), indent=4), 'utf-8'))
        except Exception as e:
            self.send_error(500, explain = str(e))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 12000), DeviceQueryHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
