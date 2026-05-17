import socket

from datetime import datetime

def scan_ports(target, ports):
    open_ports = []

    print("\nScanning Ports...\n")

    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            result = s.connect_ex((target, port))

            if result == 0:
                print(f"[OPEN] Port {port}")
                open_ports.append(port)

            s.close()

        except:
            pass

    return open_ports


def grab_banner(target, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((target, port))

        banner = s.recv(1024).decode().strip()

        s.close()

        return banner

    except:
        return "Banner not detected"


def check_outdated_software(banner):
    weak_versions = [
        "Apache/2.2",
        "OpenSSH 5",
        "vsFTPd 2.3.4",
        "PHP/5"
    ]

    for version in weak_versions:
        if version in banner:
            return f"⚠ Outdated Software Detected: {version}"

    return "No outdated software detected"


def web_security_check(target):
    issues = []

    try:
        response = requests.get(f"http://{target}", timeout=5)

        headers = response.headers

        if "Server" in headers:
            issues.append(f"Server Information Exposed: {headers['Server']}")

        if "X-Frame-Options" not in headers:
            issues.append("Missing X-Frame-Options Header")

        if "Content-Security-Policy" not in headers:
            issues.append("Missing Content-Security-Policy Header")

        if "Strict-Transport-Security" not in headers:
            issues.append("Missing HSTS Header")

    except:
        issues.append("Website not reachable")

    return issues


def generate_report(target, open_ports, banners, outdated, web_issues):
    report_name = "vulnerability_report.txt"

    with open(report_name, "w") as file:

        file.write("====================================\n")
        file.write("      VULNERABILITY SCAN REPORT\n")
        file.write("====================================\n\n")

        file.write(f"Target: {target}\n")
        file.write(f"Scan Time: {datetime.now()}\n\n")

        file.write("---------- OPEN PORTS ----------\n")

        if open_ports:
            for port in open_ports:
                file.write(f"Port {port} : OPEN\n")
                file.write(f"Banner: {banners[port]}\n")
                file.write(f"{outdated[port]}\n\n")
        else:
            file.write("No open ports found\n\n")

        file.write("------- WEB VULNERABILITIES -------\n")

        for issue in web_issues:
            file.write(f"- {issue}\n")

    print("\n====================================")
    print(" Scan Completed Successfully")
    print(" Report Saved as vulnerability_report.txt")
    print("====================================")

print("====================================")
print("     SIMPLE VULNERABILITY SCANNER")
print("====================================")

target = input("\nEnter Target IP or Domain: ")

ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 8080]

open_ports = scan_ports(target, ports)

banners = {}
outdated = {}

print("\nDetecting Services and Versions...\n")

for port in open_ports:
    banner = grab_banner(target, port)

    banners[port] = banner

    outdated_result = check_outdated_software(banner)

    outdated[port] = outdated_result

    print(f"Port {port}")
    print(f"Banner: {banner}")
    print(f"{outdated_result}\n")
print("Checking Web Vulnerabilities...\n")

web_issues = web_security_check(target)

for issue in web_issues:
    print(f"- {issue}")
generate_report(target, open_ports, banners, outdated, web_issues)