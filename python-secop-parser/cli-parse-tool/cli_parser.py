import argparse
import json


class JsonParser:
    @staticmethod
    def cli_parser(source_file: str, output_file: str, target_severities: list[str]) -> None:
        try:
            with open(source_file, "r", encoding="utf-8") as text:
                data = json.load(text)
                filtered_results = []

                print("---VULNERABILITIES DETECTED---")
                for item in data:
                    if item.get("severity") in target_severities and item.get("fix_available"):
                        
                        print(
                            f"Vulnerability {item['id']}:\n"
                            f"\t Package: {item['package']} [version {item['installed_version']}]\n"
                            f"\t Severity: {item['severity']} | Fix available: {item['fixed_version']}\n"
                        )
                        
                        vuln_dict = {
                            "id": item["id"],
                            "package": item["package"],
                            "severity": item["severity"],
                            "installed_version": item["installed_version"],
                            "fixed_version": item["fixed_version"]
                        }
                        filtered_results.append(vuln_dict)
                
            with open("for_repair.json", "w", encoding="utf-8") as file:
                json.dump(filtered_results, file, indent=4, ensure_ascii=False)
                print("[+] Filtered data saved to file: for_repair.json")
                        
        except FileNotFoundError:
            print(f"[!] File {source_file} not found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="SecOps CLI Parser", description="Parser for security reports")
    
    parser.add_argument("-i", "--input", required=True, help="Input file with security report")
    parser.add_argument("-o", "--output", required=False, default="for_repair.json", help="Output file with filtered vulnerabilities")
    parser.add_argument("-s", "--severity", nargs="+", default=["CRITICAL", "HIGH"], help="Severity levels to filter (e.g. CRITICAL HIGH)")

    args = parser.parse_args()

    JsonParser.cli_parser(
        source_file=args.input, 
        output_file=args.output, 
        target_severities=args.severity
    )
